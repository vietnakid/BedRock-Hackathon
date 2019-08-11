import requests
import json
import time

def upload_file(filepath):
    url = "https://api.accusoft.com/PCCIS/V1/WorkFile"
    files = open(filepath, 'rb')
    headers = {
        "acs-api-key": "j37Hdf_z8n_ooFvOVauafaojyiWe97p0-gVg8ocl7-wQBhLbqtboBmOxUXKFyqF4"
    }
    r = requests.post(url, headers=headers, data=files)
    # print r.json()
    return r.json()

def form_extract(fileId, affinity_token):
    url = "https://api.accusoft.com/v2/formExtractors"
    headers = {
        "Content-Type": "application/json",
        "acs-api-key": "j37Hdf_z8n_ooFvOVauafaojyiWe97p0-gVg8ocl7-wQBhLbqtboBmOxUXKFyqF4",
        "Accusoft-Affinity-Token": affinity_token
    }
    data = {
        "input": {
            "fileId": fileId,
            "formType": "acroform"
        }
    }
    r = requests.post(url, headers=headers, json=data)
    # print r.json()
    return r.json()

def get_form(processId, affinity_token):
    url = "https://api.accusoft.com/v2/formExtractors/" + processId
    headers = {
        "acs-api-key": "j37Hdf_z8n_ooFvOVauafaojyiWe97p0-gVg8ocl7-wQBhLbqtboBmOxUXKFyqF4",
        "Accusoft-Affinity-Token": affinity_token
    }
    r = requests.get(url, headers=headers)
    # print r.json()
    return r.json()

def normalize_data(raw_data):
    pages = raw_data['output']['acroform']['pages']
    result = list()
    for page in pages:
        fields = page['fields']
        for field in fields:
            list_field = dict()
            fieldType = field['fieldType']
            name = field['name']
            boundingBox = normalize_bounding(field['boundingBox'])
            list_field['position'] = boundingBox
            list_field['text'] = name
            list_field['fieldType'] = fieldType
            result.append(list_field)
    return result  

def normalize_bounding(bounding):
    x = bounding['lowerLeftX']
    y = bounding['lowerLeftY']
    width = bounding['upperRightX'] - x
    height = bounding['upperRightY'] - y
    result = dict()
    result['x'] = x
    result['y'] = y
    result['width'] = width
    result['height'] = height
    return result

a = upload_file('/Users/trananhduc/Desktop/BedRock/Hackathon 1.0 inputs/Washington and Lee university.pdf')
affinity_token = a['affinityToken']
fileId = a['fileId']

resp = form_extract(fileId, affinity_token)
# print resp
processId = resp['processId']

final_resp = get_form(processId, affinity_token)
while final_resp['percentComplete'] != 100:
    time.sleep(3)
    final_resp = get_form(processId, affinity_token)

print json.dumps(normalize_data(final_resp))