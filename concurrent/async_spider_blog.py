"""
@author kingfish
之前我们用单线程和多线程分别实现了爬虫
这个例子用协程实现爬虫，和之前对比一下性能
注意：
之前的多线程编程中，我们使用的是 requests 库，但这里用的是 aiohttp 库
原因就是 requests 库并不兼容 Asyncio，但是 aiohttp 库兼容
"""
import asyncio
import aiohttp
import blog_spider
import time

async def async_craw(url):
    print("craw url:",url)
    async with aiohttp.ClientSession() as session:
        async with  session.get(url) as resp:
            result = await resp.text()
            print(f"craw url:{url},{len(result)}")

loop = asyncio.get_event_loop()

tasks = [
    loop.create_task(async_craw(url))
    for url in blog_spider.urls 
]

start = time.time()
loop.run_until_complete(asyncio.wait(tasks))
end = time.time()
print("use time seconds :",end-start)

