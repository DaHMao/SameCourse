import requests

Dict_mdh = {
    "status": 0,
    "clientId": "4110b22812f3cb8ec988a097a255f9613c3d3deaef9c",
    "phone": "17338347182",
    "pwd": "12345678@",
    "user_type": "0",
    "device": {
        "clientInfo": {"device": "957117cdb8f4fa90|x86|720*1280*192|VOG-AL00|49307774",
                       "deviceId": "957117cdb8f4fa90", "networkType": "wifi",
                       "pushInfo": "bdbd6386b82bc4d746ddb378ce74f8089aca48d9",
                       "mac": "0e:73:c1:0d:5b:9f",
                       "extend": "4^5.1.1,5^VOG-AL00,6^-1,os_v^22,app_v^10.0.0,devicetoken^20200421182011d41748c1434fdd5b171c62eb166aec9a016b17bb96ca9e69",
                       "clientIp": "10.0.2.15", "systemCode": "tc",
                       "clientId": "4110b22812f3cb8ec988a097a255f9613c3d3deaef9c",
                       "versionType": "android", "refId": "42931004", "area": "1|25|321",
                       "versionNumber": "10.0.0", "manufacturer": "HUAWEI"},
        "AndroidImei": "",
        "sxx": "3f75bea2b1becd8d11e7e23fc7dbd022",
    },
    "token": {
        "memberIdNew": "0KMn6q8kgbhEHPFOexUnYIrEgGseIYhMlY-FDjD6M20LBEf8C2b2v8STE-wsp4jljTiZTBGCP8ozgb8lyM73Ov4VILS7EsapNPtsAZeYBsqL9XQFDSTEXWmFZosXqRyMoxHJe-DmCSW9iAV8w3NXaeaIhLmS7sV9fniPqux6k5f6T3nLRewdM3vZpTZ04oo8AB",
        "memberId": "I0_96adb2efbf19211bbf6794254ba11733", "loginName": "17338347182", "userName": "尊敬的会员",
        "mobile": "17338347182", "email": "",
        "password": "sIanhT1BBBC6SgGwj8yV6AvGxao/d3pG7auUSv1m+eU8ho0JIbQMlDP1GM08F71v",
        "oldPassword": "",
        "trueName": "17338347182", "isBlack": "0", "externalMemberId": "fcce29a3f887841b2e1df6a7545d36be",
        "sUserList": []},
    "proxy": ""
}

Dict_lwk = {
    "status": 0,
    "clientId": "4110966ac3d628bbbc96048c95e11c1f62e19c16f26f",
    "phone": "15922525355",
    "pwd": "12345678@",
    "user_type": "0",
    "device": {
        "clientInfo": {"versionType": "android", "area": "1|32|394",
                       "clientId": "4110966ac3d628bbbc96048c95e11c1f62e19c16f26f",
                       "deviceId": "c3a74964878a5d24",
                       "versionNumber": "10.0.0", "mac": "02:00:00:00:00:00",
                       "manufacturer": "Xiaomi",
                       "extend": "4^8.0.0,5^MI 5,6^-1,os_v^26,app_v^10.0.0.2,devicetoken^20200413145123decba7cba3c107d976a64ce6f5e412c90145320258f47e22,memberidnew^LxfkUJnhqMvUFdqADBkAEPrgYbSUrlc0f-cSul5hyElBKA04M-a-Az9fu65_z5skbtDYCqwql4ErrqjYcM0_pfSeJawKF-XrEoWAPvZI_cZvvsDCN4qp8jknSYqFLhOGoJ0xhEGzMCJJHxJEV0c7d7Jg-w6kxFk0P-zPgcJbEAbCpXNertHzRoUf1XGUaLYGAB",
                       "systemCode": "tc", "clientIp": "192.168.1.119",
                       "refId": "16359978", "networkType": "wifi",
                       "device": "c3a74964878a5d24|arm64-v8a|1080*1920*480|MI 5|406a0cf9",
                       "pushInfo": "d566caceb578b12ed99c8913e31065f489c854cc"},
        "AndroidImei": "",
        "sxx": "da5795c5b7422194a5286f1803d82ca1",

    },  # 设备参数及其他重要值
    "token": {
        "memberIdNew": "LxfkUJnhqMvUFdqADBkAEPrgYbSUrlc0f-cSul5hyElBKA04M-a-Az9fu65_z5skbtDYCqwql4ErrqjYcM0_pdWeei-HEyqLKmanhSvc4Tm4pNBDtEH9f4PXwxvENA49us5z5m5bl6P7Q52MZdubXrEZ7cojGYK9686gN0OWO-AhcjLX7mmTOuDcHKQh-lkPAB",
        "memberId": "I0_8a3952f6a83a78710ab34cdf399a6c56",
        'loginName': '15922525355',
        'userName': '尊敬的会员',
        'mobile': '15922525355',
        'email': '',
        "password": "LbSG0pTpXhpllikV+meyzPryRojI49X1A1z7FjtdI6yV6xbjfUzGp8IO5VOepc2s",
        'oldPassword': '',
        'trueName': '15922525355',
        'isBlack': '0',
        "externalMemberId": "0c3055acd2f80e28131b32e5ebfd950c",
        'sUserList': []},  # 用于二次登录的重要 token
    "proxy": ""  # 代理IP
}

Dict_cl = {
    'status': 0,
    "user_type": "0",
    "device": {
        "clientInfo": {"versionType": "android", "area": "1|32|394",
                       "clientId": "31100101ca8ed2f4bb8c696d1e52f7a89cd6870532da",
                       "deviceId": "c27a9485c8f80f74",
                       "versionNumber": "10.0.0", "mac": "02:00:00:00:00:00",
                       "manufacturer": "Xiaomi",
                       "extend": "4^8.0.0,5^MI 5,6^-1,os_v^26,app_v^10.0.0.2,devicetoken^20200413145123decba7cba3c107d976a64ce6f5e412c90145320258f47e22,memberidnew^FmAv-NrmQHc6n-IEzFYs1qxM4n6ss23GFWSrT1achMexGUhAI1dlp-YMfUZ7dWGnzbB-1k5m2GyYWbEeGxTMAURfH9xQClIBM5qMk_M0LKKT8EgHC_r3wjn5s0TTvz21c4BTSAqY-XXi8kOloXUWkUj7WZGKbmqwM3TeLDHMarRmWxI8MyJlVbz5IjR9blKsAB",
                       "systemCode": "tc", "clientIp": "192.168.1.119",
                       "refId": "16359978", "networkType": "wifi",
                       "device": "c27a9485c8f80f74|arm64-v8a|1080*1920*480|MI 5|406a0cf9",
                       "pushInfo": "f4497daa8181c71647c0b1c7cd22bfac8112614f"},
        "AndroidImei": "",
        "sxx": "fcc31597471e83ddab5bb7688b3f3314",
        "clientId": "31100101ca8ed2f4bb8c696d1e52f7a89cd6870532da",

    },
    'token': {
        "memberIdNew": "FmAv-NrmQHc6n-IEzFYs1qxM4n6ss23GFWSrT1achMexGUhAI1dlp-YMfUZ7dWGnzbB-1k5m2GyYWbEeGxTMAVBRH7YrjQKC6W4SOhvQEHhgCIlE5qnEmtqI1ZKgKQqbc4BTSAqY-XXi8kOloXUWkSCvA7LWMgkyyCHM62u_aaZ9A6ttJFyPqBWsLi1RvrD1AB",
        "memberId": "I0_6018a7008b70fec61f7964c532d40734",
        'loginName': '13062991445',
        'userName': '尊敬的会员',
        'mobile': '13062991445',
        'email': '',
        "password": "k50+jVAlg1nQU10jgk+hXX+DimMgq9FgaTAbcUGsV+QNzwuk1+wP9o0sr8JIrVib",
        'oldPassword': '',
        'trueName': '13062991445',
        'isBlack': '0',
        "externalMemberId": "dcc7e93d456d1e0429b3103cace60036",
        'sUserList': []},
    "phone": "13062991445",
    "pwd": "12345678@",
}

Dict_zf = {
    "status": 0,
    "user_type": "0",
    "device": {
        "clientInfo": {"device": "957117cdb8f4fa90|x86|720*1280*192|VOG-AL00|49307774",
                       "deviceId": "957117cdb8f4fa90", "networkType": "wifi",
                       "pushInfo": "bdbd6386b82bc4d746ddb378ce74f8089aca48d9", "mac": "60:71:6c:6d:2c:cb",
                       "extend": "4^5.1.1,5^VOG-AL00,6^-1,os_v^22,app_v^10.0.0,devicetoken^20200421182011d41748c1434fdd5b171c62eb166aec9a016b17bb96ca9e69",
                       "clientIp": "10.0.2.15", "systemCode": "tc",
                       "clientId": "4110b22812f3cb8ec988a097a255f9613c3d3deaef9c", "versionType": "android",
                       "refId": "42931004", "area": "1|25|321", "versionNumber": "10.0.0",
                       "manufacturer": "HUAWEI"},
        "AndroidImei": "",
        "sxx": "ad9e835682f7724832e2e96a76f4128c",
        "clientId": "4110b22812f3cb8ec988a097a255f9613c3d3deaef9c",

    },  # 设备参数及其他重要值
    "token": {
        "memberIdNew": "FmAv-NrmQHc6n-IEzFYs1qTBtjYKqFhhO76AbH1fImTNw_4YkRT_psjWYzLtecSAD-DwWQUS6aZd48NdIzzT6FAqqf8DNGmcgXYBifuEXfEZxG45jmLLFISxmzmdoirrc4BTSAqY-XXi8kOloXUWkdlUVkoyY1XVyYdgS1PJnJJtVSaifTZ4xg09EAZXkCHuAB",
        "memberId": "I0_bcad196e7b09ddcb72ea877cdb445cc7", "loginName": "13330340777", "userName": "尊敬的会员",
        "mobile": "13330340777", "email": "",
        "password": "k50+jVAlg1nQU10jgk+hXX+DimMgq9FgaTAbcUGsV+QNzwuk1+wP9o0sr8JIrVib",
        "oldPassword": "",
        "trueName": "13330340777", "isBlack": "0", "externalMemberId": "fdd573569992edcdfa3a0e0fd9065628",
        "sUserList": []},  # 用于二次登录的重要 token
    "proxy": "",  # 代理IP
    "phone": "13330340777",
    "pwd": "12345678@"
}

Dict_ycc = {
    "status": 0,
    "user_type": "0",
    "device": {
        "clientInfo": {
            "mac": "6a:2a:6f:4e:11:e2",
            "extend": "4^9.1.0,5^MI 9,6^-1,os_v^22,app_v^10.0.0,devicetoken^20200323173110fa0a5fa3d5c3ed152b5f0469a166f17001c74af463e38cbd",
            "device": "vbvz49rerj1f6i2|armeabi-v7a|2248*1080*402|MI 9|qcuwqefqkf4feqe",
            "deviceId": "vbvz49rerj1f6i2",
            "manufacturer": "Xiaomi",
            "clientIp": "10.198.230.163",
            "networkType": "wifi",
            "pushInfo": "89fsnnabd601a7nck4hvtvmr7upcpniodekioprw",
            "systemCode": "tc",
            "clientId": "31100101ca8ed2f4bb8c696d1e52f7a89cd6870532da",
            "versionType": "android",
            "refId": "16359978",
            "area": "||",
            "versionNumber": "10.0.0"
        },
        "AndroidImei": "",
        "sxx": "ad9e835682f7724832e2e96a76f4128c",
        "clientId": "31100101ca8ed2f4bb8c696d1e52f7a89cd6870532da",

    },  # 设备参数及其他重要值
    "token": {
        "memberIdNew": "4zxZ6IjSFlysV-twbD2EUpPpuRrqO7I4bhE8ORq48DSSyZFUxR-QUsbbWl3fPp4ZMfkP0IFhB-pJ8O4ZQoeQsNqqvMiCg5PKHF72SEuUL_4yTSxE0dhE_Po0pNftqyE27qAdKz-pJc-EFy3btTTc5RBTl6FdXQ94i7Ec-IYKmrFnZqJSKsAaa9H8ZWM2jTGBAB",
        "memberId": "I0_09eba09ea43329a1b28df2392ff6c5a2", "loginName": "18223791767", "userName": "尊敬的会员",
        "mobile": "18223791767", "email": "",
        "password": "5ZLLCoJBFyQH44QV8UyMxc60GzteWweubGntXFPYmHo4RflWLUoJ1UjvFEvz7JYK",
        "oldPassword": "",
        "trueName": "18223791767", "isBlack": "0", "externalMemberId": "36b261668620b386f94bc4275780ef04",
        "sUserList": []},  # 用于二次登录的重要 token
    "proxy": "",  # 代理IP
    "phone": "18223791767",
    "pwd": "12345678@"
}

Dict_16521956748 = {
    "status": 0,
    "user_type": "0",
    "device": {
        "clientInfo": {"device": "957117cdb8f4fa90|x86|720*1280*192|VOG-AL00|49307774",
                       "deviceId": "957117cdb8f4fa90", "networkType": "wifi",
                       "pushInfo": "bdbd6386b82bc4d746ddb378ce74f8089aca48d9", "mac": "0e:73:c1:0d:5b:9f",
                       "extend": "4^5.1.1,5^VOG-AL00,6^-1,os_v^22,app_v^10.0.0,devicetoken^20200421182011d41748c1434fdd5b171c62eb166aec9a016b17bb96ca9e69,memberidnew^7-BwMboYz5q9dHFcG6JzbK2yflTKH_oIMEtkYUCd_UILBEf8C2b2v8STE-wsp4jljTiZTBGCP8ozgb8lyM73OtxwP8Z_oDuLU8XJVJibyl54yntojPbXvdhni-PVfz_1AQm_ZVWUQdx9kyzaFZpjC5xtVL985G1ahFJUV-0ln6gGurMwc9DgNvqSKNCJT1tSAB",
                       "clientIp": "10.0.2.15", "systemCode": "tc",
                       "clientId": "4110b22812f3cb8ec988a097a255f9613c3d3deaef9c",
                       "versionType": "android", "refId": "42931004", "area": "1|25|321",
                       "versionNumber": "10.0.0", "manufacturer": "HUAWEI"},
        "AndroidImei": "",
        "sxx": "3f75bea2b1becd8d11e7e23fc7dbd022",
        "clientId": "4110b22812f3cb8ec988a097a255f9613c3d3deaef9c",

    },  # 设备参数及其他重要值
    "token": {
        "memberIdNew": "7-BwMboYz5q9dHFcG6JzbK2yflTKH_oIMEtkYUCd_UILBEf8C2b2v8STE-wsp4jljTiZTBGCP8ozgb8lyM73OrS9MM4MVdDXQx2JxPJfzureh-abAydqce7E-FN1qVXu37mxocWwgeuwbQlYUF-ZuDOuJfvpAu0DfL74-axONixnZqJSKsAaa9H8ZWM2jTGBAB",
        "memberId": "I0_c180aade647be173443ed339aa68dafc", "loginName": "16521956748", "userName": "尊敬的会员",
        "mobile": "16521956748", "email": "",
        "password": "ZeR59UsiEgmG2kf0+QB0n3cEWilY/9lS1k41PREbc3ghqUd36aHnfpXUmxvlzgOd",
        "oldPassword": "",
        "trueName": "16521956748", "isBlack": "0", "externalMemberId": "4887bb96e31d6680d09091bf10d88983",
        "sUserList": [
            {"socialType": "4", "accessToken": "", "userId": "oOCyauGWqA6B6UN8NBD9-2ler4vQ",
             "unionId": "ohmdTt8P6GI2cr6mBZVGmOq1jtac", "bindDate": "2019-4-14 13:08:34"}]},  # 用于二次登录的重要 token
    "proxy": "",  # 代理IP
    "phone": "16521956748",
    "pwd": "12345678@"
}

Dict_18300194952 = {
    "status": 0,
    "user_type": "2",
    "device": {
        "clientInfo": {"mac": "37:53:68:28:11:d9",
                       "extend": "4^9.0.0,5^samsung SM-G930K,6^-1,os_v^28,app_v^10.0.0.2,devicetoken^20200323173110fa0a5fa3d5c3ed152b5f0469a166f17001c74af463e38cbd",
                       "device": "6cozvlek7235fj0|armeabi-v7a|1080*1920*480|samsung SM-G930K|zgu4vabkkfk24u6",
                       "deviceId": "6cozvlek7235fj0", "manufacturer": "samsung",
                       "clientIp": "192.36.230.22", "networkType": "wifi",
                       "pushInfo": "jah523cv4ssrml95idyru0zx3h3r3yqluufb8axa", "systemCode": "tc",
                       "clientId": "911600a48e140d7601856ff6690a706a50c05f17e4ad",
                       "versionType": "android", "refId": "42931004", "area": "||",
                       "versionNumber": "10.0.0"},
        "AndroidImei": "",
        "sxx": "d825026657e045b1d6eec0db6431268f",
        "clientId": "911600a48e140d7601856ff6690a706a50c05f17e4ad",

    },  # 设备参数及其他重要值
    "token": {
        "memberIdNew": "YYhSaw1NSYRqX0MNtgs8xAhqkd_NFEzUyW0SkAf9Xxp8KTi35HA6zJhy4x65mM9DUx6pVj1o2TuGIn-V39rni-apEG49tGcm1YR1JuLxrHbNvxC4IyBQ6A0gbFfR-NILSkobxWb1zhY-WddP_bvVd7jVEuZwZbcfjM98qgr-IPFnZqJSKsAaa9H8ZWM2jTGBAB",
        "versionNo": "", "isSocialMember": "0", "isblack": "0",
        "memberId": "I0_338edd527d638078fa4f52ae639c4168",
        "externalMemberId": "566b01090789a3cefc7a0800af29c41f", "loginName": "18300194952",
        "userName": "尊敬的会员",
        "mobile": "18300194952", "email": "",
        "password": "/n+TGltm6VpGQoyPjTwWg2tKkiLpKb4d/mhgrEkhanplbalcpGtkkcKXScCdgsnG",
        "trueName": "18300194952",
        "score": "0",
        "sUserList": [{"socialType": "4", "accessToken": "", "userId": "oOCyauNHT8c0brsBkcFLy7tPpB3U",
                       "unionId": "ohmdTt5lLiNXktoEVc1PsgvkS5wk", "bindDate": "2019-10-17 19:38:23"}],
        "userId": "", "socialType": "", "cityId": "0", "cityName": "",
        "headImg": "https://pic5.40017.cn/i/ori/PELe6f5TBC.jpg", "provinceId": "0", "provinceName": "",
        "authorizeCode": "",
        "socialUserLists": {"isWxMulBind": "0", "isCanUnbind": "0", "isCanUnbindElong": "0",
                            "isShowWxCheck": "1",
                            "sUserList": [{"socialType": "4", "accessToken": "",
                                           "userId": "oOCyauNHT8c0brsBkcFLy7tPpB3U",
                                           "unionId": "ohmdTt5lLiNXktoEVc1PsgvkS5wk",
                                           "bindDate": "2019-10-17 19:38:23"}]}}}

Dict_16571555934 = {
    "status": 0,
    "user_type": "2",
    "proxy": "",  # 代理IP
    "phone": "16571555934",
    "pwd": "vrvrvr1",
    "device": {
        "clientInfo": {"versionType": "android", "area": "1|32|394",
                       "clientId": "4110966ac3d628bbbc96048c95e11c1f62e19c16f26f",
                       "deviceId": "c3a74964878a5d24",
                       "versionNumber": "10.0.0", "mac": "02:00:00:00:00:00",
                       "manufacturer": "Xiaomi",
                       "extend": "4^8.0.0,5^MI 5,6^-1,os_v^26,app_v^10.0.0.3,devicetoken^20200413145123decba7cba3c107d976a64ce6f5e412c90145320258f47e22,memberidnew^YYhSaw1NSYRqX0MNtgs8xC1r8s4fGjdJ-gBEAQaiIqlBKA04M-a-Az9fu65_z5skbtDYCqwql4ErrqjYcM0_pXWq0CM2WOhxIaMQMncU6wjl_RfyRtco5piUPD2G3zdfZKwwQ4Ub1anbbPuguc98iR4KFviByePt2IYwlcuKM_RnZqJSKsAaa9H8ZWM2jTGBAB",
                       "systemCode": "tc", "clientIp": "192.168.1.119",
                       "refId": "16359978", "networkType": "wifi",
                       "device": "c3a74964878a5d24|arm64-v8a|1080*1920*480|MI 5|406a0cf9",
                       "pushInfo": "09ada374abeff0a5466e9f70df758f917beec3ea"},
        "AndroidImei": "",
        "sxx": "da5795c5b7422194a5286f1803d82ca1",
        "clientId": "4110966ac3d628bbbc96048c95e11c1f62e19c16f26f",

    },  # 设备参数及其他重要值
    "token": {"tanping": {"content": []},
              "memberIdNew": "YYhSaw1NSYRqX0MNtgs8xC1r8s4fGjdJ-gBEAQaiIqlBKA04M-a-Az9fu65_z5skbtDYCqwql4ErrqjYcM0_pcu2qcPPaeTk0bEozPU6wKlkYt84ttVMt3nSTV3xIlW53-fdQrqIK-5DaEMdEMoFhFQlQKOgf0d78jMJvt3lj7xF-xS0YEnvaxc9BXR_MVavAB",
              "versionNo": "", "isSocialMember": "0", "regexLogin": "", "isblack": "0",
              "memberId": "I0_052d2937d91158ce154783254f3cc22f",
              "externalMemberId": "ff00837b1297c1a851700e76af4610fd", "loginName": "16571555934",
              "userName": "尊敬的会员", "mobile": "16571555934", "email": "",
              "password": "/n+TGltm6VpGQoyPjTwWg2tKkiLpKb4d/mhgrEkhanplbalcpGtkkcKXScCdgsnG",
              "trueName": "16571555934", "score": "0", "sUserList": [
            {"socialType": "4", "accessToken": "", "userId": "oOCyauKvECQUmQHwzUqdqAv9jVlA",
             "unionId": "ohmdTt7V95yU9mTg8ETqswgbmTIs", "bindDate": "2019-10-17 19:59:55"}], "userId": "",
              "socialType": "", "cityId": "0", "cityName": "",
              "headImg": "https://pic5.40017.cn/i/ori/PELe6f5TBC.jpg", "provinceId": "0",
              "provinceName": "",
              "authorizeCode": "y4hmNwdCT6uc8Nti0FpRX9b2w6x5SdkaNaOtCJ/q9ZM0MKb4IsahtTJaEgaEUt9WTOcKFytZuD94vOYj7gkxjg=="}}

Dict_16531044495 = {
    "status": 0,
    "user_type": "2",
    "proxy": "",  # 代理IP
    "phone": "16531044495",
    "pwd": ".....",
    "device": {
        "clientInfo": {"versionType": "android", "area": "1|32|394",
                       "clientId": "31100101ca8ed2f4bb8c696d1e52f7a89cd6870532da",
                       "deviceId": "c27a9485c8f80f74",
                       "versionNumber": "10.0.0", "mac": "02:00:00:00:00:00",
                       "manufacturer": "Xiaomi",
                       "extend": "4^8.0.0,5^MI 5,6^-1,os_v^26,app_v^10.0.0.3,devicetoken^20200413145123decba7cba3c107d976a64ce6f5e412c90145320258f47e22,memberidnew^Ioe2wFckEOdxWv2EkI78Vg-hRD4jzFIj9v44NFDtu4ixGUhAI1dlp-YMfUZ7dWGnzbB-1k5m2GyYWbEeGxTMAa24hzpfv5QWctoQCN0S-e1gab2IHH_SYuE6pSF2907yc4BTSAqY-XXi8kOloXUWkfuPcnaRhaTLBP1BezeU3BruIO-OwTMhWa1TACr32fc6AB",
                       "systemCode": "tc", "clientIp": "192.168.1.100",
                       "refId": "16359978", "networkType": "wifi",
                       "device": "c27a9485c8f80f74|arm64-v8a|1080*1920*480|MI 5|406a0cf9",
                       "pushInfo": "f4497daa8181c71647c0b1c7cd22bfac8112614f"},
        "AndroidImei": "",
        "sxx": "fcc31597471e83ddab5bb7688b3f3314",
        "clientId": "31100101ca8ed2f4bb8c696d1e52f7a89cd6870532da",

    },  # 设备参数及其他重要值
    "token": {"tanping": {"content": []},
              "memberIdNew": "Ioe2wFckEOdxWv2EkI78Vg-hRD4jzFIj9v44NFDtu4ixGUhAI1dlp-YMfUZ7dWGnzbB-1k5m2GyYWbEeGxTMAei3IyPzaQ6xfCyt9cA5jDVVZ9mNMcwzuOHp3Kej4PUCc4BTSAqY-XXi8kOloXUWkXeQ93O3POl3vW10dYEV2ckYBVJ6tONLvEvpo8cXPikIAB",
              "versionNo": "", "isSocialMember": "0", "regexLogin": "", "isblack": "0",
              "memberId": "I0_f80d47e6db63f7f5fdc46f49d7f6e3a9",
              "externalMemberId": "b2cdd0479170af6a5520adea258d2f28", "loginName": "16531044495",
              "userName": "尊敬的会员", "mobile": "16531044495", "email": "",
              "password": "+raXxSau6+dVusK+Uk6ivHfxs5n0hE2Nc3lqAOZwQ9VV32yiBdO7uQCpJ/UbseJr",
              "trueName": "16531044495", "score": "0", "sUserList": [
            {"socialType": "4", "accessToken": "", "userId": "oOCyauBvoR1LX_ClQ3owwg-YHxcw",
             "unionId": "ohmdTt8ErSqKXxWLqH013maUlM4k", "bindDate": "2020-5-8 22:08:13"}], "userId": "",
              "socialType": "", "cityId": "0", "cityName": "",
              "headImg": "https://pic5.40017.cn/i/ori/PELe6f5TBC.jpg", "provinceId": "0",
              "provinceName": "",
              "authorizeCode": "LyhDBYwlNJ9Ams8DGaGSft96tcq42jw47I+kZn5O/750uGGsQ8xDjvt7XQ6JsfGbRgTjeNj4QaSvrO/549BiKA=="}}

