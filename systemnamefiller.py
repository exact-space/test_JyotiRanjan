import requests
import json

# incident_url = 'https://pulse.thermaxglobal.com/exactapi/incidents?filter={"where": {"systemName": []}, "fields": ["criticalTags", "startTime", "id"], "order": "startTime DESC"}&access_token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhcnVuQGV4YWN0c3BhY2UuY28iLCJqdGkiOiJURU1QLTA3YzcwOTMxLWUzODEtNGIwYS1hMGQ1LWFjOGVjOGY1MmM4YSIsImF1ZCI6IlRoZXJtYXgiLCJpc3MiOiJUaGVybWF4IiwiaWF0IjoxNjYzMDU2OTc1LCJleHAiOjE2NjMwNjA1NzUsInJvbGUiOiJFREdFX0xJVkUiLCJ1aWQiOiJURU1QLTA3YzcwOTMxLWUzODEtNGIwYS1hMGQ1LWFjOGVjOGY1MmM4YSIsImFpZCI6IjAwMTdGMDAwMDA1eXZXMVFBSSJ9.6R2dbwRurAHMAZW5Fo6wuZGtSRornWKTk54Hq1gCneY'
incident_url = 'https://pulse.thermaxglobal.com/exactapi/incidents?filter={"where": { "open":true}}&access_token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhcnVuQGV4YWN0c3BhY2UuY28iLCJqdGkiOiJURU1QLTA3YzcwOTMxLWUzODEtNGIwYS1hMGQ1LWFjOGVjOGY1MmM4YSIsImF1ZCI6IlRoZXJtYXgiLCJpc3MiOiJUaGVybWF4IiwiaWF0IjoxNjYzMDU2OTc1LCJleHAiOjE2NjMwNjA1NzUsInJvbGUiOiJFREdFX0xJVkUiLCJ1aWQiOiJURU1QLTA3YzcwOTMxLWUzODEtNGIwYS1hMGQ1LWFjOGVjOGY1MmM4YSIsImFpZCI6IjAwMTdGMDAwMDA1eXZXMVFBSSJ9.6R2dbwRurAHMAZW5Fo6wuZGtSRornWKTk54Hq1gCneY'

#incident_url ='https://pulse.thermaxglobal.com/exactapi/incidents/634cd1c557d7e47b68302144?access_token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhcnVuQGV4YWN0c3BhY2UuY28iLCJqdGkiOiJURU1QLTA3YzcwOTMxLWUzODEtNGIwYS1hMGQ1LWFjOGVjOGY1MmM4YSIsImF1ZCI6IlRoZXJtYXgiLCJpc3MiOiJUaGVybWF4IiwiaWF0IjoxNjYzMDU2OTc1LCJleHAiOjE2NjMwNjA1NzUsInJvbGUiOiJFREdFX0xJVkUiLCJ1aWQiOiJURU1QLTA3YzcwOTMxLWUzODEtNGIwYS1hMGQ1LWFjOGVjOGY1MmM4YSIsImFpZCI6IjAwMTdGMDAwMDA1eXZXMVFBSSJ9.6R2dbwRurAHMAZW5Fo6wuZGtSRornWKTk54Hq1gCneY'

inc = requests.get(incident_url).json()
#inc = [inc]
print("incidents fetched")
for i in inc:
    print(i["id"])
    systemNames = []
    eqNames = []
    eqIds = []
    equipments = []
    tagsToFetch = []
    if i["criticalTags"]:
        for cT in i["criticalTags"]:
            print(cT["dataTagId"])
            tagsToFetch.append(cT["tagmetaId"])
            tagsToFetch = list(set(tagsToFetch))
        print('https://pulse.thermaxglobal.com/exactapi/tagmeta?filter={"where":{"id":{"inq":["'+'","'.join(tagsToFetch)+'"]}}}')
        tagList = requests.get('https://pulse.thermaxglobal.com/exactapi/tagmeta?filter={"where":{"id":{"inq":["'+'","'.join(tagsToFetch)+'"]}}}').json()
        for tagM in tagList:
            systemNames.append(tagM["systemName"])
            eqNames.append(tagM["equipmentName"])
            eqIds.append(tagM["equipmentId"])
        #equipments.append(tagM["equipment"])
        print(list(set(systemNames)))
        print(i["id"])
        response = requests.post('https://pulse.thermaxglobal.com/exactapi/incidents/update?where={"id":"'+i["id"]+'"}&access_token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhcnVuQGV4YWN0c3BhY2UuY28iLCJqdGkiOiJURU1QLTA3YzcwOTMxLWUzODEtNGIwYS1hMGQ1LWFjOGVjOGY1MmM4YSIsImF1ZCI6IlRoZXJtYXgiLCJpc3MiOiJUaGVybWF4IiwiaWF0IjoxNjYzMDU2OTc1LCJleHAiOjE2NjMwNjA1NzUsInJvbGUiOiJFREdFX0xJVkUiLCJ1aWQiOiJURU1QLTA3YzcwOTMxLWUzODEtNGIwYS1hMGQ1LWFjOGVjOGY1MmM4YSIsImFpZCI6IjAwMTdGMDAwMDA1eXZXMVFBSSJ9.6R2dbwRurAHMAZW5Fo6wuZGtSRornWKTk54Hq1gCneY', json={"systemName": list(set(systemNames)), "equipmentName": list(set(eqNames)), "equipmentIds": list(set(eqIds))})
        print(response)