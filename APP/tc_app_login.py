# encoding="utf-8"
from APP.setting import *
import requests
import urllib3
import random
from APP.tc_code import Code
import traceback
from tc_app_log.Journal_class import Journal
from APP.RedisProxyClient import RedisClientClass
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout, ProxyError
from urllib3.exceptions import MaxRetryError, NewConnectionError
from OpenSSL.SSL import Error, WantReadError

urllib3.disable_warnings()


class Login(object):
    def __init__(self, params, ip):
        self.ip = ip
        self.clientInfo = get_device_info()
        self.user = params.get("user")
        self.password = params.get("password")
        self.loginName = f'+86 {self.user}'
        self.im_ie = random.choice(Android)
        self.sxx = ""
        self.client_id = ""
        self.token = {}
        self.usable = {}
        self.vxid = ""
        self.pwd = ""
        self.vx_token = {}
        self.memberId = ""
        self.ua = "Mozilla/5.0 (Linux; Android 8.0.0; MI 5 Build/OPR1.170623.032; wv) AppleWebKit/537.36 " \
                  "(KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/7.0." \
                  "13.1640(0x27000D39) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64 WeChat/arm64"

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
        res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=self.ip)
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
        res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=self.ip)
        client_id = res.json().get("response").get("body").get("clientId")
        self.clientInfo["clientId"] = client_id

    def post_location_handler_login_pwd(self, pwd):
        """
        :param pwd:
        :return:
        """
        secInfo = self.do_get_sec_info_data()
        req_time = get_time()
        url = "https://appgateway.ly.com/member/MembershipHandler.ashx"
        data = {"request": {
            "body": {"isUserLogin": "1",
                     "secInfo": secInfo,
                     "clientInfo": self.clientInfo,
                     "rawText": do_raw_text(self.user, pwd)},
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
        req_json = requests.post(url=url, headers=headers, data=data, verify=False, proxies=self.ip).json()
        print("登录返回数据：", req_json)
        if req_json['response']['header']['rspCode'] == "5587":
            return {'status': 302, 'msg': f"{req_json['response']['header']['rspDesc']}'出现短信验证码'"}
        elif req_json['response']['header']['rspCode'] == "3001":
            return {'status': 300, 'msg': f"{req_json['response']['header']['rspDesc']}' 密码错误"}
        elif req_json['response']['header']['rspCode'] == '0000':
            self.token = req_json.get("response").get("body")
            self.memberId = self.token.get("memberId")
            self.pwd = pwd
            if req_json.get("response").get("body").get("sUserList"):
                return True
            else:
                return {
                    "status": 3,
                    "msg": "该账号未绑定",
                }
        else:
            return {'status': 300, 'msg': f"{req_json['response']['header']['rspDesc']}' 密码错误"}

    def post_location_handler_login(self):
        secInfo = self.do_get_sec_info_data()
        req_time = get_time()
        url = "https://appgateway.ly.com/member/MembershipHandler.ashx"
        data = {"request": {
            "body": {"isUserLogin": "1",
                     "secInfo": secInfo,
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
        print("登录返回数据：", req_json)
        if req_json['response']['header']['rspCode'] == "5587":
            return {'status': 302, 'msg': f"{req_json['response']['header']['rspDesc']}'出现短信验证码'"}
        elif req_json['response']['header']['rspCode'] == "3001":
            return {'status': 300, 'msg': f"{req_json['response']['header']['rspDesc']}' 密码错误"}
        elif req_json['response']['header']['rspCode'] == '0000':
            self.token = req_json.get("response").get("body")
            self.memberId = self.token.get("memberId")
            if req_json.get("response").get("body").get("sUserList"):
                return {
                    "status": 3,
                    "msg": "该账号已绑定",
                }
        else:
            return {
                "status": 3,
                "msg": "登录失败"
            }

    def post_social_user_bind(self, social_code):
        """
        绑定微信
        :param social_code: app 绑定微信的code
        :return:
        """
        req_time = get_time()
        url = "https://appgateway.ly.com/member/membershiphandler.ashx"
        data = {"request": {"body": {"clientInfo": self.clientInfo,
                                     "secInfo": self.get_sec_info_data(),
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
                "msg": "登录成功，绑定微信失败",
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
                "msg": "登录成功，绑定微信成功，获取微信token失败",
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
        req_time = get_time()
        url = "https://appgateway.ly.com/member/MembershipHandler.ashx"
        data = {"request": {
            "body": {"mobile": self.loginName,
                     "secInfo": self.get_sec_info_data(),
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
            if req_json.get("response").get("body").get("sUserList"):
                return {
                    "status": 0,
                    "msg": "登录成功",
                }
            else:
                return {
                    "status": 3,
                    "msg": "该账号已绑定",
                }
        else:
            return {
                "status": 3,
                "msg": "短信登录失败，请重新尝试登录",
                "rspDesc": req_json.get("response").get("header").get("rspDesc")
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

    def do_login_retry(self):
        """
        密码错误重新登录
        :return:
        """
        for pwd in Pwd:
            self.post_foundation_handler_one()
            self.post_foundation_handler_two()
            res = self.post_location_handler_login_pwd(pwd=pwd)
            if isinstance(res, dict):
                if res.get("status") == 300:
                    continue
                else:
                    return res
            else:
                return True
        else:
            return {
                "status": 3,
                "msg": "登录失败,三个密码重试完成，依然失败"
            }

    def do_login(self):
        try:
            self.post_foundation_handler_one()
            self.post_foundation_handler_two()
            res = self.post_location_handler_login()
            if isinstance(res, dict):
                res["index"] = "post_location_handler_login"
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
                return res
            self.vx_token["vxid"] = self.vxid
            self.usable["vx_token"] = self.vx_token
            return self.usable

        finally:
            res = self.do_login_save()
            print(res)

    def do_login_save(self):
        """
        将注册成功的推送到
        :return:
        """
        if self.usable:
            url = "http://192.168.0.47:12004/regsave.do"
            data = self.usable
            res = requests.post(url=url, json=data)
            if res.text == "OK":
                return {
                    "status": 0,
                    "msg": "登录成功，并存储成功"
                }
            else:
                return {
                    "status": 1,
                    "msg": "登录成功，并存储失败",
                    "Remark": res.text
                }
        else:
            return {
                "status": 1,
                "msg": "未绑定微信",
            }

    def do_login_by_one(self):
        try:
            res = self.do_login_retry()
            if isinstance(res, dict):
                res["index"] = "do_login_retry"
                return res
            self.usable = {
                "status": 0,
                "phone": self.user,
                "pwd": self.pwd,
                "user_type": "2",
                "device": {
                    "clientInfo": self.clientInfo,
                    "AndroidImei": self.im_ie,
                    "sxx": self.sxx,
                    "clientId": self.client_id,
                },  # 设备参数及其他重要值
                "token": self.token,  # 用于二次登录的重要 token
                "proxy": self.ip,  # 代理IP
                "vx_token": {},
                "integral": 0
            }
            res = perform_get_integral(data=self.usable)
            if isinstance(res, dict):
                pass
            else:
                self.usable["integral"] = int(res)
            print(self.usable)
            return self.usable
        finally:
            self.do_login_save()
            # print(res)

    def do_login_by_code(self):
        self.post_foundation_handler_one()
        self.post_foundation_handler_two()
        res = self.post_location_handler_login()
        print(res)
        if isinstance(res, dict):
            if res.get("status") == 302:
                print("ssss")
                res_l = self.post_get_login_dynamic_code()
                if isinstance(res_l, dict):
                    return res_l
                v = input("请输入短信验证码：")
                return self.post_login_by_dynamic_code(verify_code=v)
            else:
                return res
        return res


def do_login_log(data):
    try:
        ret = Login(params=data).do_login()
        resp = {
            "登录信息": data,
            "返回信息": ret
        }
        Journal().save_journal_login(massage=json.dumps(resp))
    except Exception:
        ret = {'status': 500, 'msg': traceback.format_exc()}
        resp = {
            "登录信息": data,
            "响应数据": ret
        }
        Journal().save_journal_login(massage=json.dumps(resp), level="error")
    return json.dumps(ret)


def do_login_one():
    """
    使用账号登录
    :param data:
    :return:
    """
    ip_res = get_zhima_ip()
    if ip_res.get("status") == 30:
        return ip_res
    ip = {
        "http": ip_res.get("http"),
        "https": ip_res.get("https"),
    }
    res_r = RedisClientClass().s_data_all("TC_account")
    if len(res_r) == 0:
        return {
            "status": 3000,
            "msg": "无添加账号可以使用"
        }
    for data in res_r:
        print(data)
        param = {
            "user": data
        }
        try:
            ret = Login(params=param, ip=ip).do_login_by_one()
            resp = {
                "登录账号": data,
                "返回信息": ret
            }
            RedisClientClass().srem_delete("TC_account", data)
            Journal().save_journal_login(massage=json.dumps(resp))
        except (
                ConnectionError, ConnectTimeout, ReadTimeout, ProxyError, Error, WantReadError, MaxRetryError,
                NewConnectionError):
            ret = {'status': 11, 'msg': "请换ip"}
            return ret
        except Exception:
            ret = {'status': 500, 'msg': traceback.format_exc()}
            resp = {
                "登录信息": data,
                "响应数据": ret
            }
            Journal().save_journal_login(massage=json.dumps(resp), level="error")
            return ret


if __name__ == "__main__":
    pass
    # while True:
    #     res_01 = do_login_one()
    #     if res_01.get("status") == 3000:
    #         break
