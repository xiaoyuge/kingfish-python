"""
@author = kingfish
用BeautifulSoup这个库，可以对Html的内容进行解析
"""

from bs4 import BeautifulSoup

with open("crawler/bs4_case/hello_world.html") as fin:
    html_doc = fin.read()
    
soup = BeautifulSoup(html_doc,"html.parser")

#获取所有的链接
links= soup.find_all("a")

for link in links:
    print(link.name,link["href"],link.get_text())
    
#获取所有的图片地址
imgs = soup.find_all(name="img")

for img in imgs:
    print(img.name,img["src"])
    
#为优化解析，可以先先定位到某个区块，然后在这个区块里查找目标节点和内容
print("#"*50)
div = soup.find(name="div",id="content")
print(div)

links = div.find_all(name="a")
for link in links:
    print(link.name,link["href"],link.get_text())
    
imgs = div.find_all(name="img")
 
for img in imgs:
    print(img.name,img["src"])
 
 

        