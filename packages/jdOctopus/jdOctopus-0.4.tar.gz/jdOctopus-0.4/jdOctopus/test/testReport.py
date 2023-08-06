import unittest   #单元测试模块
from BeautifulReport import BeautifulReport as bf  #导入BeautifulReport模块，这个模块也是生成报告的模块，但是比HTMLTestRunner模板好看
from jdOctopus.index import newOctopus
from jdOctopus.model import *
from time import sleep


err = ""
def slideDown(x):
    point.clickByPixel(540,450)
    sleep(2)
    for i in range(x):
        point.clickByPixel(540,1902)
        sleep(1)
    point.clickByPixel(950,1350)
    sleep(3)

def qiehuan(x,y,shangquan,city):
    for j in range(len(shangquan)):
        if j >12 :
            y = 2164
            for i in range(j-12):
                swipe.verticalRoll(0.0625)
                sleep(2)

        point.clickByPixel(x,y)
        sleep(3)
        if not text("扫码开玩").existByOCR():
            global err
            err += "\n" + city + "--" + shangquan[j] + "  是银行"

        sleep(2)
        point.clickByPixel(50,270)
        sleep(2)
        y+=124

newOctopus("10.222.50.39:8080")
uuid = ["ca829b6"]

class TestCalc(unittest.TestCase):
    def setUp(self):  #每个用例运行之前运行的
        print('setup是啥时候运行的')

    def tearDown(self): #每个用例运行之后运行的
        print('teardown是啥时候运行的')

    @classmethod
    def setUpClass(cls):  #在所有用例执行之前运行的
        print('我是setUpclass，我位于所有用例的开始')


    @classmethod
    def tearDownClass(cls): #在所有用例都执行完之后运行的
        print('我是tearDownClass，我位于多有用例运行的结束')


    def test1(self):    #函数名要以test开头，否则不会被执行
        '''获取控制设备'''       #用例描述，在函数下，用三个单引号里面写用例描述
        device.bindDevices(uuid)
        sleep(1)
        self.assertEqual(1,1)
        print('第一个用例')

    def test2(self):
        '''进入趣玩街'''
        img("./img/趣玩街.png").click()
        sleep(4)
        img("./img/允许.png").click()
        sleep(2)
        self.assertEqual(1,1)
        print('第二个用例')

    def test3(self):
        '''执行切换商城'''
        point.clickByPixel(50, 270)
        sleep(2)
        cityList = ["上海", "东莞", "中山", "乐山", "佛山", "兰州", "凉山", "北京"]
        for i in range(len(cityList)):
            x = 200
            y = 676
            if i == 0:
                list = ["保利国际影城上海曹路宝龙店", "世博源广场", "百联中环购物广场", "静安大悦城"]
                slideDown(i)
                qiehuan(x, y, list, cityList[i])
            if i == 1:
                list = ["九珑璧支行", "季华支行"]
                slideDown(i)
                qiehuan(x, y, list, cityList[i])
            if i == 2:
                list = ["京东6号楼四层C1区09", "京东商超移动点位5区"]
                slideDown(i)
                qiehuan(x, y, list, cityList[i])

            if i == 3:
                list = ["厦门国际会议展览中心"]
                slideDown(i)
                qiehuan(x, y, list, cityList[i])

            if i == 4:
                list = ["中国银行广州合景支行"]
                slideDown(i)
                qiehuan(x, y, list, cityList[i])

            if i == 5:
                list = ["西安曲江大悦城"]
                slideDown(i)
                qiehuan(x, y, list, cityList[i])

            if i == 6:
                list = ["郑州农商银行老鸦陈支部"]
                slideDown(i)
                qiehuan(x, y, list, cityList[i])

            if i == 7:
                list = ["京东电器超级体验店"]
                slideDown(i)
                qiehuan(x, y, list, cityList[i])
        print(err)
        self.assertEqual(err,"") # 也会输出一遍err
        print('第三个用例')

    def test4(self):
        '''退出'''
        device.runKeyCode(4)
        sleep(2)
        device.runKeyCode(3)
        sleep(2)

        print('第四个用例')

suite = unittest.TestSuite()  #定义一个测试集合
suite.addTest(unittest.makeSuite(TestCalc))  #把写的用例加进来（将TestCalc类）加进来
run = bf(suite) #实例化BeautifulReport模块
run.report(filename='test',description='网点实例')