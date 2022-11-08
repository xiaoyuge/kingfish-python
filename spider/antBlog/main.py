"""
@author kingfish
爬取antBlog网站首页所有标题和连接
"""
import requests
from bs4 import BeautifulSoup

#从url下载html内容
url = "http://www.crazyant.net/"

r = requests.get(url)
if r.status_code != 200:
    raise Exception()

#解析html内容
soup = BeautifulSoup(r.text,"html.parser")

#查找所有名字是h2且class属性是entry-title的节点
h2s = soup.find_all(name="h2",attrs={"class":"entry-title"})

#定义一个集合存放所有解析到的链接和标题
links = set()

#遍历h2节点，找到子节点a，把链接和标题作为元组放入集合
for h2 in h2s:
    link = h2.find("a")
    links.add((link["href"],link.get_text()))

#看一下我们爬取到的内容
print(links)