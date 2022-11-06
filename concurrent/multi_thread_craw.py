"""
@author kingfish
多线程爬虫
"""

import blog_spider
import threading

def single_thread_craw():
    for url in blog_spider.urls:
        blog_spider.craw(url)
        
def multi_thread_craw():
    threads = []
    for url in blog_spider.urls:
        threads.append(
            threading.Thread(target=blog_spider.craw,args=(url,))
        )
    for thread in threads:
        thread.start()
        
    for thread in threads:
        thread.join()