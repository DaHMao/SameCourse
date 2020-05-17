from flask import Flask, request
import traceback
from APP.tc_app_order_coupon import *
from tc_app_log.loghelper import __write_log__
from tc_app_log.Journal_class import Journal

app = Flask(__name__)


# http://192.168.1.101:11100/order_tc_app
@app.route('/order_tc_app', methods=['POST', 'GET'])
def register_tc():
    log = ''
    params = json.loads(request.get_data(as_text=True))
    print(params)
    try:
        ret = Order(params=params).do_order_login()
        resp = {
            "请求数据": params,
            "响应数据": ret
        }
        Journal().save_journal_order(massage=json.dumps(resp))
    except Exception:
        ret = {'code': 500, 'msg': traceback.format_exc()}
        resp = {
            "请求数据": params,
            "响应数据": ret
        }
        Journal().save_journal_order(massage=json.dumps(resp), level="error")
    log = log + str(ret) + '\n'
    __write_log__(log, tag="order")
    return json.dumps(ret)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11100, threaded=True)
