import numpy as np
import pandas as pd
import datetime 
from dateutil import parser
import time
import timeseries as ts
qr = ts.timeseriesquery()

def meghmani_processplant_coolingtower():
    df= pd.read_excel("CWT REPORT - PROCESS.xlsx",sheet_name='Cooling Tower')
    df1=df.copy()
    df1=df1.tail(-5)
    df1=df1.reset_index(drop=True)
    df1 = df1.loc[:24]
    df1.columns = df1.iloc[0]
    df1 = df1.drop(0).reset_index(drop=True)
    df1 = df1.loc[:, :'CPVC']
    df1 = df1.drop(columns=['Sr No.', 'UOM','Make Up Water Analysis','ALL CT'])
    df1 = df1.replace('NIL', '')
    df1 = df1.replace('-', '')
    df1 = df1.replace('S/D', '')

    df1 = df1.drop(index=df1.index[:3]).reset_index(drop=True)
    df1 = df1.fillna('')
    df1["Parameter"] = df1["Parameter"].replace("Make Up", "Make Up Water")
    df1['CMS- PRO'][0]= df1['CMS-VAM'][0]
    df1 = df1.rename(columns={df1.columns[1]: "Make Up Water Actual Value"})



    Date = df.iloc[4, 0]
    date_str = Date[5:]
    format_str = '%d.%m.%Y'
    dt = datetime.datetime.strptime(date_str, format_str)
    # Set the time component to midnight in the IST timezone
    ist_tz = datetime.timedelta(hours=5, minutes=30)
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0) - ist_tz
    # Convert the datetime object to an epoch timestamp
    Time = int(time.mktime(dt.timetuple()))
    df1['Date'] = Time
    df1['Parameter'] = df1['Parameter'].str.strip() #To remove extra spaces
    #print(df1)
    #create a list of dictionaries
    data = []
    for col in df1.columns[1:11]:
        for i, value in enumerate(df1[col]):
            if value != '':
                name = col + '_' + df1.iloc[i, 0]
                data.append({'name': name, 'v': value, 't': df1.iloc[i, -1]})


    #print(data)
    for d in data:
        name = d['name']
        name = name.replace('&', '_').replace(' ', '_').replace('-_', '_').replace('-', '_')
        d['name'] = name

    dictionary = pd.DataFrame(data)
    #print(dictionary)
    finaldict=dictionary.to_dict('index')
    finaldict=dictionary.to_dict('records')
    print(finaldict)
    for i in finaldict:
        qr.postData(i['name'], [[i['t']*1000,i['v']]] ,{"tags":i['name']})
    print("Data posted successfully for meghmani process plant(Cooling-Tower)",date_str) 
    
def process_plant_Chiller_Process():
    df= pd.read_excel("CWT REPORT - PROCESS.xlsx",sheet_name='Chiller-Process')
    df1=df.copy()
    df1=df1.tail(-5)
    df1=df1.reset_index(drop=True)
    df1 = df1.loc[:9]
    df1.columns = df1.iloc[0]
    df1 = df1.drop(0).reset_index(drop=True)
    df1 = df1.loc[:, :'CMS Chiller']
    df1 = df1.drop(columns=['Sr No.', 'UOM','DESIGN LIMIT'])
    df1 = df1.replace('NIL', '')
    df1 = df1.replace('-', '')
    df1 = df1.replace('S/D', '')
    df1 = df1.drop(index=df1.index[:3]).reset_index(drop=True)
    df1 = df1.fillna('')



    Date = df.iloc[4, 0]
    date_str = Date[6:]
    format_str = '%d.%m.%Y'
    dt = datetime.datetime.strptime(date_str, format_str)
    # Set the time component to midnight in the IST timezone
    ist_tz = datetime.timedelta(hours=5, minutes=30)
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0) - ist_tz
    # Convert the datetime object to an epoch timestamp
    Time = int(time.mktime(dt.timetuple()))
    #print(Time)
    df1['Date'] = Time
    df1['Parameter'] = df1['Parameter'].str.strip() #To remove extra spaces

    #create a list of dictionaries
    data = []
    for col in df1.columns[1:4]:
        for i, value in enumerate(df1[col]):
            if value != '':
                name = col + '_' + df1.iloc[i, 0]
                data.append({'name': name, 'v': value, 't': df1.iloc[i, -1]})


    #print(data)
    for d in data:
        name = d['name']
        name = name.replace('&', '_').replace(' ', '_').replace('-_', '_').replace('-', '_')
        d['name'] = name

    dictionary = pd.DataFrame(data)
    finaldict=dictionary.to_dict('index')
    finaldict=dictionary.to_dict('records')
    print(finaldict)
    for i in finaldict:
        qr.postData(i['name'], [[i['t']*1000,i['v']]] ,{"tags":i['name']})
    print("Data posted successfully for meghmani process plant(Chiller-Process)",date_str)

meghmani_processplant_coolingtower()
process_plant_Chiller_Process()