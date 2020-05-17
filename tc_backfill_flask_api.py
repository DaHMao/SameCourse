from flask import Flask, request
import traceback
from APP.tc_pc_backfill import *
from tc_app_log.loghelper import __write_log__
from tc_app_log.Journal_class import Journal

app = Flask(__name__)


@app.route("/")
def dd():
    print("hello")
    return "hello"


# http://192.168.0.173:11101/backfill_tc_pc
@app.route('/backfill_tc_pc', methods=['POST', 'GET'])
def register_tc():
    log = ''
    params = json.loads(request.get_data(as_text=True))
    print(params)
    try:
        ret = do_backfill(data0=params)
        print(ret)
        resp = {
            "请求数据": params,
            "响应数据": ret
        }
        Journal().save_journal_backfill(massage=json.dumps(resp))
    except Exception:
        ret = {'code': 500, 'msg': traceback.format_exc()}
        resp = {
            "请求数据": params,
            "响应数据": ret
        }
        Journal().save_journal_backfill(massage=json.dumps(resp), level="error")
    log = log + str(ret) + '\n'
    __write_log__(log, tag="backfill_")
    return json.dumps(ret)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11101, threaded=True)
