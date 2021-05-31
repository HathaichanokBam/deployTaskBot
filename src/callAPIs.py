import requests
import json
from requests.exceptions import HTTPError
from datetime import datetime


def getToken(url):
    jsonData = {
        "username": "aae01",
        "password": "aae01P@ssw0rd"
    }
    try:
        res = requests.post(url + 'v1/authentication', data=json.dumps(jsonData))
        res.raise_for_status()
        res_dict = json.loads(res.text)
        token = res_dict["token"]
        return token
    except HTTPError as err:
        print(err)


def listPublicTasks(url, token):
    jsonData = {
        "filter": {
            "operator": "eq",
            "field": "botStatus",
            "value": "PUBLIC"
        }
    }

    try:
        headers = {"X-Authorization": token}
        res = requests.post(url + 'v2/repository/workspaces/public/files/list', data=json.dumps(jsonData), headers=headers)
        res.raise_for_status()
    except HTTPError as err:
        status_code = err.response.status_code
        if status_code == 401:
            token = getToken(url)
            headers = {"X-Authorization": token}
            res = requests.post(url + 'v2/repository/workspaces/public/files/list', data=json.dumps(jsonData), headers=headers)
    publicTasks = []
    res_dict = json.loads(res.text)
    for i in res_dict["list"]:
        publicTasks.append({"id": i['id'], "taskname": i['name']})
    return publicTasks


def getRequestIDforExport(url, token, id, taskname):     # export func
    now = datetime.now()
    date, time = str(now).split(" ")
    date = date.replace("-", "")
    time = time.replace(":", "")
    jsonData = {
        "name": "Export." + taskname + '.' + date + '_' + time[0:6],
        "fileIds": [
            id
        ],
        "includePackages": "true"
    }

    try:
        headers = {"X-Authorization": token}
        res = requests.post(url + 'v2/blm/export', data=json.dumps(jsonData), headers=headers)
        res.raise_for_status()
    except HTTPError as err:
        status_code = err.response.status_code
        if status_code == 401:
            token = getToken(url)
            headers = {"X-Authorization": token}
            res = requests.post(url + 'v2/blm/export', data=json.dumps(jsonData), headers=headers)
    res_dict = json.loads(res.text)
    return res_dict


def getStatus(url, token, requestID):

    try:
        headers = {"X-Authorization": token}
        res = requests.get(url + 'v2/blm/status/' + requestID, headers=headers)
        res.raise_for_status()
    except HTTPError as err:
        status_code = err.response.status_code
        if status_code == 401:
            token = getToken(url)
            headers = {"X-Authorization": token}
            res = requests.get(url + 'v2/blm/status/' + requestID, headers=headers)
    res_dict = json.loads(res.text)
    return res_dict


def downloadFile(url, token, downloadID):
    try:
        headers = {"X-Authorization": token}
        res = requests.get(url + 'v2/blm/download/' + downloadID, headers=headers)
        res.raise_for_status()
    except HTTPError as err:
        status_code = err.response.status_code
        if status_code == 401:
            token = getToken(url)
            headers = {"X-Authorization": token}
            res = requests.get(url + 'v2/blm/download/' + downloadID, headers=headers)
    # res_dict = json.loads(res.text)
    print(res.text)


def getRequestIDforImport(url, token, filepath):    # import func

    filezip = open(filepath, 'rb')
    files = {
        "upload": ("testttttt.zip", filezip),
        "actionIfExisting": "OVERWRITE",
        "publicWorkspace": "true"
    }
    headers = {"X-Authorization": token}

    try:
        res = requests.post(url + 'v2/blm/import', files=files, headers=headers)
        res.raise_for_status()
    except HTTPError as err:
        status_code = err.response.status_code
        if status_code == 401:
            token = getToken(url)
            res = requests.post(url + 'v2/blm/import', files=files, headers=headers)
    res_dict = json.loads(res.text)
    return res_dict
