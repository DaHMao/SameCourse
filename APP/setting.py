import requests
import time
import random
import hashlib
import json
from Crypto.Cipher import AES
from binascii import a2b_base64
from urllib import parse
from APP.ABY_porxy import porxy_pool

mileageSteps = [4000, 2000, 1000, 600, 200]  # 里程兑换列表
# mileageSteps = [4000]

Pwd = ["vrvrvr1", "asdj23233", "cecece1"]  # 旧账号的密码列表

URL = "http://192.168.0.98:12004"  #

URL_ycc = "http://192.168.0.29:11005"


def log_wechat_author(taskid, app_id, success, vxid, phone=""):
    """
      记录微信授权
    :param taskid:
    :param app_id:
    :param success:
    :param vxid:
    :param phone:
    :return:
    """
    data = {
        "taskid": taskid,
        "phone": phone,
        "app_id": app_id,
        "success": success,
        "vxid": vxid
    }
    res = requests.post(url=URL + "/logWeChatAuth.do", json=data)
    print(res.text)


def get_get_user_do(phone):
    """
    根据电话号码获取指定账号的登录信息
    :param phone:
    :return:
    """
    res = requests.post(url=URL + "/getUser.do", json={"phone": phone}).json()
    if res.get("status") == 0:
        return res
    else:
        return res


def get_set_token_sta(phone, i_d):
    """
    获取的账号不能使用里程下单，
    :param phone:
    :param i_d:
    :return:
    """
    res = requests.post(url=URL + "/setVxTokenSta.do",
                        json={"phone": phone, "can_use_integral": i_d})
    print(res.text)


aip_token = "9a8553c606c2c837187614cd1ce2b926540aebeb"  # 接码平台api


def prohibit_coupon(type_id):
    """
    短时间禁用某红包
    :param type_id: 优惠劵类型ID
    :return:
    """
    data = {
        "type_id": type_id,
    }
    res = requests.get(url=URL + "/disCoupon.do", json=data)
    if res.text == "OK":
        return True
    else:
        return {
            "status": 3,
            "msg": "领取红包失败，设置该类红包禁用失败"
        }


def dict_to_json(body):
    return json.dumps(body, separators=(',', ':'))


def dict_to_json_two(body):
    return json.dumps(body, separators=(',', ':'), ensure_ascii=False)


# headers 中的参数
# devicetoken 参数暂时作为配置文件固定

devicetoken = "20200323173110fa0a5fa3d5c3ed152b5f0469a166f17001c74af463e38cbd"


def get_time():
    return str(int(time.time() * 1000))


def get_time_stamp():
    """
    返回17位时间戳 eg:20200421135352059
    :return:
    """
    local_time = time.localtime(time.time())
    data_head = time.strftime("%Y%m%d%H%M%S", local_time)
    data_secs = (time.time() - int(time.time())) * 1000
    time_stamp = "%s%03d" % (data_head, data_secs)
    return time_stamp


def get_count(count):
    """
    返回访问次数 eg:00001
    :param count:
    :return:
    """
    call_count = "%05d" % count
    return call_count


def get_push_info():
    """"""
    look = 'abcdefghijklmnopqrstuvwxyz0123456789'
    push_info = ''.join(random.choices(look, k=40))
    return push_info


def get_device_profile(device):
    wait_encrypt_str = device + "tcmobile2016"
    md5_encrypt = hashlib.md5(wait_encrypt_str.encode(encoding='UTF-8')).hexdigest()
    return md5_encrypt


def get_device_id():
    look = 'abcdefghijklmnopqrstuvwxyz0123456789'
    device_id = ''.join(random.choices(look, k=15))
    return device_id


def get_digital_sign(req_time, service_name, version):
    data_str = f"AccountID=c26b007f-c89e-431a-b8cc-493becbdd8a2&ReqTime={req_time}&" \
        f"ServiceName={service_name}&Version={version}8874d8a8b8b391fbbd1a25bda6ecda11"
    md5_encrypt = hashlib.md5(data_str.encode(encoding="UTF-8")).hexdigest()
    return md5_encrypt


def get_req_data(req_str):
    req = req_str + "4957CA66-37C3-46CB-B26D-E3D9DCB51535"
    md5_encrypt = hashlib.md5(req.encode(encoding="UTF-8")).hexdigest()
    return md5_encrypt


def get_device_info():
    mobile_list = ['Xiaomi', 'OPPO', 'HUAWEI', 'samsung', 'vivo']
    mobile_version_dict = {'Xiaomi': ['MI 9', 'MI 5'], 'OPPO': ['OPPO R17', 'OPPO R11'],
                           'HUAWEI': ['HUAWEI MLA-AL10', 'HUAWEI ALP-AL00', 'HUAWEI MLA-L12'],
                           'samsung': ['samsung SM-N960F', 'samsung SM-G955N', 'samsung SM-G9350', 'samsung SM-G930K'],
                           'vivo': ['vivo X9i', 'vivo X20A', 'vivo X20']}
    android_version_list = ['9.0.0']
    look = 'abcdefghijklmnopqrstuvwxyz0123456789'
    device_id = ''.join(random.choices(look, k=15))
    sequence_num = ''.join(random.choices(look, k=15))
    mac = [
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)]
    mac = ':'.join(map(lambda x: "%02x" % x, mac))
    mobile = random.choice(mobile_list)
    android_version = random.choice(android_version_list)
    mobile_version = random.choice(mobile_version_dict[mobile])
    extend = f"4^{android_version},5^{mobile_version},6^-1,os_v^28,app_v^10.0.0.2,devicetoken^{devicetoken}"
    device = f"{device_id}|armeabi-v7a|1080*1920*480|{mobile_version}|{sequence_num}"
    client_ip = f'{random.choice(["192", "127", "172", "10"])}.{random.randint(0, 255)}.' \
        f'{random.randint(0, 255)}.{random.randint(0, 255)}'

    device_info = {
        "mac": mac,
        "extend": extend,
        "device": device,
        "deviceId": device_id,
        "manufacturer": mobile,
        "clientIp": client_ip,
        "networkType": "wifi",
        "pushInfo": get_push_info(),
        "systemCode": "tc",
        "clientId": "00000000000000000000",
        "versionType": "android",
        "refId": "42931004",
        "area": "||",
        "versionNumber": "10.0.0",
    }
    return device_info


def get_secsign(body):
    url = "http://192.168.0.62:8696/secsign.do?"
    data = body
    res = requests.get(url=url, params=data)
    return res.text


def get_password(password):
    url = f'http://192.168.0.62:8696/password.do?pwd={parse.quote(password)}'
    res = requests.get(url=url)
    return res.text


def http_do_decrypt(s="", p="30d082f152924c7f8f12e6df427a9459", i="234567899876ABCD"):
    """
    加密
    :param s:
    :param p:
    :param i:
    :return:
    """
    url = "http://tool.chacuo.net/cryptaes"
    headers = {
        "Host": "tool.chacuo.net",
        "Connection": "keep-alive",
        # "Content-Length": "17993",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML"
                      ", like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://tool.chacuo.net",
        "Referer": "http://tool.chacuo.net/cryptaes",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    data = {
        "data": s,
        "type": "aes",
        "arg": f"m=cbc_pad=pkcs5_block=128_p={p},_i={i}_o=0_s=utf-8_t=0"
    }
    try:
        res = requests.post(url=url, data=data, headers=headers, proxies=porxy_pool.get_proxy()).json()
        if res.get("status") == 1:
            print(res)
            return res.get("data")[0]
        else:
            print("获取secsign失败")
            return {
                'status': 1, 'msg': "请不要这么快提交，稍后再试",
            }
    except Exception:
        return {
            'status': 1, 'msg': "请不要这么快提交，稍后再试",
        }


def do_decrypt(key, text):
    """
    解密 AES.CBC
    :param key: 秘钥
    :param text: 解密字符串
    :return:
    """
    key = key.encode('utf-8')
    mode = AES.MODE_CBC
    crypt_or = AES.new(key, mode, b'234567899876ABCD')
    plain_text = crypt_or.decrypt(text)
    print(plain_text)
    return a2b_base64(plain_text)


def do_raw_text(user, pwd):
    """
    :param user:
    :param pwd:
    :return:
    """
    url = f"http://192.168.0.62:8696/rawText.do?phone={user}&pwd={pwd}"
    res = requests.get(url)
    return res.text


def perform_first_sign_in(data):
    """
    APP注册成功后执行首次签到
    :param data:请求参数
    :return: 里程数
    """
    url = URL_ycc + "/appSign.do"
    res = requests.post(url=url, json=data).json()
    if res.get("status") == 0:
        return res.get("integral")
    return {
        "status": 3,
        "msg": "注册成功，签到失败，未绑定微信",
    }


def perform_get_integral(data):
    """
    获取里程数
    :return: 里程数
    """
    url = URL_ycc + "/getIntegral.do"
    res = requests.post(url=url, json=data).json()
    if res.get("status") == 0:
        return res.get("integral")
    return {
        "status": 3,
        "msg": "获取里程数失败",
    }


def get_red_envelopes(data):
    """
    领取红包
    :return:
    """
    res = requests.post(url=URL_ycc + "/getCoupon.do", json=data).json()
    if res.get("status") in (0, 1):
        return res.get("ID")
    else:
        res = prohibit_coupon(type_id=data.get("coupon").get("type_id"))
        if isinstance(res, dict):
            res["msg"] = f"生单失败,{res.get('msg')}"
            return res
        return "请重新获取账号"


AgeType = {
    "ADT": "1",
    "CHD": "",
    "INF": "",
}

CabinTypeName = {
    1: "航司旗舰店",
    2: "同程特惠",
    3: "品质出行",
    4: "公务舱",
}

Android = [
    "862095513523651",
    "865371194729181",
    "860193570443723",
    "867078895963757",
    "866273050292917",
    "864115355264764",
    "862013281129114",
    "862677959424765",
    "865222654150717",
    "862602475155743",
    "861721950283035",
    "866531327926157",
    "865376262852377",
    "862788182542370",
    "863466130615072",
    "863711236724348",
    "861495528193436",
    "862554755499202",
    "862975863741369",
    "864743711252221",
    "866531004476807",
    "867016220857609",
    "862434987911482",
    "863253261346200",
    "863371001731539",
    "866254175535224",
    "863170211576944",
    "864277751452540",
    "862354243322433",
    "862157512612214",
    "865059527912133",
    "865315597363734",
    "866355791360556",
    "863315542453947",
    "862106738197732",
    "861691947201749",
    "867951231760493",
    "862154388583413",
    "861292104323648",
    "868533345889175",
    "862942515008233",
    "865790774520530",
    "864653949530852",
    "863775663140351",
    "862397541879125",
    "867492124672065",
    "864077377145811",
    "862735454533744",
    "860413517072447",
    "864158613783241",
    "862211311875710",
    "863358314042753",
    "863638927552144",
    "862739861802171",
    "862523400718795",
    "866000155770210",
    "863705336971577",
    "861247154712223",
    "866633250402709",
    "861543727150721",
    "863549204843371",
    "861424396519373",
    "860397452644742",
    "861463272181775",
    "860724351144971",
    "864457784524735",
    "865514470473228",
    "865132755611527",
    "862979937572115",
    "867272433224877",
    "863240145973150",
    "868798446595837",
    "867446152902083",
    "867148857736309",
    "863000356177945",
    "860932224271174",
    "866408787530821",
    "867476877139042",
    "867507052805039",
    "867285418110630",
    "862518314254812",
    "861155153416326",
    "866253548655628",
    "861444773644412",
    "867252727614728",
    "861326341531199",
    "861473312111401",
    "869359243733771",
    "865806036077729",
    "865450854147478",
]

# 用三字码查询城市列表
city_name = {'AQG': '安庆', 'AVA': '安顺', 'AOG': '鞍山', 'AKA': '安康', 'AKU': '阿克苏', 'AAT': '阿勒泰', 'YIE': '阿尔山',
             'AMR': '阿拉善盟', 'AXF': '阿拉善左旗', 'RHT': '阿拉善右旗', 'AHJ': '红原', 'NGQ': '阿里', 'AHT': '阿图什', 'AYN': '安阳',
             'AJB': '安吉', 'AEC': '阿拉尔', 'MFM': '澳门', 'BFU': '蚌埠', 'PEK': '北京', 'AEB': '百色', 'BHY': '北海', 'BAV': '包头',
             'BDL': '巴音郭楞', 'BSD': '保山', 'NBS': '白山', 'ETL': '博尔塔拉', 'RLK': '巴彦淖尔', 'DBC': '白城', 'BPL': '博乐',
             'BFJ': '毕节', 'BYE': '白银', 'BZX': '巴中', 'BJC': '宝鸡', 'BAD': '保定', 'BZJ': '亳州', 'BBU': '滨州', 'BXC': '本溪',
             'BSZ': '白沙', 'BIC': '保亭', 'BIF': '北安', 'BPO': '北票', 'CGD': '常德', 'CSX': '长沙', 'CGQ': '长春', 'CZX': '常州',
             'CHG': '朝阳', 'CIF': '赤峰', 'CIH': '长治', 'CTU': '成都', 'BPX': '昌都', 'CXD': '楚雄', 'CKG': '重庆', 'JUH': '九华山',
             'CDE': '承德', 'CNI': '长海', 'CWJ': '沧源', 'CJE': '昌吉', 'CZD': '郴州', 'CIA': '从化', 'SWA': '汕头', 'CZI': '沧州',
             'CHD': '巢湖', 'CZZ': '滁州', 'CSJ': '常熟', 'CXE': '慈溪', 'CZV': '崇左', 'CMN': '澄迈', 'CLW': '昌黎', 'CJX': '昌江',
             'CJQ': '昌江黎族自治县', 'DQA': '大庆', 'DXL': '大兴安岭', 'DLC': '大连', 'DDG': '丹东', 'DOY': '东营', 'DAT': '大同',
             'DAX': '达州', 'DYB': '德阳', 'DLU': '大理', 'LUM': '芒市', 'DIG': '迪庆', 'DNH': '敦煌', 'HXD': '德令哈', 'DCY': '稻城',
             'DOJ': '都江堰', 'DXQ': '儋州', 'DGQ': '东莞', 'DZB': '德州', 'DYC': '丹阳', 'HEW': '东阳', 'DXN': '定西', 'DZX': '大足',
             'DFX': '东方', 'DAE': '定安', 'DYX': '大庸', 'DEQ': '德清', 'DHU': '敦化', 'DGB': '东港', 'DYV': '都匀', 'DHE': '德惠',
             'DF1': '丹凤', 'DSX': '东沙岛', 'ENH': '恩施', 'DSN': '鄂尔多斯', 'ERL': '二连浩特', 'EJN': '额济纳旗', 'EMQ': '峨眉山',
             'ENP': '恩平', 'EZH': '鄂州', 'FUG': '阜阳', 'FOC': '福州', 'FUO': '佛山', 'FYN': '富蕴', 'FYJ': '抚远', 'FCG': '防城港',
             'FEH': '奉化', 'FUX': '阜新', 'FUS': '抚顺', 'FHX': '凤凰', 'FUZ': '抚州', 'FUD': '福鼎', 'FQU': '福泉', 'FCE': '凤城',
             'CAN': '广州', 'KWL': '桂林', 'KWE': '贵阳', 'KOW': '赣州', 'GZG': '甘孜', 'GYS': '广元', 'GYU': '固原',
             'GNW': '甘南藏族自治州', 'GGA': '贵港', 'GMQ': '果洛', 'GNX': '广安', 'GOQ': '格尔木', 'GBI': '高碑店', 'GHG': '根河',
             'KHH': '高雄', 'HFE': '合肥', 'TXN': '黄山', 'HUZ': '惠州', 'HAK': '海口', 'HDG': '邯郸', 'HRB': '哈尔滨', 'HEK': '黑河',
             'HNY': '衡阳', 'HJJ': '芷江', 'HDL': '葫芦岛', 'HET': '呼和浩特', 'HLD': '呼伦贝尔', 'HZG': '汉中', 'HMI': '哈密',
             'HTN': '和田', 'HGH': '杭州', 'HIA': '淮安', 'HZO': '湖州', 'HCJ': '河池', 'HXA': '海西蒙古族藏族自治州', 'HUO': '霍林郭勒',
             'HTT': '花土沟', 'HYN': '台州', 'HBI': '鹤壁', 'HEY': '河源', 'HGS': '黄石', 'HZE': '菏泽', 'HSU': '衡水', 'HBE': '淮北',
             'HNE': '淮南', 'HNJ': '海宁', 'HIC': '海城', 'HEG': '鹤岗', 'HCS': '珲春', 'HHS': '红河', 'FCS': '防城', 'HGB': '黄冈',
             'HYX': '海盐', 'HDO': '海东', 'HND': '黄南', 'HNZ': '海南藏族自治州', 'HZS': '贺州', 'HUA': '侯马', 'HUP': '化州',
             'HYM': '华阴', 'HXI': '华蓥', 'HYH': '海阳', 'HUN': '花莲', 'HCN': '恒春', 'JGN': '嘉峪关', 'CHW': '酒泉', 'JXA': '鸡西',
             'JMU': '佳木斯', 'JIL': '吉林', 'KNC': '吉安', 'JDZ': '景德镇', 'JIU': '九江', 'JNZ': '锦州', 'TNA': '济南', 'JNG': '济宁',
             'JNH': '金华', 'JIC': '金昌', 'JXS': '嘉兴', 'JYI': '江阴', 'SHS': '荆州', 'JGS': '井冈山', 'JGD': '加格达奇', 'JSJ': '建三江',
             'JHG': '西双版纳', 'JSN': '吉首', 'JMN': '荆门', 'JYA': '济源', 'JCS': '晋城', 'JMA': '江门', 'JZU': '焦作', 'JJN': '泉州',
             'JID': '建德', 'JDU': '江都', 'JIZ': '胶州', 'JZH': '九寨沟', 'JYX': '缙云', 'JSX': '嘉善', 'JZO': '晋中', 'JMP': '即墨',
             'JAY': '简阳', 'JHE': '蛟河', 'KNH': '金门', 'CYI': '嘉义', 'KHG': '喀什', 'KRY': '克拉玛依', 'KMG': '昆明', 'KVN': '昆山',
             'KRL': '库尔勒', 'KCA': '库车', 'KJH': '凯里', 'KTP': '奎屯', 'KPD': '开平', 'KFC': '开封', 'KJI': '喀纳斯', 'KGT': '康定',
             'KAH': '开原', 'KZL': '克孜勒苏柯尔克孜自治州', 'LCX': '龙岩', 'LHW': '兰州', 'LZH': '柳州', 'LYA': '洛阳', 'LYG': '连云港',
             'LYI': '临沂', 'LZO': '泸州', 'LXA': '拉萨', 'LZY': '林芝', 'LJG': '丽江', 'LNJ': '临沧', 'LFQ': '临汾', 'LHC': '丽水',
             'LLB': '荔波', 'LPF': '六盘水', 'JMJ': '澜沧', 'LLV': '吕梁', 'LXB': '临夏', 'LSF': '乐山', 'LZB': '阆中', 'LDC': '娄底',
             'LHD': '漯河', 'LCK': '聊城', 'LAG': '六安', 'LWP': '莱芜', 'LXX': '兰溪', 'LYN': '溧阳', 'LXZ': '莱西', 'LHB': '临海',
             'LYD': '辽阳', 'LYY': '辽源', 'LPZ': '梁平', 'HZH': '黎平', 'LDT': '乐东', 'LBG': '来宾', 'LGV': '临高', 'LSD': '陵水',
             'LSG': '庐山', 'LFA': '廊坊', 'LCS': '连城', 'LPW': '滦平', 'LIN': '临安', 'LYZ': '龙游', 'LNL': '陇南',
             'LSR': '凉山彝族自治州', 'LYF': '耒阳', 'LFE': '陆丰', 'LCU': '乐昌', 'LNA': '涟源市', 'LJS': '冷水江', 'LIJ': '乐平',
             'LBH': '灵宝', 'LHH': '凌海', 'LOJ': '潞城', 'LFH': '兰坪', 'LZL': '莲洲', 'GNI': '绿岛', 'KYD': '兰屿', 'MXZ': '梅县',
             'MDG': '牡丹江', 'MIG': '绵阳', 'NZH': '满洲里', 'OHE': '漠河', 'MMR': '茂名', 'MAC': '马鞍山', 'MZS': '蒙自', 'MIQ': '绵竹',
             'MSK': '眉山', 'MLH': '穆棱', 'MHJ': '梅河口', 'YUN': '密云', 'MQI': '莫力达瓦达斡尔族自治旗', 'MFK': '马祖', 'MZG': '马公',
             'NNP': '南平', 'NNG': '南宁', 'NNY': '南阳', 'NKG': '南京', 'NTG': '南通', 'KHN': '南昌', 'NAO': '南充', 'NGB': '宁波',
             'NLH': '宁蒗', 'NJB': '内江', 'NHB': '南海', 'NID': '宁德', 'NHY': '宁海', 'NQX': '那曲', 'NJX': '怒江', 'NSD': '南沙',
             'LHJ': '讷河', 'NNC': '宁安', 'NJJ': '嫩江', 'LZN': '南竿', 'PZI': '攀枝花', 'SYM': '普洱', 'PLB': '平凉', 'PDQ': '平顶山',
             'PXB': '萍乡', 'PUO': '濮阳', 'PTE': '莆田', 'PLG': '蓬莱', 'PHH': '平湖', 'PJD': '盘锦', 'PYZ': '平遥', 'PNW': '普宁',
             'PZC': '彭州', 'PIF': '屏东', 'IQN': '庆阳', 'QDN': '黔东南', 'QXN': '黔西南', 'BPE': '秦皇岛', 'NDG': '齐齐哈尔',
             'TAO': '青岛', 'JUZ': '衢州', 'BAR': '琼海', 'QJA': '曲靖', 'IQM': '且末', 'JIQ': '黔江', 'QZO': '钦州', 'QIJ': '潜江',
             'QYN': '清远', 'QUF': '曲阜', 'QIT': '七台河', 'QZX': '琼中', 'QAS': '迁安', 'QID': '启东', 'QXX': '黔西', 'HBQ': '祁连',
             'QIH': '千岛湖', 'QZH': '青州', 'QNB': '黔南布依族苗族自治州', 'XXA': '栖霞', 'CMJ': '七美', 'RIZ': '日照', 'RKZ': '日喀则',
             'RUL': '瑞丽', 'RAD': '瑞安', 'RQA': '若羌', 'SZX': '深圳', 'SYX': '三亚', 'SJW': '石家庄', 'SHE': '沈阳', 'SHA': '上海',
             'SXF': '绍兴', 'SZV': '苏州', 'WDS': '十堰', 'SHF': '石河子', 'SQJ': '三明', 'SQD': '上饶', 'WGN': '邵阳', 'SUS': '宿迁',
             'SXJ': '鄯善', 'QSZ': '莎车', 'HPG': '神农架', 'YSQ': '松原', 'SYQ': '思茅', 'SNX': '遂宁', 'SZQ': '石嘴山', 'SMF': '三门峡',
             'SZC': '朔州', 'SSF': '韶山', 'SZB': '随州', 'HSC': '韶关', 'SWF': '汕尾', 'SKA': '商丘', 'XIO': '宿州', 'SES': '三河',
             'SSB': '石狮', 'SAI': '上虞', 'SPA': '四平', 'SUC': '绥化', 'SYB': '双鸭山', 'SFB': '绥芬河', 'SPX': '松潘', 'SFW': '什邡',
             'SDA': '顺德龙山', 'SMD': '三门', 'SKF': '商洛', 'SND': '山南', 'SZO': '嵊州', 'SSU': '嵊泗', 'SZT': '深州', 'THQ': '天水',
             'TKM': '铜陵', 'TNH': '通化', 'TGO': '通辽', 'TYN': '太原', 'TSN': '天津', 'TLQ': '吐鲁番', 'TCG': '塔城', 'TVS': '唐山',
             'YTY': '扬州', 'TEN': '铜仁', 'TCZ': '腾冲', 'TCM': '铜川', 'TSA': '台山', 'TMV': '天门', 'TAN': '泰安', 'TXA': '桐乡',
             'TAF': '太仓', 'TIS': '铁岭', 'TCV': '屯昌', 'TLC': '桐庐', 'TTY': '天台', 'TZA': '天柱', 'TWC': '图木舒克', 'TZB': '滕州',
             'TPE': '台北', 'TNN': '台南', 'TTT': '台东', 'RMQ': '台中', 'WUZ': '梧州', 'WUH': '武汉', 'WUX': '无锡', 'WUA': '乌海',
             'WEH': '威海', 'WEF': '潍坊', 'URC': '乌鲁木齐', 'WNH': '文山', 'WNZ': '温州', 'WHU': '芜湖', 'UCB': '乌兰察布',
             'WUS': '武夷山', 'HLH': '乌兰浩特', 'WXN': '万州', 'WUW': '武威', 'WZS': '吴忠', 'WEN': '渭南', 'WXI': '武穴', 'WJI': '吴江',
             'WEG': '温岭', 'DTU': '五大连池', 'WNB': '万宁', 'WEC': '文昌', 'WYX': '婺源', 'WYC': '武义', 'XZS': '五指山', 'WJQ': '五家渠',
             'WCB': '五常', 'WOM': '武安', 'WSK': '巫山', 'WOT': '望安', 'XMN': '厦门', 'XNT': '邢台', 'XFN': '襄阳', 'XUZ': '徐州',
             'XIL': '锡林浩特', 'XAM': '兴安盟', 'XNN': '西宁', 'XIY': '咸阳', 'WUT': '忻州', 'ACX': '兴义', 'GXH': '夏河', 'NLT': '新源',
             'XIC': '西昌', 'XIT': '湘潭', 'XIA': '仙桃', 'XCA': '许昌', 'XIX': '新乡', 'XGM': '孝感', 'XAI': '信阳', 'XAN': '咸宁',
             'XYU': '新余', 'XNS': '兴宁', 'XEN': '兴城', 'XXX': '湘西', 'XLA': '兴隆', 'XUC': '宣城', 'XCX': '新昌', 'XSS': '象山',
             'XAX': '兴安', 'XNX': '湘乡', 'HKG': '香港', 'HSZ': '新竹', 'LDS': '伊春', 'YIH': '宜昌', 'LLF': '永州',
             'YAF': '延边朝鲜族自治州', 'YNZ': '盐城', 'INC': '银川', 'YUS': '玉树', 'YNT': '烟台', 'YCU': '运城', 'ENY': '延安',
             'UYN': '榆林', 'YBP': '宜宾', 'YIN': '伊宁', 'YKH': '营口', 'YIW': '义乌', 'YNJ': '延吉', 'YIC': '宜春', 'YXV': '玉溪',
             'YAE': '雅安', 'YLU': '玉林', 'YJJ': '阳江', 'YFD': '云浮', 'YIY': '益阳', 'YYA': '岳阳', 'YQE': '阳泉', 'YIT': '鹰潭',
             'YIZ': '仪征', 'YIX': '宜兴', 'YKB': '永康', 'YHX': '余杭', 'YYS': '余姚', 'YMX': '元谋', 'YSR': '阳朔', 'YMI': '义马',
             'YKP': '牙克石', 'ZHA': '湛江', 'ZUH': '珠海', 'ZYI': '遵义', 'CGO': '郑州', 'DYG': '张家界', 'ZAT': '昭通', 'HSN': '舟山',
             'ZHY': '中卫', 'YZY': '张掖', 'ZUJ': '镇江', 'NZL': '扎兰屯', 'ZQZ': '张家口', 'ZIY': '资阳', 'ZGA': '自贡', 'ZHQ': '肇庆',
             'ZHC': '株洲', 'ZSB': '中山', 'ZCS': '增城', 'ZME': '驻马店', 'ZHK': '周口', 'ZZA': '枣庄', 'ZHZ': '漳州', 'ZIB': '淄博',
             'ZJI': '诸暨', 'ZHJ': '张家港', 'ZJS': '中江', 'ZDO': '肇东', "PVG": "浦东机场", "PKX": "大兴机场"}


def get_zhima_ip():
    """
    获取芝麻代理
    :return:
    """
    res = requests.get(
        url="http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1"
            "&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=").json()
    if res.get("code") == 0 and res.get("success"):
        ip = res.get('data')[0].get('ip')
        host = res.get('data')[0].get('port')
        return {
            "status": 0,
            "http": f"http://{ip}:{host}",
            "https": f"https://{ip}:{host}",
        }
    else:
        return {
            "status": 30,
            "msg": "获取芝麻ip失败"
        }


RoomCode = ["E", "L", "Q", "N", "W1"]
