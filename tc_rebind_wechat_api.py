from flask import Flask, request
import traceback
from APP.tc_rebind_wechat import ReBindWeChat
from tc_app_log.loghelper import __write_log__
from tc_app_log.Journal_class import Journal
import json

app = Flask(__name__)

@app.route("/")
def dd():
    print("hello")
    return "hello"


# http://192.168.0.173:11102/tc_rebind_wechat
@app.route('/tc_rebind_wechat', methods=['POST', 'GET'])
def register_tc():
    log = ''
    params = json.loads(request.get_data(as_text=True))
    print(params)
    try:
        ret = ReBindWeChat(params).do_do_rebind()
        print(ret)
        resp = {
            "请求数据": params,
            "响应数据": ret
        }
        Journal().save_journal_rebind(massage=json.dumps(resp))
    except Exception:
        ret = {'code': 500, 'msg': traceback.format_exc()}
        resp = {
            "请求数据": params,
            "响应数据": ret
        }
        Journal().save_journal_rebind(massage=json.dumps(resp), level="error")
    log = log + str(ret) + '\n'
    __write_log__(log, tag="rebind_")
    return json.dumps(ret)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11102, threaded=True)
