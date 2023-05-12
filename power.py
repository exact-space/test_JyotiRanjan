import pandas as pd
import numpy as np
import math
import app_config as cfg
import sys, os
import json
import requests
import logging
from datetime import datetime, timedelta
from flask_cors import CORS
import timeseries as ts
from flask import Flask, jsonify, request, abort
from werkzeug.middleware.profiler import ProfilerMiddleware
from datetime import datetime as dt
import time
import math
import grequests
from functools import reduce
from pprint import pprint as pp

config = cfg.getconfig()
qr=ts.timeseriesquery()



#@app.route('/test/sensordata/tbwes-summary-report', methods=['POST']) 
def get_summary_report():
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    ############ TEST CODE  ###############
    #responsebody = [{"name":"Net Feul Consuption","value":11,"startTime":13443142100,"endTime":13243421200},{"name":"Net Steam Generation","value":11,"startTime":13443142100,"endTime":13243421200},{"name":"Resultant Steam To Fuel Ratio","value":11,"startTime":13443142100,"endTime":13243421200},{"name":"Average Indirect Efficiency","value":11,"startTime":13443142100,"endTime":13243421200},{"name":"Net Power Consumption","value":11,"startTime":13443142100,"endTime":13243421200},{"name":"Cost of Power","value":11,"startTime":13443142100,"endTime":13243421200},{"name":"Cost of Fuel","value":11,"startTime":13443142100,"endTime":13243421200},{"name":"Cost of Water","value":11,"startTime":13443142100,"endTime":13243421200},{"name":"Cost of Steam","value":11,"startTime":13443142100,"endTime":13243421200},{"name":"Cost of 1 Kg Steam","value":11,"startTime":13443142100,"endTime":13243421200}]
    #return json.dumps(responsebody), 200
    #######################################
    
    # if not request.json or not 'startTime' in request.json or not 'endTime' in request.json or not 'unitsId' in request.json:
        # abort(400)
    # startTime = request.json["startTime"]
    # endTime = request.json["endTime"]
    # unitId = request.json["unitsId"]
    startTime = 1672554219000
    endTime = 1673437324000
    unitId = "61c0c34bb45a623b64fc3b12"
    # FETCHING META
    netFuelFlowMeta = getTags("Fuel Feeding And Combustion System","Fuel","Totalized Flow",unitId)
    print(netFuelFlowMeta)
    netSteamFlowMeta = getTags("Steam Flow System","Steam","Totalized Flow",unitId)
    costOfFuelMeta = getTags("Station Performance","Fuel","Cost",unitId)  # not req
    print(costOfFuelMeta)
    costOfWaterMeta = getTags("Station Performance","Water","Cost",unitId) # tbwes not req
    print(costOfWaterMeta)
    IndBlrEffGCV = getTags("Performance Kpi","Boiler","Indirect Boiler Efficiency Gcv",unitId)
    print(IndBlrEffGCV)
    netFwFlowMeta = getTags("Feed Water System","Feed Water","Totalized Flow",unitId)
    print(netFwFlowMeta)
    blrDirectEff = getTags("Performance Kpi","Boiler","Direct Efficiency",unitId)
    print(blrDirectEff)
    sfr = getTags("Station Performance","Boiler","SFR",unitId)

    # indirect eff req for tbwes
    
    
    # print blrDirectEff
    # if len(netFuelFlowMeta)==len(netSteamFlowMeta)==len(costOfFuelMeta)==len(costOfWaterMeta)==len(IndBlrEffGCV)==len(netFwFlowMeta)== (blrDirectEff)==1:
        # print " *******************  meta is properly fetched.  *******************"
    # else:
        # print len(netFuelFlowMeta),len(netSteamFlowMeta),len(costOfFuelMeta),len(costOfWaterMeta),len(IndBlrEffGCV),len(netFwFlowMeta),len(blrDirectEff)    #costOfWaterMeta = getTags("Station Performance","Water","Cost",unitId)
        # print "xxxxxxxxxxxxxxxxxxxxxx   lenght of meta is misallinged. xxxxxxxxxxxxxxxxxxxxxx"
    try:    
        meta1,meta2,meta3,meta4,meta5,meta6,meta7,meta8 = matching1MetaBySysIns(netFuelFlowMeta,netSteamFlowMeta,costOfFuelMeta,costOfWaterMeta,IndBlrEffGCV,netFwFlowMeta,blrDirectEff,sfr)
    except Exception as e:
        print "Exception Error proprer meta not found ," ,e
        meta1,meta2,meta3,meta4,meta5,meta6,meta7,meta8 = netFuelFlowMeta[0],netSteamFlowMeta[0],costOfFuelMeta[0],costOfWaterMeta[0],IndBlrEffGCV[0],netFwFlowMeta[0],blrDirectEff[0],sfr[0]
    #print("EEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    #print meta6
    # print "@@@@@@@@@@@@@@@@@@1213@@@@@@@@@@@@@@@@@@@"
    if len(meta1) != 0 and len(meta2) != 0 and len(meta3) != 0 and len(meta4) != 0  and len(meta5) != 0  and len(meta6) != 0 and len(meta7) and len(meta8) :
        
        tag1 = meta1["dataTagId"]
        tag2 = meta2["dataTagId"]
        tag3 = meta3["dataTagId"]
        tag4 = meta4["dataTagId"]
        tag5 = meta5["dataTagId"]
        tag6 = meta6["dataTagId"]
        tag7 = meta7["dataTagId"]
        tag8 = meta8["dataTagId"]

        #print tag1 ,tag2, tag3, tag4,tag5, tag7
       
        data1 = getData2(tag1,startTime,endTime)
        data2 = getData2(tag2,startTime,endTime)
        data3 = getData2(tag3,startTime,endTime)
        data4 = getData2(tag4,startTime,endTime)
        data5 = getData2(tag5,startTime,endTime)
        data6 = getData2(tag6,startTime,endTime)
        data7 = getData2(tag7,startTime,endTime)
        data8 = getData2(tag8,startTime,endTime)

        #print data3
        
        for d1,d2,d3,d4,d5,d6,d7,d8 in zip(data1,data2,data3,data4,data5,data6,data7,data8):
            for q1,q2,q3,q4,q5,q6,q7,q8 in zip(d1["queries"],d2["queries"],d3["queries"],d4["queries"],d5["queries"],d6["queries"],d7["queries"],d8["queries"]):
                                    
                df1 = pd.DataFrame(q1["results"][0]["values"],columns=["time","tag1"])
                df2 = pd.DataFrame(q2["results"][0]["values"],columns=["time","tag2"])
                df3 = pd.DataFrame(q3["results"][0]["values"],columns=["time","tag3"])
                df4 = pd.DataFrame(q4["results"][0]["values"],columns=["time","tag4"])
                df5 = pd.DataFrame(q5["results"][0]["values"],columns=["time","tag5"])
                df6 = pd.DataFrame(q6["results"][0]["values"],columns=["time","tag6"])
                df7 = pd.DataFrame(q7["results"][0]["values"],columns=["time","tag7"])
                df8 = pd.DataFrame(q8["results"][0]["values"],columns=["time","tag8"])
                
                
                df1 = dataCleaning(df1,'tag1')
                df2 = dataCleaning(df2,'tag2')
                df3 = dataCleaning(df3,'tag3')
                df4 = dataCleaning(df4,'tag4')
                df5 = dataCleaning(df5,'tag5')
                df6 = dataCleaning(df6,'tag6')
                df7 = dataCleaning(df7,'tag7')
                df8 = dataCleaning(df8,'tag8')

                
                # Net Fuel flow
                if len(df1)> 0:
                    try:
                        
                        # first_df1 = df1["tag1"].tolist()[0]
                        # last_df1 = df1['tag1'].tolist()[-1]
                        # netFuelFlow = (last_df1 - first_df1)
                        netFuelFlow = removingNegativeDiff(df1,'tag1')
                        if 'kg' in meta1['measureUnit'].lower() or 'kgs' in meta1['measureUnit'].lower():
                            netFuelFlow  /=1000.0
                            meta1['measureUnit'] = 'TONS'
                        # if netFuelFlow > 100000:
                            # netFuelFlow  /=1000.0  
                            # meta1['measureUnit'] = 'TONS'
                    except Exception as e:
                        print e, "first_df1"
                        netFuelFlow = 0
                else:
                    netFuelFlow = 0
                    
                #print "netFuelFlow : ",netFuelFlow
                
                
                # Net Steam Flow
                if len(df2)> 0:
                    try:
                        
                        # first_df2 = df2["tag2"].tolist()[0]
                        # last_df2 = df2['tag2'].tolist()[-1]
                        # netSteamFlow = (last_df2 - first_df2)
                        
                        # using shift method to find and remove the negative diff
                        netSteamFlow = removingNegativeDiff(df2,'tag2')
                        if 'kg' in meta2['measureUnit'].lower() or 'kgs' in meta2['measureUnit'].lower():
                            netSteamFlow  /=1000.0
                            meta2['measureUnit'] = 'TONS'
                        
                    except Exception as e:
                        print e , "first_df2"
                        netSteamFlow = 0
                else:
                    netSteamFlow = 0
                #print "netSteamFlow: ",netSteamFlow
                
                # Steam to fuel ratio
                if netFuelFlow > 0:
                    if 'kg' in meta1['measureUnit'].lower() and 'ton' in meta2['measureUnit'].lower():
                        #steamToFuel = netSteamFlow/netFuelFlow                        
                        steamToFuelUnit = "ton/kg"
                    elif ('ton' in meta1['measureUnit'].lower() or 'tons' in meta1['measureUnit'].lower()) and 'kg' in meta2['measureUnit'].lower():
                        #steamToFuel = netSteamFlow/netFuelFlow                        
                        steamToFuelUnit = "kg/ton"
                    else:
                        #steamToFuel = netSteamFlow/netFuelFlow  
                        steamToFuelUnit = ""
                else:
                    steamToFuelUnit = ""
                    #steamToFuel= 0             
                    
                    
                    
                #print "steamToFuel : " , steamToFuel
                #print df3
                
                # Cost of fuel
                #if len(df3)==0:
                
                # get last value from database.
                data = getLastValues(tag3)
                df3 = pd.DataFrame(data[0]['values'],columns=["time","tag3"])
                    
                    #print "Rohit"*100
                    #print df3
                if len(df3) > 0:
                    if 'kg' in meta1['measureUnit'].lower():
                        costOfFuel = netFuelFlow*df3["tag3"].tolist()[-1]
                    elif 'ton' in meta1['measureUnit'].lower() or 'tons' in meta1['measureUnit'].lower():
                        costOfFuel = 1000*netFuelFlow*df3["tag3"].tolist()[-1]
                    else:
                        costOfFuel = netFuelFlow*df3["tag3"].tolist()[-1]
                    #print "costOfFuel : ", costOfFuel
                else:
                    costOfFuel = 0
                    
                    
                # Net Fw flow    
                #print df6
                if len(df6) > 0:
                    try:
                        # first_df6 = df6["tag6"].tolist()[0]
                        # last_df6 = df6['tag6'].tolist()[-1]
                        # netFwFlow = (last_df6 - first_df6)
                        netFwFlow = removingNegativeDiff(df6,"tag6")
                    except Exception as e:
                        print e , "first_df6"
                        netFwFlow = 0
                else:
                    netFwFlow = 0
                #print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                #print "netFwFlow: ",netFwFlow , " first_df6 ", first_df6, " last_df6 "  ,last_df6," startdate ",df6["time"].tolist()[0], "enddate :",df6['time'].tolist()[-1]
                
                #print("#################")
                
                # cost of water
                #if len(df4)==0:
                data = getLastValues(tag4)                   
                df4 = pd.DataFrame(data[0]['values'],columns=["time","tag4"])

                   
                if len(df4) > 0:
                    if 'kg' in meta6['measureUnit'].lower():  # meta6 has Feed water flow tag.
                        costOfWater = netFwFlow*df4["tag4"].tolist()[-1]  # df4["tag4"] is cost of water, received from manual entry.
                    elif ('ton' in meta6['measureUnit'].lower() or 'tons' in meta6['measureUnit'].lower()):
                        costOfWater = 1000*netFwFlow*df4["tag4"].tolist()[-1]
                    else:
                        costOfWater = 1000*netFwFlow*df4["tag4"].tolist()[-1]
                else:
                    costOfWater = 0 
                    
                #print "cost of water : ", costOfWater , " len of df4 : ", len(df4) , " net fuel flow : ", netFwFlow, " meta6 measureunit ", meta6['measureUnit']
                

               
                # cost if steam per kg
                costOfSteam = costOfWater + costOfFuel
                if netSteamFlow > 0:
                    if 'kg' in meta2['measureUnit'].lower():  # meta2 has net steam flow tag.
                        costOfSteam_1kg = costOfSteam/netSteamFlow 
                    elif 'ton' in meta2['measureUnit'].lower():
                        costOfSteam_1kg = costOfSteam/(1000*netSteamFlow)
                    else:
                        costOfSteam_1kg = costOfSteam/netSteamFlow
                else:
                    costOfSteam_1kg = 0
                    
                    
                    
                # average Indirect eff
                #print df5
                if len(df5) ==0:
                    df5 = 0
                else:
                    df5 = df5["tag5"].mean()
                
                
                # average direct eff
                #print df5
                if len(df7) ==0:
                    df7 = 0
                else:
                    df7 = df7["tag7"].mean()
                
                
                ## SFR
                if len(df8) == 0:
                    steamToFuel = 0
               
                else:
                    steamToFuel = df8['tag8'].mean()
                    if steamToFuel > 100:
                        steamToFuel = steamToFuel / 1000
                    
                body = [{"name": "Net Fuel Consumption" ,"value": round(netFuelFlow,2),"unit":meta1['measureUnit'],"startTime":startTime,"endTime":endTime},
                           {"name":"Net Steam Generation","value":round(netSteamFlow,2),"unit":meta2['measureUnit'],"startTime":startTime,"endTime":endTime},
                           {"name":"Resultant Steam To Fuel Ratio","value":round(steamToFuel,2),"unit":steamToFuelUnit,"startTime":startTime,"endTime":endTime},
                           {"name":"Average Indirect Efficiency","value":round(df5,2),"unit":"%","startTime":startTime,"endTime":endTime},
                           {"name":"Average direct Efficiency","value":round(df7,2),"unit":"%","startTime":startTime,"endTime":endTime},                           
                           {"name":"Net Power Consumption","value":"-","unit":"MW","startTime":startTime,"endTime":endTime},
                           {"name":"Cost of Power","value":"-","unit":"Rs","startTime":startTime,"endTime":endTime},
                           {"name":"Cost of Fuel","value":round(costOfFuel,2),"unit":"Rs","startTime":startTime,"endTime":endTime},
                           {"name":"Cost of Water","value":round(costOfWater,2),"unit":"Rs","startTime":startTime,"endTime":endTime},		   
                           {"name":"Cost of Steam","value":round(costOfSteam,2),"unit":"Rs","startTime":startTime,"endTime":endTime},	
                           {"name":"Cost of 1 Kg Steam","value":round(costOfSteam_1kg,2),"unit":"Rs","startTime":startTime,"endTime":endTime}]
                           
                
                df1=pd.DataFrame(body)
                df1.dropna(inplace=True)
                body =  df1.to_dict(orient='records')
                print body
                #return json.dumps(body), 200
                


v = get_summary_report()
print(v)
                