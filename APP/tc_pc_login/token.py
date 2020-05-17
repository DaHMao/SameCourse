# -*- coding: utf-8 -*-
import execjs

JS_m2 = """
function m2() {
    var sty = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx";
    var m3 = {
        'hkSRE': function (m4, m5) {
            return m4 * m5;
        },
        'ZHAtc': function (m6, m7) {
            return m6 | m7;
        }
    };
    if (false) {
        return obj[b('0xf4')](iterator);
    } else {
        return sty.replace(/[xy]/g, function (m9) {
            var ma = m3['hkSRE'](Math.random(), 0x10) | 0x0
                , mb = m9 === 'x' ? ma : m3['ZHAtc'](ma & 0x3, 0x8);
            return mb.toString(16);
        });
    }
}
"""


def m2():
    func = execjs.compile(JS_m2)
    return func.call("m2")


def get_js():
    f = open("token.js", 'r', encoding='utf-8')  # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


def get_des_psswd(e):
    js_str = get_js()
    ctx = execjs.compile(js_str)  # 加载JS文件
    return ctx.call('App_tc', e)  # 调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数
