import pandas as pd
import requests
import json
import logging
import paho.mqtt.client as paho
import os





def get_config(unitId):
    url = "http://10.211.19.36:3000/exactapi/units/"+unitsId+"/configs"
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
def getEquipmentId(unitsId,equipment,systemName):
    urlQuery = 'https://pulse.thermaxglobal.com/exactapi/units/'+unitsId+'/equipment?filter={"where":{"name":"'+equipment+'","systemName":"'+systemName+'"},"limit":1,"fields":["id"]}'
    response= requests.get(urlQuery)
    print("url",urlQuery)
    print("response",response)
    if(response.status_code==200):
        equipmentMeta = json.loads(response.content)
        # print(equipmentId)
        if equipmentMeta==[]:
            return equipmentMeta
        else:
            return equipmentMeta[0]
    else:
        print(response.status_code)
        print(response.content)
        
def get_unitIds(unitsId):
    unitIds = []
    query = {"id":unitsId}
    urlQuery = 'https://pulse.thermaxglobal.com/exactapi/units/?filter={"where":' + json.dumps(query) + '}'
    #urlQuery = config['api']['meta']+'/units/?filter={"where":' + json.dumps(query) + '}'
    response = requests.get(urlQuery)
    if(response.status_code==200):
        unitMeta = json.loads(response.content)
    return unitMeta
    
def getmetadata(unitsId,dataTagId):
    #print(dataTagId)
    urlQuery = 'https://pulse.thermaxglobal.com/exactapi/units/'+unitsId+'/tagmeta?filter={"where":{"dataTagId":"'+dataTagId+'"},"fields":["dataTagId"]}'
    response= requests.get(urlQuery)
    print("urlQuery",urlQuery)
    if(response.status_code==200):
        
        tagmeta = json.loads(response.content)
        # print(equipmentId)
        if tagmeta==[]:
            return tagmeta
        else:
            return tagmeta[0]
    else:
        print(response.status_code)
        print(response.content)
        
        
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
    sys = [item for item in sys if 'Permeate' not in item['system']]
    global uniqueSys
    uniqueSys = []
    #print("sys",sys)
    body={"chemicalManager":[],"unitsId":unitsId}
    for i in sys:
        uniqueSys.append(i.copy())
        
        if "Ro" in i["system"]:
            ro = {"HCL":"Kg", "SMBS":"Kg", "Antiscalant8115":"Litre", "Mincare":"Litre", "Maxtreat9202":"Litre", "Maxtreat9206":"Litre", "EDTA":"Kg", "SLS":"Kg", "Citric Acid":"Kg"}
            i["params"] = []
            for name, unit in ro.items():
                i["params"].append({"name":name, "unit":unit, "flowPerDay":100, "projectedConsumption":9, "ppmDose":90, "costPerKg":10, "cost":90, "costPerM3":0.9})
            body["chemicalManager"].append(i)
            
            permeate = {"Hypo":"Kg", "Caustic":"Kg"}
            j={"system":"Ers_Ro_Permeate", "systemInstance":i["systemInstance"], "systemName":"Ers_Ro_Permeate"+str(i["systemName"][-1]), "params":[]}
            
            for name, unit in permeate.items():
                j["params"].append({"name":name, "unit":unit, "flowPerDay":100, "projectedConsumption":9, "ppmDose":90, "costPerKg":10, "cost":90, "costPerM3":0.9})
            
            body["chemicalManager"].append(j)
        
        if "Uf" in i["system"]:
            uf = {"HCL":"Kg", "Caustic":"Kg", "Hypo":"Kg"}
            i["params"] = []
            for name, unit in uf.items():
                i["params"].append({"name":name, "unit":unit, "flowPerDay":100, "projectedConsumption":9, "ppmDose":90, "costPerKg":10, "cost":90, "costPerM3":0.9})
            body["chemicalManager"].append(i)
    print("body",body)
    print("unique_system =",uniqueSys)
    if body["chemicalManager"]==[]:
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
        res = requests.post(url,json=body)
        if res.status_code == 200:
            client.publish("onboarding/"+unitsId+"/chemicalManagerdone", json.dumps([body]),2,False)
            sendLogs("Chemical Manager created successfully",unitsId,msg2='success')
            print("published")
        else:
            print("status code",res.status_code)
    else:
        print("ChemicalManager already found")
        client.publish("onboarding/"+unitsId+"/chemicalManagerdone", json.dumps(heatrate),2,False)
        sendLogs("Chemical Manager already created",unitsId,msg2='success')
        
def forms_meta(unitsId):
    url='https://pulse.thermaxglobal.com/exactapi/ingestconfigs?filter={"where":{"unitsId":"'+unitsId+'"},"fields":["TAG_PREFIX"]}'
    response = requests.get(url).json()
    tag_prefix = response[0].get('TAG_PREFIX')
    
    
    
    heatrate_url = 'https://pulse.thermaxglobal.com/exactapi/heatrates?filter={"where":{"unitsId":"'+unitsId+'"},"fields":["chemicalManager"]}'
    response = requests.get(heatrate_url)
    if response.status_code==200:
        totaldata = json.loads(response.content)
        print("totaldata",totaldata)
    data = {k: v for d in totaldata for k, v in d.items()} 
    
    dataTagId=[]
    display=[]
    for i in data["chemicalManager"]:
        
        for j in i['params']:
            dataTagId.append(tag_prefix+i["system"]+"_"+str(i["systemInstance"])+"_"+j["name"]+"_received")
            display.append(i["system"]+"_"+str(i["systemInstance"])+" "+j["name"]+" received")
           
    
            
            
    for i in range(len(dataTagId)):
        dataTagId[i] = dataTagId[i].replace(" ", "_").replace("__", "_")
                
        
    chemical_names = [param['name'] for system in data['chemicalManager'] for param in system['params']]
    chemical_unit = [param['unit'] for system in data['chemicalManager'] for param in system['params']]
    chemical_systemName = [system_name['systemName'] for system_name in data['chemicalManager']]

    Chemical_Manager = {
        "fields": [],
        "name": "chemical Manager",
        "unitsId": unitsId
    }

    for i in range(len(chemical_names)):
        field = {
            "name": chemical_names[i],
            "dataTagId":dataTagId[i],
            "range": [1,10000],
            "units": chemical_unit[i],
            "type": "number",
            "display":display[i]
            }
        Chemical_Manager["fields"].append(field)
        
    num_dicts_to_add = len(Chemical_Manager["fields"])
    for i in range(num_dicts_to_add):
        new_dict = Chemical_Manager["fields"][i].copy()
        new_dict['dataTagId'] = new_dict['dataTagId'].replace('received', 'consumed')
        new_dict['display'] = new_dict['display'].replace('received', 'consumed')
        Chemical_Manager["fields"].append(new_dict)
    Chemical_Manager["fields"] = sorted(Chemical_Manager["fields"], key=lambda k: k['dataTagId'])
    #print(sorted_list)
    print(Chemical_Manager)
    url = config["api"]["meta"]+"/units/"+unitsId+'/forms?filter={"where":{"name":"chemical Manager"},"fields":["id"]}}'
    res = request.get(url)
    #res = json.loads(res.content)
    if res.status_code==200:
            
        url = config["api"]["meta"]+"/units/"+unitsId+"/forms"
        res = requests.post(url,json=Chemical_Manager)
        if res.status_code == 200:
            #client.publish("onboarding/"+unitsId+"/chemicalManagerdone", json.dumps([Chemical_Manager]),2,False)
            sendLogs("Chemical Manager form created successfully",unitsId,msg2='success')
            print("published")
        else:
            print("status code",res.status_code)
    else:
        idx = res[0]["id"]
        url = config["api"]["meta"]+"/forms/update/"+idx
        res = requests.post(url,json=Chemical_Manager)
        if res.status_code == 200:
            #client.publish("onboarding/"+unitsId+"/chemicalManagerdone", json.dumps([y]),2,False)
            sendLogs("Chemical Manager form updated successfully",unitsId,msg2='success')
            print("published")
        else:
            print("status code",res.status_code)
        
        
    measureType = []
    measureUnit = []
    description = [] #display
    dataTagId=[]#tagId
    system=[]
    systemName = []
    systemInstance = []
    for i in Chemical_Manager["fields"]:
        dataTagId.append(i["dataTagId"])
        measureProperty.append(i["name"])
        measureType.append(i["dataTagId"].split("_")[-1])
        description.append(i["display"])
        measureUnit.append(i["units"])
        result = re.search(r'^[^_]+_(.+?)_\d', i["dataTagId"]).group(1)
        system.append(result)
        result2 = re.search(r'^[^_]+_(.+?\d)', i["dataTagId"]).group(1)
        systemName.append(result2)
        result3 = re.search(r'(?<=_)\d+', i["dataTagId"]).group(0)
        systemInstance.append(result3)


    data = { "measureProperty":measureProperty,"measureType":measureType,"measureUnit":measureUnit,"description":description,"dataTagId":dataTagId,"system":system,"systemName":systemName,"systemInstance":systemInstance}
    df = pd.DataFrame(data)
    df['equipmentName'] = "Performance Kpi"
    df['equipmentInstance'] = "-"
    df['component'] = "-"
    df['componentName'] = "-"
    df['componentInstance'] = "-"
    df['subcomponent'] = "-"
    df['subcomponentInstance'] = "-"
    df['measureInstance'] = "-"
    df['tagType'] = "manual"
    df['group'] = "-"
    df['badDirection'] = "-"
    df['limRangeHi'] = "-"
    df['limHiHi'] = "-"
    df['limHi'] = "-"
    df['limRangeLo'] = "-"
    df['limLoLo'] = "-"
    df['limLo'] = "-"
    df['measureLocationInstance'] = "-"
    df['measureLocation'] = "-"
    df['measureLocationName'] = "-"
    df['subcomponentName'] = "-"
    df['equipment'] = "-"
    df['equipmentType'] = "-"
    df['unitsId'] = unitsId
    tagmeta=df.to_dict("records")
    for entry in tagmeta:
        
    #print(entry,"\n\n")
        system_instance = entry['systemInstance']
        system = entry['system']
        for item in uniqyeSys:
            if item['systemInstance'] == int(system_instance) and item['system'] == system:
                entry['systemName'] = item['systemName']
    pp(tagmeta)            
            



        
    #creation of equipment
    for item in tagmeta:
        
        eqId = getEquipmentId(unitsId,"Performance Kpi",item["systemName"])
        #print("rrrrr",eqId)
        if not eqId:
            print("equipment not found")
            details = {
                "system": item["system"],
                "systemName": item["systemName"],
                "systemInstance": item["systemInstance"],
                "name": item["equipmentName"],
                "equipment": item["equipmentName"],
                "equipmentInstance": 1,
                "conditionalTag": item["dataTagId"],
                "condition": "gt",
                "value": 1,
                "descriptionCondTag": item["description"],
                "equipmentLoad": {
                    "loadTagLimit": 0,
                    "loadTag": item["dataTagId"],
                    "descriptionLoadTag": item["description"],
                    "loadBucketSize": 2
                },
                "unitsId": unitsId,
                "kpiGroup": item["equipmentName"]
            }

            print(details)#post this to equipment endpoint
            res = requests.post('https://pulse.thermaxglobal.com/exactapi/equipment', json=details)
            print(res.status_code)
            posteqp = json.loads(res.content)
            unitMeta = get_unitIds(unitsId)
            item["equipmentId"] = posteqp['id']
            item["customerId"] = unitMeta[0]['customerId']
            item["siteId"] = unitMeta[0]['siteId']
        else:
            #print("eqid",eqId[0]['id'])
            item["equipmentId"] = eqId['id']
    #         print(item["equipmentId"])
            item["customerId"] = unitMeta[0]['customerId']
            item["siteId"] = unitMeta[0]['siteId']
        metadata=getmetadata(unitsId,item["dataTagId"])
        print("metadata",metadata)
        if not metadata:
            print("metadata not found")
            res = requests.post('https://pulse.thermaxglobal.com/exactapi/tagmeta', json=item)
            print(res.status_code)
            if res.status_code == 200:
                print("posted successfully")
                print(res.content)
        
    

            
    
            
        
#def add_entry(unitsId,body):
    #url = config["api"]["meta"]+"/units/"+unitsId+'/heatrates?filter={"fields":["chemicalManager"]}'
    # print("url",url)
    #heatrates = requests.get(url).json()
    # print("heatrates=",heatrates)
    # manger_list = heatrates[0]["chemicalManager"]
    #manger_list = next(item['chemicalManager'] for item in heatrates if 'chemicalManager' in item)
    # print(manger_list)
    # print(i)
    #for i in body[0]["chemicalManager"]:
        #print("body",body)
        # for item in heatrates:
            # if "chemicalManager" in item:
                
                # if i not in manger_list:
                    # print("hhhhh",item["chemicalManager"])
                    # manger_list.append(i)
                    #item["chemicalManager"].append(i)
                    #print("item",item)
                    # url = config["api"]["meta"]+"/units/"+unitsId+'/heatrates/update'
                    # res = requests.post(url,json=heatrates)
                    # sendLogs("Some Chemical Manager entry added",unitsId,msg2='success')
                # else:
                    # print("same entry exists")
                    # sendLogs("same entry exists",unitsId,msg2='success')    
        






        # res = requests.post('https://pulse.thermaxglobal.com/exactapi/equipment', json=equip)
        # print(res.status_code)
        # eqId = getEquipmentId(unitsId,"Performance Kpi",i["systemInstance"])
        # if res.status_code == 200:
            # client.publish("onboarding/"+unitsId+"/chemicalmanagerFormdone", json.dumps(Chemical_Manager),2,False)
            # client.publish("onboarding/"+unitsId+"/chemicalmanagerFormdone", json.dumps(Chemical_Manager),2,False)
            # sendLogs("Chemical_Manager forms done ",unitsId,msg2='success')
    # else:
        # print("Chemical_Manager forms already found")
        # client.publish("onboarding/"+unitsId+"/chemicalmanagerFormdone", json.dumps(Chemical_Manager),2,False)
        # sendLogs("Chemical_Manager forms already created",unitsId,msg2='success')
        
       

    

    



def on_message(client, userdata, msg):
    if msg.topic.endswith("/chemicalManager"):
        print("recieved")
        unitId = msg.topic.split("/")[1]
        chemManager(unitId)
        
        
    if msg.topic.endswith("/chemicalManagerForms"):
        print("recieved")
        unitId = msg.topic.split("/")[1]

        
    if msg.topic.endswith("/chemicalManagerMetaData"):
        
        unitId = msg.topic.split("/")[1]
        
    if msg.topic.endswith("/addEntry"):
        body=json.loads(msg.payload)
        unitId = msg.topic.split("/")[1]
        #add_entry(unitId,body)
        forms_meta(unitId)
        
    if msg.topic.endswith("/deleteEntry"):
        unitId = msg.topic.split("/")[1]
        forms_meta(unitId) 
        
    
def on_log(client, userdata, obj, buff):
    print("log: " + str(buff))   
    
def on_connect(client, obj, flags, rc):
    print("connect: " + str(rc))
    # #print(k)
    topic_line = "onboarding/+/chemicalManager"
    client.subscribe(topic_line)
    topic_line = "onboarding/+/chemicalManagerMetaData"
    client.subscribe(topic_line)
    topic_line = "onboarding/+/addEntry"
    client.subscribe(topic_line)
    topic_line = "onboarding/+/deleteEntry"
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
