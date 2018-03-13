import re
from collections import defaultdict, Counter

# 匹配ip地址
reg = re.compile(r'(\d{1,3}\.){3}(\d{1,3})')

# 第一种方法：使用dict.get(key, defaultvalue)
def count_ip1(file_path):
    # 统计ip次数
    ip_seq = {}
    with open(file_path, 'r') as e:
        f = e.readlines()
        for i in f:
            t = re.search(reg, i)
            if t:
                ip_key = t.group(0)
                ip_seq[ip_key] = ip_seq.get(ip_key, 0) + 1
    return ip_seq



# 第二种方法：使用defaultdict
# 设置默认值为0
def count_ip2(file_path):
    ip_seq = defaultdict(lambda: 0)
    with open(file_path, 'r') as e:
        f = e.readlines()
        for i in f:
            t = re.search(reg, i)
            if t:
                ip_key = t.group(0)
                ip_seq[ip_key] += 1
    return ip_seq


if __name__ == '__main__':
    file_path = '/var/log/secure'
    ip_seq1 = count_ip1(file_path)
    ip_seq2 = count_ip2(file_path)
    # print(ip_seq1)
    # print(ip_seq2)
    assert ip_seq1.items() == ip_seq2.items(), 'file open time not same, so maybe not equal'
    # 打印频率前十的ip
    most_ip = Counter(ip_seq2)
    print(most_ip.most_common(10))
