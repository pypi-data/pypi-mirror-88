from jdOctopus.index import newOctopus
from jdOctopus.model import *

newOctopus("10.222.50.39:8080").ping()

# print(device.getOnline())
device.bindDevices(["6HJ4C19C12030463"])
print(device.getBindInfo())
# print(info.getOCR())
# device.screenCapture()
# device.runKeyCode(3)
# point.clickByPixel(200,200)