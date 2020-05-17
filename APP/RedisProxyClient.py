import redis
import json


class RedisClientClass(object):
    def __init__(self):
        pool = redis.ConnectionPool(host='192.168.0.29', port=6379, decode_responses=True, db=6,
                                    password='')
        self.r = redis.Redis(connection_pool=pool)
        # print(self.r.keys())

    def s_data_all(self, name):
        data = self.r.smembers(name)
        return data

    def srem_delete(self, name, value):
        return self.r.srem(name, value)


class RedisClientClassCookies(object):
    def __init__(self):
        pool = redis.ConnectionPool(host='192.168.0.29', port=6379, decode_responses=True, db=7,
                                    password='')
        self.r = redis.Redis(connection_pool=pool)
        # print(self.r.keys())

    def s_data_all(self, name):
        data = self.r.smembers(name)
        return data

    def srem_delete(self, name, value):
        return self.r.srem(name, value)

    def h_get(self, name, key):
        """
        以key，查找value，取出来
        :param name:
        :param key:
        :return:
        """
        return self.r.hget(name, key)


def get_cookies(phone):
    tc_c = json.loads(RedisClientClassCookies().h_get(name="TC_COOKIE", key=phone))
    cookie = ""
    for key in tc_c:
        cookie += key + "=" + tc_c[key] + ";"
    return cookie



