import time
import random
import requests
import urllib3

urllib3.disable_warnings()


class Order(object):
    def __init__(self, params):
        self.params = params
        self.flight = params.get("flight")
        self.price = params.get("priceInfo").get("adtPrice")
        self.ua = "Mozilla/5.0 (Linux; Android 5.1.1; PRO 6 Plus Build/LMY48Z; wv) AppleWebKit" \
                  "/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36 MicroMessenger/" \
                  "7.0.13.1640(0x27000D34) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm32 WeChat/arm32"
        self.session = requests.session()
        self.msg = {}
        self.tcsessionid = TT.get("openId") + "-" + str(int(time.time() * 1000))

    def post_flightbffwx(self):
        url = "https://wx.17u.cn/flightbffwx/query/getflightlist"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "799",
            "tcsessionid": "o498X0TWrMMRUq4KlzRRSsOj3p5E-1586745982677",
            "charset": "utf-8",
            "tcversion": "1.0.0",
            "tctracerid": "12318534-c5da-40ce-8b82-32f6a4b33611",
            "tcplat": "852",
            "User-Agent": self.ua,
            "tcuserid":  TT.get("unionId"),
            "appversion": "3.8.0",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "tcsectoken": TT.get("sectoken"),
            "apmat": f'{TT.get("openId")}|{time.strftime("%Y%m%d%H%M", time.localtime(time.time()))}|{str(random.random())[-6:]}',
            "content-type": "application/json",
            "Referer": "https://servicewechat.com/wx336dcaf6a1ecf632/246/page-frame.html",
        }
        data = {"Departure": "SHA", "Arrival": "CKG", "GetType": "0", "IsBaby": 0, "flightno": "FM9421",
                "QueryType": "1", "DepartureName": "上海", "ArrivalName": "重庆", "DepartureDate": "2020-04-17 07:55",
                "ProductType": "1", "GoFlight": "", "GoFlyTime": "", "AirCode": "FM", "GoArrivalTime": "",
                "IsBook15": 1, "newCabinDeal": 2, "openId":  TT.get("unionId"),
                "session_key": "3D3D25F7ABFB0B52C72C7C54020445AA", "unionid":  TT.get("unionId"),
                "refid": "319527329", "plat": 852, "SessionId": "o498X0TWrMMRUq4KlzRRSsOj3p5E-1586745982677",
                "SecToken": TT.get("sectoken"),
                "xcxVersion": "2020.04.02", "linkTrackerId": "769e2675-c72a-f426-9471-02a14b84f331"}
        res = requests.post(url=url, headers=headers, json=data, verify=False).json()
        print(res)
        if res.get("resCode") == 0:
            if res.get("body").get("newCabinList"):
                return res.get("body")
            else:
                self.msg = {
                    "status": 3,
                    "msg": "未查询到对应航班"
                }
        else:
            self.msg = {
                "status": 3,
                "msg": "查询失败"
            }

    def get_GSGuid(self, res):
        economyList = res.get("newCabinList").get("economyList")
        for Price in economyList:
            if int(Price.get("clientTicketPrice")) == self.price:
                return Price.get("stag")
            continue
        businessList = res.get("newCabinList").get("businessList")
        for Price in businessList:
            if int(Price.get("clientTicketPrice")) == self.price:
                return Price.get("stag")
            continue
        return {
            "status": 3,
            "msg": "没有匹配到对应的价格"
        }

    # def post_buildtemporder(self, GSGuid):
    #     url = " https://wx.17u.cn/flightcreateorder/buildtemporder"
    #     headers = {
    #         "Host": "wx.17u.cn",
    #         "Connection": "keep-alive",
    #         "Content-Length": "818",
    #         "tcsessionid": TT.get("openId") + "-" + str(int(time.time() * 1000)),
    #         "tcuserid": TT.get("unionId"),
    #         "tcsectoken": TT.get("sectoken"),
    #         "apmat": f'{TT.get("openId")}|{time.strftime("%Y%m%d%H%M", time.localtime(time.time()))}|{str(random.random())[-6:]}',
    #         "tctracerid": "b284d97a-3339-4b05-97e1-7383830e5797",
    #         "content-type": "application/json",
    #         "User-Agent": self.ua,
    #         "Accept-Encoding": "gzip,compress,br,deflate",
    #         "tcplat": "852",
    #         "charset": "utf-8",
    #         "appversion": "3.7.9",
    #         "tcversion": "1.0.0",
    #         "Referer": "https://servicewechat.com/wx336dcaf6a1ecf632/245/page-frame.html",
    #     }
    #
    #     data = {"FlightDataBack": "", "FlightData": "", "DataKey": "", "BackDataKey": "", "IsBackOrder": False,
    #             "IsMultipleIns": True, "IsUnionOrder": False, "IsYouXuan": 0,
    #             "GSGuid": GSGuid,
    #             "InsType": 1, "InsurBind": 0, "FlightType": 1, "IsXuanGou": 0,
    #             "TcAllianceID": "477490115",
    #             "openId": TT.get("openId"),
    #             "session_key": "2B515A9F853063DF356DFEBFD8E134F1",
    #             "unionid": TT.get("unionId"),
    #             "refid": "319527329", "plat": 852,
    #             "SessionId": TT.get("openId") + "-" + str(int(time.time() * 1000)),
    #             "SecToken": TT.get("sectoken"),
    #             "xcxVersion": "2020.04.02", "linkTrackerId": "2882dc68-8ba9-4daa-bde2-902c70570c3b"
    #             }
    #     res = requests.post(url=url, headers=headers, json=data, verify=False).json()
    #     print(res)
    #     if res.get("resCode") == 100:
    #
    #         return res.get("Data").get("SerialId")
    #
    #     else:
    #         self.msg = {
    #             "status": 3,
    #             "msg": "查询失败"
    #         }

    def post_submitorder(self):
        url = "https://wx.17u.cn/flightcreateorder/submitorder"

    def do_order(self):
        res = self.post_flightbffwx()
        print(res)
        if self.msg:
            return self.msg
        res = self.get_GSGuid(res=res)
        print(res)
        # if isinstance(res, dict):
        #     return res
        # ress = self.post_buildtemporder(res)
        # print(ress)

    #         F1XK9LV0XP0UJ0H1TJH9


if __name__ == "__main__":
    data = {
        "vcode": "",
        "extra": "",
        "adultNum": 1,
        "childNum": 0,
        "priceInfo": {
            "proType": "",
            "extra": "",
            "cabin": "M",
            "adtPrice": 360,
            "adtTax": 50,
            "chdPrice": 600,
            "chdTax": 0,
            "infPrice": 600,
            "infTax": 0
        },
        "flight": {
            "tripType": 1,
            "departure": "SHA",
            "arrival": "CKG",
            "depTime": "2020-04-17 07:55",
            "flightNos": [
                "MF9421"
            ]
        },
        "passengers": [
            {
                "name": "",
                "firstName": "",
                "lastName": "",
                "ageType": "",
                "birthday": "",
                "gender": "",
                "cardType": "",
                "cardNum": "",
                "mobile": ""
            }
        ],
        "contact": {
            "name": "",
            "firstName": "",
            "lastName": "",
            "mobile": "",
            "email": ""
        },
        "loginInfo": {
            "loginType": "",
            "loginUser": "user",
            "loginPwd": "pwd"
        }
    }

    d = Order(params=data)
    d.do_order()
