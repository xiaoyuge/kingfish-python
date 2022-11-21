"""
@author kingfish
爬取一下cnblogs，这是个SPA应用，也即加载首页url后，再访问其他页面，浏览器url是不变的
其他页面内容是通过Ajax或fetch异步加载数据然后更新dom的
我们的目标：
1.爬取前20页；
2.获取每页上的文章列表，包括每个文章的标题，作者，点赞数，评论数和浏览数
"""
import requests
import json
from bs4 import BeautifulSoup

craw_url = "https://www.cnblogs.com/AggSite/AggSitePostList"

#构造url请求要post的数据
postDatas = []
for page in range(1,21):
    postData = {}
    postData["CategoryType"] = "SiteHome"
    postData["ParentCategoryId"] = 0
    postData["CategoryId"] = 808
    postData["PageIndex"] = page
    postData["TotalPostCount"] = 4000
    postData["ItemListActionName"] = "AggSitePostList"
    postDatas.append(postData)

print(postDatas)

#构造url的request headers
headers = {
    "accept":"text/plain, */*; q=0.01",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9,en;q=0.8",
    "content-type":"application/json; charset=UTF-8"
}

#遍历postDatas，请求url
with open("crawler/cnblogs/cnBlogArticles.txt","w") as fout:
    for data in postDatas:
        r = requests.post(craw_url,data=json.dumps(data),headers=headers,timeout=3)
        if r.status_code != 200:
            print("error return code ",r.status_code)
            continue
        #返回状态码没问题，拿到内容，开始解析
        content = r.text
        soup = BeautifulSoup(content,"html.parser")
        #先找到article节点
        article_nodes = soup.find_all("article"   ,class_="post-item")
        for article_node in article_nodes:
            #拿到文章标题和url
            article_a = article_node.find("a",class_="post-item-title",recursive=True)
            article_title = article_a.get_text()
            article_url = article_a["href"]
            print(article_url,article_title)
            #拿到文章的点赞、浏览和评论数
            interactNum = []
            btns =  article_node.find_all("a",class_="post-meta-item btn",recursive=True)
            for btn in btns:
                num = btn.find("span")
                interactNum.append(num.get_text())
                
            print(interactNum)
            starNum = interactNum[0]
            commentNum = interactNum[1]
            viewNum = interactNum[2]
            
            #输出到文件
            fout.write("%s\t%s\t点赞数：%s\t评论数：%s\t浏览数：%s\n"%(article_url,article_title,starNum,commentNum,viewNum))
        
        
    
    