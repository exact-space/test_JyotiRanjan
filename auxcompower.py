import pandas as pd
import numpy as np
import sys, os
import json
import requests
import app_config as cfg
import paho.mqtt.client as mqtt
from pprint import pprint
import timeseries as ts
import pandas as pd
from datetime import datetime
from pprint import pprint as pp

config = cfg.getconfig()
qr = ts.timeseriesquery()


startTime =1655510400000
endTime = 1655596800000
sampleValue=((int(endTime)-int(startTime))/(1000*60*60*24)+1)
#unitId="61c4a9a9515e2f6d59bff021"
unitId="61caeda654bf6a5bf94bf59a"
sampleUnit = 'days'
agg = "avg"


def getAggVal(startTime, endTime, tags, agg, sampleValue, sampleUnit):
    queries = {}
    metrics = []
    var = {
    "tags": {},
    "name": "",
    "aggregators": [
    {
      "name": agg,
      "sampling": {
        "value": sampleValue,
        "unit": sampleUnit
      }, "align_start_time": True
    }
    ]
    }
    def getdata_api(url,queries):
        #print(url)
        #print(queries)
        res = requests.post(url=url,json = queries)
        
        custJson = json.loads(res.content)
        df_list = []
        for cust in custJson['queries']:

            listOfList = cust['results'][0]['values']
            time = [lists[0] for lists in listOfList ]
            value = [lists[1] for lists in listOfList ]
            tag = cust['results'][0]['name']
            df = pd.DataFrame({"time":time,tag:value})
            df_list.append(df)
        df = pd.concat(df_list, axis=1)
        df = df.loc[:,~df.columns.duplicated()]
        #print df
        return df
    for tag in tags:
        var["name"] = tag
        var_dummy = var.copy()
        metrics.append(var_dummy)
        queries["metrics"] = metrics
        queries["start_absolute"] = startTime
        queries["end_absolute"] = endTime
        url = config['api']['query']
        
        result = getdata_api(url, queries)
        #print result
    return result


@app.route('/devflask1/Auxpowern_Consumption_report', methods=['POST'])

def get_tbwesConfig(unitId):

    if not request.json or not "startTime" in request.json or not "endTime" in request.json or not 'unitsId' in request.json:
        print(request.json)
        abort(400)
    unitId = request.json["unitsId"]
    startTime = request.json["startTime"]
    endTime = request.json["endTime"]
    sampleValue=((int(endTime)-int(startTime))/(1000*60*60*24)+1)
    
    sampleValue=((int(endTime)-int(startTime))/(1000*60*60*24)+1)
    sampleUnit = 'days'
    agg = "avg"
    
    
    urlQuery = config['api']['meta']+'/boilerStressProfiles/?filter={"where":{"unitsId":"'+unitId+'", "type":"AuxpconsRpt"}}'

    
    response = requests.get(urlQuery)
    tagBody = json.loads(response.content)
    
      
    list1=[]
    for k in tagBody[0]["input"]["table"]:
       
        DataTagId = k["tagList"]
        print(DataTagId)
        
        if k["tagList"]==[]:
            avg="-"
        else:
            
            
            try:
                result =getAggVal(startTime, endTime, DataTagId, agg, sampleValue, sampleUnit)
                try:    
                    if np.isnan(result.loc[0][DataTagId[0]]) == True:
                        raise Exception("NaN value found")
                    else:
                        avg = round(result.loc[0][DataTagId[0]],2)
                        #print(avg)

                except Exception as E:
                    print(E)
                    avg = "-"
                
            except:
                print("error at getAggVal")
                table = {"headers":headers,"section":[]}
                return(json.dumps(table),200)    
        #print("______________")
        #print(result[DataTagId[0]].loc[0])
        #print(result.loc[0][DataTagId[0]])
            
        uom = k["unit"]
        desc = k["description"]

        dictionary = {
            "description":desc,
            "unit":uom,
            "average":avg
                        }
        #print(dictionary)               
        list1.append(dictionary)
    #print(list1)
            
        

    #return list1  
    headers=[
    {
        "name":"description",
        "field":"description",
    },
    {
        "name":"UOM",
        "field":"unit"
    },
    {
        "name":"Day Avg",
        "field":"average"
    }
    
    

    ]        
    

    
    
    section =[
        {"values":list1}]

    tables={"headers":headers,"sections":section}
    pp(tables)
    return tables

    

    
    
    
    
tables =get_tbwesConfig(unitId)  
# headers=[
    # {
        # "name":"description",
        # "field":"description",
    # },
    # {
        # "name":"UOM",
        # "field":"unit"
    # },
    # {
        # "name":"Day Avg",
        # "field":"average"
    # }
    
    

    # ]        
    

    
    
# section =[
    # {"values":list1}]

# tables={"headers":headers,"sections":section}
# pp(tables)     
  