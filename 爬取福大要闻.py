# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 18:32:15 2021

@author: jyw2000
"""

import requests # 导入请求包
from bs4 import BeautifulSoup # 导入解析包
import sqlalchemy
import pandas as pd
import re # 导入正则

# 创建空字典用于储存数据
ids=[] 
urls=[]
times=[]
texts=[]
names=[]
titles=[]
readcount=[] 
num=1

for i in range(1,17,1): 
    url="http://news.fzu.edu.cn/html/fdyw/{}.html".format(i)   # for循环实现自动翻页
    
    html=requests.get(url)    
    soup=BeautifulSoup(html.text,"lxml") # 解析url
    
    
    lis=soup.select(".list_main_content li")
    
   
    for li in lis:
        
        time=li.select(".list_time")[0].text  # 获取并打印要闻发布日期
        if "2019" not in time:
            print(num,"发布日期：",time)
            times.append(time) # 储存发布时间
        else:
            break
            
        title=li.select("a")[0].text # 获取并打印要闻标题
        print("标题：",title) 
        titles.append(title) # 储存标题
        
        innerUrl="http://news.fzu.edu.cn"+li.select("a")[0]["href"] # 获取并打印单条要闻网页链接
        print("链接：",innerUrl)   
        urls.append(innerUrl)
        
        num+=1  # 给结果标号
        
        
        innerHtml=requests.get(innerUrl)
        soup=BeautifulSoup(innerHtml.text,"lxml") # 解析innerUrl
        
        
        authors=soup.select(".detail_main_content div") # 获取并打印要闻作者
        for au in authors:
            author=au.select("span#author")[0].text
            print("作者：",author)
            names.append(author) # 储存作者
            
        contents=soup.select("div#news_content_display") # 获取并打印要闻内容
        for co in contents:
            print("内容：",co.text)  
            texts.append(co.text)
            
        
        a=re.compile("id=(.*?)'",re.S|re.I) # 惰性匹配       
        result=a.findall(innerHtml.text)[-1]
        ids.append(result)
        
        readcount_url='https://news.fzu.edu.cn/interFace/getDocReadCount.do?id='+ids[-1] # 获取并打印阅读数
        print(readcount_url)
        r = requests.get(readcount_url)
        print("阅读数：",r.text)
        readcount.append(r.text) # 储存阅读数


#保存数据为df格式
data = {"title":titles,
     "author":names,
     "release_time":times,
     "click_number":readcount,
     "url":urls,
     "content":texts}
df=pd.DataFrame(data)


# 存入数据库
engine=sqlalchemy.create_engine("mysql+pymysql://root:@localhost:3306/demo")
df.to_sql(name="要闻",con=engine,if_exists="append",index=False)