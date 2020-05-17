import requests
from APP.tc_pc_login import token
import hashlib
import random
import urllib3

urllib3.disable_warnings()


class Login(object):
    def __init__(self, params):
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, li" \
                  "ke Gecko) Chrome/80.0.3987.149 Safari/537.36"
        self.constId = ""
        self.user = params.get("user")
        self.pwd = params.get("password")
        self.session = requests.session()
        self.cookies = ""

    def md5_pwd(self):
        """
        密码md5加密
        :return:
        """
        md5_encrypt = hashlib.md5(self.pwd.encode(encoding='UTF-8')).hexdigest()
        return md5_encrypt

    def get_random_v(self):
        return str(round(random.random(), 15))

    def get_token(self):
        """
        获取constId
        :return:
        """
        URL = "https://sec.ly.com/mobile/secapi/zid?"
        headers = {
            "Host": "sec.ly.com",
            "Connection": "keep-alive",
            "User-Agent": self.ua,
            "Sec-Fetch-Dest": "script",
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "no-cors",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        uuid = token.m2()
        data = token.get_des_psswd(e=uuid)
        data["appid"] = "c1a628bc7b4418a9c9ea1f5cd252485c"
        res = requests.get(url=URL, params=data, headers=headers, verify=False).json()
        print(res)
        self.constId = res.get("token")

    def post_login(self):
        """
        执行登录
        :return:
        """
        url = "https://passport.ly.com/login/login?tdleonid=tdleonid"
        headers = {
            "Host": "passport.ly.com",
            "Connection": "keep-alive",
            "Content-Length": "150",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Sec-Fetch-Dest": "empty",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": self.ua,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://passport.ly.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Referer": "https://passport.ly.com/?pageurl=https%3A%2F%2Fwww.ly.com%2F",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        data = {
            "constId": self.constId,
            "name": self.user, "pass": self.md5_pwd(), "areaCode": 86,
            "v": self.get_random_v(), "remember": 30
        }
        res = self.session.post(url=url, data=data, headers=headers, verify=False)
        res_json = res.json()
        print(res_json)
        if res_json.get("Message") == "登录成功":
            for i in self.session.cookies.items():
                if i[1] is None:
                    self.cookies += i[0] + '' + '; '
                else:
                    self.cookies += i[0] + '=' + i[1] + '; '
            return True
        else:
            return {
                "status": 3,
                "msg": "登录失败"
            }

    def do_login(self):
        i = 0
        while i <= 3:
            self.get_token()
            res = self.post_login()
            if isinstance(res, dict):
                i += 1
            return res
        else:
            return {
                "status": 3,
                "msg": "登录失败,已重新尝试登录3次"
            }


if __name__ == "__main__":
   pass
