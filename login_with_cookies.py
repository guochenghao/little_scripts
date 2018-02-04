# python3
import requests
import os
import sqlite3
from win32crypt import CryptUnprotectData
from collections import namedtuple

# cookies存放路径
cookie_path = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"

# 获取cookie
def get_cookie_from_chrome(host=None):
    sql = "select host_key,name,encrypted_value from cookies where host_key='{}'".format(host)
    with sqlite3.connect(cookie_path) as conn:
        cursor = conn.cursor()
        cookies = { name:CryptUnprotectData(encrypted_value)[1].decode() 
                     for host_key, name, encrypted_value in cursor.execute(sql).fetchall() }
        return cookies

# 获取指定一组域名的cookies
cookies_domain = ['.youdao.com', '.note.youdao.com', 'note.youdao.com'] # example
def get_all_cookies(domains=None):
    cookies = {}
    for domain in domains:
        cookies.update(get_cookie_from_chrome(domain))
    return cookies
all_domain_cookies = get_all_cookies(cookies_domain) # 获取指定域名的cookies

# 更新指定cookies
def update_cookies(new_cookies, old_cookies):
    flash_cookies = {}
    for key in old_cookies.keys():
        flash_cookies[key] = new_cookies[key] if key in new_cookies.keys() else old_cookies[key]
    return flash_cookies

# flash_cookies = update_cookies(new_cookies=all_domain_cookies, old_cookies=format_cookies )
# old_cookies 接收字典，主要包含需要的字段名，以及一些预备值，以防新cookies中没有某些值
    
# 获取所有hosts
def get_hosts():
    sql = "select host_key from cookies"
    with sqlite3.connect(cookie_path) as conn:
        cursor = conn.cursor()
        hosts = set(cursor.execute(sql).fetchall())
    return hosts

headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }


test_url = 'http://i.baidu.com'                         # 设定测试url
test_host = '.baidu.com'                                # 设定测试host
test_cookies = get_cookie_from_chrome(test_host)        # 获取测试host的cookies
user_name = "那******晴"


if __name__ == "__main__" :
    # 使用get请求访问测试url
    resp = requests.get(
            url = test_url,
            headers = headers,
            cookies = test_cookies,
            allow_redirects = 1
            )

    # 保存到txt中查看是否访问成功
    with open('test.txt', 'w', encoding='utf-8') as f:
        f.write(resp.text)
    
    # 检查是否登录成功
    assert user_name in resp.text, '使用cookie模拟访问失败'

# 备注：其中test_url, test_host, user_name需要替换，替换完成后可以直接运行
