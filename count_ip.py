import re

# 匹配ip地址
reg = re.compile(r'(\d{1,3}\.}){3}(\d{1,3})')

# 统计ip次数
ip_seq = {}

with open('/var/log/secure') as e:
    f = e.readline()
    for i in f:
        t = re.search(reg, i)
        if t:
            ip_key = t.group(0)
            ip_seq[ip_key] = ip_seq.get(ip_key, 0) + 1

if __name__ == '__main__':
    print(ip_seq)
