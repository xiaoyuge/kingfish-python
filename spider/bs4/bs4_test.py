"""
@author = kingfish
用BeautifulSoup这个库，可以对Html的内容进行解析
"""

from bs4 import BeautifulSoup

with open("spider/bs4/helloworld.html") as fin:
    html_doc = fin.read()
    
soup = BeautifulSoup(html_doc,"html.parser")

links= soup.findAll("a")

for link in links:
    print(link.name,link["href"],link.get_text())