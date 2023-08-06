from jdOctopus.tool import post

class info:

    @staticmethod
    def getOCR(uuids=""):
        return post("/getOCRInfo",{
            'uuids': uuids
        })

    @staticmethod
    def getXML(uuids=""):
        return post("/getHierarchy",{
            'uuids': uuids
        })