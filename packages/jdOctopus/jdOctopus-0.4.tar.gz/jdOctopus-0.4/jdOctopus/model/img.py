from jdOctopus.index import newOctopus
from jdOctopus.tool import postFile
from requests_toolbelt import MultipartEncoder

class img:

    def __init__(self, imgPath):
        octopus = newOctopus()
        self.addr = octopus.addr
        self.devices = octopus.devices
        self.headers = octopus.headers
        self.imgPath = imgPath

    def click(self, uuids=""):
        if uuids == "":
            uuids = self.devices
        data = MultipartEncoder(fields={'uuids': str(uuids).replace("'", '"'), 'imgPath': self.imgPath,
                                     'img': ("weixin.png", open(self.imgPath, 'rb'))})
        header = {
            'Content-Type': data.content_type, 'Uuid': self.headers["Uuid"]
        }
        postFile("/clickByImage",data,header)

    def exists(self, uuids=""):
        if uuids == "":
            uuids = self.devices
        data = MultipartEncoder(fields={'uuids': str(uuids).replace("'", '"'), 'imgPath': self.imgPath,
                                     'img': ("weixin.png", open(self.imgPath, 'rb'))})
        header = {
            'Content-Type': data.content_type, 'Uuid': self.headers["Uuid"]
        }
        return postFile("/existImage",data,header,"exist")

    def save(self, savePath, uuids=""):
        if uuids == "":
            uuids = self.devices
        data = MultipartEncoder(fields={'uuids': str(uuids).replace("'", '"'), 'imgPath': self.imgPath, 'savepath': savePath,
                                     'img': ("weixin.png", open(self.imgPath, 'rb'))})
        header = {
            'Content-Type': data.content_type, 'Uuid': self.headers["Uuid"]
        }
        postFile("/addImg", data, header)

    def getPointsByImage(self, uuids=""):
        if uuids == "":
            uuids = self.devices
        data = MultipartEncoder(fields={'uuids': str(uuids).replace("'", '"'), 'imgPath': self.imgPath,
                                     'img': ("weixin.png", open(self.imgPath, 'rb'))})
        header = {
            'Content-Type': data.content_type, 'Uuid': self.headers["Uuid"]
        }
        return postFile("/getPointsByImage", data, header)