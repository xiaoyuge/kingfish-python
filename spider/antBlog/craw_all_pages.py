"""
@author kingfish
我们来爬取一下antBlog的所有链接页面
"""
from __init__ import *
from utils import url_manager
import requests
from bs4 import BeautifulSoup
import re

entry_url = "http://www.crazyant.net/"
#要爬的目标url的正则
pattern = r'^http://www.crazyant.net/\d+.html$'

#先加入入口Url,然后开始遍历爬取
um = url_manager.UrlManager()
um.add_new_url(entry_url)
with open("spider/antBlog/antBlogArticles.txt","w") as fou:
    while um.has_new_url():
        url = um.get_url()
        #爬取其url内容
        r  = requests.get(url,timeout=3)
        if r.status_code != 200:
            print("error,return code is not 200",url)
            continue
        #解析内容
        soup = BeautifulSoup(r.text,"html.parser")
        #找到所有链接节点，加入待爬取集合
        links = soup.find_all(name="a")
        for link in links:
            #href可能有问题，跳过
            href = link.get("href")
            content = link.get_text()
            if href is None:
                continue
            #如果符合目标url，保存起来
            if re.match(pattern,href):
                # 如果添加成功，说明是新url，则输出到文件
                if um.add_new_url(href):
                    print(href,content)
                    fou.write("%s\t%s\n"%(href,content))

