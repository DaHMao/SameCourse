# --coding:utf-8--
from APP.setting import *
import requests
import json
import urllib3
from tc_app_log.Journal_class import Journal
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout, ProxyError
from urllib3.exceptions import MaxRetryError, NewConnectionError
from OpenSSL.SSL import Error, WantReadError
import traceback
from tc_app_log.loghelper import __write_log__

urllib3.disable_warnings()


class Order(object):

    def __init__(self, params, ip={}):
        self.flight = params.get("flight")  # 航班信息
        self.passengers = params.get("passengers")  # 乘客信息
        self.contact = params.get("contact")  # 联系人信息
        self.departure = self.flight.get("departure")
        self.departure_name = ""
        self.arrival = self.flight.get("arrival")
        self.arrival_name = ""
        self.high_price = float(params.get("priceInfo").get("highPrice")) - 50
        self.low_price = float(params.get("priceInfo").get("lowPrice")) - 50
        self.clientInfo = {}  # clientInfo
        self.couponInfo = {}  # 所有红包列表
        self.tcunionId = ""
        self.externalMemberId = ""
        self.memberId = ""
        self.memberIdNew = ""
        self.userId = ""
        self.price = ""  # 生单价格
        self.stag = ""
        self.cabinTypeName = ""
        self.NoMileAge = 0  # 判断是否叠加里程
        self.serial_id = ""  # 生成的假单的订单号
        self.GWPassengerLimitSwitch = ""
        self.orderNo = ""
        self.Price = ""
        self.red_id = ""
        self.departure_date = ""
        self.sxx = ""
        self.loginUser = ""
        self.loginPwd = ""
        self.type_id = ""  # 红包类型id
        self.mileage = ""
        self.unifiedMileages = []  # 使用里程列表
        self.cabin = params.get("priceInfo").get("cabin")
        self.siloCell = "Y"
        if ip:
            self.ip = ip
        else:
            self.ip = None

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

    def do_compare_price(self, price):
        """
        判断价格是否在所给的价格区间
        :return:
        """
        return self.low_price <= int(price) <= self.high_price

    def post_query_flight_list(self):
        """
        获取航班的起飞时间
        :return:
        """
        url = "https://wx.17u.cn/flightbffquery/query/getkylinflightlist"
        data = {"plat": 434, "unionid": "", "refid": "0", "openid": "", "IsFromPhoenix": 1,
                "Departure": self.departure, "Arrival": self.arrival, "GetType": "1",
                "IsBaby": 0, "QueryType": "1", "FlightNo": "",
                "DepartureName": self.departure_name,
                "ArrivalName": self.arrival_name, "ProductType": "1",
                "DepartureDate": self.flight.get("depTime"),
                "hasAirPort": "3",
                "isFromKylinApp": True}
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "482",
            "tcplat": "434",
            "Origin": "https://wx.17u.cn",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; VOG-AL00 Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML"
                          ", like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36/TcTravel/10.0.0",
            "auth": "true",
            "Content-Type": "application/json",
            "tcversion": "1.1.0",
            "Accept": "application/json, text/plain, */*",
            "cache-control": "no-cache",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "X-Requested-With": "com.tongcheng.android",
        }
        data = dict_to_json(data)
        try:
            res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=self.ip).json()
            print(res)
            if res.get("resCode") == 0 and res.get("body").get("ErrorCode") == 0:
                info_simple_list = res.get("body").get("FlightInfoSimpleList")
                if info_simple_list:
                    for info_simple in info_simple_list:
                        if info_simple.get("flightNo") == self.flight.get('flightNo'):
                            self.departure_date = info_simple.get("flyOffTime")
                            print(self.departure_date)
                        continue
                else:
                    return {
                        "status": 3,
                        "msg": "没有找到对应的航程信息"
                    }
            else:
                return {
                    "status": 3,
                    "msg": f"航班号：{self.flight.get('flightNo')},获取对应的起飞日期{self.flight.get('depTime')}的失"
                    f"败，请求：{res.get('resDesc')},原因：{res.get('body').get('ErrorMessage')}"
                }
        except json.decoder.JSONDecodeError:
            return {
                "status": 301,

            }

    def post_get_flight_list_one(self):
        """
         根据航班获取价格信息,排除不在价格区间的票价
         inoo ：判断是否是绑定活动
        :return:
        """
        l_price = []
        url = "https://wx.17u.cn/flightbffquery/query/getkylinflightlist"
        data = {"plat": 434, "unionid": "",
                "openid": "", "IsFromPhoenix": 1,
                "Departure": self.departure,
                "Arrival": self.arrival,
                "GetType": "0", "IsBaby": 0, "flightno": self.flight.get("flightNo"),
                "QueryType": "1",
                "DepartureName": self.departure_name,
                "ArrivalName": self.arrival_name,
                "DepartureDate": self.flight.get("depTime"),
                "ProductType": "1",
                "AirCode": self.flight.get("flightNo")[:2], "IsBook15": 1, "TripType": "0", "newCabinDeal": 2,
                "isFromKylinApp": True}
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "482",
            "tcplat": "434",
            "Origin": "https://wx.17u.cn",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; VOG-AL00 Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML"
                          ", like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36/TcTravel/10.0.0",
            "auth": "true",
            "Content-Type": "application/json",
            "tcversion": "1.1.0",
            "Accept": "application/json, text/plain, */*",
            "cache-control": "no-cache",
            "Referer": "https://wx.17u.cn/kylinapp/nbook1_5?RefId=0&filterCabin=&traceId=",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "X-Requested-With": "com.tongcheng.android",

        }
        data = dict_to_json(data)
        try:
            res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=self.ip).json()
            if res.get("resCode") == 0 and res.get("body").get("ErrorCode") == 0:
                if self.siloCell == "Y":
                    economy_list = res.get("body").get("newCabinList").get("economyList")
                    if economy_list:
                        for economy in economy_list:
                            client_ticket_price = economy.get("clientTicketPrice")
                            if self.cabin == economy.get("realRoomCode"):
                                if self.do_compare_price(client_ticket_price):
                                    l_price.append(economy)
                        if l_price:
                            return l_price
                        else:
                            return {
                                "status": 3,
                                "msg": "未匹配到符合该舱位价格区间的机票"
                            }
                    else:
                        return {
                            "status": 3,
                            "msg": "未找到该航班的所对应的--经济舱--信息"
                        }
                elif self.siloCell == "C":
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
                                "msg": "未匹配到该价格区间的机票"
                            }
                    else:
                        return {
                            "status": 3,
                            "msg": "未找到该航班的所对应的--公务舱--信息"
                        }
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
        except json.decoder.JSONDecodeError:
            return {
                "status": 301,
            }

    def get_fit_lower_price(self):
        """
        获取符合要求的最低价的机票价格
        :return:
        """
        res = self.post_get_flight_list_one()
        if isinstance(res, dict):
            res["index_one"] = "post_get_flight_list_one"
            return res
        res = self.do_binding_price(price_l=res)
        # print(res)
        if isinstance(res, dict):
            res["index_one"] = "do_binding_price"
            return res
        print("符合价格区间的个数：", len(res))
        self.get_lowest_price(price_ll=res)

    def get_order_user_price(self):
        """
        通过价格获取生单账号
        :return:
        """
        url = f"{URL}/getCouponUser.do?price={self.price}"
        res = requests.get(url=url).json()
        if res.get("status") == 0:
            self.clientInfo = res.get("device").get("clientInfo")
            user_list = res.get("token").get("sUserList")
            try:
                self.tcunionId = user_list[0].get("unionId")
                self.userId = user_list[0].get("userId")
            except IndexError:
                self.tcunionId = ""
                self.userId = ""
            self.externalMemberId = res.get("token").get("externalMemberId")
            self.memberId = res.get("token").get("memberId")
            self.memberIdNew = res.get("token").get("memberIdNew")
            self.sxx = res.get("device").get("sxx")
            self.loginUser = res.get("phone")
            self.loginPwd = res.get("pwd")
            self.type_id = res.get("coupon").get("type_id")
            res_red = get_red_envelopes(res)  # 领取优惠券
            print(res_red)
            if isinstance(res_red, dict):
                return res_red
            if res_red == "请重新获取账号":
                return False
            print("领取优惠券成功")
            self.red_id = res_red
            return True
        else:
            res["msg"] = "领取优惠券失败"
            return res

    def do_get_order_user_price(self):
        """
        重复获取到可用的账号
        :return:
        """
        while True:
            res = self.get_order_user_price()
            if isinstance(res, dict):
                return res
            elif res:
                break

    def get_order_user_mail(self, mail):
        """
        通过里程获取账号
        :param mail:
        :return:
        """
        url = URL + "/getIntegralUser.do"
        data = {
            "integral": mail,
        }
        res = requests.post(url=url, json=data).json()
        # res = get_get_user_do(phone="17820570249")
        if res.get("status") == 0:
            self.clientInfo = res.get("device").get("clientInfo")
            user_list = res.get("token").get("sUserList")
            try:
                self.tcunionId = user_list[0].get("unionId")
                self.userId = user_list[0].get("userId")
            except IndexError:
                self.tcunionId = ""
                self.userId = ""
            self.externalMemberId = res.get("token").get("externalMemberId")
            self.memberId = res.get("token").get("memberId")
            self.memberIdNew = res.get("token").get("memberIdNew")
            self.sxx = res.get("device").get("sxx")
            self.loginUser = res.get("phone")
            self.loginPwd = res.get("pwd")
            return True
        else:
            res["msg"] = "获取账号失败"
            return res

    def do_get_order_user_mail(self):
        """
        通过里程重复获取到可用的账号
        :return:
        """
        for mail in mileageSteps:
            res = self.get_order_user_mail(mail=str(mail))
            if isinstance(res, dict):
                continue
            else:
                self.mileage = str(mail)
                return "获取账号成功"
        else:
            return {
                "status": 3,
                "msg": "没有获取里程账号"
            }

    def post_get_flight_list_two(self):
        """
         根据航班获取指定价格信息的机票,
         inoo ：判断是否是绑定活动
        :return:
        """
        l_price = []
        url = "https://wx.17u.cn/flightbffquery/query/getkylinflightlist"
        data = {"plat": 434, "unionid": "",
                "openid": "", "IsFromPhoenix": 1,
                "Departure": self.departure,
                "Arrival": self.arrival,
                "GetType": "0", "IsBaby": 0, "flightno": self.flight.get("flightNo"),
                "QueryType": "1",
                "DepartureName": self.departure_name,
                "ArrivalName": self.arrival_name,
                "DepartureDate": self.flight.get("depTime"),
                "ProductType": "1",
                "AirCode": self.flight.get("flightNo")[:2], "IsBook15": 1, "TripType": "0", "newCabinDeal": 2,
                "MemberId": self.externalMemberId,
                "deviceId": self.clientInfo.get('deviceId'),
                "kylinAppMemberId": self.externalMemberId,
                "isFromKylinApp": True}
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "482",
            "tcunionid": self.tcunionId,
            "tcplat": "434",
            "Origin": "https://wx.17u.cn",
            "tcuserid": self.externalMemberId,
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; VOG-AL00 Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML"
                          ", like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36/TcTravel/10.0.0",
            "auth": "true",
            "Content-Type": "application/json",
            "tcversion": "1.1.0",
            "Accept": "application/json, text/plain, */*",
            "cache-control": "no-cache",
            "tcsectoken": self.externalMemberId,
            "tcdeviceid": self.clientInfo.get('deviceId'),
            "Referer": "https://wx.17u.cn/kylinapp/nbook1_5?RefId=0&filterCabin=&traceId=",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "X-Requested-With": "com.tongcheng.android",

        }
        data = dict_to_json(data)
        res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=self.ip).json()
        if res.get("resCode") == 0 and res.get("body").get("ErrorCode") == 0:
            if self.siloCell == "Y":
                economy_list = res.get("body").get("newCabinList").get("economyList")
                if economy_list:
                    for economy in economy_list:
                        client_ticket_price = economy.get("clientTicketPrice")
                        if self.cabin == economy.get("realRoomCode"):
                            if self.do_compare_price(client_ticket_price):
                                l_price.append(economy)
                    if l_price:
                        return l_price
                    else:
                        return {
                            "status": 3,
                            "msg": "未匹配到符合该舱位价格区间的机票"
                        }
                else:
                    return {
                        "status": 3,
                        "msg": "未找到该航班的所对应的--经济舱--信息"
                    }
            elif self.siloCell == "C":
                business_list = res.get("body").get("newCabinList").get("businessList")
                if business_list:
                    for business in business_list:
                        if int(business.get("clientTicketPrice")) == self.price and \
                                self.cabin == business.get("realRoomCode"):
                            l_price.append(business)
                    if l_price:
                        return l_price
                    else:
                        return {
                            "status": 3,
                            "msg": "未匹配到该价格区间的机票"
                        }
                else:
                    return {
                        "status": 3,
                        "msg": "未找到该航班的所对应的--公务舱--信息"
                    }
            else:
                return {
                    "status": 3,
                    "msg": "传入的舱等有误，未匹配的到对应的舱等的信息"
                }
        else:
            return {
                "status": 3,
                "msg": "根据航班获取价格信息失败"
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
            if price.get("pcks") or price.get("freeRefundChange") or price.get(
                    "isBindInus") == 1:
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

        l_one = [(int(price.get("clientTicketPrice")), price.get("stag"), price.get("realRoomCode"),
                  price.get("ProductIndexes"), price.get("drm")) for price in price_ll]
        l_two = sorted(l_one, key=lambda x: x[0])
        self.price = l_two[0][0]
        print("生单价格（不含税）：", self.price)
        # print(type(self.price))
        self.stag = l_two[0][1]
        self.cabin = l_two[0][2]
        self.cabinTypeName = CabinTypeName[l_two[0][3]]
        if l_two[0][4]:
            self.NoMileAge = 1  # 是否累加同程里程 1 表示不累加
        else:
            self.NoMileAge = 0
        print(self.cabinTypeName)

    def post_build_temp_order(self):
        """
        获取 SerialId
        :return:
        """
        url = "https://wx.17u.cn/kylinapp/api/json/buildtemporder.html"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "tcunionid": self.tcunionId,
            "tcplat": "434",
            "Origin": "https://wx.17u.cn",
            "tcuserid": self.externalMemberId,
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; VOG-AL00 Build/LMY48Z; wv) AppleWebKit/537.36 ("
                          "KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36/TcTravel/10.0.0",
            "auth": "true",
            "Content-Type": "application/json",
            "tcversion": "1.1.0",
            "Accept": "application/json, text/plain, */*",
            "cache-control": "no-cache",
            "tcsectoken": self.externalMemberId,
            "tcdeviceid": self.clientInfo.get('deviceId'),
            "Referer": "https://wx.17u.cn/kylinapp/nbook1_5?RefId=0&filterCabin=&traceId=",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "X-Requested-With": "com.tongcheng.android",
        }
        data = {"FlightDataBack": "", "FlightData": "", "DataKey": "", "BackDataKey": "", "IsBackOrder": False,
                "OrderTypeAirline": 1, "IsMultipleIns": True, "IsUnionOrder": False, "IsYouXuan": 0,
                "GSGuid": self.stag,
                "InsType": 1, "InsurBind": 0, "IsFromPhoenix": 1, "TcAllianceID": self.clientInfo.get("refId"),
                "finfo": 0, "xcxVersion": "2019.09.10", "UnionId": self.tcunionId, "Plat": 434, "IsMuilteSite": 1,
                "MemberId": self.externalMemberId, "deviceId": self.clientInfo.get('deviceId'),
                "kylinAppMemberId": self.externalMemberId, "isFromKylinApp": True}
        data = dict_to_json(data)
        try:
            res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=self.ip).json()
            if res.get("ErrorCode") == 100 and res.get("Data").get("RspCode") == "0":
                self.serial_id = res.get("Data").get("SerialId")
                self.GWPassengerLimitSwitch = res.get("Data").get("GWPassengerLimitSwitch")
                red_packages = res.get("Data").get("RedPackages")  # 红包列表
                res = self.use_available_coupons(red_packages_l=red_packages)
                if isinstance(res, dict):
                    return res
                self.couponInfo = res[-1]
            else:
                return {
                    "status": 3,
                    "msg": f"生成同程假订单失败, 请求：{res.get('ErrorMsg')},原因：{res.get('Data').get('ErrorMsg')}"
                }
        except json.decoder.JSONDecodeError:
            return {
                "status": 301,

            }

    def post_build_temp_order_by_mail(self):
        """
        获取 SerialId,  unifiedMileages里程提交列表
        :return:
        """
        url = "https://wx.17u.cn/kylinapp/api/json/buildtemporder.html"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "tcunionid": self.tcunionId,
            "tcplat": "434",
            "Origin": "https://wx.17u.cn",
            "tcuserid": self.externalMemberId,
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; VOG-AL00 Build/LMY48Z; wv) AppleWebKit/537.36 ("
                          "KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36/TcTravel/10.0.0",
            "auth": "true",
            "Content-Type": "application/json",
            "tcversion": "1.1.0",
            "Accept": "application/json, text/plain, */*",
            "cache-control": "no-cache",
            "tcsectoken": self.externalMemberId,
            "tcdeviceid": self.clientInfo.get('deviceId'),
            "Referer": "https://wx.17u.cn/kylinapp/nbook1_5?RefId=0&filterCabin=&traceId=",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "X-Requested-With": "com.tongcheng.android",
        }
        data = {"FlightDataBack": "", "FlightData": "", "DataKey": "", "BackDataKey": "", "IsBackOrder": False,
                "OrderTypeAirline": 1, "IsMultipleIns": True, "IsUnionOrder": False, "IsYouXuan": 0,
                "GSGuid": self.stag,
                "InsType": 1, "InsurBind": 0, "IsFromPhoenix": 1, "TcAllianceID": self.clientInfo.get("refId"),
                "finfo": 0, "xcxVersion": "2019.09.10", "UnionId": self.tcunionId, "Plat": 434, "IsMuilteSite": 1,
                "MemberId": self.externalMemberId, "deviceId": self.clientInfo.get('deviceId'),
                "kylinAppMemberId": self.externalMemberId, "isFromKylinApp": True}
        data = dict_to_json(data)
        try:
            res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=self.ip).json()
            if res.get("ErrorCode") == 100 and res.get("Data").get("RspCode") == "0":
                self.serial_id = res.get("Data").get("SerialId")
                self.GWPassengerLimitSwitch = res.get("Data").get("GWPassengerLimitSwitch")
                try:
                    mile_rules = res.get("Data").get("MileageInfo").get("MileRules")[0]  # 里程兑换原则列表
                    self.unifiedMileages.append(
                        {"type": mile_rules.get("type"),
                         "ruleId": mile_rules.get("code"),
                         "mileageName": mile_rules.get("name"),
                         "mileageScale": mile_rules.get("proportion"),
                         "mileage": int(self.mileage),
                         "mileageAmount": int(int(self.mileage) / mile_rules.get("proportion")),
                         "memberCardNo": "",
                         "mileageMemberName": "",
                         "mileageMemberCertNo": ""})
                except TypeError:
                    return {
                        "status": 302,
                        "msg": "生单失败，不能使用里程支付"
                    }
            else:
                return {
                    "status": 3,
                    "msg": f"生成同程假订单失败, 请求：{res.get('ErrorMsg')},原因：{res.get('Data').get('ErrorMsg')}"
                }
        except json.decoder.JSONDecodeError:
            return {
                "status": 301,

            }

    def use_available_coupons(self, red_packages_l):
        """
         使用可以使用的优惠劵
         {"couponAmount": 5, "couponNo": "AP_CO_TC4Q37C5F3G8FSTJ33SRAHYE","couponBatchNo": "AP_AC3G4HTXAYZ", "
         couponOrderAmount": 615}
        :param red_packages_l:
        :return:
        """
        l_three = []
        if red_packages_l:
            for red in red_packages_l:
                if red.get("SmallAmount") <= self.price:
                    l_three.append(
                        {"couponAmount": red.get("ParValue"), "couponNo": red.get("CouponNo"),
                         "couponBatchNo": red.get("BatchNo"),
                         "couponOrderAmount": int(self.price) - red.get("ParValue") + 50})
            if l_three:
                l_four = sorted(l_three, key=lambda x: x["couponAmount"])
                return l_four
            else:
                return {
                    "status": 3,
                    "msg": "没有符合该价格优惠劵可以使用"
                }
        else:
            return {
                "status": 3,
                "msg": "该账号无优惠劵可用"
            }

    def post_anvendte_passager_handler_addlinker(self, passager_one):
        """
        添加乘客信息(目前只限身份证)
        :param passager_one:
        :return:
        """
        sex = "1" if passager_one.get("gender") == "M" else "0"
        req_time = get_time()

        url = "https://tcmobileapi.17usoft.com/flight/AnvendtePassagerHandler.ashx"
        data = {"request": {
            "body": {
                "birthday": passager_one.get("birthday"),
                "certList": [{"certNo": passager_one.get("cardNum"),
                              "certType": "1"}],
                "chineseName": passager_one.get("name"),
                "clientInfo": self.clientInfo,
                "memberId": self.memberId,
                "mobile": passager_one.get("mobile"),
                "memberIdNew": self.memberIdNew,
                "projectTag": "guoneijipiao",
                "sex": sex,
            },
            "header": {
                "accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                "digitalSign": get_digital_sign(req_time=req_time, service_name="addlinker", version="20111128102912"),
                "reqTime": req_time,
                "serviceName": "addlinker", "version": "20111128102912"}
        }}
        data = dict_to_json_two(data)
        data01 = {"body": data}
        headers = {
            "sxx": self.sxx,
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|00001",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "tcmobileapi.17usoft.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        try:
            res = requests.post(url=url, headers=headers, data=data.encode("utf-8"), verify=False,
                                proxies=self.ip).json()
            # print(res)
            if res.get("response").get("header").get("rspCode") == "0000":
                liker_id = res.get("response").get("body").get("linkerId")
                return f"{AgeType[passager_one.get('ageType')]};{passager_one.get('name')};" \
                    f"身份证/{passager_one.get('cardNum')}/{passager_one.get('birthday')}/{sex}" \
                    f"/{liker_id};{passager_one.get('mobile')}"
            else:
                return {
                    "status": 3,
                    "msg": f"添加乘客信息失败,{res.get('response').get('header').get('rspDesc')}"
                }
        except json.decoder.JSONDecodeError:
            return {
                "status": 301,

            }

    def do_add_addlinkers(self):
        """
        添加多名乘客
        :return: 乘客信息列表
        """
        l_passerage = []
        for passerage in self.passengers:
            res = self.post_anvendte_passager_handler_addlinker(passager_one=passerage)
            if isinstance(res, dict):
                return res
            else:
                l_passerage.append(res)
        return l_passerage

    def post_anvendte_passager_handler_chk_untrusted_person(self):
        """
        校验乘机人是否失信
        :return:
        """
        common_requests = []
        for passerage in self.passengers:
            common_requests.append(
                {"birthDate": passerage.get("birthday"), "certNo": passerage.get("cardNum"),
                 "certType": "身份证", "name": passerage.get("name")}
            )
        req_time = get_time()
        url = "https://tcmobileapi.17usoft.com/flight/AnvendtePassagerHandler.ashx"
        data = {"request": {
            "body": {
                "clientInfo": self.clientInfo,
                "commonRequests": common_requests
            },
            "header": {
                "accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                "digitalSign": get_digital_sign(req_time=req_time, service_name="ChkUntrustedPerson",
                                                version="20111128102912"),
                "reqTime": req_time,
                "serviceName": "ChkUntrustedPerson", "version": "20111128102912"}
        }}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "sxx": self.sxx,
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|00000",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "tcmobileapi.17usoft.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        try:
            res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=self.ip).json()
            if res.get("response").get("header").get("rspCode") == "0000":
                return True
            else:
                return {
                    "status": 3,
                    "msg": f"添加乘客校验失败{res.get('response').get('header').get('rspDesc')}"
                }
        except json.decoder.JSONDecodeError:
            return {
                "status": 301,

            }

    def post_check_repeat_passenger(self, ll_passenger):
        """
        判断是不是重复下单
        :param ll_passenger:
        :return:
        """
        url = "https://wx.17u.cn/kylinapp/api/json/checkwxrepeatpassenger.html"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "tcunionid": self.tcunionId,
            "tcplat": "434",
            "Origin": "https://wx.17u.cn",
            "tcuserid": self.externalMemberId,
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; VOG-AL00 Build/LMY48Z; wv) AppleWebKit/537.36"
                          " (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36/TcTravel/10.0.0",
            "auth": "true",
            "Content-Type": "application/json",
            "tcversion": "1.1.0",
            "Accept": "application/json, text/plain, */*",
            "cache-control": "no-cache",
            "tcsectoken": self.externalMemberId,
            "tcdeviceid": self.clientInfo.get('deviceId'),
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "X-Requested-With": "com.tongcheng.android",
        }
        data = {"Plist": ll_passenger,
                "InsuranceNum": 0,
                "OrderSerialId": self.serial_id, "FlightNo": self.flight.get("flightNo"),
                "StartPort": self.flight.get("departure"),
                "EndPort": self.flight.get("arrival"),
                "FlyOffDate": self.flight.get("depTime"), "MemberId": self.externalMemberId,
                "DeviceId": self.clientInfo.get('deviceId'), "plat": 434, "deviceId": self.clientInfo.get('deviceId'),
                "kylinAppMemberId": self.externalMemberId, "isFromKylinApp": True}
        data = dict_to_json(data)
        try:
            res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=self.ip).json()
            # print("post_checkwxrepeatpassenger", res)
            if res.get("ResCode") == 0:
                return True
            else:
                return {
                    "status": 3,
                    "msg": f"是否是重复出单------{res.get('ResDesc')}"
                }
        except json.decoder.JSONDecodeError:
            return {
                "status": 301,

            }

    def post_submit_order_price(self, l_passenger):
        """
        生单
        :param l_passenger:
        :return:
        """
        passager_one = {"MailABKey": 0, "HasMailCheck": 1, "BookingType": self.NoMileAge, "cabinsProductType": 0,
                        "cabinTypeName": self.cabinTypeName}
        url = "https://wx.17u.cn/kylinapp/api/json/submitorder.html"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "tcunionid": self.tcunionId,
            "tcplat": "434",
            "Origin": "https://wx.17u.cn",
            "tcuserid": self.externalMemberId,
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; VOG-AL00 Build/LMY48Z; wv) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36/TcTravel/10.0.0",
            "auth": "true",
            "Content-Type": "application/json",
            "tcversion": "1.1.0",
            "Accept": "application/json, text/plain, */*",
            "cache-control": "no-cache",
            "tcsectoken": self.externalMemberId,
            "tcdeviceid": self.clientInfo.get('deviceId'),
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "X-Requested-With": "com.tongcheng.android",
        }
        data = {"OrderSerialId": self.serial_id, "isNewInsuranceType": 1, "LinkMobile": self.contact.get("mobile"),
                "InsuranceCodeDesc": "", "DelayCodeDesc": "", "HKZHInsureCodeDesc": "", "WorryFreeInsCodeDesc": "",
                "LuggageLostInsCodeDesc": "", "EpidemicInsCodeDesc": "",
                "Plist": l_passenger,
                "IsNeedSend": "0", "submitCheckRepeat": 0, "IsRegTcMember": True, "IsCheckCertNo": 1,
                "EnsurePassageInfoStr": "{\"isEnsure\":0,\"EnsurePassage\":[]}", "UCType": "", "IsChangePrice": 0,
                "totalPassengerDiscountPrice": 0, "IsChangePlus": 0, "ErrorType": 1, "OrderTypeAirline": 1,
                "gwPassengerLimitSwitch": self.GWPassengerLimitSwitch, "reimbursementType": 0, "BackOrderSerialId": "",
                "LinkMan": self.contact.get("name"),
                "LinkCertNo": "",
                "ClientToken": dict_to_json(passager_one),
                "CouponInfo": self.couponInfo,  # 添加可用红包
                "unifiedMileages": [],
                "flightCabinVoucher": "", "tiedProductList": [], "commonProductList": [], "isNewConsumer": 0,
                "isFromKylin": "1", "MemberId": self.externalMemberId, "DeviceId": self.clientInfo.get('deviceId'),
                "UnionId": self.tcunionId, "NoMileAge": self.NoMileAge, "plat": 434,
                "deviceId": self.clientInfo.get('deviceId'),
                "kylinAppMemberId": self.externalMemberId, "isFromKylinApp": True}
        data = dict_to_json(data)
        try:
            res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=self.ip).json()
            # print(res)
            if res.get("ResponseCode") == "0":
                body = json.loads(res.get("Body"))
                self.orderNo = body.get("Serialid")
                self.Price = body.get("CustomerShouldPay")
                return {
                    "status": 0,
                    "msg": "success",
                    "currency": "CNY",
                    "totalPrice": self.Price,
                    "orderNo": self.orderNo,
                    "loginUser": self.loginUser
                }
            else:
                return {
                    "status": 3,
                    "msg": f"生单失败------{res.get('ResDesc')}"
                }
        except json.decoder.JSONDecodeError:
            return {
                "status": 301,

            }

    def post_submit_order_mail(self, l_passenger):
        """
        里程数生单
        :param l_passenger:
        :return:
        """
        passager_one = {"MailABKey": 0, "HasMailCheck": 1, "BookingType": self.NoMileAge, "cabinsProductType": 0,
                        "cabinTypeName": self.cabinTypeName}
        url = "https://wx.17u.cn/kylinapp/api/json/submitorder.html"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "tcunionid": self.tcunionId,
            "tcplat": "434",
            "Origin": "https://wx.17u.cn",
            "tcuserid": self.externalMemberId,
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; VOG-AL00 Build/LMY48Z; wv) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36/TcTravel/10.0.0",
            "auth": "true",
            "Content-Type": "application/json",
            "tcversion": "1.1.0",
            "Accept": "application/json, text/plain, */*",
            "cache-control": "no-cache",
            "tcsectoken": self.externalMemberId,
            "tcdeviceid": self.clientInfo.get('deviceId'),
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "X-Requested-With": "com.tongcheng.android",
        }
        data = {"OrderSerialId": self.serial_id, "isNewInsuranceType": 1, "LinkMobile": self.contact.get("mobile"),
                "InsuranceCodeDesc": "", "DelayCodeDesc": "", "HKZHInsureCodeDesc": "", "WorryFreeInsCodeDesc": "",
                "LuggageLostInsCodeDesc": "", "EpidemicInsCodeDesc": "",
                "Plist": l_passenger,
                "IsNeedSend": "0", "submitCheckRepeat": 0, "IsRegTcMember": True, "IsCheckCertNo": 1,
                "EnsurePassageInfoStr": "{\"isEnsure\":0,\"EnsurePassage\":[]}", "UCType": "", "IsChangePrice": 0,
                "totalPassengerDiscountPrice": 0, "IsChangePlus": 0, "ErrorType": 1, "OrderTypeAirline": 1,
                "gwPassengerLimitSwitch": self.GWPassengerLimitSwitch, "reimbursementType": 0, "BackOrderSerialId": "",
                "LinkMan": self.contact.get("name"),
                "LinkCertNo": "",
                "ClientToken": dict_to_json(passager_one),
                # "CouponInfo": self.couponInfo,  # 添加可用红包
                "unifiedMileages": self.unifiedMileages,
                "flightCabinVoucher": "", "tiedProductList": [], "commonProductList": [], "isNewConsumer": 0,
                "isFromKylin": "1", "MemberId": self.externalMemberId, "DeviceId": self.clientInfo.get('deviceId'),
                "UnionId": self.tcunionId, "NoMileAge": self.NoMileAge, "plat": 434,
                "deviceId": self.clientInfo.get('deviceId'),
                "kylinAppMemberId": self.externalMemberId, "isFromKylinApp": True}
        data = dict_to_json(data)
        try:
            res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=self.ip).json()
            print(res)
            # {'ResCode': 0, 'ResponseCode': '2003', 'ResDesc': '查询会员信息失败，请重新提交', 'ResType': 0, 'RequestTime': 142}
            if res.get("ResponseCode") == "0":
                body = json.loads(res.get("Body"))
                self.orderNo = body.get("Serialid")
                self.Price = body.get("CustomerShouldPay")
                return {
                    "status": 0,
                    "msg": "success",
                    "currency": "CNY",
                    "totalPrice": self.Price,
                    "orderNo": self.orderNo,
                    "loginUser": self.loginUser,
                    "loginPwd": self.loginPwd,
                    "mileage": self.mileage
                }
            else:
                return {
                    "status": 3,
                    "msg": f"生单失败------{res.get('ResDesc')}",
                    "loginUser": self.loginUser,
                    "loginPwd": self.loginPwd,

                }
        except json.decoder.JSONDecodeError:
            return {
                "status": 301,

            }

    def get_set_coupon_sta(self):
        """
        设置传入的优惠劵为已用状态
        :return:
        """
        res = requests.get(
            url=f"{URL}/setCouponSta.do?phone={self.loginUser}&type_id={self.type_id}")
        if res.text == "OK":
            return "设置账号的优惠劵为已用状态成功"
        return "设置账号的优惠劵为已用状态失败"

    def do_order_login_coupon(self):
        """
        使用优惠券生单
        :return:
        """
        res = self.do_get_city_name()
        if isinstance(res, dict):
            res["index"] = "do_get_city_name"
            return res
        res = self.get_fit_lower_price()
        if isinstance(res, dict):
            res["index"] = "get_fit_lower_price"
            return res
        res = self.do_get_order_user_price()
        if isinstance(res, dict):
            res["index"] = "do_get_order_user_price"
            return res
        res = self.post_get_flight_list_two()
        if isinstance(res, dict):
            res["index"] = "post_get_flight_list_two"
            return res
        res = self.do_binding_price(price_l=res)
        if isinstance(res, dict):
            res["index"] = "do_binding_price"
            return res
        self.get_lowest_price(price_ll=res)
        res = self.post_build_temp_order()
        if isinstance(res, dict):
            res["index"] = "post_build_temp_order"
            return res
        l_p = self.do_add_addlinkers()
        if isinstance(l_p, dict):
            res["index"] = "do_add_addlinkers"
            return l_p
        res = self.post_anvendte_passager_handler_chk_untrusted_person()
        if isinstance(l_p, dict):
            res["index"] = "post_anvendte_passager_handler_chk_untrusted_person"
            return res
        res = self.post_check_repeat_passenger(l_p)
        if isinstance(res, dict):
            res["index"] = "post_check_repeat_passenger"
            return res
        res = self.post_submit_order_price(l_passenger=l_p)
        if isinstance(res, dict):
            res["index"] = "post_submit_order"
            return res
        res["coupon_sta"] = self.get_set_coupon_sta()
        return res

    def do_order_login_mail(self):
        """
        使用里程生单
        :return:
        """
        res = self.do_get_city_name()
        if isinstance(res, dict):
            res["index"] = "do_get_city_name"
            return res
        res = self.get_fit_lower_price()
        if isinstance(res, dict):
            res["index"] = "get_fit_lower_price"
            return res
        res = self.do_get_order_user_mail()
        if isinstance(res, dict):
            res["index"] = "do_get_order_user_mail"
            return res
        res = self.post_get_flight_list_two()
        if isinstance(res, dict):
            res["index"] = "post_get_flight_list_two"
            return res
        res = self.do_binding_price(price_l=res)
        if isinstance(res, dict):
            res["index"] = "do_binding_price"
            return res
        self.get_lowest_price(price_ll=res)
        res = self.post_build_temp_order_by_mail()
        if isinstance(res, dict):
            res["index"] = "post_build_temp_order"
            return res
        l_p = self.do_add_addlinkers()
        if isinstance(l_p, dict):
            res["index"] = "do_add_addlinkers"
            return l_p
        res = self.post_anvendte_passager_handler_chk_untrusted_person()
        if isinstance(l_p, dict):
            res["index"] = "post_anvendte_passager_handler_chk_untrusted_person"
            return res
        res = self.post_check_repeat_passenger(l_p)
        if isinstance(res, dict):
            res["index"] = "post_check_repeat_passenger"
            return res
        res = self.post_submit_order_mail(l_passenger=l_p)
        if isinstance(res, dict):
            res["index"] = "post_submit_order"
            return res
        return res

    def do_order_by_mail(self):
        i = 0
        while i < 9:
            res_or = self.do_order_login_mail()
            print(res_or)
            if res_or.get("status") == 302:
                i += 1
                get_set_token_sta(phone=self.loginUser, i_d="1")
            elif res_or.get("status") == 301:
                i += 1
            else:
                return res_or
        return {
            "status": 3,
            "msg": f"生单失败,请求账号中心9次，没有获取到可用里程的账号,请重新请求"
        }

    def do_get_price_list(self):
        res = self.do_get_city_name()
        if isinstance(res, dict):
            res["index"] = "do_get_city_name"
            return res
        res = self.get_fit_lower_price()
        if isinstance(res, dict):
            res["index"] = "get_fit_lower_price"
            return res


def order_by_mail(param, l_o_g=""):
    i = 0
    while i < 3:
        log = ''
        ip_res = get_zhima_ip()
        if ip_res.get("status") == 30:
            i += 1
        ip = {
            "http": ip_res.get("http"),
            "https": ip_res.get("https"),
        }
        try:
            ret = Order(params=param, ip=ip).do_order_by_mail()
            resp = {
                "请求数据": param,
                "返回信息": ret
            }
            Journal().save_journal_order(massage=json.dumps(resp))
            log = log + str(param) + '\n' + str(ret) + '\n'
            __write_log__(log, tag="order_by_mail")
            return ret
        except (
                ConnectionError, ConnectTimeout, ReadTimeout, ProxyError, Error, WantReadError, MaxRetryError,
                NewConnectionError, json.decoder.JSONDecodeError):
            i += 1
        except Exception:
            ret = {'status': 500, 'msg': traceback.format_exc()}
            resp = {
                "登录信息": param,
                "响应数据": ret
            }
            Journal().save_journal_order(massage=json.dumps(resp), level="error")
            log = log + str(param) + '\n' + str(ret) + '\n'
            __write_log__(log, tag="order_by_mail")
            return ret

    else:
        return {
            "status": 3,
            "msg": "生单失败，ip问题，请稍后重试"
        }


if __name__ == "__main__":
    pass
