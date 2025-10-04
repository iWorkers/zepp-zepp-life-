import pycurl
from io import BytesIO
from urllib.parse import urlencode, urlparse, parse_qs
from Crypto.Cipher import AES
import re

KEY = b"xeNtBVqzDc6tuNTh"
IV  = b"MAAAYAAAAAAAAABg"

def encrypt_data(plain: str) -> bytes:
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    pad_len = 16 - (len(plain.encode()) % 16)
    padded = plain.encode() + bytes([pad_len]) * pad_len
    return cipher.encrypt(padded)

def getAccess_with_pycurl(username, password):
    third_name = "email" if "@" in username else "huami_phone"
    if "@" not in username:
        username = "+86" + username

    url = "https://api-user.zepp.com/v2/registrations/tokens"
    data = {
        "emailOrPhone": username,
        "password": password,
        "state": "REDIRECTION",
        "client_id": "HuaMi",
        "country_code": "CN",
        "token": "access",
        "redirect_uri": "https://s3-us-west-2.amazonaws.com/hm-registration/successsignin.html",
    }
    body_plain = urlencode(data)
    body_cipher = encrypt_data(body_plain)

    body_buf = BytesIO()
    header_buf = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.POST, 1)
    c.setopt(c.POSTFIELDS, body_cipher)
    c.setopt(c.WRITEDATA, body_buf)
    c.setopt(c.HEADERFUNCTION, header_buf.write)
    c.setopt(c.HTTPHEADER, [
        "Accept: */*",
        "Accept-Language: zh-CN,zh;q=0.9",
        "Connection: keep-alive",
        "User-Agent: Dalvik/2.1.0 (Linux; U; Android 9; MI 6 Build/PKQ1.190118.001) MiFit/4.6.0 (com.xiaomi.hm.health; build:46037; Android:28; androidBuild:PKQ1.190118.001)",
        "app_name: com.xiaomi.hm.health",
        "appplatform: android_phone",
        "x-hm-ekv: 1"
    ])
    c.setopt(c.SSL_VERIFYPEER, False)
    c.setopt(c.SSL_VERIFYHOST, False)

    c.perform()
    status = c.getinfo(pycurl.RESPONSE_CODE)
    headers = header_buf.getvalue().decode(errors="replace")
    c.close()

    # 1. 优先解析 Location 里的 query 参数
    location_match = re.search(r"Location:\s*(\S+)", headers, re.IGNORECASE)
    if location_match:
        loc_url = location_match.group(1).strip()
        qs = urlparse(loc_url).query
        params = parse_qs(qs)
        if "access" in params:
            return params["access"][0], third_name
        if "refresh" in params:
            return params["refresh"][0], third_name

    # 2. 备用：直接在 headers 里用正则搜索
    m = re.search(r"access=([^&\s]+)", headers)
    if m:
        return m.group(1), third_name
    m = re.search(r"refresh=([^&\s]+)", headers)
    if m:
        return m.group(1), third_name

    # 3. 错误处理
    if "error=" in headers:
        raise Exception("账号或密码错误！")
    raise Exception(f"登录token接口请求失败，HTTP {status}\nHeaders:\n{headers}")

if __name__ == "__main__":
    token, typ = getAccess_with_pycurl("账号@qq.com", "密码")
    print("Token:", token)
    print("Type:", typ)

