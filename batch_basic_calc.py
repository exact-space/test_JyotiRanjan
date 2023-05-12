import pandas as pd
import os
import time
import requests
import app_config as cfg
config = cfg.getconfig()
import json
import numpy as np
import time
import sys
from datetime import datetime
import time

unitId= "61c4b560515e2f6d59c00202"
#unitId= "611b7fd57afa992d36e308b0"
if "UNIT_ID" in os.environ:
    unitId = os.environ.get("UNIT_ID")
# unitId = sys.argv[1]
print(unitId)
#unitId="5df8f5a57e961b7f0bccc7ed"
#unitId="5f0ff2f892affe3a28ebb1c2"
if unitId==None:
    print "no unit id passed"
    exit()

from apscheduler.schedulers.background import BackgroundScheduler

# Input query

#  ************************  Specific coal consumption ( As on Yesterday)   ******************
"""
(Coal consumption Manual Entry as on Yesterday)/(21_KW.DACA.PV)
"""


coalFlowQuery = {"where":{
    "equipment":"Performance Kpi",
    "measureProperty":"Coal",
    "measureType":"Flow"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}


SCCQuery = {"where":{
    "equipment":"Performance Kpi",
    "measureProperty":"Scc",
    "measureType":"Ratio"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}



# **********************************  Evaporation ratio ( As on Yesterday)  **************************
"""  (11_FI_607.DACA.PV)/(Coal Consumption-Manual Entry as on yesterday)  
"""


steamFlowQuery = {"where":{
    "equipment":"Superheater",
    "measureProperty":"Main Steam",
    "measureType":"Flow"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}

evapRatioQuery = {"where":{
    "equipment":"Performance Kpi",
    "measureProperty":"Evaporation",
    "measureType":"Ratio"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}


#  *******************************  Specific DM water consumption (DA makeup) ( As on Yesterday)   **************************
"""
(DM Consumption Manual Entry as on Yesterday)/(21_KW.DACA.PV)
"""


dmWaterQuery = {"where":{
    "equipment":"Station Performance",
    "measureProperty":"Dm Water",
    "measureType":"Totaliser"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}

specDmConRatioQuery = {"where":{
    "equipment":"Station Performance",
    "measureProperty":"Sdmwc",
    "measureType":"Ratio"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}


# ********************************  Specific RAW water consumption ( As on Yesterday)  *****************************
""""
(Raw Water Consumption Manual Entry as on Yesterday)/(21_KW.DACA.PV)
"""


rawWaterQuery = {"where":{
    "equipment":"Station Performance",
    "measureProperty":"Raw Water",
    "measureType":"Totaliser"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}

specRawConQuery = {"where":{
    "equipment":"Station Performance",
    "measureProperty":"Srwc",
    "measureType":"Ratio"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}


# ________________________________


powerQuery = {"where":{
    "equipment":"Generator",
    "measureProperty":"Power",
    "measureType":"Load"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}


totalMwQuery= {"where":{
    "equipment":"Generator",
    "measureProperty":"Power",
    "measureType":"SUM"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}


def getTags(eqp,mspr,mstp,tagType):
    query =  {"where":{
    "equipment":eqp,
    "measureProperty":mspr,
    "measureType":mstp,
    "tagType":tagType,
    "measureInstance":1},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}

    url = config["api"]["meta"]+"/units/"+unitId+"/tagmeta?filter="+json.dumps(query)
    print "getTags Url : ", url
    tags = requests.get(url).json()
    if len(tags)==0:
        print("No  tags found, exitting")
        return []
        #exit()
    
    return tags



def createMeta(tag_copy,mspr,mstp,msun,tagtp,suffix):
    tag = tag_copy.copy()

    tag["measureProperty"]=mspr
    tag["measureType"]=mstp
    tag["measureUnits"]=msun
    tag["tagType"] = tagtp
    tag["dataTagId"] = tag["dataTagId"] + suffix
    url = config["api"]["meta"]+"/units/"+tag["unitsId"]+"/tagmeta"
    res = requests.post(url,tag)
    return [json.loads(res.content)]


# createMeta(tags,"Evaporation","Ratio","-","Calc","_evaporationRatio")


def checkIsOpTagAvl(tag,eqp,mspr,mstp): # input tags that you fetched and query for output tags

    print ("*********************************************")

    query =  {"where":{
    "equipment":eqp,
    "measureProperty":mspr,
    "measureType":mstp,
    "measureInstance":1},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}
    query["where"]["systemInstance"] = tag["systemInstance"]


    url = config["api"]["meta"]+"/units/"+unitId+"/tagmeta?filter="+json.dumps(query)
    query_json = requests.get(url).json()

    if(len(query_json) ==0):
        query["where"]["system"] = tag["system"]
        return query_json
    else:
        print("already there")
        query = [x for x in query_json if x["systemInstance"]==tag["systemInstance"]]
        query = query[0]
        print(query)
        return query_json




def getData(tags):
    
    print tags, "  @@@@@@@@@@@@@@@@@@"
    datas = []
    for tag in tags:
        print " "
        print tag["dataTagId"]
        print " "
        q = {"name":tag["dataTagId"],"aggregators":[{ "name": "avg", "sampling": {"value": "1", "unit": "days"  }}]}
        print q, "&&&&&&&&&&&&&&&"
        query = {"metrics":[], "start_relative": {"value": "1", "unit": "years" }}
        query["metrics"].append(q)
        print "query : ",query
        print ""
        data = requests.post(config["api"]["query"],json=query).json()
        print data
        print "11111111"
        datas.append(data)
    return datas



def getData_2(tags,startTime,endTime):
    print tags
    
    datas = []
    print "*****************  data fetching   **********************"
    for tag in tags:
        print tag["dataTagId"]
        q = {"name":tag["dataTagId"],"aggregators":[{ "name": "avg", "sampling": {"value": "1", "unit": "hours" }},
           {"name": "filter", "filter_op": "lt","threshold": "0"}]}
        query = {"metrics":[]}
        query["metrics"].append(q)
        #query["plugins"] = []
        #query["cache_time"] = 0,
        query["start_absolute"] = startTime
        query["end_absolute"] =  endTime
        #print query
        #print '------------'
        data = requests.post(config["api"]["query"],json=query).json()
        #print data
        
        datas.append(data)
    #exit()
    return datas

def getData_last7Days(tags):
    
    print tags, "  @@@@@@@@@@@@@@@@@@"
    datas = []
    for tag in tags:
        print " "
        print tag["dataTagId"]
        print " "
        q = {"name":tag["dataTagId"],"aggregators":[{ "name": "avg", "sampling": {"value": "1", "unit": "hours"  }},
          {
          "name": "filter",
          "filter_op": "lt",
          "threshold": "1"
        }]}
        print q, "&&&&&&&&&&&&&&&"
        query = {"metrics":[], "start_relative": {"value": "7", "unit": "days" }}
        query["metrics"].append(q)
        print "query : ",query
        print ""
        data = requests.post(config["api"]["query"],json=query).json()
        print data
        print "11111111"
        datas.append(data)
    return datas



#-----------------------------------------------------------------------------------------------------------------------


def postCalc(outputQuery, tags1, tags22,way_of_divide): # tags1 is  input query
    datas1 = getData(tags1)
    print "%%%%%%%%%%", datas1
    print len(datas1)
    for data1 in datas1:
        for q in data1["queries"]:
            for tag1 in tags1:
                print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                #print (tag1["dataTagId"] == q["results"][0]["name"]) , tag1["dataTagId"], q["results"][0]["name"]
                if(tag1["dataTagId"] == q["results"][0]["name"]):
                    outputTag = outputQuery[tag1["dataTagId"]]
                    df1 = pd.DataFrame(q["results"][0]["values"],columns=["time","tag1"])
                    print tag1["dataTagId"] , "output tag1 : ", outputTag
                    tags2 = [x for x in tags22 if x["systemInstance"]==tag1["systemInstance"]]
                    print tags2
                    print len(tags2),tags2[0]['dataTagId']
                    # to create a pair of consequtive timestamp
                    lastTimestamp = df1['time'].tolist()[-1]
                    nextDayTime = lastTimestamp + 1000*60*60*24
                    splitted_times = [df1['time'].tolist()[i:i+2] for i in range(0,len(df1['time'])-1)] + [[lastTimestamp, nextDayTime]]                   
                    print splitted_times
                    for times in splitted_times:
                        print times[0] # startTime
                        print times[1] # endTime
                        print "----times previous and current days --- ", times
                        datas2 = getData_2(tags2,times[0],times[1])
                        #print datas2
                        
                        for data2 in datas2:
                            for q in data2["queries"]:
                                for tag2 in tags2:
                                    if(tag2["dataTagId"] == q["results"][0]["name"]):
                                        df2 = pd.DataFrame(q["results"][0]["values"],columns=["time","tag2"])
                                        #df2.loc[0,'time'] = times[1]  # updating time with endtime of getData_2
                                        df2 = df2.dropna()
                                        df2 = df2[df2['tag2']!= "NaN"]
                                        

                                        try:
                                            df1 = df1.set_index('time')
                                        except: 
                                            pass
                                        try:
                                            df2 = df2.set_index('time')
                                        except:
                                            pass
                                        
                                        print df1.tail(3)
                                        print df2.tail(3)
                                        
                                        
                                        result = pd.DataFrame()
                                        df1_val = df1['tag1'][times[0]] # starttime of manual data
                                        if df2.shape[0] == 0:
                                            df2['tag2'] = [0]
                                            
                                        #print df2  
                                        print " mean of ", tag2["dataTagId"] , np.mean(df2['tag2'])
                                        print " last val of ", tag1["dataTagId"], " ", df1_val ," time ", times[0]
                                        
                                        if df2.shape[0] > 0:
                                        
                                            if way_of_divide == "uniformDivide" :
                                                if np.mean(df2['tag2']) > 0:
                                                    result[outputTag] = [df1_val / (np.mean(df2["tag2"])*24)]
                                                else:
                                                    result[outputTag] = [0]
                                                
                                            if way_of_divide == "oppositeDivide" :
                                                if df1_val > 0:
                                                    result[outputTag] = [(np.mean(df2["tag2"])*24) / df1_val]
                                                else:
                                                    result[outputTag] = [0]
                                                    
                                                    
                                            result["time"] = [times[0]]  # end time of manual data
                                            result = result.dropna()
                                            

        
                                            # data filteration
                                            result.replace([np.inf, -np.inf], np.nan, inplace=True)
                                            result.loc[result[outputTag] < 0 ,outputTag]= 0
                                            result.dropna(inplace=True)
                                            print way_of_divide
                                            print df1_val
                                            print np.mean(df2["tag2"])
                                            print np.mean(df2["tag2"])*24
                                            print result
                                            
                                            datapoints = result[['time',outputTag]].values.tolist()
                                            print datapoints
                                            postbody = [{"name":outputTag,"datapoints":datapoints,"tags":{"type":"derived"}}]
                                            print("######################  end #####################",postbody)
                                            res = requests.post(config["api"]["datapoints"],json=postbody)
                                        #exit()



#coaltags = getTags(coalFlowQuery)

def returnOpTags(inputTags,eqp,mspr,mstp,msunit,tagtp,suffix):
    opTags = {}
    for tag in inputTags:
        print tag
        query_json = checkIsOpTagAvl(tag,eqp,mspr,mstp)
        print tag
        if len(query_json) == 0:
            query_json = createMeta(tag,mspr,mstp,msunit,tagtp,suffix)
            print tag
            print query_json
            opTags[tag['dataTagId']] = query_json[0]['dataTagId']
        else:
            opTags[tag['dataTagId']] = query_json[0]['dataTagId']
    return opTags  
    
    
#*****************************************   Parameters Explaination   *************************************
"""
1. Output queries to get OutputTags 
2. 1st input parameters (Manual data)
3. 2nd Input queries to get the tags
"""

# ****   Evaporation Ratio   ****
 
msFlowtags = getTags("Superheater","Main Steam","Flow","-")
coalFlowtags = getTags("Performance Kpi","Coal","Flow","Manual")
# print msFlowtags
# print coalFlowtags

### parameters : inputTags,eqp,mspr,mstp,msunit,tagtp,suffix
evapTags = returnOpTags(coalFlowtags,"Performance Kpi","Evaporation","Ratio","-","Calc","_evaporationRatio")
print evapTags
#postCalc(evapTags,coalFlowtags,msFlowtags,"oppositeDivide") # opTags, inp1 and inp2 tags
#exit()
# ****   Specific Coal consumption    *****

mwtags = getTags("Generator","Power","Load","-")
coalFlowtags = getTags("Performance Kpi","Coal","Flow","Manual")
sccTags = returnOpTags(coalFlowtags,"Performance Kpi","Scc","Ratio","-","Calc","_SCC")
# print msFlowtags
# print coalFlowtags
print coalFlowtags
print sccTags
print mwtags
#postCalc(sccTags,coalFlowtags,mwtags,"uniformDivide") # opTags, inp1 and inp2 tags

# ****   Specific Raw water consumption  *****
rawWaterQuery = {"where":{
    "equipment":"Station Performance",
    "measureProperty":"Raw Water",
    "measureType":"Totaliser"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}

specRawConQuery = {"where":{
    "equipment":"Station Performance",
    "measureProperty":"Srwc",
    "measureType":"Ratio"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}

totalMwQuery= {"where":{
    "equipment":"Generator",
    "measureProperty":"Power",
    "measureType":"SUM"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}


mwtags = getTags("Generator","Power","Load","-")
totalmwtags = getTags("Generator","Power","SUM","-")

rawWatertags = getTags("Station Performance","Raw Water","Totaliser",'-')
spRawWaterTags = returnOpTags(rawWatertags,"Station Performance","Srwc","Ratio","T/Mwh","Calc","_SRWC")

print rawWatertags
print spRawWaterTags
print mwtags
#postCalc(spRawWaterTags,rawWatertags,mwtags,"uniformDivide") # opTags, inp1 and inp2 tags

#postCalc(spRawWaterTags,rawWatertags,totalmwtags,"uniformDivide") # opTags, inp1 and inp2 tags
#exit()

# ****   Specific DM water consumption  *****

dmWaterQuery = {"where":{
    "equipment":"Station Performance",
    "measureProperty":"Dm Water",
    "measureType":"Totaliser"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}

specDmConRatioQuery = {"where":{
    "equipment":"Station Performance",
    "measureProperty":"Sdmwc",
    "measureType":"Ratio"
},"fields":["systemInstance","system","equipment","equipmentId","equipmentType","equipmentName","dataTagId","unitsId","siteId","customerId"]}

mwtags = getTags("Generator","Power","Load","-")
dmWatertags = getTags("Station Performance","Dm Water","Totaliser",'-')
spdmWaterTags = returnOpTags(dmWatertags,"Station Performance","Sdmwc","Ratio","T/Mwh","Calc","_SDMWC")

print dmWatertags
print spdmWaterTags
print mwtags
#postCalc(spdmWaterTags,dmWatertags,mwtags,"uniformDivide") # opTags, inp1 and inp2 tags
#exit()


# **** APC 7th day avg  *****
def getperdayavg(df):
    df['date'] = pd.to_datetime(df['time'],unit='ms')
    df['day'] =df.date.dt.day
    if len(df)>0:
        dff1 = df.groupby(['day']).mean()
    return dff1
    
    
def postCalc_apc(outputQuery, tags1, tags22): # tags1 is  input query
    datas1 = getData_last7Days(tags1)
    print "%%%%%%%%%%", datas1
    print len(datas1)
    for data1 in datas1:
        for q in data1["queries"]:
            for tag1 in tags1:
                print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                #print (tag1["dataTagId"] == q["results"][0]["name"]) , tag1["dataTagId"], q["results"][0]["name"]
                if(tag1["dataTagId"] == q["results"][0]["name"]):
                    outputTag = outputQuery[tag1["dataTagId"]]
                    df1 = pd.DataFrame(q["results"][0]["values"],columns=["time","tag1"])

                    dff1 = getperdayavg(df1)
                    print tag1["dataTagId"] , "output tag1 : ", outputTag
                    tags2 = [x for x in tags22 if x["systemInstance"]==tag1["systemInstance"]]
                    print tags2

                    datas2 = getData_last7Days(tags2)
                        #print datas2
                        
                    for data2 in datas2:
                        for q in data2["queries"]:
                            for tag2 in tags2:
                                if(tag2["dataTagId"] == q["results"][0]["name"]):
                                    df2 = pd.DataFrame(q["results"][0]["values"],columns=["time","tag2"])
                                    #df2.loc[0,'time'] = times[1]  # updating time with endtime of getData_2
                                    df2 = df2.dropna()
                                    df2 = df2[df2['tag2']!= "NaN"]
                                    dff2 = getperdayavg(df2) -0.7

                                    print "actual total MW : ",tag2["dataTagId"]
                                    print df2
                                    print "Export : ",tag1["dataTagId"]
                                    print dff1
                                    print "total MW - 0.7: "
                                    print dff2
                                    apc = (dff2['tag2'] - dff1['tag1'])
                                    print "apc : "
                                    print apc
                                    apc7thdays = np.sum(apc*dff2['tag2']) / np.sum(dff2["tag2"])
                                    print np.sum(apc*dff2['tag2'])
                                    print np.sum(dff2["tag2"])
                                    print "apc7thdays : ",apc7thdays
                                    
                                    apc7thdays_perc = 100*(apc7thdays / np.mean(dff2["tag2"] + 0.7))
                                    print "apc7thdays_perc : ",apc7thdays_perc
                                    
                                    
                                    # APC data posting
                                    result = pd.DataFrame()
                                    result[outputTag] = [apc7thdays]
                                    result['time'] = [df2['time'].tolist()[-1]] # adding 1 hour to make real time epoch

                                    datapoints = result[['time',outputTag]].values.tolist()
                                    print datapoints
                                    postbody = [{"name":outputTag,"datapoints":datapoints,"tags":{"type":"derived"}}]
                                    print("######################  end #####################",postbody)
                                    res = requests.post(config["api"]["datapoints"],json=postbody)
                                    
                                    
                                    # APC perc data posting
                                    outputTag = outputTag+"_PERC"
                                    result = pd.DataFrame()
                                    result[outputTag] = [apc7thdays_perc]
                                    result['time'] = [df2['time'].tolist()[-1]] # adding 1 hour to make real time epoch

                                    datapoints = result[['time',outputTag]].values.tolist()
                                    print datapoints
                                    postbody = [{"name":outputTag,"datapoints":datapoints,"tags":{"type":"derived"}}]
                                    print("######################  end #####################",postbody)
                                    res = requests.post(config["api"]["datapoints"],json=postbody)
                                #exit()

totalmwtags
exporttags = getTags("Generator","Power","Export","-")

apcTags = returnOpTags(exporttags,"Generator","Power","Apc","","Calc","_7DAYS_WEIGHTAGE_AVG_APC")
print apcTags
postCalc_apc(apcTags,exporttags,totalmwtags) # opTags, inp1 and inp2 tags

exit()


########################################   BackgroundScheduler   ###########################################    


scheduler = BackgroundScheduler()

if len(coalFlowtags) != 0:
    postCalc(sccTags,coalFlowtags,mwtags,"uniformDivide") # opTags, inp1 and inp2 tags
    scheduler.add_job(func=postCalc,args = [sccTags,coalFlowtags,mwtags,"uniformDivide"] ,trigger="interval", seconds=60)
    print "BackgroundScheduler every 1 min running for Scc"

if len(coalFlowtags) != 0:
    postCalc(evapTags,coalFlowtags,msFlowtags,"oppositeDivide") # opTags, inp1 and inp2 tags
    scheduler.add_job(func=postCalc,args = [evapTags,coalFlowtags,msFlowtags,"oppositeDivide"] ,trigger="interval", seconds=60)
    print "BackgroundScheduler every 1 min running for Eva Ratio"


unitsId_list = ["61c4b560515e2f6d59c00202"]
if len(rawWatertags) != 0 and unitId in unitsId_list:
    postCalc(spRawWaterTags,rawWatertags,mwtags,"uniformDivide")
    scheduler.add_job(func=postCalc,args = [spRawWaterTags,rawWatertags,mwtags,"uniformDivide"] ,trigger="interval", seconds=60)
    print "BackgroundScheduler every 1 min running for Raw Water- unit1 MW req"


unitsId_list = ["611b7fd57afa992d36e308b0"]
if len(rawWatertags) != 0 and unitId in unitsId_list:
    postCalc(spRawWaterTags,rawWatertags,totalmwtags,"uniformDivide") # opTags, inp1 and inp2 tags
    scheduler.add_job(func=postCalc,args = [spRawWaterTags,rawWatertags,totalmwtags,"uniformDivide"] ,trigger="interval", seconds=60)
    print "BackgroundScheduler every 1 min running for Raw Water - total MW req"
    
    
unitsId_list = ["61c4b560515e2f6d59c00202"]
if len(dmWatertags) != 0 and unitId in unitsId_list:
    postCalc(spdmWaterTags,dmWatertags,mwtags,"uniformDivide") # opTags, inp1 and inp2 tags
    scheduler.add_job(func=postCalc,args = [spdmWaterTags,dmWatertags,mwtags,"uniformDivide"] ,trigger="interval", seconds=60)
    print "BackgroundScheduler every 1 min running for DM Water- unit1 MW req"


    
unitsId_list = ["611b7fd57afa992d36e308b0"]
if len(dmWatertags) != 0 and unitId in unitsId_list:
    postCalc(spdmWaterTags,dmWatertags,totalmwtags,"uniformDivide") # opTags, inp1 and inp2 tags
    scheduler.add_job(func=postCalc,args = [spdmWaterTags,dmWatertags,totalmwtags,"uniformDivide"] ,trigger="interval", seconds=60)
    print "BackgroundScheduler every 1 min running for DM Water- unit1 MW req"

    
unitsId_list = ["611b7fd57afa992d36e308b0"]
if len(exporttags) != 0 and unitId in unitsId_list:
    postCalc_apc(apcTags,exporttags,totalmwtags) # opTags, inp1 and inp2 tags
    scheduler.add_job(func=postCalc_apc,args = [apcTags,exporttags,totalmwtags] ,trigger="interval", seconds=60)
    print "BackgroundScheduler every 1 min running for Apc "

scheduler.start()       

while True:
    time.sleep(60)

scheduler.shutdown()

