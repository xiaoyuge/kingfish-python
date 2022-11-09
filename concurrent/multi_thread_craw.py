"""
@author kingfish
单线程爬虫vs多线程爬虫性能对比
我的mac本双核cpu，某次结果数据如下：
single_thread_craw cost:  8.96970796585083 seconds
multi_thread_craw cost:  0.8749051094055176 seconds
"""

import blog_spider
import threading
import time 

#单线程爬取url
def single_thread_craw():
    print("single_thread_craw start")
    for url in blog_spider.urls:
        blog_spider.craw(url)
    print("single_thread_craw end")
        
#多线程爬取url
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
    #单线程爬取，统计一下时间
    start = time.time()
    single_thread_craw()
    end = time.time();
    print("single_thread_craw cost: ",end - start,"seconds")
    
    #多线程爬取，统计一下时间
    start = time.time()
    multi_thread_craw()
    end = time.time();
    print("multi_thread_craw cost: ",end - start,"seconds")
