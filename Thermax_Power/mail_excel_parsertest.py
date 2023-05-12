import email as em
import base64
from openpyxl import Workbook
from openpyxl import load_workbook
import boto3
import botocore
# import xlsm_parse as xlsm
import pickle
# from time import gmtime, strftime
import subprocess
import os
import base64
import re
import pandas as pd 
import datetime
import timeseries as ts
import requests,json
qr = ts.timeseriesquery()
import time
import numpy as np
import app_config as cfg
import numpy as np
global config
config = cfg.getconfig()

import warnings
warnings.filterwarnings("ignore")
global token
# global afbc1
# global afbc2
# global afbc3
# global dfo
 
# from -> messenger@m.exactspace.co
#Access Key ID:
#AKIAI5ZEM6GFPCIPHFGQ
#Secret Access Key:
#hTDFA585KOzLTulldCkIdfCex7dU0YfNdHxzSN2P

# AWSAccessKeyId =	"AKIAI5ZEM6GFPCIPHFGQ"
# AWSSecretKey =	"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"

AWSAccessKeyId = "AKIATRPA35R6XGJGNVME"
AWSSecretKey = "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"
Bucket_Name = "exactmailreceiver"
 
session = boto3.Session(aws_access_key_id=AWSAccessKeyId, aws_secret_access_key=AWSSecretKey)

s3 = session.resource("s3")
FOLDER_PATH = "/space/es-master/src/excel_parser/"

try:
	with open('files_parsed.pkl', 'rb') as f:
		file_list = pickle.load(f)			
except IOError as e:
	file_list = []
	with open('files_parsed.pkl', 'wb') as f:
		pickle.dump([], f, pickle.HIGHEST_PROTOCOL)


def persist_pickle_file(file_list):
	with open('files_parsed.pkl', 'wb') as f:
		pickle.dump(file_list, f, pickle.HIGHEST_PROTOCOL)


get_last_modified = lambda obj: int(obj.last_modified.strftime('%s'))


bckt = s3.Bucket(Bucket_Name)
objs = [obj for obj in bckt.objects.all()]


objs = [obj for obj in sorted(objs, key=get_last_modified, reverse=True)][0:150]

def DailyFuelReportofJKLC(filename):
    print "Daily Fuel Report of TPP JKLC #1,2,3"    
    path=FOLDER_PATH +filename
    print(path)
    df = pd.read_excel(path)
    print(df)
    #url_loopback = config["api"]["meta"]
    url_loopback='https://pulse.thermaxglobal.com/exactapi'

    def getToken(url):
        print(url)
        query= url+ '/Users/login'
        body={"email":"rohit.r@exactspace.co","password":"Thermax@123","ttl":0}
        res=requests.post(url=query, json=body)
        token=json.loads(res.content)
        token=token['id']
        print(token)
        return token
    
    token=getToken(url_loopback)
    
    def getTagsForEachUnit():
        url='https://pulse.thermaxglobal.com/exactapi/forms?filter={"where":{"unitsId":{"inq":["611b7fd57afa992d36e308b0","61c1818371c20d4a206a2e35"]}},"fields":["fields"]}'

        response = requests.get(url,headers={'Authorization': token})
        
        if response.status_code == 200:
            tags=json.loads(response.content)
            return tags
        else:
            print (response.status_code)
            print(response.content)
            print ("Some error in fetching tags from DB")
        return
    
    
    afbc1={}
    afbc2={}
    afbc3={}

   
    allTags=getTagsForEachUnit()
    
    for i in allTags:
        for j in i["fields"]:
            if 'CHIMNEY_CO' not in j['dataTagId'] or 'RAW_WATER_TOTALIZER' not in j['dataTagId'] or 'DM_WATER' not in j['dataTagId'] or 'AUC_POW_CONS_PRCNT' not in j['dataTagId'] or 'AUX_POW_CONS_KW' not in j['dataTagId']:
                if "JKLC_BLR_1" in j['dataTagId']:
                    afbc1[j['display']]=j['dataTagId']
                elif "JKLC_JKLC" in j['dataTagId']:
                    afbc2[j['display']]=j['dataTagId']
                elif "JKLC3_JKLC3" in j['dataTagId']:
                    afbc3[j['display']]=j['dataTagId']
                
    
            
    def function_read_excel(path,sheet,i):
        df1=pd.DataFrame()
        
        df=pd.read_excel(path,sheet_name=sheet)
        # print df.head()
        df=(df.T)
        # print df.head()
        df.drop(columns={1},inplace=True)
        df.columns = df.iloc[1]
        df = df[2:]
        df=df.reset_index(drop=True)
        df = df.rename_axis(None, axis=1)
        df.rename(columns={ df.columns[0]: "Date" }, inplace = True)
        
        global df3
        if i==0:
            
            df3=df[['Date','CO at the Chimney','Station Raw Water (m3)','Station DM Water (m3)','Auxiliary Power Consumption- Direct (%)','Auxiliary Power Consumption- Direct (MW)']]
            df3["time"] = pd.to_datetime(df3["Date"],errors='coerce').values.astype(np.int64)// 10**6
            df3["time"] = df3["time"] - (5.5*60*60*1000)
            df3=df3.drop(columns=['Date'])
            df3.rename(columns={'CO at the Chimney':'JKLC_JKLC_CHIMNEY_CO', 'Station Raw Water (m3)':'JKLC_JKLC_RAW_WATER_TOTALIZER','Station DM Water (m3)':'JKLC_JKLC_DM_WATER','Auxiliary Power Consumption- Direct (%)':'JKLC_JKLC_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct (MW)':'JKLC_JKLC_AUX_POW_CONS_KW'},inplace=True)
            
        
        elif i==1:
            print('kkkkkkkkk',df.columns)
            df4=df[['Date','CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(MW)']]
            df4["time"] = pd.to_datetime(df4["Date"],errors='coerce').values.astype(np.int64)// 10**6
            df4["time"] = df4["time"] - (5.5*60*60*1000)
            df4=df4.drop(columns=['Date'])
            df4.rename(columns={'CO at the Chimney':'JKLC_JKLC_CHIMNEY_CO', 'Station Raw Water':'JKLC_JKLC_RAW_WATER_TOTALIZER','Station DM Water':'JKLC_JKLC_DM_WATER','Auxiliary Power Consumption- Direct(%)':'JKLC_JKLC_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct(MW)':'JKLC_JKLC_AUX_POW_CONS_KW'},inplace=True)
            df3=pd.concat([df3,df4],axis=0)
            df3=df3.set_index("time")
            print('ssss',df3)
            df3=df3.dropna(how='all')
            df3=df3.reset_index()
            print(df3.columns)
            print(df3)   
            
        elif i==2:
        
            df3=df[['Date','CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(MW)']]
            df3["time"] = pd.to_datetime(df3["Date"],errors='coerce').values.astype(np.int64)// 10**6
            df3["time"] = df3["time"] - (5.5*60*60*1000)
            df3=df3.drop(columns=['Date'])
            df3.rename(columns={'CO at the Chimney':'JKLC3_JKLC3_CHIMNEY_CO', 'Station Raw Water':'JKLC3_RAW_WATER_TOTALIZER','Station DM Water':'JKLC3_JKLC3_DM_WATER','Auxiliary Power Consumption- Direct(%)':'JKLC3_JKLC3_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct(MW)':'JKLC3_JKLC3_AUX_POW_CONS_KW'},inplace=True)
            # print (df3)
	    # print('zzzzzzzzz')
        
        
        if i==0:
            df=df.drop(columns = ['CO at the Chimney','Station Raw Water (m3)','Station DM Water (m3)','Auxiliary Power Consumption- Direct (%)','Auxiliary Power Consumption- Direct (MW)'])
        else:
            try:
                df=df.drop(columns = ['CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)'])
            except:
                df=df.drop(columns = ['CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(MW)'])
        

        
        
        
        df["time"] = pd.to_datetime(df["Date"],errors='coerce').values.astype(np.int64)// 10**6
        df["time"] = df["time"] - (5.5*60*60*1000)
        
        if i==0:
            col=afbc1
        elif i==1:
            col=afbc2
        elif i==2:
            col=afbc3
        df1=df.rename(columns=col)
        # df1=df1.rename(columns = {'CO at the Chimney':'JKLC_JKLC_BLR_1_CHIMNEY_CO', 'Station Raw Water (m3)':'JKLC_JKLC_BLR_1_RAW_WATER_TOTALIZER','Station DM Water (m3)':'JKLC_JKLC_BLR_1_DM_WATER','Auxiliary Power Consumption- Direct (%)':'JKLC_JKLC_BLR_1_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct (MW)':'JKLC_JKLC_BLR_1_AUX_POW_CONS_KW'})
        # df1=df1.rename(columns={'Station Raw Water':'JKLC3_JKLC3_RAW_WATER_TOTALIZER'})
        return df1
    
    path='Daily_Fuel_Report_of_TPP_JKLC.xlsx'
    file_instance = pd.ExcelFile(path)

    dft=pd.DataFrame(columns=['time'])

    for sname,m in zip(file_instance.sheet_names,range(0,len(file_instance.sheet_names))):
        df_out = function_read_excel(path,sname,m)
        if dft.empty:
            dft["time"] = df_out["time"]
        dft=dft.merge(df_out,how="outer",on="time")
        if m==0:
            continue
        else:
            print("I am df3:",df3)
            dft=dft.merge(df3,how="outer",on="time")
    return dft
    
     
def db():
    print "\n\n came to upload data\n\n"
    dfop = pd.read_csv("JKLC_Sirohi_Daily_report.csv")
    qr = ts.timeseriesquery()

    for col in dfop.columns:
        if "JKLC" in col:
        # if col not in ("time","Date", "Date.1"):
            df2 = dfop[["time", col]].dropna()
            data = df2[["time", col]].values.tolist()
            name =  col
            body=[{"name":name,"datapoints":data, "tags" : {"type":"TEST"}}]
            print(body)
            print(qr.postDataPacket(body))
    exit()


def DailyFuelReportofsudarshanchemical(filename):
    print "Daily Fuel Report of TPP SCIL"    
    path=FOLDER_PATH +filename
    print(path)
    dfr= pd.read_excel(path)
    print(dfr)
    #url_loopback = config["api"]["meta"]

    url_loopback='https://pulse.thermaxglobal.com/exactapi'
    
    def getToken(url):
        print(url)
        query= url+ '/Users/login'
        body={"email":"rohit.r@exactspace.co","password":"Thermax@123","ttl":0}
        res=requests.post(url=query, json=body)
        token=json.loads(res.content)
        token=token['id']
        print(token)
        return token
    token=getToken(url_loopback)

    def getTagsForEachUnit():
        url='https://pulse.thermaxglobal.com/exactapi/forms?filter={"where":{"unitsId":"61c4b560515e2f6d59c00202"},"fields":["fields"]}'
        response = requests.get(url,headers={'Authorization': token})
        if response.status_code == 200:
            tags=json.loads(response.content)
#                 print(tags)
            return tags
        else:
            print (response.status_code)
            print(response.content)
            print ("Some error in fetching tags from DB")
        return
    allTags=getTagsForEachUnit()
#     pprint(allTags)
        
    afbc_1={}
    afbc_2={}
    for i in allTags:
        for j in i["fields"]:
#             print(j['dataTagId'])
            if 'CHIMNEY_CO' not in j['dataTagId'] or 'RAW_WATER_TOTALIZER' not in j['dataTagId'] or 'DM_WATER' not in j['dataTagId'] or 'AUC_POW_CONS_PRCNT' not in j['dataTagId'] or 'AUX_POW_CONS_KW' not in j['dataTagId']:
                if "SDCM_CHM1_BLR_1" in j['dataTagId']:
                    afbc_1[j['display']]=j['dataTagId']
                elif "SDCM_CHM1_BLR_2" in j['dataTagId']:
                    afbc_2[j['display']]=j['dataTagId']
                    
#     print(afbc_1)
#     print(afbc_2)
    def function_read_excel(path,sheet,i):
        dfr=pd.read_excel(path,sheet_name=sheet)
        dfr=(dfr.T)
        dfr=dfr.reset_index(drop=True)
        dfr.drop(columns={1},inplace=True)
#         print(dfr.columns)
        # dfr.columns = dfr.iloc[1]
        dfr = dfr.iloc[1: , :]
        dfr.columns = dfr.iloc[0]
        dfr = dfr[1:]
        dfr= dfr.rename_axis(None, axis=1)
        dfr.rename(columns ={np.nan:'Date'}, inplace = True)
#         print(dfr.columns)
      
        global dft
        if i==0:
            dft=dfr[['Date','CO at the Chimney','Station Raw Water (m3)','Station DM Water (m3)','Auxiliary Power Consumption- Direct (%)','Auxiliary Power Consumption- Direct (MW)']]
            dft["time"] = pd.to_datetime(dfr["Date"],errors='coerce').values.astype(np.int64)// 10**6
            dft["time"] = dft["time"] - (5.5*60*60*1000)
            dft=dft.drop(columns=['Date'])
            dft.rename(columns={'CO at the Chimney':'SDCM_CHM1_CHIMNEY_CO', 'Station Raw Water (m3)':'SDCM_RAW_WATER_TOTALIZER','Station DM Water (m3)':'SDCM_CHM1_DM_WATER','Auxiliary Power Consumption- Direct (%)':'SDCM_CHM1_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct (MW)':'SDCM_CHM1_AUX_POW_CONS_KW'},inplace=True)
            print("zzz")
            # print (dft)
        
        elif i==1:
            dfts=dfr[['Date','CO at the Chimney','Station Raw Water (m3)','Station DM Water (m3)','Auxiliary Power Consumption- Direct (%)','Auxiliary Power Consumption- Direct (MW)']]
            dfts["time"] = pd.to_datetime(dfts["Date"],errors='coerce').values.astype(np.int64)// 10**6
            dfts["time"] = dfts["time"] - (5.5*60*60*1000)
            dfts=dfts.drop(columns=['Date'])
            dfts.rename(columns={'CO at the Chimney':'SDCM_CHM1_CHIMNEY_CO', 'Station Raw Water (m3)':'SDCM_RAW_WATER_TOTALIZER','Station DM Water (m3)':'SDCM_CHM1_DM_WATER','Auxiliary Power Consumption- Direct (%)':'SDCM_CHM1_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct (MW)':'SDCM_CHM1_AUX_POW_CONS_KW'},inplace=True)
#             print (dft)
            dft=pd.concat([dft,dfts],axis=0)
            dft=dft.set_index("time")
            print('ssss',dft)
            dft=dft.dropna(how='all')
            dft=dft.reset_index()
            print(dft.columns)
            print(dft)

        if i==0:
            dfr=dfr.drop(columns = ['CO at the Chimney','Station Raw Water (m3)','Station DM Water (m3)','Auxiliary Power Consumption- Direct (%)','Auxiliary Power Consumption- Direct (MW)'])
        else:
            dfr=dfr.drop(columns = ['CO at the Chimney','Station Raw Water (m3)','Station DM Water (m3)','Auxiliary Power Consumption- Direct (%)','Auxiliary Power Consumption- Direct (MW)'])


        dfr["time"] = pd.to_datetime(dfr["Date"],errors='coerce').values.astype(np.int64)// 10**6
        dfr["time"] = dfr["time"] - (5.5*60*60*1000)
        
#         print(dfr.columns)
        
        if i==0:
            col=afbc_1
        elif i==1:
            col=afbc_2
   
        dfm=pd.DataFrame()
        dfm=dfr.rename(columns=col)

        return dfm
        

    # Step-2
    path='Daily.Fuel.Report.TPP.SCIL.xlsx'
    file_instance = pd.ExcelFile(path)
    
    dfs=pd.DataFrame(columns=['time'])

    for sname,m in zip(file_instance.sheet_names,range(0,len(file_instance.sheet_names))):
        df_t = function_read_excel(path,sname,m)
        if dfs.empty:
            dfs["time"] = df_t["time"]
        dfs=dfs.merge(df_t,how="outer",on="time")
    dfs=dfs.merge(dft,how="outer",on="time")
    
    return dfs
    
def dbsudarshan():
    print "\n\n came to upload data\n\n"
    dfo = pd.read_csv("sudarshandailyfuel.csv")
    qr = ts.timeseriesquery()

    for cols in dfo.columns:
        if "SDCM" in cols:
            dft1 = dfo[["time", cols]].dropna()
            data = dft1[["time", cols]].values.tolist()
            print(data)
            name =  cols
            body=[{"name":name,"datapoints":data, "tags" : {"type":"TEST"}}]
            print(body)
            try:
                print(qr.postDataPacket(body))
            except Exception as e:

                print(e)
            
    exit()

def DailyFuelReportofwelspun(filename):
    print "Daily Fuel Report of TPP welspun"    
    path=FOLDER_PATH +filename
    print(path)
    dfw= pd.read_excel(path)
    print(dfw)
    #url_loopback = config["api"]["meta"]

    url_loopback='https://pulse.thermaxglobal.com/exactapi'
    
    
    def getToken(url):
        query= url+ '/Users/login'
        body={"email":"arun@exactspace.co","password":"Thermax@123","ttl":0}
        res=requests.post(url=query, json=body)
        token=json.loads(res.content)
        token=token['id']
    #     print token
        return token

    token=getToken(url_loopback)

    def getTagsForEachUnit():
        url='https://pulse.thermaxglobal.com/exactapi/forms?filter={"where":{"unitsId":"6305e0d850484f124710f231"},"fields":["fields"]}'

        response = requests.get(url,headers={'Authorization': token})

        if response.status_code == 200:
            tags=json.loads(response.content)
            return tags
        else:
            print (response.status_code)
            print ("Some error in fetching tags from DB")
            return
    allTags=getTagsForEachUnit()
    cfbc1={}
    cfbc2={}
    afbc1={}
    afbc2={}
    
    for i in allTags:
        for j in i["fields"]:
            if 'CHIMNEY_CO' not in j['dataTagId'] or 'RAW_WATER_TOTALIZER' not in j['dataTagId'] or 'DM_WATER' not in j['dataTagId'] or 'AUC_POW_CONS_PRCNT' not in j['dataTagId'] or 'AUX_POW_CONS_KW' not in j['dataTagId'] or 'FORCED_OUTAGE' not in j['dataTagId'] or 'STEAM_CONSUMPTION' not in j['dataTagId'] or 'HOPPER_FEEDING' not in j['dataTagId'] or 'BIOMASS_FEEDING' not in j['dataTagId'] or 'UI' not in j['dataTagId']:
                if "WEL1_WEL1_CFBC_1" in j['dataTagId']:
                    cfbc1[j['display']]=j['dataTagId']
                elif "WEL1_WEL1_CFBC_2" in j['dataTagId']:
                    cfbc2[j['display']]=j['dataTagId']
                elif "WEL1_WEL1_AFBC_1" in j['dataTagId']:
                    afbc1[j['display']]=j['dataTagId']
                elif "WEL1_WEL1_AFBC_2" in j['dataTagId']:
                    afbc2[j['display']]=j['dataTagId']
                    
    
    def function_read_excel(path,sheet,i):    
        dfw=pd.read_excel(path,sheet_name=sheet)
        dfw=(dfw.T)
        dfw.head()
        #df.drop(columns={1},inplace=True)
        dfw.columns = dfw.iloc[1]
        dfw = dfw[2:]
        dfw=dfw.reset_index(drop=False)
        dfw = dfw.rename_axis(None, axis=1)
        dfw.rename(columns={ dfw.columns[0]: "Date" }, inplace = True)
        dfw.columns
       

        global df3w
        if i==0:

            df3w=dfw[['Date','CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)','Forced Outage Hrs TG 1','Forced Outage Hrs TG 2','Process steam Consumption from TBC 60','Direct hopper Feeding(%)','Biomass Feeding(TPD)','UI(MWH/Day)']]
            print("i=0",df3w)
            df3w["time"] = pd.to_datetime(df3w["Date"],errors='coerce').values.astype(np.int64)// 10**6
            df3w["time"] = df3w["time"] - (5.5*60*60*1000)
            df3w=df3w.drop(columns=['Date'])
            df3w.rename(columns={'CO at the Chimney':'WEL1_WEL1_1_CHIMNEY_CO', 'Station Raw Water':'WEL1_WEL1_1_RAW_WATER_TOTALIZER','Station DM Water':'WEL1_WEL1_1_DM_WATER','Auxiliary Power Consumption- Direct(%)':'WEL1_WEL1_1_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct(KW)':'WEL1_WEL1_1_AUX_POW_CONS_KW','Forced Outage Hrs TG 1':'WEL1_WEL1_1_FORCED_OUTAGE','Forced Outage Hrs TG 2':'WEL1_WEL1_2_FORCED_OUTAGE','Process steam Consumption from TBC 60':'WEL1_WEL1_1_STEAM_CONSUMPTION','Direct hopper Feeding(%)':'WEL1_WEL1_1_HOPPER_FEEDING','Biomass Feeding(TPD)':'WEL1_WEL1_1_BIOMASS_FEEDING','UI(MWH/Day)':'WEL1_WEL1_1_UI'},inplace=True)
            

        elif i==1:
            df4w=dfw[['Date','CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)','Forced Outage Hrs TG 1','Forced Outage Hrs TG 2','Process steam Consumption from TBC 60']]
            df4w["time"] = pd.to_datetime(df4w["Date"],errors='coerce').values.astype(np.int64)// 10**6
            df4w["time"] = df4w["time"] - (5.5*60*60*1000)
            df4w=df4w.drop(columns=['Date'])
            df4w.rename(columns={'CO at the Chimney':'WEL1_WEL1_1_CHIMNEY_CO', 'Station Raw Water':'WEL1_WEL1_1_RAW_WATER_TOTALIZER','Station DM Water':'WEL1_WEL1_1_DM_WATER','Auxiliary Power Consumption- Direct(%)':'WEL1_WEL1_1_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct(KW)':'WEL1_WEL1_1_AUX_POW_CONS_KW','Forced Outage Hrs TG 1':'WEL1_WEL1_1_FORCED_OUTAGE','Forced Outage Hrs TG 2':'WEL1_WEL1_2_FORCED_OUTAGE','Process steam Consumption from TBC 60':'WEL1_WEL1_1_STEAM_CONSUMPTION','Direct hopper Feeding(%)':'WEL1_WEL1_1_HOPPER_FEEDING','Biomass Feeding(TPD)':'WEL1_WEL1_1_BIOMASS_FEEDING','UI(MWH/Day)':'WEL1_WEL1_1_UI'},inplace=True)
            df3w=pd.concat([df3w,df4w],axis=0)
            df3w=df3w.drop_duplicates().reset_index(drop=True)
            df3w=df3w.set_index("time")
            print('ssss',df3w)
            df3w=df3w.dropna(how='all')
            df3w=df3w.reset_index()
            print(df3w.columns)
        

        elif i==2:

            df3w=dfw[['Date','CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)','Forced Outage Hrs TG 1','Forced Outage Hrs TG 2','Process steam Consumption from TBC 60']]
            df3w["time"] = pd.to_datetime(df3w["Date"],errors='coerce').values.astype(np.int64)// 10**6
            df3w["time"] = df3w["time"] - (5.5*60*60*1000)
            df3w=df3w.drop(columns=['Date'])
            df3w.rename(columns={'CO at the Chimney':'WEL1_WEL1_2_CHIMNEY_CO', 'Station Raw Water':'WEL1_WEL1_2_RAW_WATER_TOTALIZER','Station DM Water':'WEL1_WEL1_2_DM_WATER','Auxiliary Power Consumption- Direct(%)':'WEL1_WEL1_2_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct(KW)':'WEL1_WEL1_2_AUX_POW_CONS_KW','Forced Outage Hrs TG 1':'WEL1_WEL1_3_FORCED_OUTAGE','Forced Outage Hrs TG 2':'WEL1_WEL1_4_FORCED_OUTAGE','Process steam Consumption from TBC 60':'WEL1_WEL1_2_STEAM_CONSUMPTION'},inplace=True)


        elif i==3:
            df4w=dfw[['Date','CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)','Forced Outage Hrs TG 1','Forced Outage Hrs TG 2','Process steam Consumption from TBC 60']]
            df4w["time"] = pd.to_datetime(df4w["Date"],errors='coerce').values.astype(np.int64)// 10**6
            df4w["time"] = df4w["time"] - (5.5*60*60*1000)
            df4w=df4w.drop(columns=['Date'])
            df4w.rename(columns={'CO at the Chimney':'WEL1_WEL1_2_CHIMNEY_CO', 'Station Raw Water':'WEL1_WEL1_2_RAW_WATER_TOTALIZER','Station DM Water':'WEL1_WEL1_2_DM_WATER','Auxiliary Power Consumption- Direct(%)':'WEL1_WEL1_2_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct(KW)':'WEL1_WEL1_2_AUX_POW_CONS_KW','Forced Outage Hrs TG 1':'WEL1_WEL1_3_FORCED_OUTAGE','Forced Outage Hrs TG 2':'WEL1_WEL1_4_FORCED_OUTAGE','Process steam Consumption from TBC 60':'WEL1_WEL1_2_STEAM_CONSUMPTION'},inplace=True)
            df3w=pd.concat([df3w,df4w],axis=0)
            df3w=df3w.drop_duplicates().reset_index(drop=True)

            df3w=df3w.set_index("time")
           
            print('ssss',df3w)
            df3w=df3w.dropna(how='all')
            df3w=df3w.reset_index()
            print(df3w.columns)
      
        if i==0 or i==1:
            dfw=dfw.drop(columns = ['CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)','Forced Outage Hrs TG 1','Forced Outage Hrs TG 2','Process steam Consumption from TBC 60','Direct hopper Feeding(%)','Biomass Feeding(TPD)','UI(MWH/Day)'])
            print(dfw)
        elif i==2 or i==3:
            dfw=dfw.drop(columns = ['CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)','Forced Outage Hrs TG 1','Forced Outage Hrs TG 2','Process steam Consumption from TBC 60'])

        
        dfw["time"] = pd.to_datetime(dfw["Date"],errors='coerce').values.astype(np.int64)// 10**6
        dfw["time"] = dfw["time"] - (5.5*60*60*1000)

        if i==0:
            col=cfbc1
        elif i==1:
            col=cfbc2
        elif i==2:
            col=afbc1
        elif i==3:
            col=afbc2
        df1w=dfw.rename(columns=col)
        return df1w
    
    
    path='./welspun.xlsx'

    file_instance = pd.ExcelFile(path)

    dftw=pd.DataFrame(columns=['time'])
    dft1w=pd.DataFrame(columns=['time'])
    for sname,m in zip(file_instance.sheet_names,range(0,len(file_instance.sheet_names))):
        
        print(m)
        df_outw = function_read_excel(path,sname,m)
        
        if m==0 or m==1:
            if dftw.empty:
                dftw["time"] = df_outw["time"]
            dftw=dftw.merge(df_outw,how="outer",on="time")
        if m==2 or m==3:
            if dft1w.empty:
                dft1w["time"] = df_outw["time"]
            dft1w=dft1w.merge(df_outw,how="outer",on="time")

        if m==1:
            dftw=dftw.merge(df3w,how="outer",on="time")
        if m==3:
            dft1w=dft1w.merge(df3w,how="outer",on="time")

          
    return dftw,dft1w

def dbwelspun():
    print "\n\n came to upload data\n\n"
    dfopwspn = pd.read_csv("welspun1.csv")
    dfpwpn=pd.read_csv("welspun2.csv")
    qr = ts.timeseriesquery()

    for col in dfopwspn.columns:
        if "WEL1_WEL1" in col:
        # if col not in ("time","Date", "Date.1"):
            df2wspn = dfopwspn[["time", col]].dropna()
            data = df2wspn[["time", col]].values.tolist()
            name =  col
            body=[{"name":name,"datapoints":data, "tags" : {"type":"TEST"}}]
            print(body)
            print(qr.postDataPacket(body))
            
    for col in dfpwpn.columns:
        if "WEL1_WEL1" in col:
        # if col not in ("time","Date", "Date.1"):
            df2wpn = dfpwpn[["time", col]].dropna()
            data = df2wpn[["time", col]].values.tolist()
            name =  col
            body=[{"name":name,"datapoints":data, "tags" : {"type":"TEST"}}]
            print(body)
            print(qr.postDataPacket(body))
    exit()
 
def DailyFuelReportofBataan(filename):
    print "Daily Fuel Report of TPP Bataan"    
    path=FOLDER_PATH +filename
    print(path)
    dfb = pd.read_excel(path)
    print (dfb)
    #url_loopback = config["api"]["meta"]
    url_loopback='https://pulse.thermaxglobal.com/exactapi'

    def getToken(url):
        print(url)
        query= url+ '/Users/login'
        body={"email":"rohit.r@exactspace.co","password":"Thermax@123","ttl":0}
        res=requests.post(url=query, json=body)
        token=json.loads(res.content)
        token=token['id']
        print(token)
        return token
    
    token=getToken(url_loopback)
    
    def getTagsForEachUnit():
        url='https://pulse.thermaxglobal.com/exactapi/forms?filter={"where":{"unitsId":"62ff525f0053c325ccf27a1d"},"fields":["fields"]}'

        response = requests.get(url,headers={'Authorization': token})
        
        if response.status_code == 200:
            tags=json.loads(response.content)
            return tags
        else:
            print (response.status_code)
            print(response.content)
            print ("Some error in fetching tags from DB")
        return
    
    
    

   
    allTags=getTagsForEachUnit()
    afbc1={}
    #afbc2={}
    #afbc3={}
    for i in allTags:
        for j in i["fields"]:
            #print("_________")
            #print j['dataTagId']
            if 'CHIMNEY_CO' not in j['dataTagId'] or 'RAW_WATER_TOTALIZER' not in j['dataTagId'] or 'DM_WATER' not in j['dataTagId'] or 'AUC_POW_CONS_PRCNT' not in j['dataTagId'] or 'AUX_POW_CONS_KW' not in j['dataTagId']:
                if "SIK_Bataan_BLR_1" in j['dataTagId']:
                    afbc1[j['display']]=j['dataTagId']
                    #print "{{{{}}"
                    #print afbc1[j['display']]
                # elif "JKLC_JKLC" in j['dataTagId']:
                    # afbc2[j['display']]=j['dataTagId']
                # elif "JKLC3_JKLC3" in j['dataTagId']:
                    # afbc3[j['display']]=j['dataTagId']
                
    
            
    def function_read_excel(path,sheet,i):
        dfb1=pd.DataFrame()
        
        dfb=pd.read_excel(path,sheet_name=sheet)
        # print df.head()
        dfb=(dfb.T)
        print dfb.head()
        
        dfb.columns = dfb.iloc[1]
        dfb = dfb[2:]
        dfb=dfb.reset_index(drop=False)
        dfb = dfb.rename_axis(None, axis=1)
        dfb.rename(columns={ dfb.columns[0]: "Date" }, inplace = True)
        dfb.columns
        print "df is"
        print dfb.columns
        
        global dfb3
        if i==0:
            
            dfb3=dfb[['Date','CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)']]
            dfb3["time"] = pd.to_datetime(dfb3["Date"],errors='coerce').values.astype(np.int64)// 10**6
            dfb3["time"] = dfb3["time"] - (5.5*60*60*1000)
            dfb3=dfb3.drop(columns=['Date'])
            dfb3.rename(columns={'CO at the Chimney':'SIK_Bataan_CHIMNEY_CO', 'Station Raw Water':'SIK_RAW_WATER_TOTALIZER','Station DM Water':'SIK_Bataan_DM_WATER','Auxiliary Power Consumption- Direct(%)':'SIK_Bataan_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct(KW)':'SIK_Bataan_AUX_POW_CONS_KW'},inplace=True)
            #print ("**************")
            #print dfb3
            
        
        # elif i==1:
            # print('kkkkkkkkk',df.columns)
            # dfb4=dfb[['Date','CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)']]
            # dfb4["time"] = pd.to_datetime(dfb4["Date"],errors='coerce').values.astype(np.int64)// 10**6
            # dfb4["time"] = dfb4["time"] - (5.5*60*60*1000)
            # dfb4=dfb4.drop(columns=['Date'])
            # dfb4.rename(columns={'CO at the Chimney':'SIK_Bataan_CHIMNEY_CO', 'Station Raw Water':'SIK_RAW_WATER_TOTALIZER','Station DM Water':'SIK_Bataan_DM_WATER','Auxiliary Power Consumption- Direct(%)':'SIK_Bataan_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct(KW)':'SIK_Bataan_AUX_POW_CONS_KW'},inplace=True)
            # dfb3=pd.concat([dfb3,dfb4],axis=0)
            # dfb3=dfb3.drop_duplicates().reset_index(drop=True)
            # print('ssss',dfb3)
            # dfb3=dfb3.dropna(how='all')
            # dfb3=dfb3.reset_index()
            # print(dfb3.columns)
            # print(dfb3)   
            
        # elif i==2:
        
            # dfb3=df[['Date','CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)']]
            # dfb3["time"] = pd.to_datetime(dfb3["Date"],errors='coerce').values.astype(np.int64)// 10**6
            # dfb3["time"] = dfb3["time"] - (5.5*60*60*1000)
            # dfb3=dfb3.drop(columns=['Date'])
            # dfb3.rename(columns={'CO at the Chimney':'SIK_Bataan_CHIMNEY_CO', 'Station Raw Water':'SIK_RAW_WATER_TOTALIZER','Station DM Water':'SIK_Bataan_DM_WATER','Auxiliary Power Consumption- Direct(%)':'SIK_Bataan_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct(KW)':'SIK_Bataan_AUX_POW_CONS_KW'},inplace=True)
            # print (dfb3)
	    # print('zzzzzzzzz')
        
        
        if i==0:
            dfb=dfb.drop(columns = ['CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)'])
        # else:
            # try:
                # df=df.drop(columns = ['CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)'])
            # except:
                # df=df.drop(columns = ['CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(MW)'])
        

        
        
        
        dfb["time"] = pd.to_datetime(dfb["Date"],errors='coerce').values.astype(np.int64)// 10**6
        dfb["time"] = dfb["time"] - (5.5*60*60*1000)
        
        if i==0:
            col=afbc1
        # elif i==1:
            # col=afbc2
        # elif i==2:
            # col=afbc3
            dfb1=dfb.rename(columns=col)
            # dfb1=dfb1.rename(columns = {'CO at the Chimney':'SIK_Bataan_CHIMNEY_CO', 'Station Raw Water (m3)':'SIK_RAW_WATER_TOTALIZER','Station DM Water (m3)':'SIK_Bataan_DM_WATER','Auxiliary Power Consumption- Direct(%)':'SIK_Bataan_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct (MW)':'SIK_Bataan_AUX_POW_CONS_KW'})
            # dfb1=dfb1.rename(columns={'Station Raw Water':'SIK_RAW_WATER_TOTALIZER'})
            return dfb1
    
    #path ="Daily_Fuel_Report_of_TPP_Bataan.xlsx"
    file_instance = pd.ExcelFile(path)

    dfbt=pd.DataFrame(columns=['time'])

    for sname,m in zip(file_instance.sheet_names,range(0,len(file_instance.sheet_names))):
        print m
        dfb_out = function_read_excel(path,sname,m)
        print ("++++++++++")
        print dfb_out
        if dfbt.empty:
            dfbt["time"] = dfb_out["time"]
        dfbt=dfbt.merge(dfb_out,how="outer",on="time")
        
        dfbt=dfbt.merge(dfb3,how="outer",on="time")
    return dfbt
    
    
     
def dbBataan():
    print "\n\n came to upload data\n\n"
    dfbop = pd.read_csv("Bataan_Daily_report.csv")
    qr = ts.timeseriesquery()

    for col in dfbop.columns:
        if "SIK" in col:
        # if col not in ("time","Date", "Date.1"):
            dfb2 = dfbop[["time", col]].dropna()
            data = dfb2[["time", col]].values.tolist()
            name =  col
            body=[{"name":name,"datapoints":data, "tags" : {"type":"TEST"}}]
            print(body)
            print(qr.postDataPacket(body))
    exit()
    
    
    
    
 
# def SERUMWTP(filename):
    # print "Daily  Report of serum wtp"    
    # path=FOLDER_PATH +filename
    # df = pd.read_excel(path)
    # url_loopback = config["api"]["meta"]
    
    # def getToken(url):
        # query= url+ '/Users/login'
        # body={"email":"admin@exactspace.co","password":"exact@123","ttl":0}
        # res=requests.post(url=query, json=body)
        # token=json.loads(res.content)
        # token=token['id']
        # return token
    # token=getToken(url_loopback)


    # def getTagsForEachUnit():
        # url='https://pulse.thermaxglobal.com/exactapi/forms?filter={"where":{"unitsId":"61c300dc515e2f6d59bfcb48"},"fields":["fields"]}'
        # response = requests.get(url,headers={'Authorization': token})
        # if response.status_code == 200:
            # tags=json.loads(response.content)
                # print(tags)
            # return tags
        # else:
            # print (response.status_code)
            # print ("Some error in fetching tags from DB")
        # return

    # tagsdic={}
    # allTags=getTagsForEachUnit()
    # print(allTags) 
    # for i in allTags:
        # for j in i["fields"]:
            # tagsdic[j['display']]=j['dataTagId']
            # print(tagsdic)
    
    # df=df.T
    # df.head()
    # df.columns=df.iloc[1]
    # df=df[2:]
    # df1=pd.DataFrame()
    # df1=df.rename(columns=tagdic)
    # return df1
    
# def serumdatapostingtodb():
    # print "\n\n came to upload data\n\n"
    # dfo = pd.read_csv("serumwtp.csv")
    # qr = ts.timeseriesquery()

    # for col in dfo.columns:
        # if col!="time":
            # data = df2[["time", col]].values.tolist()
            # name =  col
            # body=[{"name":name,"datapoints":data, "tags" : {"type":"TEST"}}]
            # print(body)
            # print(qr.postDataPacket(body))
    # exit()





def DailyFuelReportofAnkurBio(filename):
    print "Daily Fuel Report of TPP Ankur Bio"    
    path=FOLDER_PATH +filename
    print(path)
    dfb = pd.read_excel(path)
    print (dfb)
    #url_loopback = config["api"]["meta"]
    url_loopback='https://pulse.thermaxglobal.com/exactapi'

    def getToken(url):
        print(url)
        query= url+ '/Users/login'
        body={"email":"rohit.r@exactspace.co","password":"Thermax@123","ttl":0}
        res=requests.post(url=query, json=body)
        token=json.loads(res.content)
        token=token['id']
        print(token)
        return token
    
    token=getToken(url_loopback)
    
    def getTagsForEachUnit():
        url='https://pulse.thermaxglobal.com/exactapi/forms?filter={"where":{"unitsId":"6368e23b9b0d4a0007083d82"},"fields":["fields"]}'

        response = requests.get(url,headers={'Authorization': token})
        
        if response.status_code == 200:
            tags=json.loads(response.content)
            return tags
        else:
            print (response.status_code)
            print(response.content)
            print ("Some error in fetching tags from DB")
        return
    
    
    

   
    allTags=getTagsForEachUnit()
    afbc1={}
    #afbc2={}
    #afbc3={}
    for i in allTags:
        for j in i["fields"]:
            #print("_________")
            #print j['dataTagId']
            if 'CHIMNEY_CO' not in j['dataTagId'] or 'RAW_WATER_TOTALIZER' not in j['dataTagId'] or 'DM_WATER' not in j['dataTagId'] or 'AUC_POW_CONS_PRCNT' not in j['dataTagId'] or 'AUX_POW_CONS_KW' not in j['dataTagId']:
                if "AEE_Abio_BLR_1" in j['dataTagId']:
                    afbc1[j['display']]=j['dataTagId']
                    #print "{{{{}}"
                    #print afbc1[j['display']]
                # elif "JKLC_JKLC" in j['dataTagId']:
                    # afbc2[j['display']]=j['dataTagId']
                # elif "JKLC3_JKLC3" in j['dataTagId']:
                    # afbc3[j['display']]=j['dataTagId']
                
    
            
    def function_read_excel(path,sheet,i):
        dfb1=pd.DataFrame()
        
        dfb=pd.read_excel(path,sheet_name=sheet)
        # print df.head()
        dfb=(dfb.T)
        print dfb.head()
        
        dfb.columns = dfb.iloc[1]
        dfb = dfb[2:]
        dfb=dfb.reset_index(drop=False)
        dfb = dfb.rename_axis(None, axis=1)
        dfb.rename(columns={ dfb.columns[0]: "Date" }, inplace = True)
        dfb.columns
        print "df is"
        print dfb.columns
        
        global dfb3
        if i==0:
            
            dfb3=dfb[['Date','CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)']]
            dfb3["time"] = pd.to_datetime(dfb3["Date"],errors='coerce').values.astype(np.int64)// 10**6
            dfb3["time"] = dfb3["time"] - (5.5*60*60*1000)
            dfb3=dfb3.drop(columns=['Date'])
            dfb3.rename(columns={'CO at the Chimney':'AEE_Abio_CHIMNEY_CO', 'Station Raw Water':'AEE_RAW_WATER_TOTALIZER','Station DM Water':'AEE_Abio_DM_WATER','Auxiliary Power Consumption- Direct(%)':'AEE_Abio_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct(KW)':'AEE_Abio_AUX_POW_CONS_KW'},inplace=True)
            #print ("**************")
            #print dfb3
            
        
        # elif i==1:
            # print('kkkkkkkkk',df.columns)
            # dfb4=dfb[['Date','CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)']]
            # dfb4["time"] = pd.to_datetime(dfb4["Date"],errors='coerce').values.astype(np.int64)// 10**6
            # dfb4["time"] = dfb4["time"] - (5.5*60*60*1000)
            # dfb4=dfb4.drop(columns=['Date'])
            # dfb4.rename(columns={'CO at the Chimney':'SIK_Bataan_CHIMNEY_CO', 'Station Raw Water':'SIK_RAW_WATER_TOTALIZER','Station DM Water':'SIK_Bataan_DM_WATER','Auxiliary Power Consumption- Direct(%)':'SIK_Bataan_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct(KW)':'SIK_Bataan_AUX_POW_CONS_KW'},inplace=True)
            # dfb3=pd.concat([dfb3,dfb4],axis=0)
            # dfb3=dfb3.drop_duplicates().reset_index(drop=True)
            # print('ssss',dfb3)
            # dfb3=dfb3.dropna(how='all')
            # dfb3=dfb3.reset_index()
            # print(dfb3.columns)
            # print(dfb3)   
            
        # elif i==2:
        
            # dfb3=df[['Date','CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)']]
            # dfb3["time"] = pd.to_datetime(dfb3["Date"],errors='coerce').values.astype(np.int64)// 10**6
            # dfb3["time"] = dfb3["time"] - (5.5*60*60*1000)
            # dfb3=dfb3.drop(columns=['Date'])
            # dfb3.rename(columns={'CO at the Chimney':'SIK_Bataan_CHIMNEY_CO', 'Station Raw Water':'SIK_RAW_WATER_TOTALIZER','Station DM Water':'SIK_Bataan_DM_WATER','Auxiliary Power Consumption- Direct(%)':'SIK_Bataan_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct(KW)':'SIK_Bataan_AUX_POW_CONS_KW'},inplace=True)
            # print (dfb3)
	    # print('zzzzzzzzz')
        
        
        if i==0:
            dfb=dfb.drop(columns = ['CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)'])
        # else:
            # try:
                # df=df.drop(columns = ['CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(KW)'])
            # except:
                # df=df.drop(columns = ['CO at the Chimney','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(MW)'])
        

        
        
        
        dfb["time"] = pd.to_datetime(dfb["Date"],errors='coerce').values.astype(np.int64)// 10**6
        dfb["time"] = dfb["time"] - (5.5*60*60*1000)
        
        if i==0:
            col=afbc1
        # elif i==1:
            # col=afbc2
        # elif i==2:
            # col=afbc3
            dfb1=dfb.rename(columns=col)
            # dfb1=dfb1.rename(columns = {'CO at the Chimney':'SIK_Bataan_CHIMNEY_CO', 'Station Raw Water (m3)':'SIK_RAW_WATER_TOTALIZER','Station DM Water (m3)':'SIK_Bataan_DM_WATER','Auxiliary Power Consumption- Direct(%)':'SIK_Bataan_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct (MW)':'SIK_Bataan_AUX_POW_CONS_KW'})
            # dfb1=dfb1.rename(columns={'Station Raw Water':'SIK_RAW_WATER_TOTALIZER'})
            return dfb1
    
    #path ="Daily_Fuel_Report_of_TPP_Bataan.xlsx"
    file_instance = pd.ExcelFile(path)

    dfbt=pd.DataFrame(columns=['time'])

    for sname,m in zip(file_instance.sheet_names,range(0,len(file_instance.sheet_names))):
        print m
        dfb_out = function_read_excel(path,sname,m)
        print ("++++++++++")
        print dfb_out
        if dfbt.empty:
            dfbt["time"] = dfb_out["time"]
        dfbt=dfbt.merge(dfb_out,how="outer",on="time")
        
        dfbt=dfbt.merge(dfb3,how="outer",on="time")
    return dfbt
    
    
     
def dbAnkurBio():
    print "\n\n came to upload data\n\n"
    dfbop = pd.read_csv("AnkurBio_Daily_report.csv")
    qr = ts.timeseriesquery()

    for col in dfbop.columns:
        if "AEE" in col:
        # if col not in ("time","Date", "Date.1"):
            dfb2 = dfbop[["time", col]].dropna()
            data = dfb2[["time", col]].values.tolist()
            name =  col
            body=[{"name":name,"datapoints":data, "tags" : {"type":"TEST"}}]
            print(body)
            print(qr.postDataPacket(body))
    exit()


def DailyFuelReportofmcl(filename):
    print "Daily Fuel Report of TPP mcl"    
    path=FOLDER_PATH +filename
    print(path)
    dfmc= pd.read_excel(path)
    print(dfmc)
    #url_loopback = config["api"]["meta"]

    url_loopback='https://pulse.thermaxglobal.com/exactapi'
    
    def getToken(url):
        print(url)
        query= url+ '/Users/login'
        body={"email":"rohit.r@exactspace.co","password":"Thermax@123","ttl":0}
        res=requests.post(url=query, json=body)
        token=json.loads(res.content)
        token=token['id']
        print(token)
        return token
    token=getToken(url_loopback)

    def getTagsForEachUnit():
        url='https://pulse.thermaxglobal.com/exactapi/forms?filter={"where":{"unitsId":"639810021dda6e0007878d47"},"fields":["fields"]}'
        response = requests.get(url,headers={'Authorization': token})
        if response.status_code == 200:
            tags=json.loads(response.content)
#                 print(tags)
            return tags
        else:
            print (response.status_code)
            print(response.content)
            print ("Some error in fetching tags from DB")
        return
    allTags=getTagsForEachUnit()
#     pprint(allTags)
        
    afbc1={}
    afbc2={}
    for i in allTags:
        for j in i['fields']:
            if (('RAW_WATER_TOTALIZER' not in j['dataTagId']) or ('DM_WATER' not in j['dataTagId']) or ('AUC_POW_CONS_PRCNT' not in j['dataTagId']) or ('AUX_POW_CONS_KW' not in j['dataTagId']) or ('FORCED_OUTAGE' not in j['dataTagId'])):
            # if 1==1:
                if "NLJ_NLJ_BLR_1" in j['dataTagId']:
                    afbc1[j['display']]=j['dataTagId']
                
                elif "NLJ_NLJ_BLR_2" in j['dataTagId']:
                    afbc2[j['display']]=j['dataTagId']
	 
    def function_read_excel(path,sheet,i):
        dfm2=pd.DataFrame()
        dfmc=pd.read_excel(path,sheet_name=sheet)
        dfmc=(dfmc.T)
        dfmc.columns = dfmc.iloc[1]
        dfmc = dfmc[2:]
        dfmc=dfmc.reset_index(drop=False)
        dfmc = dfmc.rename_axis(None, axis=1)
        dfmc.rename(columns={ dfmc.columns[0]: "Date" }, inplace = True)
        dfmc = dfmc.drop(dfmc.columns[[1]], axis=1)  
		#dfmc.columns
        # print dfmc
    
    
        global dfc
        if i==0:
            dfc=dfmc[['Date','Fuel Cost AFBC 1','DM Water Cost','Unit Cost TG 1','Unit Cost TG 2','Steam Generation Cost AFBC 1']]
            dfc["time"] = pd.to_datetime(dfmc["Date"],errors='coerce').values.astype(np.int64)// 10**6
            dfc["time"] = dfc["time"] - (5.5*60*60*1000)
            dfc=dfc.drop(columns=['Date'])
            dfc=dfc.rename(columns={'Fuel Cost AFBC 1':'NLJ_1_FUEL_COST','DM Water Cost':'NLJ_DM_WATER_COST','Unit Cost TG 1':'NLJ_1_UNIT_COST','Unit Cost TG 2':'NLJ_2_UNIT_COST','Steam Generation Cost AFBC 1':'NLJ_NLJ_1_STEAM_COST'})
        #         print(dfc)
        elif i==1:
            dfco=dfmc[['Date','Fuel Cost AFBC 2','DM Water Cost','Unit Cost TG 1','Unit Cost TG 2','Steam Generation Cost AFBC 2']]
            dfco["time"] = pd.to_datetime(dfmc["Date"],errors='coerce').values.astype(np.int64)// 10**6
            dfco["time"] = dfco["time"] - (5.5*60*60*1000)
            dfco=dfco.drop(columns=['Date'])
            dfco=dfco.rename(columns={'Fuel Cost AFBC 2':'NLJ_2_FUEL_COST','DM Water Cost':'NLJ_DM_WATER_COST','Unit Cost TG 1':'NLJ_1_UNIT_COST','Unit Cost TG 2':'NLJ_2_UNIT_COST','Steam Generation Cost AFBC 2':'NLJ_NLJ_2_STEAM_COST'})
            #         print(dfco)
            dfc=pd.concat([dfc,dfco],axis=0)
            dfc=dfc.set_index("time")
            #         print('ssss',dft1)
            dfc=dfc.dropna(how='all')
            dfc=dfc.reset_index()
            #         print(dft1.columns)
        
        
   
        global dft1
        if i==0:
            dft1=dfmc[['Date','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(MW)','Forced Outage Hrs TG 1 (hours)','Forced Outage Hrs TG 2 (hours)']]
            dft1["time"] = pd.to_datetime(dfmc["Date"],errors='coerce').values.astype(np.int64)// 10**6
            dft1["time"] = dft1["time"] - (5.5*60*60*1000)
            dft1=dft1.drop(columns=['Date'])
            dft1.rename(columns={'Station Raw Water':'NLJ_NLJ_1_RAW_WATER_TOTALIZER','Station DM Water':'NLJ_NLJ_1_DM_WATER','Auxiliary Power Consumption- Direct(%)':'NLJ_NLJ_1_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct(MW)':'NLJ_NLJ_1_AUX_POW_CONS_KW','Forced Outage Hrs TG 1 (hours)':'NLJ_NLJ_1_FORCED_OUTAGE','Forced Outage Hrs TG 2 (hours)':'NLJ_NLJ_2_FORCED_OUTAGE'},inplace=True)
            #         print("zzz")
            #         print (dft1)

        elif i==1:
            dft1s=dfmc[['Date','Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(MW)','Forced Outage Hrs TG 2 (hours)','Forced Outage Hrs TG 1 (hours)']]
            dft1s["time"] = pd.to_datetime(dft1s["Date"],errors='coerce').values.astype(np.int64)// 10**6
            dft1s["time"] = dft1s["time"] - (5.5*60*60*1000)
            dft1s=dft1s.drop(columns=['Date'])
            dft1s.rename(columns={'Station Raw Water':'NLJ_NLJ_2_RAW_WATER_TOTALIZER','Station DM Water':'NLJ_NLJ_2_DM_WATER','Auxiliary Power Consumption- Direct(%)':'NLJ_NLJ_2_AUC_POW_CONS_PRCNT','Auxiliary Power Consumption- Direct(MW)':'NLJ_NLJ_2_AUX_POW_CONS_KW','Forced Outage Hrs TG 2 (hours)':'NLJ_NLJ_2_FORCED_OUTAGE','Forced Outage Hrs TG 1 (hours)':'NLJ_NLJ_1_FORCED_OUTAGE'},inplace=True)
            #         print (dft1)
            dft1=pd.concat([dft1,dft1s],axis=0)
            dft1=dft1.set_index("time")
            #         print('ssss',dft1)
            dft1=dft1.dropna(how='all')
            dft1=dft1.reset_index()
            #         print(dft1.columns)
            #         print(dft1)

        if i==0:
            dfmc=dfmc.drop(columns = ['Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(MW)','Forced Outage Hrs TG 1 (hours)','Forced Outage Hrs TG 2 (hours)','Fuel Cost AFBC 1','DM Water Cost','Unit Cost TG 1','Unit Cost TG 2','Steam Generation Cost AFBC 1'])
            
        elif i==1:
            dfmc=dfmc.drop(columns = ['Station Raw Water','Station DM Water','Auxiliary Power Consumption- Direct(%)','Auxiliary Power Consumption- Direct(MW)','Forced Outage Hrs TG 2 (hours)','Forced Outage Hrs TG 1 (hours)','Fuel Cost AFBC 2','DM Water Cost','Unit Cost TG 1','Unit Cost TG 2','Steam Generation Cost AFBC 2'])
            



        dfmc["time"] = pd.to_datetime(dfmc["Date"],errors='coerce').values.astype(np.int64)// 10**6
        dfmc["time"] = dfmc["time"] - (5.5*60*60*1000)

		#         print(dfmc.columns)

        if i==0:
            col=afbc1
        elif i==1:
            col=afbc2

        dfm2=pd.DataFrame()

        dfm2=dfmc.rename(columns=col)

        return dfm2



    path='DailyFuelReportofTPPMCL2.xlsx'
    file_instance = pd.ExcelFile(path)

    dfmcl2=pd.DataFrame(columns=['time'])

    for sname,m in zip(file_instance.sheet_names,range(0,len(file_instance.sheet_names))):
        df_mcl = function_read_excel(path,sname,m)
        if dfmcl2.empty:
            dfmcl2["time"] = df_mcl["time"]
        #print(dfmcl2['time']
        dfmcl2=dfmcl2.merge(df_mcl,how="outer",on="time")
    # dfs=dfs.merge(dft1,how="outer",on="time")
    
    df_mclfinal = pd.merge(pd.merge(dfmcl2,dft1,on='time',how='outer'),dfc,how="outer",on='time')
    
    #df4.columns
    #print(df_mclfinal)
    return df_mclfinal


def dbmcl2():
    print "\n\n came to upload data\n\n"
    dfml = pd.read_csv("MCL2.csv")
    qr = ts.timeseriesquery()


    for col in dfml.columns:
        if "NLJ" in col:
            df2MCL = dfml[["time", col]].dropna()
            data = df2MCL[["time", col]].values.tolist()
            name =  col
            body=[{"name":name,"datapoints":data, "tags" : {"type":"TEST"}}]
            print(body)
            print(qr.postDataPacket(body))
    exit()


    
for obj in objs:
    try:
        print obj.key
        s3.Bucket(Bucket_Name).download_file(obj.key, 'local_email_copy.txt')
        msg = em.message_from_file(open('local_email_copy.txt'))
        print(msg['Subject'])
        # print(msg['From'])
        msg_From = re.findall("[a-zA-Z0-9._]*@[a-zA-Z0-9._]*", msg['From'])

        # if "JKLC" in msg['Subject'] or "Jklc" in msg['Subject']:
            # if "utssq0s9298lgvbgilmsc2cml95gpgfv36c0kd01" in obj.key:
                # continue
            # print "\n\n JKLC fuel Reports Found"
            # attachment = msg.get_payload()[1]
            # msg['Subject'] = msg['Subject'].replace("Fwd: ","")
            # msg['Subject'] = msg['Subject'].replace("RE: ", "re")
            # print msg['Subject'], type(msg['Subject'])
            # fyl = open("Daily_Fuel_Report_of_TPP_JKLC.xlsx","w")
            # print(msg['Subject'])
            # print(msg_From)
            # fylName ="Daily_Fuel_Report_of_TPP_JKLC.xlsx"
            # fyl.write(attachment.get_payload(decode=True)) 
            # fyl.close()
            # df_final=DailyFuelReportofJKLC(fylName)
            # print df_final

            # df_final.to_csv("JKLC_Sirohi_Daily_report.csv",index=False)            
            # db()
            # time.sleep(5)
            # os.remove(fylName)
            
            
            
            
            
        # if "TPP SCIL" in msg['Subject'] or "SCIL" in msg['Subject']:
            # if "utssq0s9298lgvbgilmsc2cml95gpgfv36c0kd01" in obj.key:
                # continue
            # print "\n\n sudarshan chemical daily fuel Reports Found"
            # attachment = msg.get_payload()[1]
            # msg['Subject'] = msg['Subject'].replace("Fwd: ","")
            # msg['Subject'] = msg['Subject'].replace("RE: ", "re")
            # print msg['Subject'], type(msg['Subject'])
            # fyl = open("Daily.Fuel.Report.TPP.SCIL.xlsx","w")
            # print(msg['Subject'])
            # print(msg_From)
            # fylName="Daily.Fuel.Report.TPP.SCIL.xlsx"
            # fyl.write(attachment.get_payload(decode=True)) 
            # fyl.close()
            # dframe=DailyFuelReportofsudarshanchemical(fylName)
            # print(dframe)
            # dframe.to_csv("sudarshandailyfuel.csv",index=False)            
            # dbsudarshan()
            # time.sleep(5)
            # os.remove(fylName) 
            
            
        # if "TPP Welspun" in msg['Subject'] or "Welspun" in msg['Subject']:
            # if "utssq0s9298lgvbgilmsc2cml95gpgfv36c0kd01" in obj.key:
                # continue
            # print "\n\n welspun daily fuel Reports Found"
            # attachment = msg.get_payload()[1]
            # msg['Subject'] = msg['Subject'].replace("Fwd: ","")
            # msg['Subject'] = msg['Subject'].replace("RE: ", "re")
            # print msg['Subject'], type(msg['Subject'])
            # fyl = open("welspun.xlsx","w")
            # print(msg['Subject'])
            # print(msg_From)
            # fylName="welspun.xlsx"
            # fyl.write(attachment.get_payload(decode=True)) 
            # fyl.close()
            # dframewspn,dfrmwpn=DailyFuelReportofwelspun(fylName)
            # dframewspn.to_csv("welspun1.csv",index=False)
            # dfrmwpn.to_csv("welspun2.csv",index=False)            
            # print(dframewspn)
            # dbwelspun()
            # time.sleep(5)
                
        if "TPP Bataan" in msg['Subject'] or "Bataan" in msg['Subject']:
            if "utssq0s9298lgvbgilmsc2cml95gpgfv36c0kd01" in obj.key:
                continue
            print "\n\n Bataan fuel Reports Found"
            attachment = msg.get_payload()[1]
            msg['Subject'] = msg['Subject'].replace("Fwd: ","")
            msg['Subject'] = msg['Subject'].replace("RE: ", "re")
            print msg['Subject'], type(msg['Subject'])
            fyl = open("Daily_Fuel_Report_of_TPP_Bataan.xlsx","w")
            print(msg['Subject'])
            print(msg_From)
            fylName ="Daily_Fuel_Report_of_TPP_Bataan.xlsx"
            fyl.write(attachment.get_payload(decode=True)) 
            fyl.close()
            dfb_final=DailyFuelReportofBataan(fylName)
            print dfb_final

            dfb_final.to_csv("Bataan_Daily_report.csv",index=False)            
            dbBataan()
            time.sleep(5)
        os.remove(fylName)
        
           
        # if "WTP Serum" in msg['Subject']:
            # if "utssq0s9298lgvbgilmsc2cml95gpgfv36c0kd01" in obj.key:
                # continue
            # print "\n\n WTP Serum daily  Reports Found"
            # attachment = msg.get_payload()[1]
            # msg['Subject'] = msg['Subject'].replace("Fwd: ","")
            # msg['Subject'] = msg['Subject'].replace("RE: ", "re")
            # print msg['Subject'], type(msg['Subject'])
            # fyl = open("Serum_WTP_NEW_Format.csv","w")
            # print(msg['Subject'])
            # print(msg_From)
            # fylName ="Serum_WTP_NEW_Format.csv"
            # fyl.write(attachment.get_payload(decode=True)) 
            # fyl.close()
            # df_f=SERUMWTP(fylName)

            # df_f.to_csv("serumwtp.csv",index=False)            
            # serumdatapostingtodb()
            # time.sleep(5)
            # os.remove(fylName)
        
        # if "TPP Ankur" in msg['Subject'] or "Ankur" in msg['Subject']:
            # if "utssq0s9298lgvbgilmsc2cml95gpgfv36c0kd01" in obj.key:
                # continue
            # print "\n\n Ankur Bio fuel Reports Found"
            # attachment = msg.get_payload()[1]
            # msg['Subject'] = msg['Subject'].replace("Fwd: ","")
            # msg['Subject'] = msg['Subject'].replace("RE: ", "re")
            # print msg['Subject'], type(msg['Subject'])
            # fyl = open("Daily_Fuel_Report_of_TPP_AnkurBio.xlsx","w")
            # print(msg['Subject'])
            # print(msg_From)
            # fylName ="Daily_Fuel_Report_of_TPP_AnkurBio.xlsx"
            # fyl.write(attachment.get_payload(decode=True)) 
            # fyl.close()
            # dfb_final=DailyFuelReportofAnkurBio(fylName)
            # print dfb_final

            # dfb_final.to_csv("AnkurBio_Daily_report.csv",index=False)            
            # dbAnkurBio()
            # time.sleep(5)

            
        # if "MCL2" in msg['Subject'] or "TPP MCL2" in msg['Subject']:
            # if "utssq0s9298lgvbgilmsc2cml95gpgfv36c0kd01" in obj.key:
                # continue
            # print "\n\n mcl2 Reports Found"
            # attachment = msg.get_payload()[1]
            # msg['Subject'] = msg['Subject'].replace("Fwd: ","")
            # msg['Subject'] = msg['Subject'].replace("RE: ", "re")
            # print msg['Subject'], type(msg['Subject'])
            # fyl = open("DailyFuelReportofTPPMCL2.xlsx","w")
            # print(msg['Subject'])
            # print(msg_From)
            # fylName ="DailyFuelReportofTPPMCL2.xlsx"
            # fyl.write(attachment.get_payload(decode=True)) 
            # fyl.close()
            # dfofmcl2=DailyFuelReportofmcl(fylName)
            # print(dfofmcl2)
            # dfofmcl2.to_csv("MCL2.csv",index=False)            
            # dbmcl2()
            # time.sleep(5)
      
        
        
        
        
        
        
        
    except:
        pass
        
   
