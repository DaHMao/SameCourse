from APP.tc_app_login import *

from multiprocessing import Pool


def login_():
    i = 0
    while i <= 10:
        res = do_login_one()
        if res.get("status") == 3000:
            i += 1


if __name__ == "__main__":
    pool = Pool(16)
    for i in range(16):
        print(i)
        p = pool.apply_async(func=login_)
        print(p)
    pool.close()
    pool.join()
