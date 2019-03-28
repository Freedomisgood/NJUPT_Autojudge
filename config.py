import configparser
import json
account_data={}

class myconf(configparser.ConfigParser):
    '''
    由于ConfigParser会自动将配置文件的大写字母转换为小写字母,所以需要重写下optionxform方法
    '''
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        return optionstr

conf = myconf() #声明一个全局的configparse



def getConfig(filename,sectionName):
    '''
    获得配置文件内容
    :param filename: 配置文件名
    :param sectionName: 字段名
    :return: 账号信息键值对
    '''
    conf.read(filename)
    kvs = conf.items(sectionName)
    return kvs


def modifyConfig(filename,sectionName):
    '''
    :param filename:
    :param sectionName:
    :return:
    '''
    conf.add_section(sectionName)
    for UID,PWD in account_data.items():
        print(UID,PWD)
        conf.set(sectionName, UID, PWD)
    with open(filename,'w') as f:
        conf.write(f)

def get_jsonData(filename):
    '''
    获得账号信息
    :param filename:
    :return:
    '''
    global account_data
    with open('d.json','r') as f:
        account_data = json.load(f)
    return account_data

if __name__ == "__main__":
    # modifyConfig("dada.conf", "config")
    account = getConfig("dada.conf", "account")
    print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")