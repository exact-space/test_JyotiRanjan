import pandas as pd
import requests
import json
import logging
import paho.mqtt.client as paho
import os





def get_config(unitId):
    url = "http://10.211.19.36:3000/exactapi/units/"+unitId+"/configs"
    res = requests.get(url)
    config = json.loads(res.content)
    if len(config)>0 and res.status_code==200:
        BROKER_ADDRESS = config[0]["BROKER_ADDRESS"]
        BROKER_USERNAME = config[0]['BROKER_USERNAME']
        BROKER_PASSWORD = config[0]['BROKER_PASSWORD']

        cfg = config[0]["api"]["meta"]
        return cfg, BROKER_ADDRESS, BROKER_USERNAME, BROKER_PASSWORD
    else:
        print res

#cfg,BROKER_ADDRESS, BROKER_USERNAME, BROKER_PASSWORD = get_config("61bb218e5b5042014bb996c7")


import app_config as cfg
config = cfg.getconfig()
cfg = config["api"]["meta"]
# print config
try:
    BROKER_ADDRESS = config["BROKER_ADDRESS"]
    BROKER_USERNAME = config['BROKER_USERNAME']
    BROKER_PASSWORD = config['BROKER_PASSWORD']
except:
    BROKER_ADDRESS = config["BROKER_ADDRESS"]
    BROKER_USERNAME = "ES-MQTT"
    BROKER_PASSWORD = "iota#re-mqtt39"



def sendLogs(msg,unitId,msg2=''):
    logStatus = [{"log":msg,"alert":msg2}] ## alert : "success" / "warning" / "danger"
    client.publish("onboarding/"+unitId+"/logsStatus", json.dumps(logStatus))
    print ("*******************     published on /logsStatus    **************************")

def chemManager(unitsId):
    
    url = 'https://pulse.thermaxglobal.com/exactapi/equipment?filter={"where":{"unitsId":"'+unitsId+'"},"fields":["system","systemInstance","systemName"]}'
    #print(url)
    res= requests.get(url)
    res = json.loads(res.content)
    #print(res)
    
    sys=[]
    for i in res:
        #print(i["system"])
        if "Ro" in i["system"] or "Uf" in i["system"]:
            sys.append(i)
            
    sys = list({(d['system'], d['systemInstance']): d for d in sys}.values())
    #print("sys",sys)
    y={"chemicalManager":[],"unitsId":unitsId}
    for i in sys:
#         if " " in i["systemName"]:
#             continue
        if "Ro" in i["system"]:
            ro = {"HCL":"Kg", "SMBS":"Kg", "Antiscalant8115":"Litre", "Mincare":"Litre", "Maxtreat9202":"Litre", "Maxtreat9206":"Litre", "EDTA":"Kg", "SLS":"Kg", "Citric Acid":"Kg"}
            i["params"] = []
            for name, unit in ro.items():
                i["params"].append({"name":name, "unit":unit, "flowPerDay":100, "projectedConsumption":9, "ppmDose":90, "costPerKg":10, "cost":90, "costPerM3":0.9})
            y["chemicalManager"].append(i)
            
            permeate = {"Hypo":"Kg", "Caustic":"Kg"}
            j={"system":"Ers_Ro_Permeate", "systemInstance":i["systemInstance"], "systemName":"Ers_Ro_Permeate"+str(i["systemName"][-1]), "params":[]}
            
            for name, unit in permeate.items():
                j["params"].append({"name":name, "unit":unit, "flowPerDay":100, "projectedConsumption":9, "ppmDose":90, "costPerKg":10, "cost":90, "costPerM3":0.9})
            
            y["chemicalManager"].append(j)
        
        if "Uf" in i["system"]:
            uf = {"HCL":"Kg", "Caustic":"Kg", "Hypo":"Kg"}
            i["params"] = []
            for name, unit in uf.items():
                i["params"].append({"name":name, "unit":unit, "flowPerDay":100, "projectedConsumption":9, "ppmDose":90, "costPerKg":10, "cost":90, "costPerM3":0.9})
            y["chemicalManager"].append(i)
    print("body",y)
    if y["chemicalManager"]==[]:
        sendLogs("Chemical Manager can't be created(meta not found)",unitsId,msg2='warning')
        client.publish("onboarding/"+unitsId+"/chemicalManagerdone", json.dumps([{}]),2,False)
        

    url = config["api"]["meta"]+"/units/"+unitsId+'/heatrates?filter={"fields":["chemicalManager"]}'
    print("url",url)
    heatrates = requests.get(url).json()
    heatrate = [heat for heat in heatrates if heat!= {} and "chemicalManager" in heat]
    
    print("heatrate = ",heatrate)
    if len(heatrate)==0:
    # if "chemicalManager" not in heatrates:
    
        url = config["api"]["meta"]+"/units/"+unitsId+"/heatrates"
        res = requests.post(url,json=y)
        if res.status_code == 200:
            client.publish("onboarding/"+unitsId+"/chemicalManagerdone", json.dumps([y]),2,False)
            sendLogs("Chemical Manager created successfully",unitsId,msg2='success')
            print("published")
        else:
            print("status code",res.status_code)
    else:
        print("ChemicalManager already found")
        client.publish("onboarding/"+unitsId+"/chemicalManagerdone", json.dumps(heatrate),2,False)
        sendLogs("Chemical Manager already created",unitsId,msg2='success')
      
    

    



def on_message(client, userdata, msg):
    if msg.topic.endswith("/chemicalManager"):
        print("recieved")
        unitId = msg.topic.split("/")[1]
        chemManager(unitId)
        
        
            
    if msg.topic.endswith("/chemicalManagerMetaData"):
        
        unitId = msg.topic.split("/")[1]
        
        
            
            
        
        
    
def on_log(client, userdata, obj, buff):
    print("log: " + str(buff))   
    
def on_connect(client, obj, flags, rc):
    print("connect: " + str(rc))
    # #print(k)
    topic_line = "onboarding/+/chemicalManager"
    client.subscribe(topic_line)
    topic_line = "onboarding/+/chemicalManagerMetaData"
    client.subscribe(topic_line)
client = paho.Client()


#run on Q_PORT
port = os.environ.get("Q_PORT")
if not port:
    port = 1883
else:
    port = int(port)

print "Running port", port

#run on_connect and on_message functioins
# client.username_pw_set(username="ES-MQTT", password="iota#re-mqtt39")
client.username_pw_set(username=BROKER_USERNAME, password=BROKER_PASSWORD)
client.on_log = on_log
client.on_connect = on_connect
client.on_message = on_message
# client.connect("0.0.0.0", port, 180)
client.connect(BROKER_ADDRESS, port, 180)
# def keepalive():
#     global client
#     topic_line = "u/"+unitId+"/"
#     service_name = os.environ.get("SERVICE_NAME") or "metaValidation"
#     client.publish(topic_line+"keepalive", json.dumps({"t": int(time.time()//60*60), "sv": service_name}))

# scheduler = BackgroundScheduler()
# scheduler.add_job(func=keepalive, trigger="interval", seconds=60)
# scheduler.start()


client.loop_forever(retry_first_connection=True)
