# encoding="utf-8"
from APP.setting import *
import urllib3
from APP.tc_code import Code
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout, ProxyError
from urllib3.exceptions import MaxRetryError, NewConnectionError
from OpenSSL.SSL import Error, WantReadError

urllib3.disable_warnings()


class ReBindWeChat(object):
    def __init__(self, params):
        self.params = params
        self.device = params.get("device")
        self.clientInfo = self.device.get("clientInfo")
        self.token = params.get("token")
        self.phone = self.token.get("loginName")
        self.memberId = self.token.get("memberId")
        self.im_ie = self.device.get("AndroidImei")
        self.sxx = self.device.get("sxx")
        self.clientId = self.device.get("clientId")
        try:
            self.socialType = int(self.token.get("sUserList")[0].get("socialType"))
        except Exception:
            self.socialType = 0
        try:
            self.tcunionId = self.token.get("sUserList")[0].get("unionId")
        except Exception:
            self.tcunionId = ""
        try:
            self.userId = self.token.get("sUserList")[0].get("userId")
        except Exception:
            self.userId = ""
        self.externalMemberId = self.token.get("externalMemberId")
        self.memberIdNew = "memberId"
        self.vxid = ""
        self.vx_token = {}
        self.usable = {"status": 1,
                       "integral": "0",
                       "vx_token": {}
                       }

        self.ua = "Mozilla/5.0 (Linux; Android 8.0.0; MI 5 Build/OPR1.170623.032; wv) AppleWebKit/537.36 (KHTML, like" \
                  " Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/7.0.13.1640(0x27000D39)" \
                  " Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64 WeChat/arm64"
        try:
            self.ip = self.params.get("proxy")
            if self.ip:
                pass
            else:
                self.ip = None
        except Exception:
            self.ip = None

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

    def post_member_ship_handler_home_login(self):
        """
        执行二次登录
        :return:
        """
        sec_info = self.do_get_sec_info_data()
        req_time = get_time()
        url = "https://appgateway.ly.com/member/MembershipHandler.ashx"
        data = {"request": {
            "body": {"isUserLogin": "0",
                     "loginName": self.params.get("token").get("loginName"),
                     "memberIdNew": self.params.get("token").get("memberIdNew"),
                     "password": get_password(self.params.get("token").get("password")),
                     "secInfo": sec_info,
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
        res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=self.ip).json()
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
                "status": 1,
                "msg": "二次登录失败"
            }

    def post_social_user_unbundling(self):
        """
        取消微信绑定
        :return:
        """
        req_time = get_time()
        url_un = "https://appgateway.ly.com/member/membershiphandler.ashx"
        data_b = {"request": {"body": {"clientInfo": self.clientInfo,
                                       "memberId": self.externalMemberId,
                                       "socialType": "4",
                                       "userId": self.userId},
                              "header": {"accountID": "c26b007f-c89e-431a-b8cc-493becbdd8a2",
                                         "digitalSign": get_digital_sign(req_time=req_time,
                                                                         service_name="SocialUserUnbundling",
                                                                         version="20111128102912"), "reqTime": req_time,
                                         "serviceName": "SocialUserUnbundling", "version": "20111128102912"}}}
        data_un = dict_to_json(data_b)
        data01 = {"body": data_un}
        headers = {
            "sxx": self.sxx,
            "secsign": get_secsign(data01),
            "secver": "4",
            "apmat": f"{self.clientInfo.get('deviceId')}|i|{get_time_stamp()}|00052",
            "reqdata": get_req_data(data_un),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "tcmobileapi.17usoft.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.2",
        }
        res_un = requests.post(url=url_un, headers=headers, data=data_un, verify=False, proxies=self.ip).json()
        if res_un.get("response").get("header").get("rspType") == "0" and \
                res_un.get("response").get("header").get("rspCode") == "0000":
            return True
        else:
            return {
                "status": 1,
                "msg": "解绑失败",
                "rspDesc": res_un.get("response").get("header").get("rspDesc")
            }

    def post_social_user_bind(self, social_code):
        """
        绑定微信
        :param social_code: app 绑定微信的code
        :return:
        """
        sec_info = self.do_get_sec_info_data()
        req_time = get_time()
        url = "https://appgateway.ly.com/member/membershiphandler.ashx"
        data = {"request": {"body": {"clientInfo": self.clientInfo,
                                     "secInfo": sec_info,
                                     "socialType": "4",
                                     "socialCode": social_code[0],
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
        res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=self.ip).json()
        print("post_social_user_bind", res)
        if res.get("response").get("header").get("rspType") == "0" and \
                res.get("response").get("header").get("rspCode") == "0000":
            # 保存同程APP授权重要参数日志
            log_wechat_author(taskid=social_code[2], app_id="3908282825", success="0",
                              vxid=social_code[4], phone=self.phone)
            return True
        elif res.get("response").get("header").get("rspType") == "1" and \
                res.get("response").get("header").get("rspCode") == "2000":
            log_wechat_author(taskid=social_code[2], app_id="3908282825", success="2",
                              vxid=social_code[4], phone=self.phone)
            return {
                "status": 1000,
                "msg": "请重新绑定微信",
                "rspDesc": res.get("response").get("header").get("rspDesc")
            }
        else:
            return {
                "status": 1,
                "msg": "绑定微信失败",
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
        res = requests.post(url=url, headers=headers, data=dict_to_json(data), verify=False, proxies=self.ip).json()
        if res.get("openId"):
            log_wechat_author(taskid=vx_code[2], app_id="3117146270", success="0", vxid=vx_code[3], phone=self.phone)
            self.vx_token = res
        else:
            log_wechat_author(taskid=vx_code[2], app_id="3117146270", success="2", vxid=vx_code[3], phone=self.phone)
            return {
                "status": 1,
                "msg": "绑定微信成功，获取微信token失败",
            }

    def get_social_code(self):
        """
        获取微信code
        :return:
        """
        code = Code()
        res_code = code.do_get_tc_app_code()
        if isinstance(res_code, dict):
            return res_code
        print(" res_code:", res_code)
        res = self.post_social_user_bind(social_code=res_code)
        if isinstance(res, dict):
            return res
        print("vxid:", self.vxid)
        res_vx = code.do_get_tc_wechat_code(vxid=self.vxid)
        if isinstance(res_vx, dict):
            return res_vx
        print("微信授权code:", res_vx)
        res = self.app_wx_user(vx_code=res_vx)
        if isinstance(res, dict):
            return res
        return True

    def do_try_get_social_code(self):
        """
        :return:
        """
        while True:
            res = self.get_social_code()
            print("是否授权成功:", res)
            if isinstance(res, dict):
                if res.get("status") == 1000:
                    continue
                else:
                    return res
            return True

    def do_rebind(self):
        try:
            res = self.post_member_ship_handler_home_login()
            if isinstance(res, dict):
                return res
            if self.userId and self.socialType == 4:
                res = self.post_social_user_unbundling()
                if isinstance(res, dict):
                    return res
                print("解绑成功：", res)
                time.sleep(5)
            res = perform_first_sign_in(data=self.params)
            print("里程数:", res)
            if isinstance(res, dict):
                pass
            else:
                self.usable["integral"] = int(res)
            res = self.do_try_get_social_code()
            if isinstance(res, dict):
                res["msg"] = "登录成功，" + res["msg"]
                return res
            self.vx_token["vxid"] = self.vxid
            self.usable["vx_token"] = self.vx_token
            self.usable["status"] = 0
            return self.usable
        except (
                ConnectionError, ConnectTimeout, ReadTimeout, ProxyError, Error, WantReadError, MaxRetryError,
                NewConnectionError):
            ret = {'status': 11, 'msg': "请换ip"}
            return ret

    def do_do_rebind(self):
        i = 0
        while i <= 3:
            res = self.do_rebind()
            if res.get("status") == 11:
                i += 1
                time.sleep(1)
                ip_res = get_zhima_ip()
                if ip_res.get("status") == 30:
                    i += 1
                ip = {
                    "http": ip_res.get("http"),
                    "https": ip_res.get("https"),
                }
                self.ip = ip
            else:
                return res
        else:
            return {'status': 3, 'msg': "ip失效，已切换ip重试3次"}

    def do_rebind_one(self):
        """
        未绑定的账号绑定微信；
        绑定的重新绑定微信
        :return:
        """
        res = self.post_member_ship_handler_home_login()
        if isinstance(res, dict):
            return res
        if self.userId and self.socialType == 4:
            res = self.post_social_user_unbundling()
            if isinstance(res, dict):
                return res
            print("解绑成功：", res)
            time.sleep(5)
        licheng = perform_first_sign_in(data=self.params)
        print("里程数:", licheng)
        if isinstance(licheng, dict):
            licheng = 0
        res = self.do_try_get_social_code()
        print("授权是否成功：", res)
        if isinstance(res, dict):
            res["msg"] = "登录成功，" + res["msg"]
            return res
        self.vx_token["vxid"] = self.vxid
        print(self.vxid)
        vx_token = self.vx_token
        return vx_token, licheng


if __name__ == "__main__":
    L = {}
    Lw = ReBindWeChat(params=L)
    Lw.do_rebind()
