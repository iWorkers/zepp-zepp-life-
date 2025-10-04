import requests
import sys
import urllib.parse
import time

def test_apptoken(apptoken):
    url = "https://api-mifit-cn3.zepp.com/v2/users/me/events"

    #8D2CE5A9-6876-4D61-B6D9-589A566C96B7  1759212397122   phn
    
    params = {
        "eventType": "phn",
        "limit": "200",    
    }
    
    headers = {
        "User-Agent": "Zepp/9.13.0 (iPhone; iOS 26.1; Scale/3.00)",
        "apptoken": apptoken
    }
    
    try:
        r = requests.get(url, params=params, headers=headers, timeout=5)
        return r.status_code == 200
    except:
        return False

def test_band(apptoken,userid):


    headers = {
        'Host': 'weixin.amazfit.com',
        'Connection': 'keep-alive',
        'hm-privacy-ceip': 'false',
        'Accept': '*/*',
        'channel': 'appstore',
        'apptoken': apptoken,
        'appname': 'com.huami.midong',
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'timezone': 'Asia/Shanghai',
        'X-Request-Id': '9726A384-E00F-4182-9041-BA13193EBAD5',
        'cv': '1403_8.9.1',
        'lang': 'zh_CN',
        'User-Agent': 'Zepp/8.9.1 (iPhone; iOS 17.3; Scale/3.00)',
        'appplatform': 'ios_phone',
        'country': 'CN',
        'v': '2.0',
        'hm-privacy-diagnostics': 'false',
    }

    params = {
        'brandName': 'amazfit',
        'userid': userid,
        'wxname': 'md',
    }

    response = requests.get('https://weixin.amazfit.com/v1/bind/qrcode.json', params=params, headers=headers).json()
    
    data = response # 获取 JSON 数据
    return data['data']['ticket']


def test_band_v2(apptoken,userid):
    headers = {
    "Host": "api-mifit-cn3.zepp.com",
    "User-Agent": "Zepp/9.13.0 (iPhone; iOS 26.1; Scale/3.00)",
    "Connection": "keep-alive",
    "appname": "com.huami.midong",
    "apptoken":  apptoken,
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br"
    }
    url = "https://api-mifit-cn3.zepp.com/v1/thirdParties/auth.json"
    params = {

        "userid": userid
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()  # 获取 JSON 数据
    print(data['data']['authInfo'])
    return build_alipay_url(data['data']['authInfo'])  # 获取指定字段

def build_alipay_url(info_str):
    # 解析info字符串为字典
    params_dict = urllib.parse.parse_qs(info_str)
    
    # 从info中提取需要的参数
    app_id = params_dict.get('app_id', [''])[0]
    sign = params_dict.get('sign', [''])[0]
    biz_type = params_dict.get('biz_type', [''])[0]
    auth_type = params_dict.get('auth_type', [''])[0]
    api_name = params_dict.get('apiname', [''])[0]
    scope = params_dict.get('scope', [''])[0]
    target_id = params_dict.get('target_id', [''])[0]
    product_id = params_dict.get('product_id', [''])[0]
    pid = params_dict.get('pid', [''])[0]
    
    # 构建基础URL（保留原有结构）
    url = 'https://authweb.alipay.com/auth?v=h5'
    
    # 添加从info中提取的参数
    if app_id: url += f'&app_id={app_id}'
    if sign: url += f'&sign={urllib.parse.quote(sign)}'
    if biz_type: url += f'&biz_type={biz_type}'
    if auth_type: url += f'&auth_type={auth_type}'
    if api_name: url += f'&apiname={api_name}'
    if scope: url += f'&scope={scope}'
    if target_id: url += f'&target_id={target_id}'
    if product_id: url += f'&product_id={product_id}'
    if pid: url += f'&pid={pid}'
    
    timestamp = int(time.time() * 1000)  # 毫秒级时间戳
    url += f'&mqpNotifyName=CashierAuth_{timestamp}'
    url += f'&clientTraceId={timestamp}'
    
    # 添加固定参数
    url += '&bundle_id=com.huami.watch'
    url += '&app_name=mc'
    url += '&msp_type=embeded-ios'
    url += '&method='
    
    return urllib.parse.quote(url)



if __name__ == "__main__":

    apptoken = "ZQVBQDZOQmJaR0YyajYmWnJoBAgAAAAAAYT1aZzhLRDkyWHlHWW0tSTJrSFdpQ3dIQUFBQVptYWo3cVUmcj0xMiZ0PWh1YW1pJnRpPWhoaGgwMDAwQHFxLmNvbSZoPTE3NTk1NTM1NDYwODQmaT04NjQwMDAmdXNlcm5hbWU9aGhoaDAwMDCsJfJIDwX_Qo3qBUaaRY_X"
    #apptoken = "ZQVBQFJyQktGHlp6QkpbRl5LRl5qek4uXAQABAAAAAC_pv2RE9jn82Rt6Jxe7kbB65__70hP1YGvIOO0KxMG-SBUq1kCEE2Ecm-a36nfkR9inM3MTMteVPnwWgyouG72gzp4iDEp0pVlaSrp1nEXlolepQe8oEIl1wTZnu4v6m_2VCibx6NFAqwIoQaDiKHM-cJCQ-9-o4P6vdNh7O1IcwPs7QhX2YtVX5b2ppG-m2A"
    userid = "1196601470"
    success = test_apptoken(apptoken)
    print(f"token: {'有效' if success else '无效'}")
    if success:
        result1=test_band(apptoken,userid)
        result=test_band_v2(apptoken,userid)
        print(result1 ,result)
    
