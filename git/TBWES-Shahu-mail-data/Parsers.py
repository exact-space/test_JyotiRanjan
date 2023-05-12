#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import time
import re
import requests
import math
import os
from time import strptime
import messaging as mg
import csv
# import paho.mqtt.client as paho
# client.connect("13.251.5.125", 183, 120)



# level -1
# def getEpochFromFilename(filename):
    # return int(time.mktime(strptime(filename[0:9],'%d-%b-%y'))*1000)

def getEpoch(subject):
    # print(subject)
    return (int(time.mktime(strptime(subject[-9:],'%d-%b-%y'))*1000)-19800000)

def transform(taginput):
    filename = "tags-transform.csv"
    taginput = re.sub("([\(\[]).*?([\)\]])", "", taginput.replace("/","").replace("%","").replace(":","_").replace(" ","_").replace("U#","").upper().strip())
    taginput = str(taginput).rstrip("_").replace("___","_").replace("__","_").replace("+","").replace(".","").replace("-","")
    Store = {}
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            Store[line['old_tag']] = line['new_tag'].strip()
    
    if taginput in Store:
        return Store[taginput]
    return taginput

# level 0

# Mill Fineness

def Mill_Fineness_Parser(df):
#     print df.head()
#     if df.empty:
#         print df.shape
#         return "Bad report - " + subject.replace("Fwd: ","")

#     if df.shape[1]!=8 and df.shape[0]>0:
#         return "Bad report - " + subject.replace("Fwd: ","")
    epoch = df.iloc[1][0]
    print epoch
    epoch = strptime(str(epoch), '%Y-%m-%d %H:%M:%S')
    epoch = float(time.mktime(epoch)*1000)
    print epoch
    
    prefix = "LPG_"
    
    tags = []
    for col in df:
        col = col
        if col!="UNIT" and col!="DATE" and col!="MILL":
            suffix = "_" + re.sub("([\(\[]).*?([\)\]])", "", col.replace("%","").replace(" ","_").strip().upper())
#             print suffix
            
            for i, row_value in df[col].iteritems():
                if row_value!="NIL":
#                     mill = "FINENESS_MILL_"+
                    if not math.isnan(df["UNIT"][i]):
                        unit_id = str(int(df["UNIT"][i]))
                    if not math.isnan(row_value):
                        tag = {"name":transform(prefix + unit_id + "_MILL" +str(df["MILL"][i])+ "_" +suffix), "value": float(row_value), "timestamp": epoch, "tags": {"id":"lpgx"}}
                        tags.append(tag)
#     return tags
    return tags

# Master_sheet_Parser
def Master_Sheet_Parser(df):
    print("master sheet called")
    prefix = "LPG_"
    tags = []

    df1 = df.iloc[0:24,].reset_index(drop=True)
    
    df2 = df.iloc[25:,].reset_index(drop=True)
    df2.columns = df.columns
    
    df2 = df2.iloc[ : , [1,2,-1]]
    df1 = df1.iloc[ : , [1,2,-1]]

    for col in df1:
        if col!="Date" and col!="UOM" and col!="Parameter" and col!="Unnamed: 0":
#             unit = re.sub("([\(\[]).*?([\)\]])", "", col.replace("%","").replace(" ","_").replace("U#","").strip().upper())+"_"
            unit = "_3_"
            for i, row_value in df1[col].iteritems():
                epoch = df1[col][0]
                epoch = strptime(str(epoch), '%Y-%m-%d %H:%M:%S')
                epoch = float(time.mktime(epoch)*1000) - 19800000
                if i >=1:
                    if str(df["Unnamed: 0"][i])!="nan":
                        mid = str(df["Unnamed: 0"][i]).upper().replace(" ","_").replace("-","_")
                    if str(df["Parameter"][i])!="nan":
                        mid2 = str(df["Parameter"][i]).upper().replace(" ","_").replace("-","_")
                    else:
                        mid2= ""
                    try:
                        if row_value!="NIL" and not math.isnan(row_value):
                            tag = {"name":transform(prefix +unit+mid+"_"+mid2), "value": float(row_value), "timestamp": epoch, "tags": {"id":"lpgx"}}
                            tags.append(tag)
                    except:
                        continue
    for col in df2:
        if col!="Date" and col!="UOM" and col!="Parameter" and col!="Unnamed: 0":
            unit = "_4_"
            epoch = df1[col][0]
            epoch = strptime(str(epoch), '%Y-%m-%d %H:%M:%S')
            epoch = float(time.mktime(epoch)*1000) - 19800000
            for i, row_value in df2[col].iteritems():
                # if i >=1:
                if str(df["Unnamed: 0"][i])!="nan":
                    mid = str(df["Unnamed: 0"][i]).upper().replace(" ","_").replace("-","_")
                if str(df["Parameter"][i])!="nan":
                    mid2 = str(df["Parameter"][i]).upper().replace(" ","_").replace("-","_")
                else:
                    mid2= ""
                try:
                    if row_value!="NIL" and not math.isnan(row_value):
                        tag = {"name":transform(prefix +unit+mid+"_"+mid2), "value": float(row_value), "timestamp": epoch, "tags": {"id":"lpgx"}}
                        tags.append(tag)
                except:
                    continue
    return tags

# old parsers
def coalParser(filename, subject):
    epoch = getEpoch(subject)
    prefix = "HRD_"
    
    df = pd.read_excel(filename,skiprows=1)
    if df.empty:
        print df.shape
        return "Bad report - " + subject.replace("Fwd: ","")

    if df.shape[1]!=8 and df.shape[0]>0:
        return "Bad report - " + subject.replace("Fwd: ","")
    
    print df
    tags = []
    for col in df:
    #     print(col)
        if col!="Unit":
            suffix = "_" + re.sub("([\(\[]).*?([\)\]])", "", col.replace("%","").replace(" ","_").strip().upper())
            for i, row_value in df[col].iteritems():
                if not math.isnan(row_value):
                    tag = {"name":prefix + str(df["Unit"][i])+suffix, "value": float(row_value), "timestamp": epoch, "tags": {"id":"hrdx"}}
                    tags.append(tag)
    return tags


def unburntParser(filename, subject):
    epoch = getEpoch(subject)

    prefix = "HRD_"
    
    df = pd.read_excel(filename,skiprows=1)
    print(df.shape)
    if df.empty:
        print df.shape
        return "Bad report - " + subject.replace("Fwd: ","")

    if df.shape[1]!=27 and df.shape[0]>0:
        return "Bad report - " + subject.replace("Fwd: ","")

    tags = []

    for col in df:
        col = str(col).strip()
        if col!="Unit" and col!="Sample Date" and col!="SHIFT":
            suffix = "_" + re.sub("([\(\[]).*?([\)\]])", "", col.replace("%","").replace(" ","_").strip().upper())
            for i, row_value in df[col].iteritems():
                if not math.isnan(row_value):
                    epoch2 = time.mktime(strptime(str(df["Sample Date"][i])[:-9] + str(df["SHIFT"][i]),'%Y-%m-%d%H:%M:%S'))*1000 - 19800000
                    tag = {"name":prefix + str(df["Unit"][i])+suffix, "value": float(row_value), "timestamp": int(epoch2), "tags": {"id":"hrdx"}}
                    tags.append(tag)

    # logic for _AVG
#     sample_date = df['Sample Date'].dt.date[0]        
    df = df.groupby('Unit').mean().reset_index()

    for col in df:
        col = str(col).strip()
        if col!="Unit" and col!="Sample Date" and col!="SHIFT":
            suffix = "_" + re.sub("([\(\[]).*?([\)\]])", "", col.replace("%","").replace(" ","_").strip().upper())+"_AVG"
            for i, row_value in df[col].iteritems():
                if not math.isnan(row_value):
                    tag = {"name":prefix + str(df["Unit"][i])+suffix, "value": float(row_value), "timestamp": int(epoch), "tags": {"id":"hrdx"}}
                    tags.append(tag)

    return tags

def sieveParser(filename, subject):
    epoch = getEpoch(subject)
    prefix = "HRD_"
    
    df = pd.read_excel(filename,skiprows=1)
    if df.empty:
        print df.shape
        return "Bad report - " + subject.replace("Fwd: ","")
    
    if df.shape[1]!=9 and df.shape[0]>0:
        return "Bad report - " + subject.replace("Fwd: ","")

    new_cols = [str(col) for col in df.columns][:-1]

    df = df.drop(columns=[-1])
    df.columns = new_cols
    print(df)
    
    tags = []
    for col in df:
#         print(col)
        col = str(col).strip()
        if col!="Unit" and col!="Crusher":
            suffix = "_" + re.sub("([\(\[]).*?([\)\]])", "", col.replace("%","").replace(" ","_").strip().upper())
            for i, row_value in df[col].iteritems():
#                 print(row_value)
                if not math.isnan(row_value):
                    tag = {"name":prefix + str(df["Unit"][i])+"_"+str(df["Crusher"][i])+suffix, "value": float(row_value), "timestamp": epoch, "tags": {"id":"hrdx"}}
#                 print(tag)
                    tags.append(tag)
#                 print(row_value)
            
    return tags

def sieveParser2(filename, subject):
    epoch = getEpoch(subject)
    prefix = "HRD_"
    
    df = pd.read_excel(filename,skiprows=1)
    if df.empty:
        print df.shape
        return "Bad report - " + subject.replace("Fwd: ","")
    
    if df.shape[1]!=8 and df.shape[0]>0:
        print df.shape
        return "Bad report - " + subject.replace("Fwd: ","")
    
    tags = []
    print df
    for col in df:
        if col!="Unit" and col!="Crusher":
            for i, row_value in df[col].iteritems():
                suffix = "_" + re.sub("([\(\[]).*?([\)\]])", "", str(col).strip().upper())
                if not math.isnan(row_value):
                    tag = {"name":prefix + str(df["Unit"][i])+"_"+str(df["Crusher"][i])+suffix, "value": float(row_value), "timestamp": epoch, "tags": {"id":"hrdx"}}
                    tags.append(tag)
            
    return tags

def coalConsumptionParser(filename, subject):
    prefix = "HRD_"

    df = pd.read_excel(filename,skiprows=1)
    if df.empty:
        print df.shape
        return []
    if df.shape[1]!=6 and df.shape[0]>0:
        return []

    print df
    tags = []
    for col in df:
        if col!="Unit" and col!="Unnamed: 0" and col!="Unnamed: 4" and col!="Unnamed: 5" and col!="Boiler":
            suffix = "_" + re.sub("([\(\[]).*?([\)\]])", "", col.replace("%","").replace(" ","_").strip().upper())
            for i, row_value in df[col].iteritems():
                if not math.isnan(row_value):
                    tag = {"name":prefix + str(df["Boiler"][i])+suffix, "value": float(row_value), "timestamp": getEpoch(subject), "tags": {"id":"hrdx"}}
                    print(tag)
                    tags.append(tag)
    return tags

def AdityaMasterParser(filename, subject):
    prefix = "LPG_"
    tags = []

    try:
        tags = tags + Master_Sheet_Parser(pd.read_excel(filename,skiprows=1,sheet_name="Master sheet"))
    except:
        print "master processor not found"

    try:
        tags = tags + Mill_Fineness_Parser(pd.read_excel(filename,skiprows=0,sheet_name="Mill Fineness"))
    except:
        print "mill finness not found"

    return tags

def GSD_Parser(filename, subject):
    df  = pd.read_excel(filename,skiprows=2,sheet_name="Section J",header=0)
    tags = []
    prefix = "GAP_"    
    for col in df:
        if col == "Unnamed: "+ str(len(df.columns) - 1) or col == "Unnamed: "+ str(len(df.columns) - 2):
            for i, row_value in df[col].iteritems():
                if i == 0:
                    tdate = row_value
                    print tdate
                    print "-----"
                elif i == 1:
                    ttime = row_value
                elif i == 2 or i == 13 or i == 41:
                    # empty values or ignore values or nan values or non usefule values
                    continue
                
                else:
                    try:
                        epoch = 1000*int(datetime.datetime.combine(tdate, ttime).strftime('%s'))
                    except:
                        epoch = 1000*int(tdate.strftime('%s'))
                    
                
                if df["Unnamed: 2"][i]!=df["Unnamed: 2"][i]:
                    continue
                    # nan values
                    
                tmp = df["Unnamed: 2"][i]
                    
                if tmp in ["GRAINS","FINES","DRY MIX"]:
                    midfix = tmp
                    continue
                    
                try:
                    newfix =  midfix + "_"+tmp
                except:
                    newfix = tmp
                    
                newfix =  re.sub("([\(\[]).*?([\)\]])", "", newfix.replace("%","").replace(" ","_").strip().upper())
                newfix = newfix.encode('ascii','ignore')
                
                newfix = ''.join(str(newfix).split("\u039c"))                
                newfix = newfix.replace('G\/S','GS').replace('G/S','GS').replace("\|","").replace('\n','').replace('\r\n','')
                newfix = newfix.strip()
                newfix = newfix.replace("_MM","_M")
                
                
                if i>=64 and i<=78:
                    tag_to_post = prefix + newfix.replace("DRY_MIX", "DRY_MIX_CUM") 
                else: 
                    tag_to_post = prefix + newfix
                
                try:
                    tag_payload = {"name": tag_to_post, "timestamp": epoch, "value": float(row_value), "tags": {"unitId": "60ae9143e284d016d3559dfb"}}
                    tags.append(tag_payload)
                except:
                    print "exception"
                    print tag_to_post
                    print row_value
                    
                continue
    return tags

#level 1


def IsBadReport(li):
    if isinstance(li, str):
        print(li)
        # bad report
        # email.add_attachment("/home/ubuntu/app/prc-es/generate-daily-report/report-generator","exactspace_daily_report_11_03_2019.pdf")
        to = ["kshitish.bisi@adityabirla.com","mayur.kakade@adityabirla.com"]
        # to = ["peeyush.s@exactspace.co"]
        data = {"to": to, "subject": str(li), "content": str(li), "fileData": os.environ.get("fileData")}
        res = requests.post(url="http://13.251.5.125/mail/bad-report", json=data)
        print(res)
        print("mail sent")
        return []
    else:
        return li

# def publishToMqtt(dpoint):
#     client.publish("ui")


def postToKairos(li):
    if len(li)==0:
        return
    
    print "posted " + str(len(li)) + " datapoints"
    res = requests.post("http://13.68.199.3/api/v1/datapoints", json=li)
    print(res)
    # print(li)
    # print(res.json())
    return 
# retry

def selectParser(filename, subject):
    # epoch = getEpoch(subject)
    if "Aditya" in subject:
        return AdityaMasterParser(filename,subject)
    elif "Mahan _Carbon" in subject:
        return Mahan_GSD_Parser(filename,subject)
    elif "Sieve Report" in subject:
        datapoints = sieveParser(filename, subject) 
        if "Bad" in datapoints:
            print("using new parser!")
            datapoints = sieveParser2(filename, subject)
        return datapoints
    elif "Unburnt Report" in subject:
        return unburntParser(filename, subject)
    elif "Coal Quality Report" in subject:
        return coalParser(filename, subject)
    elif "Coal Consumption Report" in subject:
        return coalConsumptionParser(filename, subject)
    else:
        print("Parser not found!")
        return []
    
def deleteFile(filename):
    try:
        os.remove(filename)
        print "File deleted"
    except:
        print "File not there"
        

subject = os.environ.get("subject")
filename = os.environ.get("filename")
# filecontents = os.environ.get("fileContents")
print(subject)
print(filename)

if subject and filename:
    print "Processing file"
    if "Mahan" in subject:
        postToKairos(selectParser(filename, subject))
    elif "Aditya" in subject:
        postToKairos(selectParser(filename, subject))
    else:
        postToKairos(IsBadReport(selectParser(filename, subject)))
    # deleteFile(filename)
else:
    print "Subject of filename not found!"
