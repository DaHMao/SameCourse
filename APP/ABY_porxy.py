import requests
import urllib3

urllib3.disable_warnings()
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"


class ProxyPool:
    def __init__(self):
        self.proxy_list = [
            {'user': 'HZ0684M4LN2K857D',
             'pass': 'F7D8A292F462F5EC'},

        ]
        self.curr_index = 0

    def get_proxy(self):
        porxy = self.proxy_list[self.curr_index]
        self.curr_index = self.curr_index + 1
        if self.curr_index >= len(self.proxy_list):
            self.curr_index = 0
        proxy_meta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": porxy['user'],
            "pass": porxy['pass'],
        }
        proxies = {
            "http": proxy_meta,
            "https": proxy_meta,
        }
        return proxies


porxy_pool = ProxyPool()

if __name__ == '__main__':
    pass
    # for x in range(10):
    #     s = requests.session()
    #     s.verify = False
    #     s.proxies = porxy_pool.get_proxy()
    #     print(s.proxies)
    #     req = s.get('https://baidu.com')
    #     print(req.text)
