"""
@author kingfish
使用生产者-消费者模式来爬取url，解析html，并输出到文件
"""
import queue
import blog_spider
import threading
import time
import random

def do_craw(urlQueue:queue.Queue,htmlQueue:queue.Queue):
    while True:
        url = urlQueue.get()
        html= blog_spider.craw(url) 
        htmlQueue.put(html)
        print(threading.current_thread().name,f"craw {url}",f"urlQueue size={urlQueue.qsize()}")
        time.sleep(random.randint(1,2))
        
def do_parse(htmlQueue:queue.Queue,fout):
    while True:
        html = htmlQueue.get()
        results = blog_spider.parse(html)
        for result in results:
            fout.write(str(result)+"\n")
        print(threading.current_thread().name,f"parse {html}",f"htmlQueue size={htmlQueue.qsize()}")
        time.sleep(random.randint(1,2))
        
if __name__ == "__main__":
    #创建两个队列
    urlQueue = queue.Queue()
    htmlQueue = queue.Queue()
    
    #将要爬取的url放入队列
    for url in blog_spider.urls:
        urlQueue.put(url)
    
    #起三个线程进行url爬取并把结果放入队列
    for idx in range(3):
        t = threading.Thread(target=do_craw,args=(urlQueue,htmlQueue),name=f"do_craw_thread-{idx}")
        t.start()
        
    #起两个线程，从队列获取html并解析，然后输出到文件
    fout = open("concurrent/parseResult.txt","w")
    for idx in range(2):
        t = threading.Thread(target=do_parse,args=(htmlQueue,fout),name=f"do_parse_thread-{idx}")
        t.start()