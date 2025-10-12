import requests
import hashlib
import base64
import time
import uuid
from Crypto.Cipher import AES

# 密钥和IV
KEY = b"xeNtBVqzDc6tuNTh"
IV = b"MAAAYAAAAAAAAABg"

# 加密函数
def encrypt_data(plain: str) -> bytes:
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    pad_len = 16 - (len(plain.encode()) % 16)
    padded = plain.encode() + bytes([pad_len]) * pad_len
    return cipher.encrypt(padded)


# 生成 r
def generate_r(t: int) -> str:
    uuid_str = uuid.uuid4().hex
    data = f"{uuid_str}{t}".encode()
    hash_val = hashlib.sha256(data).hexdigest().upper()
    return hash_val[:64]
# 下载验证码图片并获取 captcha-key


t = int(time.time() * 1000) 
r = generate_r(t)
captcha_url = f"https://api-user.zepp.com/captcha/register?r={r}&t={t}"
try:
    response = requests.get(captcha_url)
    if response.status_code == 200:
        with open("captcha.png", "wb") as f:
            f.write(response.content)
        print("验证码图片已保存为 captcha.png，请查看图片并输入验证码。")
        # 提取 captcha-key
        captcha_key = None
        if "Set-Cookie" in response.headers:
            cookies = response.headers["Set-Cookie"]
            if "captcha-key=" in cookies:
                captcha_key = cookies.split("captcha-key=")[1].split(";")[0]
                print("Captcha-key:", captcha_key)
        if not captcha_key:
            print("未找到 captcha-key")
            exit(1)
    else:
        print(f"下载验证码图片失败: HTTP {response.status_code}")
        exit(1)
except Exception as e:
    print(f"下载验证码错误: {str(e)}")
    exit(1)

# 用户输入验证码
code = input("请输入验证码 (4位): ").strip()

# 动态参数
t1 = int(time.time() * 1000)  # 当前时间戳（毫秒，基于 2025-10-13 01:46 AM JST）
email_or_phone = "<name@qq.com>"
name = email_or_phone.split('@')[0]  # 提取@符号前的部分
client_id = "HuaMi"
#key = generate_key(captcha_key, t, email_or_phone)
key =captcha_key
x_request_id = str(uuid.uuid4()).upper()
password="<PASSWORD>"
# 请求体（明文，包含 key 和 r）
body_plain = (
    f"client_id={client_id}&code={code}&country_code=CN&emailOrPhone={email_or_phone}"
    f"&key={key}&name={name}&password={password}"
    f"&r={r}"
    f"&redirect_uri=https%3A//s3-us-west-2.amazonaws.com/hm-registration/successsignin.html"
    f"&state=REDIRECTION&t={t1}&token=refresh&token=access"
)

# 加密请求体
body_cipher = encrypt_data(body_plain)

# 请求头
headers = {
    "callid": str(t - 1000),
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "app_name": "com.huami.midong",
    "appname": "com.huami.midong",
    "shouldHookRedirection": "YES",
    "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9",
    "X-Hm-Ekv": "1",
    "Accept-Encoding": "compress",
    "X-Request-Id": x_request_id,
    "cv": "9.13.0",
    "lang": "zh_CN",
    "timezone": "Asia/Shanghai",
    "appplatform": "ios_phone",
    "country": "US",
    "User-Agent": "Zepp/9.13.0 (iPhone; iOS 26.1; Scale/3.00)",
    "Connection": "keep-alive"
    #"Cookie": f"captcha-key={captcha_key}"  # 添加 captcha-key 到 Cookie
}

# 发送请求
url = "https://api-user.zepp.com/v2/registrations/register"
try:
    response = requests.post(url, data=body_cipher, headers=headers)
    print(f"HTTP Status: {response.status_code}")
    print("Response Headers:\n", response.headers)
    print("Response Body:\n", response.text)

    # 提取 Location 中的 token
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
