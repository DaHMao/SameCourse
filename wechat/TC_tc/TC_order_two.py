import time
import random
import requests
import urllib3
from Token.token_ import token_17338347182 as TT
import uuid

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
        self.tctracerid = uuid.uuid1()

    def post_flightbffwx(self):
        url = "https://wx.17u.cn/flightbffwx/query/getflightlist"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "799",
            "tcsessionid": self.tcsessionid,
            "charset": "utf-8",
            "tcversion": "1.0.0",
            "tctracerid": "769e2675-c72a-f426-9471-02a14b84f331",
            "tcplat": "852",
            "User-Agent": self.ua,
            "tcuserid": TT.get("unionId"),
            "appversion": "3.8.0",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "tcsectoken": TT.get("sectoken"),
            "apmat": f'{TT.get("openId")}|{time.strftime("%Y%m%d%H%M", time.localtime(time.time()))}|{str(random.random())[-6:]}',
            "content-type": "application/json",
            "Referer": "https://servicewechat.com/wx336dcaf6a1ecf632/246/page-frame.html",
        }
        data = {"Departure": self.flight.get("departure"), "Arrival": self.flight.get("arrival"),
                "GetType": "0", "IsBaby": 0, "flightno": self.flight.get("flightNos")[0],
                "QueryType": "1", "DepartureName": "上海", "ArrivalName": "重庆",
                "DepartureDate": self.flight.get("depTime"),
                "ProductType": "1", "GoFlight": "", "GoFlyTime": "", "AirCode": self.flight.get("flightNos")[0][:2],
                "GoArrivalTime": "",
                "IsBook15": 1, "newCabinDeal": 2, "openId": TT.get("unionId"),
                "session_key": "3D3D25F7ABFB0B52C72C7C54020445AA", "unionid": TT.get("unionId"),
                "refid": "319527329", "plat": 852, "SessionId": self.tcsessionid,
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

    def post_buildtemporder(self, GSGuid):
        url = " https://wx.17u.cn/flightcreateorder/buildtemporder"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "818",
            "tcsessionid": self.tcsessionid,
            "tcuserid": TT.get("unionId"),
            "tcsectoken": TT.get("sectoken"),
            "apmat": f'{TT.get("openId")}|{time.strftime("%Y%m%d%H%M", time.localtime(time.time()))}|{str(random.random())[-6:]}',
            "tctracerid": "769e2675-c72a-f426-9471-02a14b84f331",
            "content-type": "application/json",
            "User-Agent": self.ua,
            "Accept-Encoding": "gzip,compress,br,deflate",
            "tcplat": "852",
            "charset": "utf-8",
            "appversion": "3.7.9",
            "tcversion": "1.0.0",
            "Referer": "https://servicewechat.com/wx336dcaf6a1ecf632/245/page-frame.html",
        }

        data = {"FlightDataBack": "", "FlightData": "", "DataKey": "", "BackDataKey": "", "IsBackOrder": False,
                "IsMultipleIns": True, "IsUnionOrder": False, "IsYouXuan": 0,
                "GSGuid": GSGuid,
                "InsType": 1, "InsurBind": 0, "FlightType": 1, "IsXuanGou": 0,
                "TcAllianceID": "477490115",
                "openId": TT.get("openId"),
                "session_key": "3D3D25F7ABFB0B52C72C7C54020445AA",
                "unionid": TT.get("unionId"),
                "refid": "319527329", "plat": 852,
                "SessionId": self.tcsessionid,
                "SecToken": TT.get("sectoken"),
                "xcxVersion": "2020.04.02", "linkTrackerId": "769e2675-c72a-f426-9471-02a14b84f331"
                }
        res = requests.post(url=url, headers=headers, json=data, verify=False).json()
        print(res)
        if res.get("resCode") == 100:

            return res.get("Data").get("SerialId")

        else:
            self.msg = {
                "status": 3,
                "msg": "查询失败"
            }

    def add_passengers(self):
        """
        添加乘客信息
        :return:
        """
        url = "https://wx.17u.cn/flightedward/passengers/dishonest/eruptpayquery"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "127",
            "charset": "utf-8",
            "User-Agent": self.ua,
            "apmat": f'{TT.get("openId")}|{time.strftime("%Y%m%d%H%M", time.localtime(time.time()))}|{str(random.random())[-6:]}',
            "content-type": "application/json",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "Referer": "https://servicewechat.com/wx336dcaf6a1ecf632/246/page-frame.html",
        }
        data = {"commonRequestDTOS": [
            {"certNo": "512201193803141329", "name": "梁昌德", "certType": "NI", "birthDate": "1938-03-14"}],
            "count": "1"}
        res = requests.post(url=url, headers=headers, json=data, verify=False).json()

    def add_promotion(self):
        """
        查看有沒有可用的优惠券
        :return:
        """
        url = "https://wx.17u.cn/flightedward/whosyourdaddy/promotion/query"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "731",
            "charset": "utf-8",
            "User-Agent": self.ua,
            "apmat": f'{TT.get("openId")}|{time.strftime("%Y%m%d%H%M", time.localtime(time.time()))}|{str(random.random())[-6:]}',
            "content-type": "application/json",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "Referer": "https://servicewechat.com/wx336dcaf6a1ecf632/246/page-frame.html",
        }
        data = {"channel": 852, "source": 1,
                "unionId": TT.get("unionId"),
                "openId": TT.get("openId"),
                "strMemberId": TT.get("memberId"),
                "traceId": "769e2675-c72a-f426-9471-02a14b84f331",
                "tools": ["mz"],
                "timespan": 1586768877344,
                "ext": {},
                "flight": {"id": "1111", "carrier": ["FM"], "operateCarrier": ["FM"],
                           "departureCityCode": "SHA",
                           "arriveCityCode": "CKG",
                           "departureDate": "202004170755",
                           "arriveDate": "202004171050",
                           "airlineType": 1,
                           "products": [
                               {"id": "0000", "tags": ["00000"], "cabinClass": [1],
                                "fare": 430,
                                "ext": {"recommendTag": "gn_allowance_pack$10", "taGoods": ""},
                                "reimbursement": "0",
                                "flightNo": ["FM9421"]}],
                           "orderAmount": 510},
                "passengers": [{"type": 0, "name": "梁昌德", "certType": "身份证", "certNo": "512201193803141329", "sex": 2}]}

    def post_submitorder(self):
        url = "https://wx.17u.cn/flightcreateorder/submitorder"
        data = {
            "OrderSerialId": "F1569LV0CPPD60U9TJH9",
            "isNewInsuranceType": 1,
            "LinkMobile": "17338347182",
            "Plist": ["1;梁昌德;身份证/512201193803141329/1938-03-14/0/1406589694832803842;"],
            "IsNeedSend": "0","submitCheckRepeat": 0, "IsRegTcMember": True, "IsCheckCertNo": 1,
            "EnsurePassageInfoStr": "{\"isEnsure\":0,\"EnsurePassage\":[]}",
            "UCType": "", "IsChangePrice": 0, "totalPassengerDiscountPrice": 0, "ErrorType": 1, "OrderTypeAirline": 1,
            "gwPassengerLimitSwitch": False, "flightTicketVoucher": True, "NoMileAge": 0, "reimbursementType": 0,
            "marks": [], "packOrderUnionNo": "", "BackOrderSerialId": None, "LinkMan": "梁昌德", "LinkCertNo": "",
            "ClientToken": "{\"MailABKey\":0,\"HasMailCheck\":1,\"BookingType\":0,\"cabinsProductType\":0,\"cabinTypeName\":\"打包立减\"}",
            "UseRedPacket": ["FGTGIQ5MEEM4O0QL0H53003814"], "unifiedMileages": [],
            "GiftCodes": [
                {"type": 0, "code": "66e353cd130c11e990b4d56d0ad0bee5", "price": 0,
                "promotionSign": "E336EE2253BC9ECFB2CF5FD2EFED7B89"}],
            "commonProductList": [], "isNewConsumer": 0,
            "openId": "o498X0TWrMMRUq4KlzRRSsOj3p5E",
            "session_key": "3D3D25F7ABFB0B52C72C7C54020445AA",
            "unionid": "ohmdTtzyKbyp9mq54bCSfGTuiPDk",
            "refid": "319527329", "plat": 852,
            "SessionId": "o498X0TWrMMRUq4KlzRRSsOj3p5E-1586771886688",
            "SecToken": "ZfOeS2YX9IStsHx-3-C4u20wwMekhHQkT2Wp-2Y3eCnGMNuykQ9q6a6FFnZRGEuxsPBu6w7o7FbdR8ooeUUHCNKh9q13Z1nys2M8NRj-MyrAD4-9TEFHZhRwldnGyjaPxyLOsRIgSJ952GtJIj3xL6HcRBgZVzOd72Iyd4RyW2xR_J6LiIoUZrLNTftid9GF4641",
            "xcxVersion": "2020.04.02",
            "linkTrackerId": "c0d6a0c7-8223-01f0-8430-f72362ae9f2d"}

    def do_order(self):
        res = self.post_flightbffwx()
        print(res)
        if self.msg:
            return self.msg
        res = self.get_GSGuid(res=res)
        print(res)
        if isinstance(res, dict):
            return res
        ress = self.post_buildtemporder(res)
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
            "adtPrice": 430,
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
            "depTime": "2020-04-22 07:55",
            "flightNos": [
                "FM9421"
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
