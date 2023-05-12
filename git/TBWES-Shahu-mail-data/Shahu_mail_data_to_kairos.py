import sys
import email as em
import base64
from openpyxl import Workbook
from openpyxl import load_workbook
import boto3
import botocore
#import xlsm_parse as xlsm
import pickle
from time import gmtime, strftime
import subprocess
import os
import base64
import re
# os.chdir('/tmp/jyoti2/')
import numpy as np
import pandas as pd
import datetime
from dateutil import parser
import time
import timeseries as ts
qr = ts.timeseriesquery()

try: os.chdir('./excel_files/')
except:
        os.mkdir('excel_files')
        os.chdir('./excel_files')

try:os.mkdir('reports')
except:pass


def persist_pickle_file(file_list):
	with open('files_parsed.pkl', 'wb') as f:
		pickle.dump(file_list, f, pickle.HIGHEST_PROTOCOL)

def shahu60():
    df = pd.read_excel('Shahu parsing report.xlsx',sheet_name='Aux Power sheet 60')

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
    print ("")
    print ("shahu60() executed successfully")
    print ("")

def shahu70():

    df = pd.read_excel('Shahu parsing report.xlsx',sheet_name='Aux Power sheet 70')

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
    print ("")
    print ("shahu70() executed successfully")
    print ("")


def shahumean60():
    df = pd.read_excel('Shahu parsing report.xlsx',sheet_name='Aux Power sheet 60')
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
    print ("")
    print ("shahumean60() executed successfully")
    print ("")


def shahumean70():

    df = pd.read_excel('Shahu parsing report.xlsx',sheet_name='Aux Power sheet 70')
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
    print ("")
    print ("Shahumean70() executed successfully")
    print ("")



AWSAccessKeyId =	"AKIATRPA35R6XGJGNVME"
AWSSecretKey =	"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"
Bucket_Name = "exactmailreceiver"

def main_func(): 
	session = boto3.Session(aws_access_key_id=AWSAccessKeyId, aws_secret_access_key=AWSSecretKey)

	client = session.client('s3')

	s3 = session.resource('s3')

	# def fromToPrefixMap(msg_from):
	# 	if msg_from == "":
	# 		return ""

	try:
		with open('files_parsed.pkl', 'rb') as f:
			file_list = pickle.load(f)			
	except IOError as e:
		file_list = []
		with open('files_parsed.pkl', 'wb') as f:
			pickle.dump([], f, pickle.HIGHEST_PROTOCOL)





	email_counter=1

	prclist =0
	for bucket in s3.buckets.all():
		#print bucket
		if(bucket.name == Bucket_Name):
			for key in bucket.objects.all():
				try:
					# print(key)
					# print(client.get_object(Bucket=Bucket_Name, Key=key.key)["LastModified"])
					# print(client.get_object(Bucket=Bucket_Name, Key=key.key)["Metadata"])
				
					if(key.key in file_list):
						# print "Already processed file: " + key.key
						continue
					else:
						s3.Bucket(Bucket_Name).download_file(key.key, 'local_email_copy.txt')
						prclist = prclist + 1
						msg = em.message_from_file(open('local_email_copy.txt'))
						print ("")
						print(msg['Subject'])
						print(msg['From'])
						msg_From = re.findall("[a-zA-Z0-9._]*@[a-zA-Z0-9._]*", msg['From'])
		                        	j=0
						if "Shahu parsing report" in msg['Subject']:
							print("Downloaded!")
							attachment = msg.get_payload()[1]
							msg['Subject'] = msg['Subject'].replace("Fwd: ","")
							file = open(msg['Subject'].split('_')[0].rstrip()+".xlsx","w")
							print(msg['Subject'])
							print(msg_From)

							print(key.key)
							file.write(attachment.get_payload(decode=True)) 
							file.close()
							# these are just for viewing purpose (above)
							# file = open(key.key.replace("reports/",""),"w")
						 
							file = open(key.key,"w") 
							file.write(attachment.get_payload(decode=True)) 
							file.close()
						
							# Popen (subject, key.key)
							# removeing prefixes in Parser.py 
							# same things to do for historic parser (select via email address)
							#if msg_From == "infocom.hirakud@adityabirla.com":
                    			        	subprocess.Popen('../Parsers.py', env=dict(os.environ,  **{"subject":msg['Subject'], "filename": key.key, "fileData": base64.b64encode(attachment.get_payload(decode=True))}),shell=True)

						
							try:shahu60()
							except Exception as e:
								exception_type, exception_object, exception_traceback = sys.exc_info()
								filename = exception_traceback.tb_frame.f_code.co_filename
								line_number = exception_traceback.tb_lineno
								print (str(exception_type) + '||||' + str(filename) + '||||' + str(line_number))
								print ('')
							try: shahu70()
							except Exception as e:
                                                        	exception_type, exception_object, exception_traceback = sys.exc_info()
                                                        	filename = exception_traceback.tb_frame.f_code.co_filename
                                                        	line_number = exception_traceback.tb_lineno
                                                        	print (str(exception_type) + '||||' + str(filename) + '||||' + str(line_number))
                                                        	print ('')
							try: shahumean60()
							except Exception as e:
                                                        	exception_type, exception_object, exception_traceback = sys.exc_info()
                                                        	filename = exception_traceback.tb_frame.f_code.co_filename
                                                        	line_number = exception_traceback.tb_lineno
                                                        	print (str(exception_type) + '||||' + str(filename) + '||||' + str(line_number))
                                                        	print ('')
							try:shahumean70()
							except Exception as e:
                                                        	exception_type, exception_object, exception_traceback = sys.exc_info()
                                                        	filename = exception_traceback.tb_frame.f_code.co_filename
                                                        	line_number = exception_traceback.tb_lineno
                                                        	print (str(exception_type) + '||||' + str(filename) + '||||' + str(line_number))
                                                        	print ('')

                       			        	j=1
						
						file_list.append(key.key)
						persist_pickle_file(file_list)
						if j==1: print email_counter," Success processing new email: " + key.key
                   		        	else: print email_counter," Appended to skip list: " + key.key
						email_counter+=1
					
				except botocore.exceptions.ClientError as e:
					if e.response['Error']['Code'] == "404":
						print("The object does not exist.")
						continue
					else:
						raise
						continue

	print "################"					
	print "Processed "	+ str(prclist) + " mails"				
	print strftime("%Y-%m-%d %H:%M:%S", gmtime())

while True:
	try: main_func()
	except Exception as e: print (str(e))

