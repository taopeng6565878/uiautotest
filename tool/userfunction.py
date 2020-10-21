import os
import random
import time
import hashlib
import base64
import datetime
import uuid
import faker
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
#随机字符串，长度num
from conftest import overalldict

def test():
    f = faker.Faker(locale='zh_CN')
    return f.company()

def Randomstr(num,paramname = None):
    S ='abcdefghijklmnopqrstuvwxyz1234567890QWERTYUIOPASDFGHJKLZXCVBNM'
    salt = ''
    num = int(num)
    for i in range(num):
        salt += random.choice(S)
    if (paramname != None) & (paramname != ''):
        overalldict[paramname] = salt
    return salt
#随机数字，长度num
def Randomnum(num,paramname = None):
    S ='1234567890'
    salt = ''
    num = int(num)
    for i in range(num):
        salt += random.choice(S)
    if (paramname != None) & (paramname != ''):
        overalldict[paramname] = salt
    return str(salt)
#随机字符串，传入可选字符str，长度num
def Random(param,num,paramname = None):
    S =param
    salt = ''
    num = int(num)
    for i in range(num):
        salt += random.choice(S)
    if (paramname != None) & (paramname != ''):
        overalldict[paramname] = salt
    return str(salt)

#时间函数
# 格式化成2016-03-20 11:45:39形式 "%Y-%m-%d %H:%M:%S"
def Time(formate = None,paramname = None):
    if formate == None:
        t = str(time.time())
        t = t[0:t.find('.')+4].replace('.','')#截取小数点后三位，返回毫秒格式
    else:
        t = time.strftime(formate, time.localtime())
    if (paramname != None) & (paramname != ''):
        overalldict[paramname] = t
    return str(t)


# 时间函数 ${__name(;;2;)}
# 当前时间的基础上加减指定的时间：years，months，days,hours，minutes，seconds可以传入负数和正数
def TimeShift(years=0,months=None,days=None,hours=None,minutes=None,seconds=None,formate = None,paramname=None):
    # region 处理'' 和 None
    if years == '' or years == None:
        years = 0
    else:
        years = int(years)
    if months == '' or months == None:
        months = 0
    else:
        months = int(months)
    if days == '' or days == None:
        days = 0
    else:
        days = int(days)
    if hours == '' or hours == None:
        hours = 0
    else:
        hours = int(hours)
    if minutes == '' or minutes == None:
        minutes = 0
    else:
        minutes = int(minutes)
    if seconds == '' or seconds == None:
        seconds = 0
    else:
        seconds = int(seconds)
    # endregion
    ti = datetime.datetime.now() + relativedelta(years=years,months=months,days=days,hours=hours,minutes=minutes,seconds=seconds)
    resulttime = ti.strftime(formate)
    if paramname:
        overalldict[paramname] = resulttime
    return resulttime

# 生成UUID：基于MAC地址，当前时间戳，随机数字生成。可以保证全球范围内的唯一性。
def UUID(paramname = None):
    uuid_str = uuid.uuid1()
    print(uuid_str)
    if paramname:
        overalldict[paramname] = uuid_str
    return str(uuid_str)

def Md5(param,paramname = None):
    hl = hashlib.md5()
    hl.update(param.encode("utf-8"))
    result = hl.hexdigest()
    if (paramname != None) & (paramname != ''):
        overalldict[paramname] = result
    return result

def Base64encode(param,paramname = None):
    result = base64.b64encode(bytearray(param.encode())).decode()
    if (paramname != None) & (paramname != ''):
        overalldict[paramname] = result
    return result

def CutString(Str,leftstr,rightstr,paramname = None):
    result = Str[Str.find(leftstr) + len(leftstr):Str.find(rightstr, Str.find(leftstr) + len(leftstr))]
    if (paramname != None) & (paramname != ''):
        overalldict[paramname] = result
    return result



def IDNumber(paramname = None):
    codelist = []
    with open(os.path.abspath('..')+'/file/districtcode.txt', mode="r", encoding="utf-8") as file:
        codelist = file.readlines()
    id = codelist[random.randint(0, len(codelist) - 1)].split(' ')[0]  # 地区项
    id = id + str(random.randint(1980, 2019))  # 年份项
    da = datetime.date.today() + datetime.timedelta(days=random.randint(1, 366))  # 月份和日期项
    id = id + da.strftime('%m%d')
    id = id + str(random.randint(100, 300))  # ，顺序号简单处理

    i = 0
    count = 0
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
    checkcode ={'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5',
                '8': '5', '9': '3', '10': '2'}  # 校验码映射
    for i in range(0, len(id)):
       count = count + int(id[i]) * weight[i]
    result = id + checkcode[str(count%11)]  # 算出校验码
    if (paramname != None) & (paramname != ''):
        overalldict[paramname] = result
    return result

if __name__ == '__main__':
    # 格式化成2016-03-20 11:45:39形式
    print(TimeShift('',))