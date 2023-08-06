from jdOctopus.tool import post

class swipe:

    @staticmethod
    def swipe(points, uuids=""):
        post("/swipe",{
            'uuids': uuids,
            'points': points
        })

    @staticmethod
    def smoothSwipe(points, uuids=""):
        post("/smoothSwipe",{
            'uuids': uuids,
            'points': points
        })

    @staticmethod
    def verticalRoll(extent, uuids=""):
        post("/verticalRoll",{
            'uuids': uuids,
            'extent': extent
        })