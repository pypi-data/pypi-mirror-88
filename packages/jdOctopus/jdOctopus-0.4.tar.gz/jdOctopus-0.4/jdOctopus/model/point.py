from jdOctopus.tool import post

class point:

    @staticmethod
    def clickLong(x, y, time, uuids=""):
        post("/clickLong", {
            'uuids': uuids,
            'x': x,
            'y': y,
            'time': time
        })

    @staticmethod
    def clickByPixel(x, y, uuids=""):
        post("/clickByPixel", {
            'uuids': uuids,
            'x': x,
            'y': y
        })

    @staticmethod
    def clickByPercentage(x, y, uuids=""):
        post("/clickByPercentage", {
            'uuids': uuids,
            'x': x,
            'y': y
        })