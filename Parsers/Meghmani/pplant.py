import numpy as np
import pandas as pd
import datetime 
from dateutil import parser
import time
import timeseries as ts
qr = ts.timeseriesquery()


df= pd.read_excel("CWT REPORT - POWER .xlsx")
df1=df.copy()
df1=df1.tail(-5)
df1=df1.reset_index(drop=True)
df1 = df1.loc[:26]
df1.columns = df1.iloc[0]
df1 = df1.drop(0).reset_index(drop=True)
df1 = df1.iloc[:, :9]
df1.columns = ['Sr No.', 'Parameter', 'UOM','Make-Up Water','Actual\nValue','Design \nLimit','CT-1&CT-2','CT-3','CT-4']
df1=df1.tail(-3)
df1 = df1.drop(columns=['Sr No.', 'UOM','Make-Up Water','Design \nLimit'])
df1.columns = ['Parameter', 'CT_ACTUAL_VALUE', 'CT-1&CT-2','CT-3','CT-4']
df1 = df1.reset_index(drop=True)
df1 = df1.replace(['NIL', '-'], '').fillna('')


#print(df1)


#Get the date string
Date = df.iloc[4, 0]
date_str = Date[5:]
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
for col in df1.columns[1:5]:
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
print("CWT report Data Uploaded Successfully for Meghmani ",date_str)