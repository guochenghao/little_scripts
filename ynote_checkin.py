import requests


def parse_cookies(data=None):
	first_data = data.split(';')
	print(first_data)
	two_data = [x.split('=') for x in first_data]
	print(two_data)
	new_data = {
	x.strip():y.strip() for x, y in two_data
	}	
	print(new_data)
	return new_data

#有道笔记签到url
url = 'http://note.youdao.com/yws/mapi/user?method=checkin'

# 构造headers
headers= {'user-agent': 'YNote'}

# 修改为你的cookie
cookies_data = '<enter your cookies here>'

# 格式化cookies
format_cookies = parse_cookies(cookies_data)

if __name__ == '__main__':    
    resp = requests.post(
        url=url,
        headers=headers,
        cookies=format_cookies
    )
    print("请求结果：\n",resp.json())
    
# 备注：其中cookies_data使用fiddler抓取即可
