import requests
from wechat.setting import *
import urllib3

urllib3.disable_warnings()


class TCWechat(object):
    def __init__(self):
        self.ua = "Mozilla/5.0 (Linux; Android 8.0.0; MI 5 Build/OPR1.170623.032; wv) AppleWebKit/537.36 (KHTML, like" \
                  " Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/7.0.13.1640(0x27000D39)" \
                  " Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64 WeChat/arm64"
        self.sectoken = ""
        self.openId = "oK_d-jpJ9GrlJYEJIRRE-qtYVdIs"
        self.unionId = ""
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
            # "apmat": f"{self.openId}|{get_time_stamp()}|{get_random_stamp()}",
            "Accept-Encoding": "gzip,compress,br,deflate",

        }
        data = {"code": code, "scene": 1019}
        res = requests.post(url=url, headers=headers, data=dict_to_json(data), verify=False).json()
        print(res)
        self.sectoken = res.get("sectoken")
        self.openId = res.get("openId")
        self.unionId = res.get("unionId")
        self.memberId = res.get("memberId")




if __name__ == "__main__":
    tc = TCWechat()
    tc.app_wx_user(code="023hMSPi19lBXs0qKmSi1YGdQi1hMSPx")
