"""
@author kingfish
web应用使用线程池优化性能
"""

import flask
import time
from concurrent.futures import ThreadPoolExecutor
import json

app = flask.Flask(__name__)
pool = ThreadPoolExecutor()

#模拟读取文件
def read_file():
    time.sleep(0.1)
    return "file"

#模拟读取数据库
def read_db():
    time.sleep(0.2)
    return "db"

#模拟通过api读取数据
def read_api():
    time.sleep(0.3)
    return "api"


@app.route("/")
def index():
    #使用线程池的多线程并发执行三个IO任务，所以整体执行时长是单个执行时间最长那个任务的时间
    file_result = pool.submit(read_file)
    db_result = pool.submit(read_db)
    api_result = pool.submit(read_api)
    return json.dumps({
        "file_result":file_result.result(),
        "db_result":db_result.result(),
        "api_result":api_result.result()}
    )
    
if __name__ == "__main__":
    app.run()