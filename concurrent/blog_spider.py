"""
@author kingfish
爬取博客园网站的网页数据
"""
import requests
from bs4 import BeautifulSoup

urls = [
    f"https://www.cnblogs.com/#p{page}"
    for page in range(1,51) 
]

print(urls)

#爬取函数
def craw(url):
    r = requests.get(url)
    return r.text
   
#解析爬取到的html的标签
def parse(html):
    # 假设解析标签是<a>且class="post-item-title"
    soup = BeautifulSoup(html,"html.parser")
    links = soup.find_all("a",class_="post-item-title")
    return [(link["href"],link.get_text()) for link in links]

if __name__ == "__main__":
    for result in parse(craw(urls[2])):
        print(result)