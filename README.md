# westonline2
西二在线2轮考核

# 简介
**项目内容：** 爬取[福大要文](http://news.fzu.edu.cn/html/fdyw/)  
**要求：**  
1.包含发布日期、作者、标题、阅读数以及正文  
2.可自动翻页  
3.范围：2020年内  

## 一. 自动翻页的实现
### 1.观察：
点开链接，下拉到底实现手动翻页并观察顶部url的变化，可以发现有一定的规律。

第一页url：
![第一页url](https://img-blog.csdnimg.cn/20201226151722595.png)  
第二页url：
![第二页url](https://img-blog.csdnimg.cn/20201226151735567.png)  
第三页url：
![第三页url](https://img-blog.csdnimg.cn/20201226151753595.png)  
...  
因此我们大致可以推断翻页的实现是通过改变(num).html中的数字num实现的。

### 2.代码实现：
利用简单的for循环实现自动翻页
```python
for i in range(1,18,1):
    url="http://news.fzu.edu.cn/html/fdyw/{}.html".format(i)   
```

## 二.时间的限定
### 1.遇到的困难：
来到福大要闻的首页，跳转至第16页（图片内备注错了），发现部分要闻为20年发布，另一些为19年。因此，单纯靠前文提及的for循环是无法实现项目要求的（会有不需要的19年数据被爬下）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201226163350732.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NzI4MjQwNA==,size_16,color_FFFFFF,t_70)
### 2.解决过程：
增加一个for循环，若“2019”字符串在时间中则break退出循环。（以下为部分代码）

```python
time=li.select(".list_time")[0].text  # 获取并打印要闻发布日期
if "2019" not in time:
	print(num,"发布日期：",time)
	times.append(time) # 储存发布时间
else:
	break
```

## 三.阅读数的爬取
### 1.遇到的困难：
使用正常的爬取方法无法爬取到阅读数
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020122615485420.png)
![困难](https://img-blog.csdnimg.cn/20201226153229382.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NzI4MjQwNA==,size_16,color_FFFFFF,t_70)
### 2.解决过程：
右键“检查”，观察网页源码，发现在下方仿佛隐藏着一个url，也许跟阅读数的爬取有些关联。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201226155229731.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NzI4MjQwNA==,size_16,color_FFFFFF,t_70)
选择Network，深入探索一下，果然有发现。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201226155959141.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NzI4MjQwNA==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201226160255112.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NzI4MjQwNA==,size_16,color_FFFFFF,t_70)

点开不同要闻，不同阅读数，仅id后的数字不一样。所以我思考，是否可以通过正则匹配扣出那串数字，就可以爬取到阅读数。（以下为部分代码）

```python
readcount=[] #建立空字典储存数据
a=re.compile("id=(.*?)'",re.S|re.I) # 惰性匹配       
result=a.findall(innerHtml.text)[-1]
ids.append(result)
        
readcount_url = 'https://news.fzu.edu.cn/interFace/getDocReadCount.do?id=' # 获取并打印阅读数
link = readcount_url+ids[-1] # 拼接url
r = requests.get(link)
print("阅读数：",r.text)
readcount.append(r.text) # 储存阅读数
```

正则匹配时候出现问题的朋友可以用这个网站测试下再写入代码：[在线正则表达式测试](https://tool.oschina.net/regex)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201226164104853.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NzI4MjQwNA==,size_16,color_FFFFFF,t_70)

## 四.完整代码

```python
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
```


写在最后：lwgg我男神
