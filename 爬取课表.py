# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 22:29:35 2020

@author: jyw2000
"""

import requests
import re

#设置请求头       
headers = {"Referer": "http://jwch.fzu.edu.cn/",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"} # 请求头
             
'''
count = 0
while count < 3 :
    UserName = str(input("请输入用户名:\n"))
    PassWord = str(input("请输入密码:\n"))
    if UserName == '831901109' and PassWord == '*******':
        print("恭喜你,登录成功！")
        break
    else:
        print("用户名/密码错误，请重试！您还有%d次机会再次正确的输入用户名和密码" %(2-count))
        if (2 - count) == 0:
            print("对不起, 你输入用户名和密码的错误次数已超过3次,你没了")
            break
    count+=1

'''
UserName=int(input("Please input your username:"))
PassWord=str(input("Please input your password:"))

session = requests.session()#实例化session

# 模拟登陆
post_url="http://59.77.226.32/logincheck.asp" # 登录模块url
post_data={"muser":UserName,"passwd":PassWord} # 请求数据
response=session.post(post_url,headers = headers,data = post_data) #使用session发起请求

r = re.compile(".*?id=([0-9]*)",re.S|re.I)# 正则匹配id
id = r.findall(response.url)[0]

table_url="http://59.77.226.35/right.aspx?id="+id  # 拼接url
table = session.get(table_url,headers = headers) # 进入个人主页并获取课表
if table.status_code == 200:
    print("课表爬取成功！请到默认保存路径中查看课表！")
else:
    print("状态异常请重试！")
    
# 保存为html格式
with open('课表.html','w',encoding = 'utf-8') as f:
    f.write(table.text)