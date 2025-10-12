import requests
import json
import time
import platform
from datetime import datetime

def bind_device(app_token: str, firmware_version: str = "V8.8.8.88", 
                device_mac: str = "05:71:F1:BD:33:39", 
                device_id: str = "4780d0e4b6f7158e409ad42c31bc1436") -> dict:
    
    # 构建系统信息参数（根据APK代码分析）
    brand = "Xiaomi"
    sys_model = "Mi 10" 
    sys_version = "10"
    soft_version = "9.13.0"  # 应用版本号
    
    # 当前时间戳（秒级，与APK一致）
    app_time = int(datetime.now().timestamp())
    
    # 构建完整的请求参数（POST表单数据）
    payload = {
        # 系统信息参数（APK中新增）
        'brand': brand,
        'sys_model': sys_model,
        'sys_version': sys_version,
        'soft_version': soft_version,
        
        # 设备信息参数（原有+新增）
        #'device_type': '0',
        'fw_version': firmware_version,
        'hardwareVersion': 'V0.18.3.6',
        'productVersion': '256',
        'productId': '19',
        'app_time': app_time,
        'displayName':'公众号：JHwl',
        # 新增的认证参数
        'code': '000000',  # 验证码（需要实际值）
        'sn': 'YHsvARCIPL1IhENe',  # 序列号（需要实际值）
        'auth_key': 'd3826daa-8dff-4b88-acec-e778d0b37bad',  # 认证密钥
        'fw_hr_version': 'V0.18.3.6',  # 心率固件版本
        'bind_timezone': '0' , # 时区（中国UTC+8）
       
        'brandType': '0',
        'activeStatus': '1',
        'createUserId': '0',
        'appid': '428135909242707968',
        'channel': 'Normal',
        'enableMultiDevice': '1',
    }
    
    url = 'https://api-mifit-cn3.zepp.com/v1/device/binds.json'
    
    # 将部分参数也放在URL中（保持原有兼容性）
    url_params = {
        'deviceid': device_id,
        'userid': '1196682840',
        'device_type': '0',
        'device_source': '16',
        'mac': device_mac
    }
    
    full_url = url + '?' + '&'.join([f"{k}={v}" for k, v in url_params.items()])
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'apptoken': app_token,
        'User-Agent': 'MiFit6.12.0 (23078RKD5C; Android 10; Density/3.00)',
        'appplatfrom':'android_phone'
    }
    
    try:
        print("发送的完整参数:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        
        response = requests.post(full_url, data=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        if result.get('code') != 1:
            raise ValueError(f"绑定错误: {result.get('message', '未知错误')}")
        
        return result
        
    except requests.RequestException as e:
        raise ValueError(f"绑定失败: {response.status_code if 'response' in locals() else 'N/A'} - {response.text if 'response' in locals() else str(e)}") from e

def info_device(app_token: str) -> dict:
    url = 'https://api-mifit-cn3.zepp.com/users/1196682840/devices?enableMultiDevice=1&enableMultiDeviceOnMultiType=1'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'apptoken': app_token,
        'User-Agent': 'Zepp/9.13.0 (iPhone; iOS 26.1; Scale/3.00)',
        'Host': 'api-mifit-cn3.zepp.com',
        'appname': 'com.huami.midong',
        'vb': '202509231429'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise ValueError(f"获取设备信息失败: {response.status_code if 'response' in locals() else 'N/A'} - {response.text if 'response' in locals() else str(e)}") from e

if __name__ == "__main__":
    app_token = "ZQVBQEJyQktGXip6SltGSlpuQkZgBAAEAAAAA6Qn5JyqP78FCy66KrGgJzbFCV4fxd1_CsDxdmbbsBdQogPJPhMDFlJGJbVPR-1jcFbJb2zYxuTaZp291KQZC13J8JEHdQi0vPWJ3xaxg3T4msZzbzWFIB_llPyrx40m53lWIgJNFevZ4qoRTHIKQdxmypAWsm2JvAMVKwHi3vyzkW-AtZf5gTDlQiSoDtf1L"
    
    try:
        result = bind_device(app_token)
        print("绑定结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        time.sleep(2)
        result = info_device(app_token)
        print("\n设备信息:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"错误: {e}")
