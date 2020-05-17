from APP.setting import *
import requests
import urllib3

urllib3.disable_warnings()


class Pay(object):
    """优惠券下单"""

    def __init__(self, params, param):
        self.orderId = params.get("orderNo")
        self.totalPrice = float(params.get("totalPrice"))
        self.param = param
        self.clientInfo = param.get("clientInfo")
        self.couponInfo = {}

    def post_MembershipHandler_HomeLogin(self):
        """
        执行二次登录
        :param param:
        :return:
        """
        reqTime = get_time()
        url = "https://appgateway.ly.com/member/MembershipHandler.ashx"
        secInfo_data = {
            "data": {"densityDpi": "240", "deviceId": self.clientInfo.get("deviceId"),
                     "heightPixels": self.clientInfo.get("device").split("|")[2].split("*")[0],
                     "manufacturer": self.clientInfo.get("manufacturer"),
                     "model": self.clientInfo.get("device").split("|")[3], "sdkInt": "22",
                     "widthPixels": self.clientInfo.get("device").split("|")[2].split("*")[1]},
            "flag": "false", "timeStamp": get_time()}
        data = {"request": {
            "body": {"isUserLogin": "0",
                     "loginName": self.param.get("body").get("loginName"),
                     "memberIdNew": self.param.get("body").get("memberIdNew"),
                     # "password": get_password(password=self.param.get("body").get("password")),
                     "password": self.param.get("body").get("password"),
                     "secInfo": http_do_decrypt(secInfo_data),
                     "clientInfo": self.clientInfo,
                     "versionNo": "1"
                     },
            "header": {
                "accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                "digitalSign": get_digital_sign(req_time=reqTime, service_name="HomeLogin", version="20111128102912"),
                "reqTime": reqTime,
                "serviceName": "HomeLogin", "version": "20111128102912"}
        }}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|00088",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "appgateway.ly.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        res = requests.post(url=url, headers=headers, data=data, verify=False).json()
        if res.get("response").get("header").get("rspCode") == "0000":
            sUserList = res.get("response").get("body").get("sUserList")
            if sUserList:
                self.tcunionId = sUserList[0].get("unionId")
                self.userId = sUserList[0].get("userId")
                self.externalMemberId = res.get("response").get("body").get("externalMemberId")
                self.memberId = res.get("response").get("body").get("memberId")
                self.memberIdNew = res.get("response").get("body").get("memberIdNew")
                return True
            return {
                "status": 3,
                "msg": "获取tcunionId,和userId失败"
            }
        else:
            return {
                "status": 3,
                "msg": "二次登录失败"
            }

    def post_NewOrderListHandler_GetOrderListInfo(self):
        """
        查找待支付订单
        :return:
        """
        reqTime = get_time()
        url = "https://appgateway.ly.com/ordercenter/Order/NewOrderListHandler.ashx"
        data = {"request": {
            "body": {
                "orderFilter": "1", "dateType": "0", "sortType": "0", "pageSize": "200",
                "clientInfo": self.clientInfo,
                "memberIdNew": self.memberIdNew,
                "page": "1", "isValidOrder": "0",
                "memberId": self.memberId
            },
            "header": {
                "accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                "digitalSign": get_digital_sign(req_time=reqTime, service_name="GetOrderListInfo",
                                                version="20111128102912"),
                "reqTime": reqTime,
                "serviceName": "GetOrderListInfo", "version": "20111128102912"}
        }}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "sxx": self.param.get("sxx"),
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|00032",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "tcmobileapi.17usoft.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        res = requests.post(url=url, headers=headers, data=data, verify=False).json()
        print(res)
        if res.get("response").get("header").get("rspCode") == "0000":
            for order in res.get("response").get("body").get("orderListAll"):
                if order.get("orderStatus") == "待支付":
                    orderId = order.get("orderId")
                    amount = order.get("amount")
                    if self.orderId == orderId and self.totalPrice == float(amount[1:]):
                        pass
                    continue
                continue
        else:
            return {
                "status": 3,
                "msg": f"查找待支付订单失败, {res.get('response').get('header').get('rspDesc')}"
            }

    def do_pay(self):
        res = self.post_MembershipHandler_HomeLogin()
        if isinstance(res, dict):
            return res
        res = self.post_NewOrderListHandler_GetOrderListInfo()
        if isinstance(res, dict):
            return res


if __name__ == "__main__":
    pass
