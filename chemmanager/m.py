#########################################################
import paho.mqtt.client as paho
import pandas as pd
import os
import time
import requests
import json
import numpy as np
import app_config as cfg
config = cfg.getconfig()
# config = {'BROKER_ADDRESS': '10.211.19.37'}
# unitId = os.environ.get("UNIT_ID")
# if unitId==None:
#     print("no unit id passed")
#     exit()

def on_connect(client, userdata, flags, rc):
    print("Connected!")

def on_log(client, userdata, obj, buff):
    print("log:" + str(buff))

port = os.environ.get("Q_PORT")
if not port:
    port = 1883
else:
    port = int(port)
print ("Running port", port)

client = paho.Client()
client.on_log = on_log
client.on_connect = on_connect
# Used for Thermax
BROKER_ADDRESS = os.environ.get("BROKER_ADDRESS")
if not BROKER_ADDRESS:
	BROKER_ADDRESS = config["BROKER_ADDRESS"]
print(BROKER_ADDRESS)
client.username_pw_set(username="ES-MQTT", password="iota#re-mqtt39")
client.connect(BROKER_ADDRESS, port, 120)

dataTagIds = ["JKLC_01_PWR_003.DACA.PV", "JKLC_23_MW_001.DACA.PV_copy_filter_JKLC_22_MW_001.DACA.PV_filter_JKLC_21_MW_001.DACA.PV_filter_sum"]

def on_essage():
    for dataTagId in dataTagIds:
        topic_line = "onboarding/642bdae6066dab000812d141/chemicalManager"
        body = [{"dataTagId":dataTagId ,"start":"1679640911000", "end":"1679651711000"}]
        client.publish(topic_line, json.dumps(body))
on_essage()
#client.loop_forever()