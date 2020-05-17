import requests
from wechat.setting import *
import urllib3

urllib3.disable_warnings()


class TCWechat(object):
    def __init__(self):
        self.ua = "Mozilla/5.0 (Linux; Android 8.0.0; MI 5 Build/OPR1.170623.032; wv) AppleWebKit/537.36 (KHTML, like" \
                  " Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/7.0.13.1640(0x27000D39)" \
                  " Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64 WeChat/arm64"
        self.sectoken = "ZfOeS2YX9IStsHx-3-C4u30F3PfCwHKcIPlDYfyVNImDrkDXoj7IAeg6xwKtgteLsPBu6w7o7FbdR8ooeUUHCNKh9q13Z1nys2M8NRj-MyrAD4-9TEFHZhRwldnGyjaPxyLOsRIgSJ952GtJIj3xL2d02mG6wi4O_zFTYZHepi4q3T4__oeb43_8FgiaIfwn4641"
        self.openId = "o498X0TWrMMRUq4KlzRRSsOj3p5E"
        self.unionId = "ohmdTtzyKbyp9mq54bCSfGTuiPDk"
        self.memberId = ""

    def app_wx_user(self, code):
        """
         微信登录同程小程序，获取token
        :param code: 微信返回的code
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
        data = {"code": code, "scene": 1019}
        res = requests.post(url=url, headers=headers, data=dict_to_json(data), verify=False).json()
        self.sectoken = res.get("sectoken")
        self.openId = res.get("openId")
        self.unionId = res.get("unionId")
        self.memberId = res.get("memberId")

    def post_send_message(self):
        """
        发送短信验证码
        :return:
        """
        url_send = "https://wx.17u.cn/xcxpubapi/pubmember/sendmessge"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "105",
            "charset": "utf-8",
            "wxapp": "0",
            "User-Agent": self.ua,
            "apmat": f"{self.openId}|{get_time_stamp()}|{get_random_stamp()}",
            "content-type": "application/json",
            "sectoken": self.sectoken,
            "Accept-Encoding": "gzip,compress,br,deflate",
        }
        data = {"openId": self.openId, "unionId": self.unionId,
                "mobile": "18223791767"}
        res = requests.post(url=url_send, headers=headers, data=dict_to_json(data), verify=False).json()
        if res.get("RspCode") == 0 and res.get("Message") == "查询成功":
            print(res)
            pass
        else:
            return {
                "status": 3,
                "msg": "绑定微信发送短信失败"
            }

    def post_bind_wechat(self, v):
        """
        绑定微信请求
        :param v: 验证码
        :return:
        """
        url_bind = "https://wx.17u.cn/xcxpubapi/pubmember/bind"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "105",
            "charset": "utf-8",
            "wxapp": "0",
            "User-Agent": self.ua,
            "apmat": f"{self.openId}|{get_time_stamp()}|{get_random_stamp()}",
            "content-type": "application/json",
            "sectoken": self.sectoken,
            "Accept-Encoding": "gzip,compress,br,deflate",
        }
        data = {"openId": self.openId, "unionId": self.unionId,
                "mobile": "18223791767", "validateCode": v}
        res = requests.post(url=url_bind, headers=headers, data=dict_to_json(data), verify=False).json()
        if res.get("RspCode") == 0 and res.get("Data").get("ErrMsg") == "绑定成功":
            print(res)
            pass
        else:
            return {
                "status": 3,
                "msg": "绑定微信失败",
                "ErrMsg": res.get("Data").get("ErrMsg")
            }

    def wc_sign(self):
        """
        微信签到
        :return:
        """
        url = "https://wx.17u.cn/wcsign/sign/SaveSignInfo"
        headers = {
            "Host": "wx.17u.cn",
            "Connection": "keep-alive",
            "Content-Length": "96",
            "charset": "utf-8",
            "wxapp": "0",
            "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; MI 5 Build/OPR1.170623.032; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/7.0.13.1640(0x27000D39) Process/appbrand2 NetType/WIFI Language/zh_CN ABI/arm64 WeChat/arm64",
            "content-type": "application/json",
            "sectoken": "ZfOeS2YX9IStsHx-3-C4u4g_AGpJ9X__1myeA0jUdYnp_A8xBTU0iORHv2OAovq6sPBu6w7o7FbdR8ooeUUHCNKh9q13Z1nys2M8NRj-MyrAD4-9TEFHZhRwldnGyjaPxyLOsRIgSJ952GtJIj3xL5tO1wConDJ4ooPZNdymNSnL40abHEFnPoJ7CCsiBg3L4",
            "Accept-Encoding": "gzip,compress,br,deflate",
        }
        data = {"unionId": "ohmdTtzyKbyp9mq54bCSfGTuiPDk", "openId": "o498X0TWrMMRUq4KlzRRSsOj3p5E", "sharerId": ""}
        data = dict_to_json(data)
        res = requests.get(url=url, headers=headers, data=data, verify=False)
        print(res.text)


tc = TCWechat()


def tc_app_wx_user(code):
    tc.app_wx_user(code)


if __name__ == "__main__":
    tc.app_wx_user(code="023Yi8H227DTUT0NHQH22xGTG22Yi8Hd")
