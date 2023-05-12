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

config = cfg.getconfig()
qr = ts.timeseriesquery()


unitId="61c4a9a9515e2f6d59bff021"


def get_tbwesConfig(unitId):
    urlQuery = config['api']['meta']+'/boilerStressProfiles/?filter={"where":{"unitsId":"'+unitId+'", "type":"prfmancsumRpt"}}'

    # urln=config['api']['meta']+'/units/'+unitId+'/tagmeta?filter={"where":' + json.dumps(q) +',"fields": ["dataTagId","description","measureUnit","systemName","designValues"]}'
    #print(urlQuery)
    response = requests.get(urlQuery)
    # a = json.loads(response.content)

    # print(json.dumps(a, indent =4))
    
    if(response.status_code==200):
        confiFile = json.loads(response.content)
    else:
        print response.status_code
        print response.content
    return confiFile

    file=get_tbwesConfig(unitId)
    
    
def getperfsumry():
    
    
        urlQuery = config['api']['meta']+'/boilerStressProfiles/?filter={"where":{"unitsId":"'+unitId+'", "type":"prfmancsumRpt"}}'
        response = requests.get(urlQuery)
    
        if(response.status_code==200):
            confiFile = json.loads(response.content)
        else:
            print response.status_code
            print response.content
        return confiFile
    
        file = get_tbwesConfig(unitId)
        
        list1 = []
        for i in file["input"]["table"]:
            tag = i["tagList"]
            print(tag)
            avg = result[tag]
            uom = i["unit"]
            desc = i["description"]
    
            dictionary = {
                "description":desc,
                "unit":uom,
                "average":avg
                            }
            list1.append(dictionary)
            print(list1)
            
            
    
# def getdata_mod2(tag, start, end):
    # urlquery = cfg['api']['query']
    # query = {"start_absolute":start,"end_absolute":end, "metrics":[{'name':tag}]}
    # res = requests.post(urlquery, json = query)
    # res = json.loads(res.content)
    # df = pd.DataFrame(res['queries'][0]['results'][0]['values'],columns=['time',tag])
    # return(df[df.columns[1]].mean())
    
        # def getAggVal(startTime, endTime, tags, agg, sampleValue, sampleUnit):
            
            # sampleValue=((int(endTime)-int(startTime))/(1000*60*60*24)+1)
    
            # result = getAggVal(startTime, endTime, tag, "avg", )
            #result=getdata_mod2(tag, startTime, endTime)
            
    
    #for a in file["input"]    
    
# def getAggVal(startTime, endTime, tags, agg, sampleValue, sampleUnit):
    # queries = {}
    # metrics = []
    # var = {
    # "tags": {},
    # "name": "",
    # "aggregators": [
    # {
      # "name": agg,
      # "sampling": {
        # "value": sampleValue,
        # "unit": sampleUnit
      # }, "align_start_time": True
    # }
    # ]
    # }
    # def getdata_api(url,queries):
        # print(url)
        # print(queries)
        # res = requests.post(url=url,json = queries)
        
        # custJson = json.loads(res.content)
        # df_list = []
        # for cust in custJson['queries']:

            # listOfList = cust['results'][0]['values']
            # time = [lists[0] for lists in listOfList ]
            # value = [lists[1] for lists in listOfList ]
            # tag = cust['results'][0]['name']
            # df = pd.DataFrame({"time":time,tag:value})
            # df_list.append(df)
        # df = pd.concat(df_list, axis=1)
        # df = df.loc[:,~df.columns.duplicated()]
        # print df
        # return df
    # for tag in tags:
        # var["name"] = tag
        # var_dummy = var.copy()
        # metrics.append(var_dummy)
        # queries["metrics"] = metrics
        # queries["start_absolute"] = startTime
        # queries["end_absolute"] = endTime
        # url = config['api']['query']
        
        # result = getdata_api(url, queries)
        # print result
    # return result
    
# def getperfsumry():
    # def get_tbwesConfig(unitId):
    # urlQuery = config['api']['meta']+'/boilerStressProfiles/?filter={"where":{"unitsId":"'+unitId+'", "type":"prfmancsumRpt"}}'

    # urln=config['api']['meta']+'/units/'+unitId+'/tagmeta?filter={"where":' + json.dumps(q) +',"fields": ["dataTagId","description","measureUnit","systemName","designValues"]}'
    # print(urlQuery)
    # response = requests.get(urlQuery)
    # a = json.loads(response.content)

    # print(json.dumps(a, indent =4))
    
    # '''if(response.status_code==200):
        # confiFile = json.loads(response.content)
    # else:
        # print response.status_code
        # print response.content
    # return confiFile'''
    # file = get_tbwesConfig(unitId)
    
    # for a in file["input"]


# for q in Queries:
        # query = config['api']['meta']+'/units/'+unitId+'/tagmeta?filter={"where":' + json.dumps(q) +',"fields": ["dataTagId","description","measureUnit","systemName","designValues"]}'
        # response = requests.get(query)
        # tagBody = json.loads(response.content)
        # print(json.dumps(tagBody, indent = 4))
        # if tagBody!= []:
            # for k in tagBody:
                # TagId.append(str(k['dataTagId']))
                # OtherData.append(k)
            
            
    