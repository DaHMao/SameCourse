import requests
import urllib3
from wechat.setting import *

urllib3.disable_warnings()

TT_token = {"openId": "o498X0TWrMMRUq4KlzRRSsOj3p5E",
            "unionId": "ohmdTtzyKbyp9mq54bCSfGTuiPDk",
            "encryOpenId": "da5e4cb2081789185d1a4837c55e4341",
            "aesOpenId": "3KhyoQ7e5Eo7Xnv6cV1Kpq7NPj5uZZcHiYXFYxLJICU=",
            "aesUnionId": "9WeMug36YGlr68SB7+CJ34+Rh9GpR768xlOe3zipDTE=",
            "memberId": "VhuLJOHlIDG070G4GavUGg==",
            "sectoken": "ZfOeS2YX9IStsHx-3-C4u0XkqtefXfGaXzNLlvdSqqyQtni3ANq129k4FdtkMmeOsPBu6w7o7FbdR8ooeUUHCNKh9q13Z1nys2M8NRj-MyrAD4-9TEFHZhRwldnGyjaPxyLOsRIgSJ952GtJIj3xLw4Kp0vhX3_D0YEQyA_mnd2v9e9KqQPo76EL0Bj7WrUG4641",
            "expts": 1588302522}


class Order(object):
    def __init__(self, params):
        self.params = params
        self.flight = params.get("flight")
        self.departure = self.flight.get("departure")
        self.departure_name = ""
        self.arrival = self.flight.get("arrival")
        self.arrival_name = ""
        self.price = params.get("priceInfo").get("adtPrice")
        self.ua = "Mozilla/5.0 (Linux; Android 5.1.1; PRO 6 Plus Build/LMY48Z; wv) AppleWebKit" \
                  "/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36 MicroMessenger/" \
                  "7.0.13.1640(0x27000D34) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm32 WeChat/arm32"
        self.session = requests.session()
        self.msg = {}
        self.tcsectoken = TT_token.get("sectoken")
        self.openId = TT_token.get("openId")
        self.tcsessionid = self.openId + "-" + str(int(time.time() * 1000))
        self.tcuserid = TT_token.get("unionId")
        self.high_price = float(params.get("priceInfo").get("highPrice")) - 50
        self.low_price = float(params.get("priceInfo").get("lowPrice")) - 50
        self.cabin = params.get("priceInfo").get("cabin")
        self.stag = ""
        self.cabinTypeName = ""
        self.NoMileAge = 0
        self.SerialId = ""

    def do_compare_price(self, price):
        """
        判断价格是否在所给的价格区间
        :return:
        """
        return self.low_price <= int(price) <= self.high_price

    @staticmethod
    def get_city_code_to_name(code):
        """
        获取城市名称
        :param code:
        :return:
        """
        try:
            return city_name[code]
        except KeyError:
            return {
                "status": 3,
                "msg": "根据三字码匹配对应的城市名称失败,传入的三字码：" + code
            }

    def do_get_city_name(self):
        res_departure = self.get_city_code_to_name(self.departure)
        if isinstance(res_departure, dict):
            return res_departure
        res_arrival = self.get_city_code_to_name(self.arrival)
        if isinstance(res_arrival, dict):
            return res_arrival
        self.departure_name = res_departure
        self.arrival_name = res_arrival

    def post_flight_list(self):
        """
        获取对应航班信息
        :return:
        """
        l_price = []
        apmat = f'{self.openId}|{time.strftime("%Y%m%d%H%M", time.localtime(time.time()))}|{str(random.random())[-6:]}'
        url = "https://wx.17u.cn/flightbffwx/query/getflightlist"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "799",
            "tcsessionid": self.tcsessionid,
            "charset": "utf-8",
            "tcversion": "1.0.0",
            # "tctracerid": self.tctracerid,
            "tcplat": "852",
            "User-Agent": self.ua,
            "tcuserid": self.tcuserid,
            "appversion": "3.8.0",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "tcsectoken": self.tcsectoken,
            "apmat": apmat,
            "content-type": "application/json",
            "Referer": "https://servicewechat.com/wx336dcaf6a1ecf632/246/page-frame.html",
        }
        data = {"Departure": self.flight.get("departure"), "Arrival": self.flight.get("arrival"),
                "GetType": "0", "IsBaby": 0, "flightno": self.flight.get("flightNo"),
                "QueryType": "1", "DepartureName": "上海", "ArrivalName": "重庆",
                "DepartureDate": self.flight.get("depTime"),
                "ProductType": "1", "GoFlight": "", "GoFlyTime": "", "AirCode": self.flight.get("flightNo")[:2],
                "GoArrivalTime": "",
                "IsBook15": 1, "newCabinDeal": 2, "openId": self.openId,
                "unionid": self.tcuserid,
                "refid": "319527329", "plat": 852, "SessionId": self.tcsessionid,
                "SecToken": self.openId,
                "xcxVersion": "2020.05.03"}
        res = self.session.post(url=url, headers=headers, json=data, verify=False).json()
        # print(res)
        if res.get("resCode") == 0 and res.get("body").get("ErrorCode") == 0:
            economy_list = res.get("body").get("newCabinList").get("economyList")
            if economy_list:
                for economy in economy_list:
                    client_ticket_price = economy.get("clientTicketPrice")
                    if self.cabin == economy.get("realRoomCode"):
                        if self.do_compare_price(client_ticket_price):
                            l_price.append(economy)
                if l_price:
                    return l_price
            business_list = res.get("body").get("newCabinList").get("businessList")
            if business_list:
                for business in business_list:
                    client_ticket_price = business.get("clientTicketPrice")
                    if self.do_compare_price(client_ticket_price):
                        l_price.append(business)
                if l_price:
                    return l_price
            else:
                return {
                    "status": 3,
                    "msg": "传入的舱等有误，未匹配的到对应的舱等的信息"
                }
        else:
            return {
                "status": 3,
                "msg": f"根据航班获取价格信息失败,请求：{res.get('resDesc')},原因：{res.get('body').get('ErrorMessage')}"
            }

    @staticmethod
    def do_binding_price(price_l):
        """
        排除绑定活动或者其他税的票价
        :param price_l:
        :return:
        """
        l1_price = []
        for price in price_l:
            if price.get("pcks") or price.get("freeRefundChange") or price.get("isBindInus") == 1:
                # price.get("oct")
                # 是否叠加里程"drm": "1"，是否含有官网税 oct，是否含有免费退改险
                continue
            else:
                l1_price.append(price)
        if l1_price:
            return l1_price
        else:
            return {
                "status": 3,
                "msg": "该价格区间内，没有符合筛选条件的票价"
            }

    def get_lowest_price(self, price_ll):
        """
        取符合条件的最低价格

        "ProductIndexes": 2, 同程特惠,精选特价
        "ProductIndexes": 1, 官方授权
        "ProductIndexes": 3, 品质出行
        "ProductIndexes": 4, 公务舱
        :param price_ll: 符合条件的价格列表
        :return:
        """

        l_one = [(int(price.get("clientTicketPrice")), price.get("stag"), price.get("brc"), price.get("ProductIndexes"),
                  price.get("drm")) for price in price_ll]
        l_two = sorted(l_one, key=lambda x: x[0])
        self.price = l_two[0][0]
        self.stag = l_two[0][1]
        self.cabin = l_two[0][2]
        self.cabinTypeName = CabinTypeName[l_two[0][3]]
        if l_two[0][4]:
            self.NoMileAge = 1  # 是否累加同程里程 1 表示不累加
        else:
            self.NoMileAge = 0
        print(self.cabinTypeName)

    def get_fit_lower_price(self):
        """
        获取符合要求的最低价的机票价格
        :return:
        """
        res = self.post_flight_list()
        if isinstance(res, dict):
            res["index_one"] = "post_get_flight_list_one"
            return res
        res = self.do_binding_price(price_l=res)
        print(res)
        if isinstance(res, dict):
            res["index_one"] = "do_binding_price"
            return res
        self.get_lowest_price(price_ll=res)

    def post_build_order(self):
        """
        生成假单
        :return:
        """
        apmat = f'{self.openId}|{time.strftime("%Y%m%d%H%M", time.localtime(time.time()))}|{str(random.random())[-6:]}'
        url = " https://wx.17u.cn/flightcreateorder/buildtemporder"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "818",
            "tcsessionid": self.tcsessionid,
            "tcuserid": self.tcuserid,
            "tcsectoken": self.tcsectoken,
            "apmat": apmat,
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
                "GSGuid": self.stag,
                "InsType": 1, "InsurBind": 0, "FlightType": 1, "IsXuanGou": 0,
                "TcAllianceID": "477490115",
                "openId": self.openId,
                "session_key": "3D3D25F7ABFB0B52C72C7C54020445AA",
                "unionid": self.tcuserid,
                "refid": "319527329", "plat": 852,
                "SessionId": self.tcsessionid,
                "SecToken": self.tcsectoken,
                "xcxVersion": "2020.04.02",
                # "linkTrackerId": "769e2675-c72a-f426-9471-02a14b84f331"
                }
        res = requests.post(url=url, headers=headers, json=data, verify=False).json()
        print(res)
        if res.get("resCode") == 100:
            self.SerialId = res.get("Data").get("SerialId")
        else:
            self.msg = {
                "status": 3,
                "msg": "创建临时单失败"
            }



    def do_order(self):
        res = self.do_get_city_name()
        if isinstance(res, dict):
            res["index"] = "do_get_city_name"
            return res
        res = self.get_fit_lower_price()
        if isinstance(res, dict):
            res["index"] = "get_fit_lower_price"
            return res
        self.post_build_order()


if __name__ == "__main__":
    data_ = {
        "vcode": "",
        "extra": "",
        "adultNum": 1,
        "priceInfo": {
            "extra": "",
            "cabin": "Q",  # 舱位
            "siloCell": "Y",  # 仓等
            "highPrice": 330,  # 是否含机建燃油
            "lowPrice": 100
        },
        "flight": {
            "departure": "CKG",
            "arrival": "CGO",
            "depTime": "2020-05-30 09:15",
            "flightNo": "3U8509"
        },
        "passengers": [
            {
                "name": "李冲",
                "cardType": "ID",
                "ageType": "ADT",
                "gender": "M",
                "birthday": "1990-03-07",
                "cardNum": "35010219900307163X",
                "mobile": ""
            }
        ],
        "contact": {
            "name": "黄小明",
            "firstName": "",
            "lastName": "",
            "mobile": "17658643223",
            "email": ""
        }
    }

    d = Order(params=data_)
    print(d.do_order())
