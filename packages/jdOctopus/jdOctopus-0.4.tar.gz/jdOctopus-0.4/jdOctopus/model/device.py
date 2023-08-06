import json
import requests
from jdOctopus.tool import get,interceptor,post,postFile
from jdOctopus.index import newOctopus
from requests_toolbelt import MultipartEncoder

class device:

    @staticmethod
    def getOnline():
        return get("/getDevices")

    @staticmethod
    def getBindInfo():
        return get("/bindDevicesInfo")

    @staticmethod
    def bindDevices(uuids):
        post("/bindDevices",{
            'uuids': uuids
        })
        octopus = newOctopus()
        for each in uuids:
            octopus.devices.append(each)

    @staticmethod
    def unBindDevices(uuids):
        post("/unBindDevices",{
            'uuids': uuids
        })
        octopus = newOctopus()
        for each in uuids:
            octopus.devices.remove(each)

    @staticmethod
    def screenCapture(imgPath="./", zoom=4, uuids=""):
        octopus = newOctopus()
        if uuids == "":
            uuids = octopus.devices
        for each in uuids:
            url = octopus.addr + "/screenCapture"
            data = {
                'uuids': [each],
                'zoom': zoom
            }
            res = requests.post(url=url, data=json.dumps(data), headers=octopus.headers)
            sub_str = imgPath[-4:]
            ip = imgPath
            if sub_str!='.png' and sub_str!='.jpg':
                filename = ''
                resheader = str(res.headers['content-disposition'])
                indirect = resheader[resheader.rfind('=')+1:]
                if indirect and len(indirect)>0:
                    filename = indirect + '.png'
                ip += filename

            if res.headers["content-type"] == "application/octet-stream":
                with open(ip, 'wb') as f:
                    f.write(res.content)
                    f.close()
            else:
                text = json.loads(res.text)
                interceptor(text)

    @staticmethod
    def addFile(filePath, savePath, uuids=""):
        data = MultipartEncoder(fields={'uuids': str(uuids).replace("'", '"'),  'savepath': savePath,
                                     'file': ("weixin.png", open(filePath, 'rb'))})
        header = {
            'Content-Type': data.content_type, 'Uuid': octopus.headers["Uuid"]
        }
        postFile("/addFile",data,header)

    @staticmethod
    def runKeyCode(code, uuids=""):
        post("/runKeyCode",{
            'uuids': uuids,
            'text': str(code)
        })

    @staticmethod
    def startApp(packageName, uuids=""):
        post("/startApp",{
            'uuids': uuids,
            'text': packageName
        })