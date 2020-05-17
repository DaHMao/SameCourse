# encoding="utf-8"
from APP.setting import *
import urllib3
import random
from text.PWD import *

urllib3.disable_warnings()


class BindWeChat(object):
    def __init__(self, params):
        self.params = params
        self.clientInfo = params.get("device").get("clientInfo")
        self.memberId = params.get("token").get("memberId")
        self.im_ie = random.choice(Android)
        self.sxx = ""
        self.clientId = ""
        self.tcunionId = ""
        self.userId = ""
        self.externalMemberId = ""
        self.memberId = ""
        self.memberIdNew = ""

    def get_sec_info_data(self):
        """
        {"data":{"densityDpi":"192","deviceId":"957117cdb8f4fa90","heightPixels":"1280","manufacturer":"HUAWEI",
        "model":"VOG-AL00","sdkInt":"22","widthPixels":"720"},"flag":"false","timeStamp":"1587549084179"}
        :return:
        """
        info_data = {
            "data": {"densityDpi": "240", "deviceId": self.clientInfo.get("deviceId"),
                     "heightPixels": self.clientInfo.get("device").split("|")[2].split("*")[0],
                     "manufacturer": self.clientInfo.get("manufacturer"),
                     "model": self.clientInfo.get("device").split("|")[3], "sdkInt": "28",
                     "widthPixels": self.clientInfo.get("device").split("|")[2].split("*")[1]},
            "flag": "false", "timeStamp": get_time()}
        return http_do_decrypt(s=dict_to_json(info_data))

    def post_foundation_handler_one(self):
        req_time = get_time()
        url = "https://tcmobileapi.17usoft.com/foundation/foundationHandler.ashx"
        data = {"request": {
            "body": {"deviceProfile": get_device_profile(self.clientInfo.get("device")),
                     "clientInfo": self.clientInfo},
            "header": {
                "accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                "digitalSign": get_digital_sign(req_time=req_time, service_name="gatewayconfig",
                                                version="20111128102912"),
                "reqTime": req_time,
                "serviceName": "gatewayconfig", "version": "20111128102912"}
        }}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "sxx": "",
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
        res = requests.post(url=url, headers=headers, data=data, verify=False)
        self.sxx = res.headers.get("sxx")

    def post_foundation_handler_two(self):
        req_time = get_time()
        url = "https://tcmobileapi.17usoft.com/foundation/foundationHandler.ashx"
        data = {"request": {
            "body": {"deviceProfile": get_device_profile(self.clientInfo.get("device")),
                     "clientInfo": self.clientInfo},
            "header": {
                "accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                "digitalSign": get_digital_sign(req_time=req_time, service_name="getclientid",
                                                version="20111128102912"),
                "reqTime": req_time,
                "serviceName": "getclientid", "version": "20111128102912"}
        }}
        data = dict_to_json(data)
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
        res = requests.post(url=url, headers=headers, data=data, verify=False)
        client_id = res.json().get("response").get("body").get("clientId")
        self.clientInfo["clientId"] = client_id

    def post_member_ship_handler_home_login(self):
        """
        执行二次登录
        :return:
        """
        req_time = get_time()
        url = "https://appgateway.ly.com/member/MembershipHandler.ashx"
        info_data = {
            "data": {"densityDpi": "240", "deviceId": self.clientInfo.get("deviceId"),
                     "heightPixels": self.clientInfo.get("device").split("|")[2].split("*")[0],
                     "manufacturer": self.clientInfo.get("manufacturer"),
                     "model": self.clientInfo.get("device").split("|")[3], "sdkInt": "22",
                     "widthPixels": self.clientInfo.get("device").split("|")[2].split("*")[1]},
            "flag": "false", "timeStamp": get_time()}
        data = {"request": {
            "body": {"isUserLogin": "0",
                     "loginName": self.params.get("token").get("loginName"),
                     "memberIdNew": self.params.get("token").get("memberIdNew"),
                     "password": get_password(self.params.get("token").get("password")),
                     "secInfo": http_do_decrypt(dict_to_json(info_data)),
                     "clientInfo": self.clientInfo,
                     "versionNo": "1"
                     },
            "header": {
                "accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                "digitalSign": get_digital_sign(req_time=req_time, service_name="HomeLogin",
                                                version="20111128102912"),
                "reqTime": req_time,
                "serviceName": "HomeLogin", "version": "20111128102912"}
        }}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|0008",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "appgateway.ly.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        res = requests.post(url=url, headers=headers, data=data, verify=False).json()
        print(res)
        if res.get("response").get("header").get("rspCode") == "0000":
            user_list = res.get("response").get("body").get("sUserList")
            try:
                self.tcunionId = user_list[0].get("unionId")
                self.userId = user_list[0].get("userId")
            except IndexError:
                self.tcunionId = ""
                self.userId = ""
            self.externalMemberId = res.get("response").get("body").get("externalMemberId")
            self.memberId = res.get("response").get("body").get("memberId")
            self.memberIdNew = res.get("response").get("body").get("memberIdNew")
            return True
        else:
            return {
                "status": 3,
                "msg": "二次登录失败"
            }

    def post_social_user_bind(self):
        """
        绑定微信
        :return:
        """
        req_time = get_time()
        url = "https://appgateway.ly.com/member/membershiphandler.ashx"
        data = {"request": {"body": {"clientInfo": self.clientInfo,
                                     "secInfo": self.get_sec_info_data(),
                                     "socialType": "4",
                                     "socialCode": "001vtL481f0qsO1BWm381Ha4581vtL43",
                                     "memberId": self.memberId},
                            "header": {"accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                                       "digitalSign": get_digital_sign(req_time=req_time, service_name="SocialUserBind",
                                                                       version="20111128102912"), "reqTime": req_time,
                                       "serviceName": "SocialUserBind", "version": "20111128102912"}}}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "sxx": self.sxx,
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|00052",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "tcmobileapi.17usoft.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        res = requests.post(url=url, headers=headers, data=data, verify=False)
        print(res.text)

    def do_bind(self):
        self.post_member_ship_handler_home_login()
        self.post_social_user_bind()


if __name__ == "__main__":
    tc = BindWeChat(params=Dict_cl)
    print(tc.do_bind())
