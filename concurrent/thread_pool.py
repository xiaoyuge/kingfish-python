"""
@author kingfish
线程池的三种使用方法
"""

import concurrent.futures
import blog_spider

#craw，使用pool.map方法，用线程池多个线程执行
with concurrent.futures.ThreadPoolExecutor() as pool:
    htmls = pool.map(blog_spider.craw,blog_spider.urls)
    htmls = list(zip(blog_spider.urls,htmls))
    for url,html in htmls:
        print(url,len(html))

print("craw over")

#parse，使用pool.submit方法，用线程池多个线程执行
with concurrent.futures.ThreadPoolExecutor() as pool:
    futures = {}
    for url,html in htmls:
        future = pool.submit(blog_spider.parse,html)
        futures[future] = url
        
    #for future,url in futures.items():
     #   print(url,future.result())
        
    for future in concurrent.futures.as_completed(futures):
        url = futures[future]
        print(url,future.result())