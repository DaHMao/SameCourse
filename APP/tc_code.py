# --coding:utf-8--
import requests
import time
import base64
import re
from tc_app_log.Journal_class import Journal
from APP.setting import log_wechat_author
import json


class Code(object):
    def __init__(self):
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, lik" \
                  "e Gecko) Chrome/80.0.3987.149 Safari/537.36"

    def get_tc_app_code(self):
        """
        创建APP授权code任务
        :return:
        """
        url = "http://221.229.197.219:8090/api/apiauth"
        data = {
            "userid": "3333516394",
            "platform": "1",
            "appid": "3908282825",
            "vxid": ""
        }
        headers = {
            "User-Agent": self.ua
        }
        try:
            res = requests.post(url=url, json=data, headers=headers, timeout=10)
            res_json = res.json()
            ret = {"创建app授权任务": res_json}
            Journal().save_journal_app_empower_taskid(massage=json.dumps(ret))
            if res_json.get("err_code") == 1:
                return res_json.get("taskid")
            else:
                return {
                    "status": 3,
                    "msg": "授权任务创建失败！，获取taskid失败",
                    "err_msg": res_json.get("err_msg")
                }
        except Exception:
            return {
                "status": 3,
                "msg": "授权任务创建失败！获取taskid失败",
            }

    def get_wechat_tc_code(self, vxid, phone=""):
        """
        创建微信小程序授权code任务
        :param vxid: 微信id
        :return:
        """
        url = "http://221.229.197.219:8090/api/apiminiauth"
        data = {
            "userid": "3333516394",
            "appid": "3117146270",
            "vxid": vxid,
        }
        headers = {
            "User-Agent": self.ua
        }
        try:
            res = requests.post(url=url, json=data, headers=headers, timeout=10)
            res_json = res.json()
            ret = {
                "创建任务请求数据": data,
                "创建任务返回结果": res_json}
            Journal().save_journal_wechat_empower_taskid(massage=json.dumps(ret))
            print(res_json)
            if res_json.get("err_code") == 1:
                return res_json.get("taskid")
            else:
                return {
                    "status": 3,
                    "msg": "授权任务创建失败！",
                    "err_msg": res_json.get("err_msg")
                }
        except Exception:
            return {
                "status": 3,
                "msg": "授权任务创建失败！",
            }

    def get_result_code(self, task_id):
        """
        获取授权code
        :param task_id:
        :return: 授权任务的id
        """
        url = "http://221.229.197.219:8090/api/apiauthresult"
        data = {
            "userid": "3333516394",
            "taskid": task_id
        }
        headers = {
            "User-Agent": self.ua
        }
        res = requests.post(url=url, json=data, headers=headers)
        res_json = res.json()
        ret = {
            "授权结果请求数据": data,
            "授权结果返回数据": res_json}
        Journal().save_journal_app_empower_result(massage=json.dumps(ret))
        if res_json.get("err_code") == 1:
            if res_json.get("task_ret") == 1:
                vxid_1 = res_json.get("vxid")
                code_str = re.findall(r"code=(.*?)&state=", res_json.get("auth_str"))[0]
                vxid = base64.b64encode(res_json.get("vxid").encode()).decode()
                return code_str, vxid, task_id, vxid_1
            else:
                return {
                    "status": 1,
                    "msg": "授权正在进行中,请重新请求",
                }
        elif res_json.get("err_code") == 0 and res_json.get("task_ret") == 0:
            return {
                "status": 2,
                "msg": "重新创建授权任务",
            }
        else:

            log_wechat_author(taskid=task_id, app_id="3908282825", success="1", vxid="")
            return {
                "status": 3,
                "msg": "授权任务创建失败！",
                "err_msg": res_json.get("err_msg")
            }

    def get_result_code_two(self, task_id, phone=""):
        """
        获取授权code
        :param task_id:
        :return: 授权任务的id
        """
        url = "http://221.229.197.219:8090/api/apiauthresult"
        data = {
            "userid": "3333516394",
            "taskid": task_id
        }
        headers = {
            "User-Agent": self.ua
        }
        res = requests.post(url=url, json=data, headers=headers)
        res_json = res.json()
        ret = {
            "授权结果请求数据": data,
            "授权结果返回数据": res_json}
        Journal().save_journal_wechat_empower_result(massage=json.dumps(ret))
        if res_json.get("err_code") == 1:
            if res_json.get("task_ret") == 1:
                vxid_1 = res_json.get("vxid")
                code_str = res_json.get("auth_str")
                vxid = base64.b64encode(res_json.get("vxid").encode()).decode()
                return code_str, vxid, task_id, vxid_1
            else:
                return {
                    "status": 1,
                    "msg": "授权正在进行中,请重新请求",
                }
        elif res_json.get("err_code") == 0 and res_json.get("task_ret") == 0:
            return {
                "status": 2,
                "msg": "重新创建授权任务",
            }
        else:
            vxid = ""
            log_wechat_author(taskid=res, app_id="3117146270", success="1", vxid=vxid, phone=phone)
            return {
                "status": 3,
                "msg": "授权任务创建失败！",
                "err_msg": res_json.get("err_msg")
            }

    def do_get_tc_app_code(self):
        """
        获取APP授权code
        :return:
        """
        while True:
            res = self.get_tc_app_code()
            if isinstance(res, dict):
                return res
            if res:
                i = 1
                while i <= 10:
                    result = self.get_result_code(res)
                    if isinstance(result, tuple):
                        return result
                    elif result.get("status") == 3:
                        return result
                    elif result.get("status") == 2:
                        break
                    else:
                        i += 1
                        time.sleep(2)
                vxid = ""
                log_wechat_author(taskid=res, app_id="3908282825", success="1", vxid=vxid)

    def do_get_tc_wechat_code(self, vxid, phone=""):
        """
         获取微信小程序code
        :param vxid: 微信id
        :return:
        """
        while True:
            res = self.get_wechat_tc_code(vxid=vxid, phone=phone)
            if isinstance(res, dict):
                return res
            i = 1
            while i <= 10:
                result = self.get_result_code_two(res, phone=phone)
                if isinstance(result, tuple):
                    return result
                elif result.get("status") == 3:
                    return result
                elif result.get("status") == 2:
                    break
                else:
                    i += 1
                    time.sleep(2)
            vxid = ""
            log_wechat_author(taskid=res, app_id="3117146270", success="1", vxid=vxid, phone=phone)


if __name__ == "__main__":
    pass
    # code = Code()
    # print(code.do_get_tc_wechat_code(vxid=base64.b64encode("##273528137".encode()).decode()))
