import requests
from Crypto.Cipher import AES
import binascii

# 密钥和IV
KEY = b"xeNtBVqzDc6tuNTh"
IV = b"MAAAYAAAAAAAAABg"

# 加密函数
def encrypt_data(plain: str) -> bytes:
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    pad_len = 16 - (len(plain.encode()) % 16)
    padded = plain.encode() + bytes([pad_len]) * pad_len
    return cipher.encrypt(padded)

# 请求体（明文）
body_plain = (
    "client_id=HuaMi&code=n86w&country_code=CN&emailOrPhone=username%40qq.com"
    "&key=R4KOQnLWYtHL8Y9sBKo9CQAAAZnT7yhT&name=username&password=password"
    "&r=605A82A43B9469CF64213789792023E9905EAB6B010000008C4F0F0801000000"
    "&redirect_uri=https%3A//s3-us-west-2.amazonaws.com/hm-registration/successsignin.html"
    "&state=REDIRECTION&t=1760197354721&token=refresh&token=access"
)

# 加密请求体
body_cipher = encrypt_data(body_plain)

# 请求头
headers = {
    "callid": "1760197273601",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "app_name": "com.huami.midong",
    "appname": "com.huami.midong",
    "shouldHookRedirection": "YES",
    "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9",
    "X-Hm-Ekv": "1",
    "Accept-Encoding": "compress",
    "X-Request-Id": "9DC3D1F2-2B99-4B32-9C07-0FDC53BAF23C",
    "cv": "9.13.0",
    "lang": "zh_CN",
    "timezone": "Asia/Shanghai",
    "appplatform": "ios_phone",
    "country": "US",
    "User-Agent": "Zepp/9.13.0 (iPhone; iOS 26.1; Scale/3.00)",
    "Connection": "keep-alive"
}

# 发送请求
url = "https://api-user.zepp.com/v2/registrations/register"
try:
    response = requests.post(url, data=body_cipher, headers=headers)
    print(f"HTTP Status: {response.status_code}")
    print("Response Headers:\n", response.headers)
    print("Response Body:\n", response.text)

    # 提取Location中的token
    if "Location" in response.headers:
        from urllib.parse import urlparse, parse_qs
        qs = urlparse(response.headers["Location"]).query
        params = parse_qs(qs)
        if "access" in params:
            print("Access Token:", params["access"][0])
        elif "refresh" in params:
            print("Refresh Token:", params["refresh"][0])
        else:
            print("No access or refresh token found in Location")
except Exception as e:
    print(f"Request failed: {str(e)}")
