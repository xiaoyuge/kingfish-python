"""
@author kingfish
之前我们用单线程和多线程分别实现了爬虫
这个例子用协程实现爬虫，和之前对比一下性能
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

