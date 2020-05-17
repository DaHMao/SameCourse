import random
import requests
from requests.exceptions import ConnectionError, ProxyError, ReadTimeout, ConnectTimeout
from concurrent.futures import ThreadPoolExecutor
import urllib3
import time
urllib3.disable_warnings()


def get_proxy(src='', stop=0):
    global res
    now = time.time()
    try:
        if src:
            url = 'http://ip.ystrip.cn:8080/api/Vps/GetUsed?group={}&user=tc_app_order'.format(src)
        else:
            url = 'http://ip.ystrip.cn:8080/api/Vps/GetUsed?group={}&user=tc_app_order'.format(random.choice(['isearch']))
        res = requests.get(url, timeout=5, verify=False).json()
        if res['ret'] == 1:
            proxy = 'YsProxy:YsProxy@0023' + '@' + str(res['data']['ip']) + ':1808'
            proxies = {'http': 'http://' + proxy, 'https': 'https://' + proxy}
            return proxies, res['data']['host'], res['data']['ip']
        else:
            stop += 1
            if stop > 3:
                return None, None
            return get_proxy(stop=stop)
    except (ConnectionError, ProxyError, ReadTimeout, ConnectTimeout):
        stop += 1
        if stop > 3:
            return None, None
        return get_proxy(stop=stop)

def freed_proxy(host, typ='false'):
    try:
        response = requests.get(
            'http://ip.ystrip.cn:8080/api/Vps/UsedReset?host={}&isDial={}&user=tc_app_order'.format(
                host, typ), timeout=5)
    except (ConnectionError, ProxyError, ReadTimeout, ConnectTimeout):
        return None


if __name__ == '__main__':
   pass