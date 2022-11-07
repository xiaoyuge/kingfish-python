"""
@author kingfish
爬虫的url管理器
"""

class UrlManager():
    
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
    
    #新增一个待爬取Url
    def add_new_url(self,url):
        if url is None or len(url) == 0:
            return
        if url in self.new_urls or url in self.old_urls:
            return
        self.new_urls.add(url)
    
    #批量新增url
    def add_new_urls(self,urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
           self.add_new_url(url)
    
    #获取一个要爬取的url
    def get_url(self):
        if self.has_new_url():
            url = self.new_urls.pop()
            self.old_urls.add(url)
            return url
        else:
            return None
    
    #判断是否有待爬取的url
    def has_new_url(self):
        return len(self.new_urls) > 0
    
    
if __name__ == "__main__":
    url_manager = UrlManager()
    
    #添加两个url，批量添加故意添加一个重复的url，看去重是否ok
    url_manager.add_new_url("url1")
    url_manager.add_new_urls(["url1","url2"])
    print(url_manager.new_urls,url_manager.old_urls)
    
    #获取一个url，然后打印两个集合
    print("#"*30)
    new_url = url_manager.get_url()
    print(url_manager.new_urls,url_manager.old_urls)
    
    #再获取一个url，然后打印两个集合
    print("#"*30)
    new_url = url_manager.get_url()
    print(url_manager.new_urls,url_manager.old_urls)
    
    #看看两个集合中还有没有Url
    print("#"*30)
    print(url_manager.has_new_url())
    
        
        
        
        