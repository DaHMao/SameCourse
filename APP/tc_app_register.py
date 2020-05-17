# --coding:utf-8--
from APP.setting import *
from APP.tc_rebind_wechat import ReBindWeChat
import requests
import urllib3
import random
from APP.tc_code import Code
from tc_app_log.Journal_class import Journal
import traceback
from APP.get_number_verfication_code_by_bm import GetNumberCodeByBM

urllib3.disable_warnings()


def random_password():
    """
    生成随机账号密码
    :return:
    """
    pwd_1 = 'abcdefghijklmnopqrstuvwxyz'
    pwd_2 = "0123456789@"
    pwd = ''.join(random.choices(pwd_1, k=6)) + "@" + ''.join(random.choices(pwd_2, k=4))
    return pwd


class Register(object):
    def __init__(self, params):
        self.clientInfo = get_device_info()
        self.user = params.get("user")
        self.password = params.get("password")
        self.loginName = f'+86 {self.user}'
        print(self.loginName)
        self.pwd = get_password(password=self.password)
        self.im_ie = random.choice(Android)
        self.sxx = ""
        self.client_id = ""
        self.token = {}
        self.usable = {}
        self.vx_token = {}
        self.memberId = ""
        self.vxid = ""
        self.ua = "Mozilla/5.0 (Linux; Android 8.0.0; MI 5 Build/OPR1.170623.032; wv) AppleWebKit/537.36 (KHTML, like" \
                  " Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/7.0.13.1640(0x27000D39)" \
                  " Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64 WeChat/arm64"

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
        res = http_do_decrypt(s=dict_to_json(info_data))
        if isinstance(res, dict):
            return res
        return res

    def do_get_sec_info_data(self):
        """
        :return:
        """
        while True:
            res = self.get_sec_info_data()
            if isinstance(res, str):
                return res
            time.sleep(5)

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
        self.client_id = res.json().get("response").get("body").get("clientId")
        self.clientInfo["clientId"] = self.client_id

    def post_member_ship_handler_check_mobile_register(self):
        """
        注册检验账号
        :return:
        """
        req_time = get_time()
        url = "https://appgateway.ly.com/member/membershiphandler.ashx"
        data = {"request": {
            "body": {"clientInfo": self.clientInfo,
                     "mobile": self.loginName},
            "header": {
                "accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                "digitalSign": get_digital_sign(req_time=req_time, service_name="CheckMobileRegister",
                                                version="20111128102912"),
                "reqTime": req_time,
                "serviceName": "CheckMobileRegister", "version": "20111128102912"}
        }}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "sxx": self.sxx,
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|00002",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            # "Content-Length": "744",
            "Host": "tcmobileapi.17usoft.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        res = requests.post(url=url, headers=headers, data=data, verify=False).json()
        if res.get("response").get("header").get("rspDesc") == "未注册过":
            return {
                "status": 1,
                "msg": "该账号未注册",
            }
        elif res.get("response").get("header").get("rspDesc") == "已注册过":
            return {
                "status": 0,
                "msg": "该账号已注册",
            }
        else:
            return {
                "status": 3,
                "msg": res.get("response").get("header").get("rspDesc")
            }

    def post_member_ship_handler_check_black_list(self):
        """
        检测该账号是否是黑名单
        :return:
        """
        url = "https://appgateway.ly.com/member/membershiphandler.ashx"
        req_time = get_time()
        data = {"request": {
            "body": {"clientInfo": self.clientInfo,
                     "mobile": self.loginName},
            "header": {
                "accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                "digitalSign": get_digital_sign(req_time=req_time, service_name="checkblacklist",
                                                version="20111128102912"),
                "reqTime": req_time,
                "serviceName": "checkblacklist", "version": "20111128102912"}
        }}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "sxx": self.sxx,
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|00003",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            # "Content-Length": "744",
            "Host": "tcmobileapi.17usoft.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        res = requests.post(url=url, headers=headers, data=data, verify=False).json()
        if res.get("response").get("header").get("rspDesc") == "未命中黑名单":
            return True
        else:
            return {
                "status": 3,
                "msg": "该账号为黑名单",
                "rspDesc": res.get("response").get("header").get("rspDesc")
            }

    def post_member_ship_handler_get_verification_code_register(self):
        """
        账号获取短信验证码
        :return:
        """
        url = "https://appgateway.ly.com/member/membershiphandler.ashx"
        req_time = get_time()
        data = {"request": {
            "body": {"clientInfo": self.clientInfo,
                     "mobile": self.loginName},
            "header": {
                "accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                "digitalSign": get_digital_sign(req_time=req_time, service_name="getverificationcoderegister",
                                                version="20111128102912"),
                "reqTime": req_time,
                "serviceName": "getverificationcoderegister", "version": "20111128102912"}
        }}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "sxx": self.sxx,
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|00004",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            # "Content-Length": "744",
            "Host": "tcmobileapi.17usoft.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        res = requests.post(url=url, headers=headers, data=data, verify=False).json()
        print(res)
        if res.get("response").get("header").get("rspDesc") == "获取成功":
            return True
        else:
            return {
                "status": 3,
                "msg": "发送验证失败",
                "rspDesc": res.get("response").get("header").get("rspDesc")
            }

    def post_member_ship_handler_register_v2(self, verify_code):
        """
        注册账号
        :return:
        """
        sec_info = self.do_get_sec_info_data()
        url = "https://appgateway.ly.com/member/membershiphandler.ashx"
        req_time = get_time()
        data = {"request": {
            "body": {"clientInfo": self.clientInfo,
                     "loginName": self.loginName,
                     "password": self.pwd,
                     "androidId": self.clientInfo.get("deviceId"),
                     "secInfo": sec_info,
                     "androidImei": self.im_ie,
                     "verifyCode": verify_code,
                     "verifyCodeType": "0"
                     },
            "header": {
                "accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                "digitalSign": get_digital_sign(req_time=req_time, service_name="RegisterV2",
                                                version="20111128102912"),
                "reqTime": req_time,
                "serviceName": "RegisterV2", "version": "20111128102912"}
        }}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "sxx": self.sxx,
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|0005",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "tcmobileapi.17usoft.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        res = requests.post(url=url, headers=headers, data=data, verify=False).json()
        print("res", res)
        if res.get("response").get("header").get("rspDesc") == "注册成功":
            self.token = res.get("response").get("body")
            self.memberId = self.token.get("memberId")
        else:
            return {
                "status": 3,
                "msg": "注册失败",
                "rspDesc": res.get("response").get("header").get("rspDesc")
            }

    def post_social_user_bind(self, social_code):
        """
        绑定微信
        :param social_code: app 绑定微信的code
        :return:
        """
        req_time = get_time()
        sec_info = self.do_get_sec_info_data()
        url = "https://appgateway.ly.com/member/membershiphandler.ashx"
        data = {"request": {"body": {"clientInfo": self.clientInfo,
                                     "secInfo": sec_info,
                                     "socialType": "4",
                                     "socialCode": social_code,
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
        res = requests.post(url=url, headers=headers, data=data, verify=False).json()
        print("post_social_user_bind", res)
        if res.get("response").get("header").get("rspType") == "0" and \
                res.get("response").get("header").get("rspCode") == "0000":
            return True
        else:
            return {
                "status": 3,
                "msg": "注册成功，绑定微信失败",
                "rspDesc": res.get("response").get("header").get("rspDesc")
            }

    def app_wx_user(self, vx_code):
        """
         微信登录同程小程序，获取token
        :param vx_code 微信返回的code
        :return:
        """
        url = "https://wx.17u.cn/appapi/wxuser/login/2"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "56",
            "charset": "utf-8",
            "User-Agent": self.ua,
            "content-type": "application/json",
            "Accept-Encoding": "gzip,compress,br,deflate",
        }
        data = {"code": vx_code, "scene": 1019}
        res = requests.post(url=url, headers=headers, data=dict_to_json(data), verify=False).json()
        if res.get("openId"):
            self.vx_token = res
        else:
            return {
                "status": 3,
                "msg": "注册成功，绑定微信成功，获取微信token失败",
            }

    def get_social_code(self):
        """
        获取微信code
        :return:
        """
        code = Code()
        res = code.do_get_tc_app_code()
        if isinstance(res, dict):
            return res
        social_code = res[0]
        self.vxid = res[1]
        print("social_code:", social_code)
        # social_code = input("请输入code:")
        res = self.post_social_user_bind(social_code=social_code)
        if isinstance(res, dict):
            return res
        print("vxid:", self.vxid)
        res_vx = code.do_get_tc_wechat_code(vxid=self.vxid)
        if isinstance(res_vx, dict):
            return res_vx
        vx_code = res_vx[0]
        print("vx_code:", vx_code)
        res = self.app_wx_user(vx_code=vx_code)
        if isinstance(res, dict):
            return res
        return True

    def post_get_verification_code(self):
        """
        修改密码获取验证码请求
        :return:
        """
        url = "https://appgateway.ly.com/member/membershiphandler.ashx"
        req_time = get_time()
        data = {"request": {
            "body": {"clientInfo": self.clientInfo,
                     "mobile": self.loginName,
                     },
            "header": {
                "accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                "digitalSign": get_digital_sign(req_time=req_time, service_name="GetVerificationCode",
                                                version="20111128102912"),
                "reqTime": req_time,
                "serviceName": "GetVerificationCode", "version": "20111128102912"}
        }}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "sxx": self.sxx,
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|0003",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "tcmobileapi.17usoft.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        res = requests.post(url=url, headers=headers, data=data, verify=False).json()
        if res.get("response").get("header").get("rspDesc") == "获取成功":
            return True
        else:
            return {
                "status": 3,
                "msg": "发送验证失败",
                "rspDesc": res.get("response").get("header").get("rspDesc")
            }

    def post_confirm_verification_code_member(self, verfy_code):
        """
        发起修改验证码请求
        :param verfy_code:
        :return:
        """
        url = "https://appgateway.ly.com/member/membershiphandler.ashx"
        req_time = get_time()
        data = {"request": {
            "body": {"clientInfo": self.clientInfo,
                     "isReturnPwd": "1",
                     "mobile": self.loginName,
                     "verifyCode": verfy_code,
                     },
            "header": {
                "accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                "digitalSign": get_digital_sign(req_time=req_time, service_name="confirmverificationcodemember",
                                                version="20111128102912"),
                "reqTime": req_time,
                "serviceName": "confirmverificationcodemember", "version": "20111128102912"}
        }}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "sxx": self.sxx,
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|0000",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "tcmobileapi.17usoft.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        res = requests.post(url=url, headers=headers, data=data, verify=False).json()
        if res.get("response").get("header").get("rspDesc") == "确认成功":
            return True
        else:
            return {
                "status": 3,
                "msg": "修改验证码确认失败",
                "rspDesc": res.get("response").get("header").get("rspDesc")
            }

    def post_update_password_without_original(self, verfy_code):
        """
        修改密码提交请求
        :param verfy_code:
        :return:
        """
        url = "https://appgateway.ly.com/member/membershiphandler.ashx"
        req_time = get_time()
        data = {"request": {
            "body": {"clientInfo": self.clientInfo,
                     "newPassword": self.password,
                     "mobile": self.loginName,
                     "verifyCode": verfy_code,
                     },
            "header": {
                "accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                "digitalSign": get_digital_sign(req_time=req_time, service_name="UpdatePasswordWithoutOriginal",
                                                version="20111128102912"),
                "reqTime": req_time,
                "serviceName": "UpdatePasswordWithoutOriginal", "version": "20111128102912"}
        }}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "sxx": self.sxx,
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|0002",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "tcmobileapi.17usoft.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        res = requests.post(url=url, headers=headers, data=data, verify=False).json()
        if res.get("response").get("header").get("rspDesc") == "修改成功":
            return {
                "status": 0,
                "msg": "修改密码成功",
            }
        else:
            return {
                "status": 3,
                "msg": "修改密码失败",
                "rspDesc": res.get("response").get("header").get("rspDesc")
            }

    def post_location_handler_login(self):
        """执行登录"""
        sec_info = self.do_get_sec_info_data()
        req_time = get_time()
        url = "https://appgateway.ly.com/member/MembershipHandler.ashx"
        data = {"request": {
            "body": {"isUserLogin": "1",
                     "secInfo": sec_info,
                     "clientInfo": self.clientInfo,
                     "rawText": do_raw_text(self.user, self.password)},
            "header": {"accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                       "digitalSign": get_digital_sign(req_time=req_time, service_name="Loginv3",
                                                       version="20111128102912"), "reqTime": req_time,
                       "serviceName": "Loginv3", "version": "20111128102912"}}}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "sxx": self.sxx,
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|00005",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "tcmobileapi.17usoft.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        req_json = requests.post(url=url, headers=headers, data=data, verify=False).json()
        if req_json['response']['header']['rspCode'] == "5587":
            return {'status': 302, 'msg': f"{req_json['response']['header']['rspDesc']}'出现短信验证码'"}
        elif req_json['response']['header']['rspCode'] == "3001":
            return {'status': 300, 'msg': f"{req_json['response']['header']['rspDesc']}' 密码错误"}
        elif req_json['response']['header']['rspCode'] == '0000':
            self.token = req_json.get("response").get("body")
            self.memberId = self.token.get("memberId")
            return {
                "status": 0,
                "msg": "登录成功"
            }
        else:
            return {
                "status": 3,
                "msg": "登录失败"
            }

    def post_get_login_dynamic_code(self):
        """
        获取登录短信验证码
        :return:
        """
        url = "https://appgateway.ly.com/member/MembershipHandler.ashx"
        req_time = get_time()
        data = {"request": {"body": {"clientInfo": self.clientInfo,
                                     "mobile": self.loginName},
                            "header": {"accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                                       "digitalSign": get_digital_sign(req_time=req_time,
                                                                       service_name="getlogindynamiccode",
                                                                       version="20111128102912"), "reqTime": req_time,
                                       "serviceName": "getlogindynamiccode", "version": "20111128102912"}}}
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
        res = requests.post(url=url, headers=headers, data=data, verify=False).json()
        if res.get("response").get("header").get("rspType") == "0" and \
                res.get("response").get("header").get("rspCode") == "0000":
            return True
        else:
            return {
                "status": 3,
                "msg": "登录获取短信验证码失败",
                "rspDesc": res.get("response").get("header").get("rspDesc")
            }

    def post_login_by_dynamic_code(self, verify_code):
        """
        使用验证码登录
        :return:
        """
        sec_info = self.do_get_sec_info_data()
        req_time = get_time()
        url = "https://appgateway.ly.com/member/MembershipHandler.ashx"
        data = {"request": {
            "body": {"mobile": self.loginName,
                     "secInfo": sec_info,
                     "clientInfo": self.clientInfo,
                     "verifyCode": verify_code
                     },
            "header": {"accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                       "digitalSign": get_digital_sign(req_time=req_time, service_name="loginbydynamiccode",
                                                       version="20111128102912"), "reqTime": req_time,
                       "serviceName": "loginbydynamiccode", "version": "20111128102912"}}}
        data = dict_to_json(data)
        data01 = {"body": data}
        headers = {
            "sxx": self.sxx,
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|00002",
            "reqdata": get_req_data(data),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "tcmobileapi.17usoft.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        req_json = requests.post(url=url, headers=headers, data=data, verify=False).json()
        if req_json.get("response").get("header").get("rspType") == "0" and \
                req_json.get("response").get("header").get("rspCode") == "0000":
            print("登陆成功")
            self.token = req_json.get("response").get("body")
            self.memberId = self.token.get("memberId")
        else:
            return {
                "status": 3,
                "msg": "短信登录失败，请重新尝试登录",
                "rspDesc": req_json.get("response").get("header").get("rspDesc")
            }

    def do_register_one(self):
        """
        账号注册
        :return:
        """
        try:
            self.post_foundation_handler_one()
            self.post_foundation_handler_two()
            res = self.post_member_ship_handler_check_mobile_register()
            if isinstance(res, dict):
                res["index"] = "post_member_ship_handler_check_mobile_register"
                return res
            res = self.post_member_ship_handler_get_verification_code_register()
            if isinstance(res, dict):
                res["index"] = "post_member_ship_handler_get_verification_code_register"
                return res
            v = input("请输入验证短信验证码：")
            res = self.post_member_ship_handler_register_v2(verify_code=v)
            if isinstance(res, dict):
                res["index"] = "post_member_ship_handler_register_v2"
                return res
            self.usable = {
                "status": 0,
                "phone": self.user,
                "pwd": self.password,
                "user_type": "0",
                "device": {
                    "clientInfo": self.clientInfo,
                    "AndroidImei": self.im_ie,
                    "sxx": self.sxx,
                    "clientId": self.client_id,
                },  # 设备参数及其他重要值
                "token": self.token,  # 用于二次登录的重要 token
                "proxy": "",  # 代理IP
                "vx_token": {},
                "integral": 0
            }
            res = perform_first_sign_in(data=self.usable)
            if isinstance(res, dict):
                pass
            else:
                self.usable["integral"] = int(res)
            res = self.get_social_code()
            if isinstance(res, dict):
                res["msg"] = "微信注册成功，" + res["msg"]
                return res
            self.vx_token["vxid"] = self.vxid
            self.usable["vx_token"] = self.vx_token
            return self.usable
        finally:
            res = self.do_register_save()
            print(res)

    def do_register_two(self):
        """
        账号注册,如果遇到已经注册过的账号修改密码
        :return:
        """
        try:
            self.post_foundation_handler_one()
            self.post_foundation_handler_two()
            res = self.post_member_ship_handler_check_mobile_register()
            print("是否注册:", res)
            if res.get("status") == 0:
                print("该号已注册，执行修改密码")
                res_1 = self.post_get_verification_code()
                if isinstance(res_1, dict):
                    res_1["index"] = "post_get_verification_code"
                    return res_1
                code = GetNumberCodeByBM(aip_token).do_get_phone_message(phone=self.user)
                if isinstance(code, dict):
                    code["index"] = "do_get_phone_message"
                    return code
                print("修改密码的验证码：", code)
                res_2 = self.post_confirm_verification_code_member(verfy_code=code)
                if isinstance(res_2, dict):
                    res_2["index"] = "post_update_password_without_original"
                    return res_2
                res_3 = self.post_update_password_without_original(verfy_code=code)
                print("修改密码：", res_3)
                if res_3.get("status") == 3:
                    res_3["index"] = "post_update_password_without_original"
                    return res_3
                else:
                    res_4 = self.post_location_handler_login()
                    print("执行登录:", res_4)
                    if res_4.get("status") == 302:
                        print("登录时出现验证码")
                        res_l1 = self.post_get_login_dynamic_code()
                        if isinstance(res_l1, dict):
                            res_l1["index"] = "post_get_login_dynamic_code"
                            return res_l1
                        v_code = GetNumberCodeByBM(aip_token).do_get_phone_message(phone=self.user)
                        if isinstance(v_code, dict):
                            v_code["index"] = "do_get_phone_message_two"
                            return v_code
                        res_5 = self.post_login_by_dynamic_code(verify_code=v_code)
                        if isinstance(res_5, dict):
                            res_5["index"] = "post_login_by_dynamic_code"
                            return res_5
                        print("使用验证码登录成功")
                    elif res_4.get("status") == 0:
                        print("登录成功未出现验证码")
                        pass
                    else:
                        return res_4
                    self.usable = {
                        "status": 0,
                        "phone": self.user,
                        "pwd": self.password,
                        "user_type": "0",
                        "device": {
                            "clientInfo": self.clientInfo,
                            "AndroidImei": self.im_ie,
                            "sxx": self.sxx,
                            "clientId": self.client_id,
                        },  # 设备参数及其他重要值
                        "token": self.token,  # 用于二次登录的重要 token
                        "proxy": {},  # 代理IP
                        "vx_token": {},
                        "integral": 0
                    }
                    res_6 = perform_get_integral(data=self.usable)
                    print("未解绑时的里程:", res_6)
                    if isinstance(res_6, dict):
                        return res_6
                    elif int(res_6) < 200:
                        rebind = ReBindWeChat(params=self.usable)
                        res_7 = rebind.do_rebind_one()
                        print(res_7)
                        if isinstance(res_7, tuple):
                            self.usable["vx_token"] = res_7[0]
                            self.usable["integral"] = int(res_7[1])
                            return self.usable
                        else:
                            return res_7
                    else:
                        print("里程数大于200，直接保持账号")
                        self.usable["integral"] = int(res_6)
                        self.usable["user_type"] = "2"
                        return self.usable
            elif res.get("status") == 1:
                print("该号未注册")
                res = self.post_member_ship_handler_get_verification_code_register()
                if isinstance(res, dict):
                    res["index"] = "post_member_ship_handler_get_verification_code_register"
                    return res
                v = GetNumberCodeByBM(aip_token).do_get_phone_message(phone=self.user)
                if isinstance(v, dict):
                    return v
                res = self.post_member_ship_handler_register_v2(verify_code=v)
                if isinstance(res, dict):
                    res["index"] = "post_member_ship_handler_register_v2"
                    return res
                self.usable = {
                    "status": 0,
                    "phone": self.user,
                    "pwd": self.password,
                    "user_type": "0",
                    "device": {
                        "clientInfo": self.clientInfo,
                        "AndroidImei": self.im_ie,
                        "sxx": self.sxx,
                        "clientId": self.client_id,
                    },  # 设备参数及其他重要值
                    "token": self.token,  # 用于二次登录的重要 token
                    "proxy": {},  # 代理IP
                    "vx_token": {},
                    "integral": 0
                }
                rebind = ReBindWeChat(params=self.usable)
                res_7 = rebind.do_rebind_one()
                print(res_7)
                if isinstance(res_7, tuple):
                    self.usable["vx_token"] = res_7[0]
                    self.usable["integral"] = int(res_7[1])
                    return self.usable
                else:
                    return res_7
            else:
                res["index"] = "post_member_ship_handler_check_mobile_register"
                return res
        finally:
            res = self.do_register_save()
            print("ok")

    def do_register_save(self):
        """
        将注册成功的推送到
        :return:
        """
        if self.usable.get("token"):
            url = URL + "/regsave.do"
            data = self.usable
            res = requests.post(url=url, json=data)
            if res.text == "OK":
                return {
                    "status": 0,
                    "msg": "注册成功，并存储成功"
                }
            else:
                return {
                    "status": 1,
                    "msg": "注册成功，并存储失败",
                    "Remark": res.text
                }
        else:
            return {
                "status": 1,
                "msg": "注册失败",
            }


def do_register_log():
    pwd = random_password()
    phone = GetNumberCodeByBM(aip_token).do_get_phone_number()
    if isinstance(phone, dict):
        return phone
    res_phone = get_get_user_do(phone=phone)
    if res_phone.get("status") in (0, 2):
        return {
            "status": 1,
            "msg": "该账号已存在账号中心",
        }
    data = {
        "user": phone,
        "password": pwd
    }
    print(data)
    try:
        ret = Register(params=data).do_register_two()
        print(ret)
        resp = {
            "注册信息": data,
            "返回信息": ret
        }
        Journal().save_journal_register(massage=json.dumps(resp))
    except Exception:
        ret = {'status': 500, 'msg': traceback.format_exc()}
        resp = {
            "注册信息": data,
            "响应数据": ret
        }
        Journal().save_journal_register(massage=json.dumps(resp), level="error")
    return json.dumps(ret)


if __name__ == "__main__":
    ress = do_register_log()
