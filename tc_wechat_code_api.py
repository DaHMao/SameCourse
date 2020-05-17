from flask import Flask, request
import traceback
from APP.tc_code import *
from APP.setting import *
import json
from tc_app_log.loghelper import __write_log__
from tc_app_log.Journal_class import Journal
import urllib3

urllib3.disable_warnings()


def app_wx_user(vx_code, phone):
    """
     微信登录同程小程序，获取token
    :param vx_code:
    :param phone:
    :return:
    """
    url = "https://wx.17u.cn/appapi/wxuser/login/2"
    headers = {
        "Host": "wx.17u.cn",
        "Connection": "keep-alive",
        "Content-Length": "56",
        "charset": "utf-8",
        "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; MI 5 Build/OPR1.170623.032; wv) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 "
                      "MicroMessenger/7.0.13.1640(0x27000D39)Process/appbrand0 NetType/WIF"
                      "I Language/zh_CN ABI/arm64 WeChat/arm64",
        "content-type": "application/json",
        "Accept-Encoding": "gzip,compress,br,deflate",
    }
    data = {"code": vx_code[0], "scene": 1019}
    res = requests.post(url=url, headers=headers, data=dict_to_json(data), verify=False).json()
    print(res)
    if res.get("openId"):
        print("AAAAAAA")
        res_log = log_wechat_author(taskid=vx_code[2], app_id="3117146270", success="0", vxid=vx_code[3], phone=phone)
        print(res_log)
        return {
            "status": 0,
            "vx_token": res,
        }
    else:
        log_wechat_author(taskid=vx_code[2], app_id="3117146270", success="2", vxid=vx_code[3], phone=phone)
        return {
            "status": 1,
            "msg": "授权失败",
        }


def wechat_code(vxid, phone):
    code_vx = Code()
    res_vx = code_vx.do_get_tc_wechat_code(vxid=vxid, phone=phone)
    if isinstance(res_vx, dict):
        return res_vx
    print("微信授权code:", res_vx)
    res = app_wx_user(vx_code=res_vx, phone=phone)
    if res.get("status") == 1:
        return res
    res.get("vx_token")["vxid"] = vxid[1]
    return res


app = Flask(__name__)


@app.route("/")
def dd():
    print("hello")
    return "hello"


# http://192.168.0.173:11103/tc_wechat_code
@app.route('/tc_wechat_code', methods=['POST', 'GET'])
def register_tc():
    log = ''
    params = json.loads(request.get_data(as_text=True))
    print(params)
    vxid = params.get("vx_token").get("vxid")
    print("vxid", vxid)
    phone = params.get("token").get("loginName")
    try:
        ret = wechat_code(vxid=vxid, phone=phone)
        print(ret)
        resp = {
            "请求数据": params,
            "响应数据": ret
        }
        Journal().save_journal_wechat_code(massage=json.dumps(resp))
    except Exception:
        ret = {'code': 500, 'msg': traceback.format_exc()}
        resp = {
            "请求数据": params,
            "响应数据": ret
        }
        Journal().save_journal_wechat_code(massage=json.dumps(resp), level="error")
    log = log + str(ret) + '\n'
    __write_log__(log, tag="wechat_code")
    return json.dumps(ret)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11103, threaded=True)

    L = {'phone': '13042779348', 'pwd': 'vrvrvr1', 'user_type': '2', 'last_sign_day': '14',
     'last_login_day': '2020-05-14 16:23:36', 'integral': 660,
     'proxy': {'http': 'http://YsProxy:YsProxy@0023@36.22.77.87:1808',
               'https': 'https://YsProxy:YsProxy@0023@36.22.77.87:1808'},
     'device': {'sxx': '9e08a9e7972f45784631ff570baa70c5', 'clientId': '',
                'clientInfo': {'mac': '32:1b:6b:5a:d2:e0', 'area': '||', 'refId': '42931004',
                               'device': 'v07ul9rayexqm5j|armeabi-v7a|1080*1920*480|vivo X9i|c0bmvqh9uljbnm3',
                               'extend': '4^9.0.0,5^vivo X9i,6^-1,os_v^28,app_v^10.0.0.2,devicetoken^20200323173110fa0a5fa3d5c3ed152b5f0469a166f17001c74af463e38cbd',
                               'clientId': '31104ee1561a2b1cbff1085af40b7d2e1a78dadc900a',
                               'clientIp': '127.204.173.214', 'deviceId': 'v07ul9rayexqm5j',
                               'pushInfo': 'j4tvg6xmxbgud9gkhq61sw3w7bswsli0k4f01ylo', 'systemCode': 'tc',
                               'networkType': 'wifi', 'versionType': 'android', 'manufacturer': 'vivo',
                               'versionNumber': '10.0.0'}, 'AndroidImei': '860724351144971'},
     'token': {'email': '13042779348@163.com', 'score': '0', 'cityId': '0', 'mobile': '13042779348', 'userId': '',
               'headImg': 'https://pic5.40017.cn/i/ori/PELe6f5TBC.jpg', 'isblack': '0', 'cityName': '',
               'memberId': 'I0_8d9e0e31e51dcf7c8f7697fe77781e31',
               'password': '/n+TGltm6VpGQoyPjTwWg2tKkiLpKb4d/mhgrEkhanplbalcpGtkkcKXScCdgsnG',
               'trueName': '13042779348', 'userName': '尊敬的会员', 'loginName': '13042779348', 'sUserList': [
             {'userId': 'oOCyauNnOQh39fMjKrXHm-BMaPxM', 'unionId': 'ohmdTt2zaVQiqKis4ZBpfod428fE',
              'bindDate': '2019-12-8 16:28:23', 'socialType': '4', 'accessToken': ''}], 'versionNo': '',
               'provinceId': '0', 'socialType': '',
               'memberIdNew': 'yMwjfsVNZPSLqqibGJUiyTDED_kP0xtvXlzKQqo1UHojrUMw7Q9MuRd3-a-_QrHouTuVD8RaI9NFUSZ6ia2B9asFjnAsAW4anIR0513-Oo7Qy2ijDbjTsZM4Ls1pnTkRwoYbjXHanXWJ44FRcP6oH7GUzgafibgqyA6ZDtaEVfo*AB',
               'provinceName': '', 'authorizeCode': '', 'isSocialMember': '0', 'socialUserLists': {'sUserList': [
             {'userId': 'oOCyauNnOQh39fMjKrXHm-BMaPxM', 'unionId': 'ohmdTt2zaVQiqKis4ZBpfod428fE',
              'bindDate': '2019-12-8 16:28:23', 'socialType': '4', 'accessToken': ''}], 'isCanUnbind': '0',
                                                                                                   'isWxMulBind': '0',
                                                                                                   'isShowWxCheck': '1',
                                                                                                   'isCanUnbindElong': '0'},
               'externalMemberId': '0db9a6977682767ff8cd3f8736ee094c'}, 'use_coupons': {}, 'vx_token_online': '0',
     'vx_token': {'vxid': 'IyMxMzQ2NzE3NDg2', 'expts': 1589437210, 'openId': 'o498X0apPsWnXla9zl3sCRVgjT1k',
                  'unionId': 'ohmdTt_AxjchSq7NXfDPrPoVgme0', 'memberId': 'Pmry7k0p7kL8hDY6AFeU4A==',
                  'sectoken': 'ZfOeS2YX9IStsHx-3-C4u_gEqWTekZ_oI1JL94nk95Lp_A8xBTU0iORHv2OAovq6kuuTn2KzzbAVJ0Wnk_jmv-8FiCqfiTz-YhVTqx05oFVlqRg5cvz2YB9U-ARLpbMbYk02exNjIo_7DOmoEPdBz3O0Mii9HvMQ_wIapy_YWLTL40abHEFnPoJ7CCsiBg3L4641',
                  'aesOpenId': '5RIwOKWY5On8tqlwbuDKse4Oy5c/xxmiPmLko/sOkAw=',
                  'aesUnionId': 'OY6/RZJ5s/VWdPLg8/SWTt0q4Hq8ILhUWut52oh6/s8=',
                  'encryOpenId': '2a17b0b51ecbdd5f685be33d96290ffc'}, 'reg_time': '2020-05-11 23:10:57', 'risk': '0',
     'vx_last_auth_time': '2020-05-14 13:26:41', 'befor_coupons': ''}

