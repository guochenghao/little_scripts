import os
import pandas

process_number = 10

def get_process_info():
	result = os.popen('tasklist')
	result = result.read().strip().split('\n')[3:]
	result = [i[:-2] for i in result]
	result = [i.split() for i in result]
	for i,v in enumerate(result):
		result[i][-1] = round(int(v[-1].replace(',', ''))/1024, 2)
	return result

result = get_process_info()

df = pandas.DataFrame(result, columns=['process_name', 'pid', 'session_name', 'session', 'mem'])


data = df.groupby('process_name').sum().sort_values(by='mem', ascending=False)[:process_number]

data_str = []
for index, value in enumerate(data.index):
    if index==0:
        data_str.append('Process Name'.ljust(20, ' ') + 'Memory'.rjust(10, ' '))
        data_str.append('-'*20+' '+'-'*11)
    data_str.append(value.ljust(20, ' ')+str(data['mem'][value]).rjust(10, ' ')+' M')

data_str.append('-'*20+' '+'-'*11)
data_str.append('Total'.ljust(20, ' ') + str(sum(df.mem)).rjust(10, ' ') + ' M')
data_str = '\n'.join(data_str)
print(data_str)

# output

# Process Name            Memory
# -------------------- -----------
# chrome.exe             1563.53 M
# Code.exe                 524.8 M
# svchost.exe             406.53 M
# python.exe              375.49 M
# YNoteCefRender.exe      202.58 M
# WeChat.exe              188.16 M
# Everything.exe          146.47 M
# YoudaoNote.exe           108.5 M
# explorer.exe            104.34 M
# WeChatWeb.exe            102.9 M
# -------------------- -----------
# Total                  4521.07 M
# [Finished in 2.4s]
