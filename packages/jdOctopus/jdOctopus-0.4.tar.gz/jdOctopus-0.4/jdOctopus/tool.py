import json
import requests

from jdOctopus.index import newOctopus

def get(api):
    octopus = newOctopus()
    url = octopus.addr + api
    text = json.loads(requests.get(url=url, headers=octopus.headers).text)
    interceptor(text)
    return text["data"]

def post(api,data,header="",fname =""):
    octopus = newOctopus()
    if header=="":
        header = octopus.headers
    url = octopus.addr + api
    if isinstance(data,(dict)) and data['uuids'] == "":
        data['uuids'] = octopus.devices
    text = json.loads(requests.post(url=url, data=json.dumps(data), headers=header).text)
    if fname == "exist":
        return exist(text)
    else:
        interceptor(text)
        return text["data"]

def postFile(api,data,header="",fname =""):
    octopus = newOctopus()

    if header=="":
        header = octopus.headers
    url = octopus.addr + api

    text = json.loads(requests.post(url=url, headers=header, data=data, timeout=5).text)

    if fname == "exist":
        return exist(text)
    else:
        interceptor(text)
        return text["data"]

def interceptor(text):
    if text["success"]:
        pass
    else:
        raise Exception(text["msg"])

def exist(text):
    if text["success"]:
        return True
    else:
        return False
