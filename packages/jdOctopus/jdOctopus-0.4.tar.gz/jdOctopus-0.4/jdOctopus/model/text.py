from jdOctopus.tool import post

class text:

    def __init__(self, text):
        self.text = text

    def clickByOCR(self, uuids=""):
        post("/clickByOCR", {
            'uuids': uuids,
            'text': self.text
        })

    def clickByXml(self, uuids=""):
        post("/clickByXml", {
            'uuids': uuids,
            'text': self.text
        })

    def existByOCR(self, uuids=""):
        return post("/existTextByOCR", {
            'uuids': uuids,
            'text': self.text
        }, fname="exist")

    def existByXML(self, uuids=""):
        return post("/existTextByXML", {
            'uuids': uuids,
            'text': self.text
        }, fname="exist")

    def input(self, uuids=""):
        post("/inputText", {
            'uuids': uuids,
            'text': self.text
        })

    def getPointsByXML(self, uuids=""):
        return post("/getPointsByXML", {
            'uuids': uuids,
            'text': self.text
        })

    def getPointsByOCR(self, uuids=""):
        return post("/getPointsByOCR", {
            'uuids': uuids,
            'text': self.text
        })