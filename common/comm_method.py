#! python3
import requests
import ssl
import configure
import time
import random

# 请求https需要添加这句（抓包工具开启的时候将会失效）
ssl._create_default_https_context = ssl._create_unverified_context

# 登录获取用户信息
def get_user_info(mobile):
    api = '/api/zm/w/account/login?appOs=' + configure.appos + '&appVersion=' + configure.appVersion
    url = configure.protocol + '://' + configure.zm_host + api

    data = {
        'username':mobile,
        'password':'e10adc3949ba59abbe56e057f20f883e'
    }
    res = requests.post(url,data,headers=configure.headers)

    return res.json()

# 注册新用户
def register():
    # 根据日期随机生成一个新号码
    moblie = int('188' + time.strftime("%m%d",time.localtime()) + '0000') + random.randint(0,9999)
    name = ['李俊','李凉','李诗韵','李修贤','王淡旦','王中齐','王中鲁','王时悦','王晨梁','王周子']

    api = '/api/zm/w/account/register'
    url = configure.protocol + '://' + configure.zm_host + api

    data = {
        'source':'',
        'name':name[random.randint(0,len(name)-1)],
        'position':'',
        'company':'',
        'username':moblie,
        'password':'e10adc3949ba59abbe56e057f20f883e',
        'originUserId':'',
        'logo':'',
        'type':'undefined'
    }

    res = requests.put(url=url,data=data)
    token = res.cookies.get_dict()['zhangmen_token_cookie']
    userId = res.json()['userId']

    user_info = {
        'token':token,
        'userId':userId
    }

    return user_info




