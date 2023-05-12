import os
import sys
import time
import math
import pytz
import json
import logging
import requests
import itertools
import numpy as np
import pandas as pd
from functools import reduce
from timezonefinder import TimezoneFinder

import messaging as mg
import timeseries as ts
import app_config as cfg

from pprint import pprint as pp
from datetime import datetime as dt
from datetime import datetime, timedelta

from flask_cors import CORS
from flask import Flask, jsonify, request, abort

config = cfg.getconfig()
qr=ts.timeseriesquery()

app = Flask(__name__)
CORS(app)


@app.route("/devflask1/availabilityRepTbwes", methods = ["POST"])
def availability():

    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return super(NpEncoder, self).default(obj)

    def getdata_mod(tag, start, end):
        urlquery =config['api']['query']
        query = {"start_absolute":start,"end_absolute":end, "metrics":[{'name':tag}]}
        res = requests.post(urlquery, json = query)
        res = json.loads(res.content)
        df = pd.DataFrame(res['queries'][0]['results'][0]['values'],columns=['time',tag])
        return(df)

    def getdata_mod_aggs(tag, start, end):
        urlquery =config['api']['query']
        aggregators =  [
            {
              "name": "avg",
              "sampling": {
                            "value": 1,
                            "unit": "hours"
                          },
              "align_sampling": True
            }
          ]
        query = {"start_absolute":start,"end_absolute":end, "metrics":[{'name':tag,"aggregators":aggregators}]}
        res = requests.post(urlquery, json = query)
        res = json.loads(res.content)
        df = pd.DataFrame(res['queries'][0]['results'][0]['values'],columns=['time',tag])
        return(df)
    
    
    def available(value):
        if value < request.json['threshold']:
            return 0
        else:
            return 1
    

    df1=getdata_mod(request.json["dataTagId"], request.json["startTime"], request.json["endTime"])
    df1['available'] = df1[request.json["dataTagId"]].apply(available)
    df1['unavailable'] = 1 - df1['available']
    sampleValue=(request.json["endTime"]-request.json["startTime"])/(1000*60*60)

    try:
        finalDict={"Availability" : round((float(df1['available'].sum())/float(len(df1)))*100,2),
                  "Unavailability" : round((float(df1['unavailable'].sum())/float(len(df1)))*100,2)
                  }
    except:
        finalDict={"Availability" : '-',
                  "Unavailability" : '-'
                  }
    
    
    end = int(time.time()*1000)
    start = end - 63072000000
    df1=getdata_mod_aggs(request.json["dataTagId"], start, end)
    
    def shutdown(value):
        if value < request.json['threshold']:
            return 1
        else:
            return 0
    df1['Shutdown'] = df1[request.json["dataTagId"]].apply(shutdown)
    df1['ShutdownDiff'] = df1['Shutdown'].diff()
    try:
        if len(df1[df1['ShutdownDiff'] == -1]):
            timestamp = df1[df1['ShutdownDiff'] == -1].iloc[-1]['time']
            finalDict['lastStartupDate'] = dt.fromtimestamp(timestamp/1000).strftime("%Y-%B-%d %H:%M:%S")
        else:
            finalDict['lastStartupDate'] = "-"
    except:
        finalDict['lastStartupDate'] = "-"
     
    try:
        if len(df1[(df1['ShutdownDiff'] != 0)]) > 1:
            if df1[(df1['ShutdownDiff'] != 0)].iloc[-1]['ShutdownDiff'] != -1:
                finalDict["lastStartupRunHours"] = (df1[(df1['ShutdownDiff'] != 0)].iloc[-1]['time'] - df1[(df1['ShutdownDiff'] != 0)].iloc[-2]['time'])
                finalDict["lastStartupRunHours"] /= (60 * 60 * 1000)
                finalDict["lastStartupRunHours"] = round(finalDict["lastStartupRunHours"],2)
            else:
                finalDict["lastStartupRunHours"] = request.json["endTime"] - df1[(df1['ShutdownDiff'] != 0)].iloc[-1]['time']
                finalDict["lastStartupRunHours"] /= (60 * 60 * 1000)
                finalDict["lastStartupRunHours"] = round(finalDict["lastStartupRunHours"],2)

        elif len(df1[(df1['ShutdownDiff'] != 0)]) == 1:
            finalDict["lastStartupRunHours"]= request.json["endTime"] - df1[(df1['ShutdownDiff'] != 0)].iloc[-1]['time']
            finalDict["lastStartupRunHours"] /= (60 * 60 * 1000)
            finalDict["lastStartupRunHours"] = round(finalDict["lastStartupRunHours"],2)

        else:
            finalDict["lastStartupRunHours"] = "-"
    except Exception as e:
        finalDict["lastStartupRunHours"]= e
        
    return json.dumps(finalDict, cls=NpEncoder)




       

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, port=7025, debug=False)