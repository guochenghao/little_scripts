import win32api
import os

def getFileProperties(fname):
    """
    读取给定文件的所有属性, 返回一个字典.
    """
    propNames = ('Comments', 'InternalName', 'ProductName',
        'CompanyName', 'LegalCopyright', 'ProductVersion',
        'FileDescription', 'LegalTrademarks', 'PrivateBuild',
        'FileVersion', 'OriginalFilename', 'SpecialBuild')
 
    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}
 
    try:
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FixedFileInfo'] = fixedInfo
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                fixedInfo['FileVersionLS'] % 65536)
 
        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]
 
        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above
 
        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            ## print str_info
            strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)
 
        props['StringFileInfo'] = strInfo
    except:
        pass
 
    return props
 
 
if __name__ == "__main__":
	# For Test
    print(getFileProperties('D:\\ProgramData\\Anaconda3\\python.exe'))
	
    folder_path = r"\\172.20.176.186\AnyFolderPath"
	# 假设已经可以访问该路径，如果不可访问，请使用以下命令
    # CMD 命令 (For Windows), 如果无法访问共享路径，请使用以下命令
    # 建立磁盘映射
	# cmd = 'net use H: folder_path /user:username password'
	# os.system(cmd)
	# 删除磁盘映射
	# cmd = 'net use H: /del'
	# os.system(cmd)
    for a, b, c in os.walk(folder_path):
        exe_dll = [i for i in c if i.endswith('.exe') or i.endswith('.dll')]
        if exe_dll:
            print('Start'.center(60, '-'))
            print('Current Path: ', a, '\n')
            for i in exe_dll:
                file_path = os.path.join(a, i)
                print('File_Path: ', file_path)
                file_properties = getFileProperties(file_path)
                copyright = file_properties['StringFileInfo'].get('LegalCopyright', 'Failed') if file_properties.get('StringFileInfo', None) else 'Failed'
                print('Copyright: ', copyright, '\n')
            print('End'.center(60, '-'), '\n')
# 参考
# https://www.cnblogs.com/sigai/p/7582367.html
# https://baike.baidu.com/item/net%20use/2298733?fr=aladdin
