from threading import Thread
import urllib3
from APP.tc_pc_login.tc_pc_login import Login
from APP.setting import *
from APP.RedisProxyClient import get_cookies

urllib3.disable_warnings()


class OrderReturn(object):

    def __init__(self, params):
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, li" \
                  "ke Gecko) Chrome/80.0.3987.149 Safari/537.36"
        self.user = params.get("loginInfo").get("loginUser")
        self.pwd = params.get("loginInfo").get("loginPwd")
        self.session = requests.session()
        self.cookies = ""
        self.constId = ""
        self.data = params
        self.orderNo = self.data["orderNo"]
        self.url_return = "http://livechat.ly.com/out/ChatSelf/SupTicketNo"
        self.ticketNos = ""
        self.messageId = ""
        self.orderN = {}
        self.orderC = {}
        self.Lticketno = []
        self.headers = {
            'User-Agent': self.ua,
            "Cookie": get_cookies(phone=self.user)
        }

    def order_negotiate(self):
        """
        获取ConnectionToken，ConnectionId
        :return:
        """
        url_1 = 'http://livechat.ly.com/signalr/negotiate?'
        data1 = {
            'clientProtocol': 1.5,
            'connectionData': json.dumps([{"name": "interactivehub"}]),
            '_': int(time.time() * 1000)
        }
        res_1 = requests.get(headers=self.headers, url=url_1, params=data1, verify=False).json()
        connection_token = res_1["ConnectionToken"]
        return {'ConnectionToken': parse.urlencode({'ConnectionToken': connection_token}),
                'ConnectionId': res_1["ConnectionId"]}

    def order_connect(self):
        url_2 = 'http://livechat.ly.com/signalr/connect?transport=longPolling&clientProtocol=1.5&' + self.orderN[
            "ConnectionToken"] + '&connectionData=%5B%7B%22name%22%3A%22interactivehub%22%7D%5D&_t=0.23669784421220497'
        res = requests.get(headers=self.headers, url=url_2, verify=False).json()
        return {"messageId": res.get("C")}

    def order_start(self):
        url_3 = 'http://livechat.ly.com/signalr/start?transport=longPolling&clientProtocol=1.5&' + self.orderN[
            "ConnectionToken"] + '&connectionData=%5B%7B%22name%22%3A%22interactivehub%22%7D%5D&_=' + str(
            int(time.time() * 1000))
        res = requests.get(headers=self.headers, url=url_3, verify=False).json()
        return res

    def order_search(self):
        url_3 = 'http://livechat.ly.com/out/ChatSelf/Search'
        while self.ticketNos == '':
            pass
        data_3 = {
            'ticketNos': self.ticketNos,
            "connectionId": self.orderN["ConnectionId"]
        }
        res_3 = requests.get(url=url_3, data=data_3, headers=self.headers, verify=False)
        if res_3.status_code == 200:
            return res_3.text

    def main_order(self):
        data_o = {
            "messageId": self.orderC
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 '
                          '(KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            "Proxy-Connection": "keep-alive",
            "X-Requested-With": "XMLHttpRequest"
        }

        url = "http://livechat.ly.com/signalr/poll?transport=longPolling&clientProtocol=1.5&" + self.orderN[
            "ConnectionToken"] + "&connectionData=%5B%7B%22name%22%3A%22interactivehub%22%7D%5D"
        res = requests.post(headers=headers, data=data_o, url=url, verify=False)
        if res.status_code == 200:
            ticket_s = json.loads(res.text)
            m_list = ticket_s["M"]
            if m_list:
                for m in m_list:
                    a_list = m["A"]
                    for a in a_list:
                        for ticket_no in a["ticketNo"]:
                            e_ticket_no = ticket_no["ETicketNO"]
                            passenger_name = ticket_no["PassengerName"]
                            self.Lticketno.append({
                                "name": passenger_name,
                                "ticketNo": e_ticket_no
                            })
            else:
                self.Lticketno = []
            # print(self.Lticketno)
            return self.Lticketno

    def order_back(self):
        """
        返回票号
        :return:
        """
        ss = {
            "status": 0,
            "msg": "success",
            "orderNo": self.orderNo,
            "ticketNos": self.Lticketno
        }
        return ss


def do_backfill(data0):
    order = OrderReturn(data0)
    order.orderN = order.order_negotiate()
    order.orderC = order.order_connect()
    order.order_start()
    threads = []
    t1 = Thread(target=order.order_search)
    t2 = Thread(target=order.main_order)
    t2.start()
    t1.start()
    threads.append(t2)
    threads.append(t1)
    order.ticketNos = data0["orderNo"]
    for t in threads:
        t.join()
    return order.order_back()


if __name__ == '__main__':
    pass
