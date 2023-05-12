import numpy as np
import pandas as pd
import datetime 
from dateutil import parser
import time
import timeseries as ts
qr = ts.timeseriesquery()

def shahu60():
    df = pd.read_excel('Shahu APC Daily report.xlsx',sheet_name='Aux Power sheet 60')

    df1=df.copy(deep=True)
    df1 = df.loc[:, ['Unnamed: 1']]
    df1.columns = ['Date']
    a = df1.iloc[3]['Date']
    b=a[5:]
    format = '%d/%m/%Y' # The format
    datetime_str = datetime.datetime.strptime(b, format)
    datetime_str=int(time.mktime(datetime_str.timetuple()))
    print(datetime_str)

    df.drop('Unnamed: 0',axis=1,inplace=True)
    df = df.iloc[5:]
    df.columns = ['Equipment','Parameter','Unit','SHIFT1','SHIFT2','SHIFT3']
    df['Equipment']=df.fillna(method='ffill')
    df = df.iloc[1:]
    df=df.reset_index(drop=True)
    df[['SHIFT1','SHIFT2','SHIFT3']] =  df[['SHIFT1','SHIFT2','SHIFT3']].fillna(0)
    df=df.replace(np.nan, '')
    date = datetime_str
    tph = "60_TPH_"



    list_of_dicts = []

    dictionary = dict(name=[],v=[],t=[])

    for i in range(len(df)):
        row = df.iloc[i]
        equipment, parameter, unit = row['Equipment'], row['Parameter'], row['Unit']
        shift1, shift2, shift3 = row['SHIFT1'], row['SHIFT2'], row['SHIFT3']
        shifts = [shift1,shift2,shift3]
        #cnt = [5,8,8]
        cnt = [5,13,21]
        count=0
        if equipment != np.nan:
            for shift in shifts:
                equipment = str(equipment).split()
                equipment = '_'.join(equipment)
                dictionary['name'].append(tph+equipment+"_"+str(parameter)+"_"+str(unit)+"_rpt")
                dictionary['v'].append(shift)
                dictionary['t'].append(date+(cnt[count]*3600)-19800)
                count=count+1

    for i in cnt:
        print(i)

    dictionary = pd.DataFrame(dictionary)
    dictionary
    dictionary['name'] = dictionary['name'].replace(['60_TPH_BOILER_STEAM_FLOW_(TPH)___rpt'], '60_TPH_BOILER_STEAM_FLOW_rpt')
    finaldict=dictionary.to_dict('index')
    finaldict=dictionary.to_dict('records')
    print("hhdhdhhdhd",finaldict)

    for i in finaldict:
        qr.postData(i['name'], [[i['t']*1000,i['v']]] ,{"tags":i['name']})
        
def shahu70():

    df = pd.read_excel('Shahu APC Daily report.xlsx',sheet_name='Aux Power sheet 70')

    df1=df.copy(deep=True)
    df1 = df.loc[:, ['Unnamed: 1']]
    df1.columns = ['Date']
    a = df1.iloc[3]['Date']
    b=a[5:]
    format = '%d/%m/%Y' # The format
    datetime_str = datetime.datetime.strptime(b, format)
    datetime_str=int(time.mktime(datetime_str.timetuple()))
    print(datetime_str)

    df.drop('Unnamed: 0',axis=1,inplace=True)
    df = df.iloc[5:]
    df.columns = ['Equipment','Parameter','Unit','SHIFT1','SHIFT2','SHIFT3']
    df['Equipment']=df.fillna(method='ffill')
    df = df.iloc[1:]
    df=df.reset_index(drop=True)
    df[['SHIFT1','SHIFT2','SHIFT3']] =  df[['SHIFT1','SHIFT2','SHIFT3']].fillna(0)
    df=df.replace(np.nan, '')
    date = datetime_str
    tph = "Applications.App_70_TPH_"


    list_of_dicts = []

    dictionary = dict(name=[],v=[],t=[])

    for i in range(len(df)):
        row = df.iloc[i]
        equipment, parameter, unit = row['Equipment'], row['Parameter'], row['Unit']
        shift1, shift2, shift3 = row['SHIFT1'], row['SHIFT2'], row['SHIFT3']
        shifts = [shift1,shift2,shift3]
        #cnt = [5,8,8]
        cnt = [5,13,21]
        count=0
        if equipment != np.nan:
            for shift in shifts:
                equipment = str(equipment).split()
                equipment = '_'.join(equipment)
                dictionary['name'].append(tph+equipment+"_"+str(parameter)+"_"+str(unit)+"_rpt")
                dictionary['v'].append(shift)
                dictionary['t'].append(date+(cnt[count]*3600)-19800)
                count=count+1

    for i in cnt:
        print(i)

    dictionary = pd.DataFrame(dictionary)
    dictionary
    dictionary['name'] = dictionary['name'].replace(['Applications.App_70_TPH_BOILER_STEAM_FLOW_(TPH)___rpt'], 'Applications.App_70_TPH_BOILER_STEAM_FLOW_rpt')
    finaldict=dictionary.to_dict('index')
    finaldict=dictionary.to_dict('records')
    print("hhdhdhhdhd",finaldict)

    for i in finaldict:
       qr.postData(i['name'], [[i['t']*1000,i['v']]] ,{"tags":i['name']})

def shahumean60():
    df = pd.read_excel('Shahu APC Daily report.xlsx',sheet_name='Aux Power sheet 60')
    #print("hhhh",df)

    df1 = df.copy(deep=True)
    df1 = df.loc[:, ['Unnamed: 1']]
    df1.columns = ['Date']
    a = df1.iloc[3]['Date']
    b=a[5:]
    format = '%d/%m/%Y' # The format
    datetime_str = datetime.datetime.strptime(b, format)
    datetime_str = int(time.mktime(datetime_str.timetuple()))
    #print(datetime_str)

    df.drop('Unnamed: 0',axis=1,inplace=True)
    df = df.iloc[5:]
    df.columns = ['Equipment','Parameter','Unit','SHIFT1','SHIFT2','SHIFT3']
    df['Equipment']=df.fillna(method='ffill')

    df = df.iloc[1:]
    df = df.reset_index(drop=True)
    df[['SHIFT1','SHIFT2','SHIFT3']] =  df[['SHIFT1','SHIFT2','SHIFT3']].fillna(0)

    df = df.replace(np.nan, '')
    df = df.replace(0, np.NaN)

    date = datetime_str
    tph = "60_TPH_"
    df['mean'] = df[['SHIFT1', 'SHIFT2','SHIFT3']].mean(axis=1)

    df = df.replace(np.NaN, 0)
    df["mean"]=df["mean"].round(2)

    list_of_dicts = []

    dictionary = dict(name=[],v=[],t=[])

    for i in range(len(df)):
        row = df.iloc[i]
        equipment, parameter, unit = row['Equipment'], row['Parameter'], row['Unit']
        mean = row['mean']
        
        if equipment != np.nan:
                equipment = str(equipment).split()
                equipment = '_'.join(equipment)
                dictionary['name'].append(tph+equipment+"_"+str(parameter)+"_"+str(unit)+"_mean_rpt")
                dictionary['v'].append(mean)
                dictionary['t'].append(date-19800)
     
    dictionary = pd.DataFrame(dictionary)
    dictionary['name'] = dictionary['name'].replace(['60_TPH_BOILER_STEAM_FLOW_(TPH)___mean_rpt'], '60_TPH_BOILER_STEAM_FLOW_mean_rpt')

    finaldict=dictionary.to_dict('index')
    finaldict=dictionary.to_dict('records')
    print(finaldict)

    for i in finaldict:
        qr.postData(i['name'], [[i['t']*1000,i['v']]] ,{"tags":i['name']})

def shahumean70():

    df = pd.read_excel('Shahu APC Daily report.xlsx',sheet_name='Aux Power sheet 70')
    #print("hhhh",df)

    df1 = df.copy(deep=True)
    df1 = df.loc[:, ['Unnamed: 1']]
    df1.columns = ['Date']
    a = df1.iloc[3]['Date']
    b=a[5:]
    format = '%d/%m/%Y' # The format
    datetime_str = datetime.datetime.strptime(b, format)
    datetime_str = int(time.mktime(datetime_str.timetuple()))
    #print(datetime_str)

    df.drop('Unnamed: 0',axis=1,inplace=True)
    df = df.iloc[5:]
    df.columns = ['Equipment','Parameter','Unit','SHIFT1','SHIFT2','SHIFT3']
    df['Equipment']=df.fillna(method='ffill')

    df = df.iloc[1:]
    df = df.reset_index(drop=True)
    df[['SHIFT1','SHIFT2','SHIFT3']] =  df[['SHIFT1','SHIFT2','SHIFT3']].fillna(0)

    df = df.replace(np.nan, '')
    df = df.replace(0, np.NaN)

    date = datetime_str
    tph = "Applications.App_70_TPH_"
    df['mean'] = df[['SHIFT1', 'SHIFT2','SHIFT3']].mean(axis=1)

    df = df.replace(np.NaN, 0)
    df["mean"]=df["mean"].round(2)

    list_of_dicts = []

    dictionary = dict(name=[],v=[],t=[])

    for i in range(len(df)):
        row = df.iloc[i]
        equipment, parameter, unit = row['Equipment'], row['Parameter'], row['Unit']
        mean = row['mean']
        
        if equipment != np.nan:
                equipment = str(equipment).split()
                equipment = '_'.join(equipment)
                dictionary['name'].append(tph+equipment+"_"+str(parameter)+"_"+str(unit)+"_mean_rpt")
                dictionary['v'].append(mean)
                dictionary['t'].append(date-19800)
     
    dictionary = pd.DataFrame(dictionary)
    dictionary['name'] = dictionary['name'].replace(['Applications.App_70_TPH_BOILER_STEAM_FLOW_(TPH)___mean_rpt'], 'Applications.App_70_TPH_BOILER_STEAM_FLOW_mean_rpt')

    finaldict=dictionary.to_dict('index')
    finaldict=dictionary.to_dict('records')
    print(finaldict)

    for i in finaldict:
        qr.postData(i['name'], [[i['t']*1000,i['v']]] ,{"tags":i['name']})
        


shahu60()
shahu70()
shahumean60()
shahumean70() 