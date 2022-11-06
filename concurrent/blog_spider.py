"""
@author kingfish
爬取博客园网站的网页数据
"""
import requests

urls = [
    f"https://www.cnblogs.com/#p{page}"
    for page in range(1,51) 
]

print(urls)

#爬取函数
def craw(url):
    r = requests.get(url)
    print(url,len(r.text))

craw(urls[0])

