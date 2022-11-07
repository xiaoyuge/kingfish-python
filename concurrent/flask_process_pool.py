"""
@author kingfish
如果是一个CPU密集型的web应用，我们也可以用多进程来进行性能优化
"""

import flask
from concurrent.futures import ThreadPoolExecutor
import math
import json

app = flask.Flask(__name__)

#计算是否是素数
def is_prime(n):
    if n<2 :
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3,sqrt_n+1,2):
        if n % i==0:
            return False
    return True

@app.route("/is_prime/<numbers>")
def process_pool_prime(numbers):
    numberlist = [int(n) for n in numbers.split(",")]
    results = process_pool.map(is_prime,numberlist)
    return json.dumps(dict(zip(numberlist,results))) 

if __name__== "__main__":
    process_pool = ThreadPoolExecutor()
    app.run()
    