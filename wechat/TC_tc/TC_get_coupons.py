import time
import requests
import urllib3
urllib3.disable_warnings()


class Conpons(object):
    def __init__(self):
        pass

    def getWinnerCodeList(self):
        url = "https://wx.17u.cn/flightactivities/nodeapi/lotteryCodeGroup/getWinnerCodeList"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "104",
            "Origin": "https://wx.17u.cn",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; MI 9 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 MMWEBID/9224 MicroMessenger/7.0.13.1640(0x27000D34) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm32 WeChat/arm32 miniProgram",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Referer": "https://wx.17u.cn/flightactivities/newAuth/lotteryCodeGroup/index?refid=0",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "X-Requested-With": "com.tencent.mm",
        }
        data = {"token": "WUD5B9C5DCFD054F59B8587FEA34E68684", "sharerToken": "",
                "unionId": "ohmdTtzyKbyp9mq54bCSfGTuiPDk"}
        res = requests.post(url=url, headers=headers, json=data, verify=False).json()
        print(res.get("success"))
        return res

    def doGetWinnerCode(self):
        url = "https://wx.17u.cn/flightactivities/nodeapi/lotteryCodeGroup/getWinnerCode"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "104",
            "Origin": "https://wx.17u.cn",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; MI 9 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 MMWEBID/9224 MicroMessenger/7.0.13.1640(0x27000D34) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm32 WeChat/arm32 miniProgram",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Referer": "https://wx.17u.cn/flightactivities/newAuth/lotteryCodeGroup/index?refid=0",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "X-Requested-With": "com.tencent.mm",
        }
        data = {"actCode": "b7dc3dcc7af211ea89445d646ea506b8", "token": "WUD5B9C5DCFD054F59B8587FEA34E68684",
                "unionId": "ohmdTtzyKbyp9mq54bCSfGTuiPDk", "sharerToken": ""}
        res = requests.post(url=url, headers=headers, json=data, verify=False)
        print(res.text)

    def do_conpons(self):
        start = time.time()
        while True:
            res = self.getWinnerCodeList()
            if res.get("success") == False:
                end = time.time()
                a = end - start
                print(a)
                break
            time.sleep(300)
# 2701.524220228195

if __name__ == "__main__":
    tc = Conpons()
    # tc.do_conpons()
    # tc.doGetWinnerCode()
