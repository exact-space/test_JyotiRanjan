import os
import sys
import json
import time
import zlib
import redis
import atexit
import logging
logging.basicConfig()
import requests
import numpy as np
import pandas as pd 
import app_config as cfg
from memory_profiler import profile
from datetime import datetime, date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import traceback


redis = redis.StrictRedis(host='vml-2',db=0)
cfg = cfg.getconfig()
query_url = cfg['api']['query']
#UNIT_ID = os.environ.get("UNIT_ID")
#print(UNIT_ID)
# if "UNIT_ID" in os.environ:
    # unitId = os.environ.get("UNIT_ID")

# if UNIT_ID==None:
    # print "no unit id passed"
    # exit()
# UNIT_IDS = ['61c4a9a9515e2f6d59bff021',
 # '61cac0fc0509fe61856a40e8',
 # '61cac1010509fe61856a40e9',
 # '61cace496c36be6370b11a72',
 # '61cacf0e6c36be6370b11a76',
 # '61cad0016c36be6370b11b11',
 # '61cae1d254bf6a5bf94bf3d3',
 # '61cae1db54bf6a5bf94bf3d4',
 # '61cae1fb54bf6a5bf94bf3d5',
 # '61cae20554bf6a5bf94bf3d6',
 # '61caeda654bf6a5bf94bf59a',
 # '61caee0154bf6a5bf94bf59f',
 # '61f3b952f3f49b0734480428',
 # '6225b60128565415e3b5ab64',
 # '62b3fa7b97349f60a5885d97',
 # '62d6776f8465e55755bdcbc0',
 # '62d67f9c1d39a8573a13bc14',
 # '62e9106d75c9b4657aebc8fb',
 # '6304549251476a14db49c3e4',
 # '630c916f8c19444ca8aed6fb',
 # '637484d11a7c8a00087cf4c8',
 # '638dc62f6049ba000768c7d2']

#UNIT_ID = "61cae1d254bf6a5bf94bf3d3"   # ghcl - 76


#UNIT_ID = "630c916f8c19444ca8aed6fb"  # vietnam
#UNIT_ID = "61caeda654bf6a5bf94bf59a"
#UNIT_ID = "637484d11a7c8a00087cf4c8" #Nestle philippines
#UNIT_ID = "638dc62f6049ba000768c7d2"
UNIT_ID = "638dc62f6049ba000768c7d2" #Nestle Abidjan
#for UNIT_ID in UNIT_IDS:
def queryRealTimeData(params):
    tagList = []
    values = []
    queryList = []
    metrics = []
    for tag in params["tags"]:
        metric = {
            "tags": {},
            "name": tag,
            "aggregators": [{
                "name": "avg",
                "align_sampling": True,
                "sampling": {
                    "value": 1,
                    "unit": params["sample_unit"]
                }, "align_start_time": True},
                {
                "name": "gaps",
                "align_sampling": True,
                "sampling": {
                    "value": 1,
                    "unit": params["sample_unit"]
                },
                "align_start_time": True
            }
        ]}
        metrics.append(metric)
    dbquery = {
        "metrics": metrics,
        "start_absolute": int(params["startTime"]) * 1000,
        "end_absolute": int(params["endTime"]) * 1000
    }
    response = requests.post(query_url, json=dbquery)
    if response.status_code == 200 and response.content:
        resp = json.loads(response.content)
        flag = 0
        for query in resp["queries"]:
            if flag == 0:
                flag = 1
                result = pd.DataFrame(query['results'][0]['values'], columns=["time", query["results"][0]["name"]])
            else:
                result[query["results"][0]["name"]] = np.array(query["results"][0]["values"])[:,1]
        return result


def fetchLoadDataFromEq(criticalTag):
    try:
        equipmentMeta = requests.get(cfg['api']['meta']+'/units/'+criticalTag['unitsId']+'/equipment/'+criticalTag['equipmentId']).json()
        loadDescription = fetchTagMeta(equipmentMeta['equipmentLoad']['loadTag'])["description"]
        loadBucket = equipmentMeta['equipmentLoad']['loadBucketSize']
        
        return equipmentMeta['equipmentLoad']['loadTag'], loadDescription, int(loadBucket)
    except Exception as e:
        print(e)

def fetchLoadTag(unitId):
    loadURL = cfg['api']['meta']+'/units/'+unitId+'/heatrates?filter={%22fields%22:%22load%22}'
    loadRes = requests.get(loadURL)
    if loadRes.status_code == 200 and json.loads(loadRes.content):

        load = json.loads(loadRes.content)
        logging.info("deb_fetchLoadTagResponse:"+str(load))
        return {load[0]['load']: cfg[unitId]["loadBucketSize"]}


def fetchTagMeta(tag):
    getTagmetaURL = cfg['api']['meta']+'/tagmeta?filter={"where":{"dataTagId": "' + tag+'"}, "fields":["description", "unitsId", "benchmarkLoad", "benchmark", "dataTagId"]}'
    res = requests.get(getTagmetaURL)
    if res.status_code == 200 and res.content:
        tagJson = json.loads(res.content)
        return tagJson[0]
    else:
        return ""


# @profile
def build_df(criticalTags, pltvars, flagvars, predvars, labels, data, params, timeFlag, incident):
    print("deb_sizeOfCriticalTags:"+str(len(criticalTags)))
    for x in criticalTags:

        tagList = []
        tagList.append(x["dataTagId"])
        tagList.append(x["alarmType"] + x["dataTagId"])
        pltvars.append(x["dataTagId"])
        flagvars.append(x["alarmType"][:-2])
        
        if x["alarmType"] == "flagModel__":
            tagList.append("pred_" + x["dataTagId"])
            predvars.append("pred_" + x["dataTagId"])

        try:
            # FETCH LOAD TAG AND LOAD BUCKET SIZE
            # -----------------------------------
            print("evt_fetchLoadTagFromEqStart")
            loadTag, loadTagDescription, loadBucketSize = fetchLoadDataFromEq(x)
            print("evt_fetchLoadTagFromEqSuccess")
        except Exception as e:
            print("evt_loadTagNotFoundInEq")
            print("evt_fetchLoadTagFromHeatratesStart")
            eqLoadMeta = fetchLoadTag(incident['unitsId'])
            #loadTag, loadTagDescription, loadBucketSize = fetchLoadTag(incident['unitsId'])
            print("evt_fetchLoadTagFromHeatratesComplete")
            loadTag = eqLoadMeta.keys()[0]
        tagList.append(loadTag)
        #pltvars.append(loadTag)

        params["tags"] = tagList

        resultSet = queryRealTimeData(params)
        resultSet = resultSet.fillna(method="ffill")
        resultSet = resultSet.fillna(method="bfill")

        resultSet["bucket"] = resultSet[loadTag] // loadBucketSize * loadBucketSize
        resultSet["bucket"] = resultSet["bucket"].astype(int).astype(str)
        resultSet = resultSet.fillna(method="ffill")
        resultSet = resultSet.fillna(method="bfill")

        tagMeta = fetchTagMeta(x["dataTagId"])
        labels.append(tagMeta["description"]+" - "+x["dataTagId"])
        resultSet[tagMeta["dataTagId"]+"_UP"] = resultSet[tagMeta["dataTagId"]]
        resultSet[tagMeta["dataTagId"]+"_DOWN"] = resultSet[tagMeta["dataTagId"]]
        
        # UP/DOWN(YELLOW) BAND CALCULATION
        # ----------------------------------
        if "flagModel" in x["alarmType"]:
            buckets =[]
            # IN CASE OF FLAGMODEL PRED DATA IS FETCHED FROM THE DB
            # PRED CALCULATION: 
            # GET SD OF MAX BENCHMARKLOAD. 
            # FORMULA: pred_tag + bias +/- (2 * sensitivity * sd)
            # ------------------------------------------------------
            for key in tagMeta["benchmarkLoad"].keys():
                try:
                    if tagMeta["benchmarkLoad"][key]["status"] == "valid":
                        buckets.append(int(key))
                except:
                    pass
            if(len(buckets)>0):
                bucket = str(np.max(buckets))
            sd = tagMeta["benchmarkLoad"][bucket]["sd"] 
            bias = tagMeta["benchmark"]["modelBias"]
            sensitivity = tagMeta["benchmark"]["sensitivity"]
            resultSet[tagMeta["dataTagId"]+"_UP"] = resultSet["pred_"+tagMeta["dataTagId"]] + bias + (2 * sensitivity * sd)
            resultSet[tagMeta["dataTagId"]+"_DOWN"] = resultSet["pred_"+tagMeta["dataTagId"]] + bias - (2 * sensitivity * sd) 
        else:
            # IN CASE OF FLAGLOAD PRED DATA IS CALCULATED
            # PRED CALCULATION: 
            # GET MEDIAN OF BENCHMARKLOAD. 
            # FORMULA: median + bias +/- (4 * sensitivity * sd)
            # ------------------------------------------------------
            for bucket in resultSet["bucket"].unique():
                if bucket in tagMeta["benchmarkLoad"] and tagMeta["benchmarkLoad"][bucket]["status"] == "valid":
                    sd = tagMeta["benchmarkLoad"][bucket]["sd"] 
                    median = tagMeta["benchmarkLoad"][bucket]["median"] 
                    bias = tagMeta["benchmark"]["bias"]
                    sensitivity = tagMeta["benchmark"]["sensitivity"]
                    resultSet.loc[resultSet["bucket"] == bucket, tagMeta["dataTagId"]+"_UP"] = median + bias + (4 * sensitivity * sd)
                    resultSet.loc[resultSet["bucket"] == bucket, tagMeta["dataTagId"]+"_DOWN"] = median + bias - (4 * sensitivity * sd)
        
        for col in resultSet.columns:
            # GET THE REALTIME VALUES OF TAGS
            # --------------------------------
            if col == "time" and timeFlag==0:
                timeFlag=1 
                eachTagResp = {}
                eachTagResp['incidentId'] = incident["id"]
                eachTagResp['tagName'] = col
                eachTagResp['values'] = resultSet[col].tolist()
                data[col]=resultSet[col].tolist()
            elif col != "bucket":
                eachTagResp = {}
                eachTagResp['incidentId'] = incident["id"]
                eachTagResp['tagName'] = col
                eachTagResp['values'] = resultSet[col].tolist()
                data[col]=resultSet[col].tolist()

    return data, pltvars, flagvars, predvars, labels
   

# @profile
def redis_persist(incident):
    print("evt_processingIncident: "+ incident["id"])
    done = set()
    criticalTags = []
    for d in incident["criticalTags"]:
        if d['dataTagId'] not in done:
            done.add(d['dataTagId'])
            criticalTags.append(d)
    timeFlag = 0
    params = {}
    params["sample_unit"] = "minutes"
    print("gdsgdgdggdgdg",incident["startTime"])
    timestruct = time.strptime(incident["startTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
    params["startTime"] = time.mktime(timestruct) - 43200 # 12 hours before incident startTime
    params["endTime"] = int(time.time())
    pltvars=[]
    labels=[]
    flagvars=[]
    predvars=[]
    data = {}

    data, pltvars, flagvars, predvars, labels = build_df(criticalTags, pltvars, flagvars, predvars, labels, data, params, timeFlag, incident)
    df = pd.DataFrame(data)
    if df.shape[0] > 0:
        df = df.to_dict('records')
        if len(df) == 0:
            print("evt_dataDataNotFoundInKairos")
            print("evt_exitingTheFlow")
            exit()
        finalResult={"data":df,"predvars":predvars,"labels":labels,"flagvars":flagvars,"pltvars":pltvars}
        print("evt_setDataToRedis")
        print("inc_"+incident["unitsId"]+"_"+ incident["id"])
        redis.set("inc_"+incident["unitsId"]+"_"+ incident["id"], json.dumps(finalResult))
        print("evt_setDataToRedisSuccess")

        rd_data = json.loads(redis.get("inc_"+incident["unitsId"]+"_"+ incident["id"]))
        if len(rd_data) == 0:
            print("evt_setDataToRedisIfNotSet")
            redis.set("inc_"+incident["unitsId"]+"_"+ incident["id"], json.dumps(finalResult))
    else:
        print("evt_dataDataNotFoundInKairos")
        print("evt_exitingTheFlow")
        exit()


def getIncidentsForUnit(unitId):
    print("evt_getIncidentsForUnit")
    return requests.get(cfg['api']['meta'] + '/units/'+unitId+'/incidents?filter={"where":{"open":true}, "order": "startTime DESC", "fields":["criticalTags", "id", "unitsId", "startTime", "endTime", "open"]}').json()


def getUnits():
    return requests.get(cfg["api"]["meta"] + '/units?filter={"fields":["id", "name"]}').json()


def persistGroupByData(request):
    now = date.today()
    lastMonth = now - timedelta(days=30)
    _startT = lastMonth.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    _endT = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    

    unitId = request["unitId"]
    result = {"incidents": [], "dates": []}
    startTime = _startT[0:10]+"T00:00:00.000Z"
    endTime = _endT[0:10]+"T23:59:59.000Z"
    groupBy = request["groupBy"]
    sysEqp = {}
    
    # Initialize a dataframe with the each date between the start and end time
    df3 = pd.DataFrame({"dates": pd.period_range(start=startTime[0:10], end=endTime[0:10], freq='1D')})
    df3["datesto"] = df3["dates"].dt.strftime("%m-%d-%Y")
    datelist = df3["datesto"].unique().tolist()
    datelist = [datetime.strftime(datetime.strptime(x, "%m-%d-%Y"), "%Y-%m-%d") for x in datelist]

    df3 = df3.drop("datesto", axis=1)
    df3["incType"] = "Incident"
    result = {"incidents": [], "dates": datelist}
    
    # Fetch the equipments for the selected system
    url = cfg["api"]["meta"] + '/equipment?filter={"where":{"unitsId":"' + unitId+'","systemName":"'+groupBy+'"}}'
    equipments = requests.get(url).json()
    for equipment in equipments:
        sysName = equipment["systemName"]
        if sysName in sysEqp:
            sysEqp[sysName].append(equipment["name"])
        else:
            sysEqp[sysName] = [equipment["name"]]

    # Fetch open incidents for the given time range for the selected system 
    url = cfg["api"]["meta"] + '/units/' + unitId + '/incidents?filter={"where":{"systemName" : "' + groupBy + '", "or":[{"open":true},{"and":[{"endTime":{"gte":"'+startTime[0:10]+"T00:00:00.000Z" + '"},"startTime":{"lte":"'+endTime[0:10]+"T23:59:59.000Z" + '"}}]}],"incidentType":{"inq":["operations","Operations"]}},"fields":{"startTime":true,"endTime":true,"faulttreeId":true,"systemName":true, "equipmentName":true}}'
    equips = sysEqp[groupBy]
    try:
        incidents = requests.get(url).json()
        equipments = []
        for incident in incidents:
            for equipment in incident["equipmentName"]:
                if(equipment in equips):
                    equipments.append(equipment)
        equipments = list(set(equipments))
        df = pd.DataFrame(incidents)
        # print(df)
    except:
        df = pd.DataFrame()
        # print("here")

    for equipment in equipments:
        df3[equipment] = 0
        
    if df.shape[0] > 0:
        # df['endTime'] = df['endTime'].fillna(datetime.now())
        try:
            df["endTime"] = pd.to_datetime(df["endTime"])
        except:
             df["endTime"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        df["startTime"] = pd.to_datetime(df["startTime"])
        df["endTime"] = pd.to_datetime(df["endTime"])

        df["duration"] = df["endTime"] - df["startTime"]
        df["duration"] = df["duration"] / np.timedelta64(1, 's')
        df = df.loc[(df["duration"] >= 60 * 60) | (df.endTime.isnull()), :]
        df.drop('duration', axis=1)

        for index, row in df.iterrows():
            try:
                for eqp in row["equipmentName"]:
                    df3.loc[(df3["dates"] >= row["startTime"]) & (df3["dates"] <= row["endTime"]), eqp] = df3.loc[(df3["dates"] >= row["startTime"]) & (df3["dates"] <= row["endTime"]), eqp] + 1
            except:
                continue

    df3["dates"] = df3["dates"].dt.strftime("%m-%d-%Y")
    df3["dates"] = pd.to_datetime(df3["dates"])
    df3["dates"] = df3["dates"].dt.strftime("%m-%d-%Y")
    
        

    # Sum each system and add the count
    for col in df3:
        if col != "incType" and col != "dates":
            if(sum(df3[col].tolist()) > 0):
                result["incidents"].append({"equipment": col, "incidentCount": df3[col].tolist()})

    # print("---------Processed Groupby data-------------")
    redis.set("dashboard_"+groupBy.replace(" ", "_")+"_"+request["unitId"], json.dumps(result))

'''
Fetch Incidents for a unit for the past 1 month and return
'''
def persistCalendarData(request):
    now = date.today()
    lastMonth = now - timedelta(days=30)
    _startT = lastMonth.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    _endT = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    groups = []

    unitId = request["unitId"]
    result = {"incidents": [], "dates": []}
    startTime = _startT[0:10]+"T00:00:00.000Z"
    endTime = _endT[0:10]+"T23:59:59.000Z"
    print("eeeeeee",endTime)
    print("ooooooo",startTime)

    # Initialize a dataframe with the each date between the start and end time
    df3 = pd.DataFrame({"dates": pd.period_range(start=startTime[0:10], end=endTime[0:10], freq='1D')})
    df3["datesto"] = df3["dates"].dt.strftime("%m-%d-%Y")
    datelist = df3["datesto"].unique().tolist()
    datelist = [datetime.strftime(datetime.strptime(x, "%m-%d-%Y"), "%Y-%m-%d") for x in datelist]

    df3 = df3.drop("datesto", axis=1)
    df3["incType"] = "Incident"
    result = {"incidents": [], "dates": datelist}
    #print("dddd",startTime)
    # Fetch open incidents for the given time range 
    url = cfg["api"]["meta"] + '/units/' + unitId + '/incidents?filter={"where":{"or":[{"open":true},{"and":[{"endTime":{"gte":"'+startTime[0:10]+"T00:00:00.000Z"+'"},"startTime":{"lte":"' + endTime[0:10]+"T23:59:59.000Z" + '"}}]}],"incidentType":{"inq":["operations","Operations"]}},"fields":{"startTime":true,"endTime":true,"systemName":true, "equipments":true, "id":true}}'
    
    #print("kkkkkkkkkkkkk",url)
    incidents = requests.get(url).json()
    print(incidents)
    print("deb_lenOfIncidents: "+str(len(incidents)))
    systems = []
    df = pd.DataFrame(incidents)
    #print(df)
    
    # Time zone correction 
    
#try:
    df["startTime"] = pd.to_datetime(df["startTime"])
    df["startTime"] =df.startTime.apply(lambda x:x.tz_localize(None))
    print("gggg",df["startTime"])
    try:
        df["endTime"] = pd.to_datetime(df["endTime"])
    except:
         df["endTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.000")
         df["endTime"] = pd.to_datetime(df["endTime"])
    #print("endend",df["endTime"]
    df["endTime"] =df.endTime.apply(lambda x:x.tz_localize(None))
        # traceback.print_exc()
       
    print(df)
        
    # except:
        # df["startTime"] = pd.to_datetime(df["startTime"])
        # df["startTime"] =df.startTime.apply(lambda x:x.tz_localize(None))
        #print("gggg",df["startTime"])
        #df["endTime"] = df['endTime'].fillna('NaN')
        #print("endend",df["endTime"]
        #df["endTime"] =df.endTime.apply(lambda x:x.tz_localize(None))
        # print(df)
    
    
    
    dfs = df["systemName"].apply(lambda x: pd.Series(x)).stack().reset_index(drop=True)
    
    # For each system initialize a dataframe with count as 0
    systems = dfs.unique().tolist()
    for system in systems:
        df3[system] = 0
    
    # For each element in a system increment the count by 1
    #try:
    if df.shape[0] > 0:
        df['endTime'] = df['endTime'].fillna(datetime.now())
        df["startTime"] = pd.to_datetime(df["startTime"])
        df["endTime"] = pd.to_datetime(df["endTime"])

        df["duration"] = df["endTime"] - df["startTime"]
        df["duration"] = df["duration"] / np.timedelta64(1, 's')
        df = df.loc[(df["duration"] >= 60 * 60) | (df.endTime.isnull()), :]
        df.drop('duration', axis=1)

        for index, row in df.iterrows():
            try:
                for system in row["systemName"]:
                    df3.loc[(df3["dates"] >= row["startTime"]) & (df3["dates"] <= row["endTime"]), system] = df3.loc[(df3["dates"] >= row["startTime"]) & (df3["dates"] <= row["endTime"]), system] + 1
            except:
                continue

    df3["dates"] = df3["dates"].dt.strftime("%m-%d-%Y")
    df3["dates"] = pd.to_datetime(df3["dates"])
    df3["incType"] = "Incident"
    print("hhhhhh",df3)
    # except:
        # if df.shape[0] > 0:
            #df['endTime'] = df['endTime'].fillna(datetime.now())
            # df["startTime"] = pd.to_datetime(df["startTime"])
            #df["endTime"] = pd.to_datetime(df["endTime"])

            #df["duration"] = df["endTime"] - df["startTime"]
            # df["duration"] = df["duration"] / np.timedelta64(1, 's')
            # df = df.loc[(df["duration"] >= 60 * 60) | (df.endTime.isnull()), :]
            # df.drop('duration', axis=1)

            # for index, row in df.iterrows():
                # try:
                    # for system in row["systemName"]:
                        # df3.loc[(df3["dates"] >= row["startTime"]) & (df3["dates"] <= row["endTime"]), system] = df3.loc[(df3["dates"] >= row["startTime"]) & (df3["dates"] <= row["endTime"]), system] + 1
                # except:
                    # continue

        # df3["dates"] = df3["dates"].dt.strftime("%m-%d-%Y")
        # df3["dates"] = pd.to_datetime(df3["dates"])
        # df3["incType"] = "Incident"
        # print("hhoohh",df3)
        
    
    # Sum each system and add the count
    for col in df3:
        if col != "incType" and col != "dates":
            if(sum(df3[col].tolist()) > 0):
                groups.append(col)
                result["incidents"].append({"system": col, "incidentCount": df3[col].tolist()})
    print("evt_populateCalendarDataComplete")
    redis.set("dashboard_"+request["unitId"], json.dumps(result))
    return groups

# @profile
def populateStreamData():
    print("!!!!!!!!!!!!!!!!!!!!evt_populateStreamDataStart")
    try:
        print("deb_populateStreamForUnit: "+str(UNIT_ID))
        # Delete topic from redis 
        # incidentsToDelete = requests.get(cfg['api']['meta'] + '/units/'+UNIT_ID+'/incidents?filter={"where":{"open":false},"order":"startTime DESC", "limit":100, "fields":["id"]}').json()
        # print("evt_removeClosedIncidentsFromRedisStart")
        # for incident in incidentsToDelete:
        #     print("deb_deleteIncident: "+str(incident["id"]))
        #     redis.delete("inc_"+UNIT_ID+"_"+incident["id"])
        # print("evt_removeClosedIncidentsFromRedisSuccess")

        ################ TEST CODE #################
        # Test with single incident 
        # ---------------------------------
        # openIncidents =  [requests.get(cfg['api']['meta'] + '/units/'+UNIT_ID+'/incidents/620187e26932d242c7b784cd').json()]
        ############################################

        openIncidents = getIncidentsForUnit(UNIT_ID)
        print("deb_lenOfOpenIncidents: "+str(len(openIncidents)))

        for incident in openIncidents:
            try:
                if len(incident["criticalTags"]) > 0:
                    redis_persist(incident)
            except Exception as e:
                print("EXP_whileCallingRedisPersistStreamData: "+str(e))
                pass
        print("!!!!!!!!!!!!!!!!!!!!evt_populateStreamDataEnd")
    except Exception as e:
        print("EXP_whileProcessingStreamData: "+str(e))
    

# req = {"unitId": UNIT_ID}
# groups = persistCalendarData(req)
# print(groups)
def populateCalendarData():
    print("evt_populateCalendarDataStart")
    # units = getUnits()
    # for unitId in units:
    try:
    
        print("deb_populateCalendarForUnit: "+str(UNIT_ID))
        req = {"unitId": UNIT_ID}
        groups = persistCalendarData(req)
        print(req)
        for group in groups:
            req["groupBy"] = group
            persistGroupByData(req)
        print("evt_populateCalendarDataSuccess")
    except Exception as e:
        print("EXP_whilePopulatingCalendarData: "+str(e))
        traceback.print_exc()
        pass

print("evt_initializeBackgroundScheduler")
sched = BackgroundScheduler()
print("evt_addJobsToScheduler")
#sched.add_job(populateStreamData,'interval',seconds=10)
sched.add_job(populateCalendarData,'interval',hours=2)
print("evt_startScheduler")
sched.start()

populateCalendarData()
#populateStreamData()

def my_listener(event):
    if event.exception:
        print('EXP_schedulerJobCrashed')
        print('EXP_addingJobsAgain')
        #sched.add_job(populateStreamData,'interval',seconds=10)
        sched.add_job(populateCalendarData,'interval',hours=2)
    else:
        print('evt_schedulerJobGood')

sched.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

try:
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    sched.shutdown() 