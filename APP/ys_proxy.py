import requests
from retrying import retry


def get_proxy_by_ys():
    @retry(stop_max_attempt_number=10, wait_fixed=1000, stop_max_delay=20000)
    def _get_proxy():
        print("获取IP代理...", end="")
        res = requests.get(url="http://ip.ystrip.cn:8080/api/Vps/GetUsed?group=isearch&user=TC_APP_order")
        data = res.json()
        ip = data.get("data", {}).get("ip")
        if not ip:
            print(f"..fail.{data.get('data', {}).get('msg')}")
            raise
        host = data.get("data", {}).get("host")
        p = {
            "http": f"http://YsProxy:YsProxy@0023@{ip}:1808",
            "https": f"https://YsProxy:YsProxy@0023@{ip}:1808"
        }
        session = requests.session()
        headers = {"User-Agent": "Mozilla/5.0"}
        session.headers.update(headers)
        session.proxies = p
        try:
            res = session.get(url="http://www.baidu.com/", timeout=6, allow_redirects=False)
            print(res.status_code)
            if res.status_code != 200:
                raise (res.status_code)
            print(f"success→获得{ip}")
            return p, ip, host
        except Exception as e:
            print(f"..fail.→释放{ip}...", end="")
            try:
                res = requests.get(
                    url=f"http://ip.ystrip.cn:8080/api/Vps/UsedReset?host={host}&isDial=true&user=TC_APP_order")
                if res.status_code == 200:
                    print("success")
                else:
                    print("fail")
            except:
                print("fail")
            raise

    try:
        p = _get_proxy()
        return p
    except:
        return {}


if __name__ == '__main__':
    print(get_proxy_by_ys())
