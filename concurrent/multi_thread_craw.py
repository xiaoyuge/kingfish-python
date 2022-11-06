"""
@author kingfish
多线程爬虫
"""

import blog_spider
import threading
import time 

def single_thread_craw():
    print("single_thread_craw start")
    for url in blog_spider.urls:
        blog_spider.craw(url)
    print("single_thread_craw end")
        
def multi_thread_craw():
    print("multi_thread_craw start")
    threads = []
    for url in blog_spider.urls:
        threads.append(
            threading.Thread(target=blog_spider.craw,args=(url,))
        )
    for thread in threads:
        thread.start()
        
    for thread in threads:
        thread.join()
    print("multi_thread_craw end")
    
if __name__ == "__main__":
    start = time.time()
    single_thread_craw()
    end = time.time();
    print("single_thread_craw cost: ",end-start,"seconds")
    
    start = time.time()
    multi_thread_craw()
    end = time.time();
    print("multi_thread_craw cost: ",end-start,"seconds")
