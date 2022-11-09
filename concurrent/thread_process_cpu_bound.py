"""
@author kingifsh
对于CPU密集型业务，对比单线程、多线程和多进程的性能
在我的双核CPU的MAC本上，跑的结果如下：
single_thread cost : 62.778594970703125 seconds
multi_thread cost : 63.94747805595398 seconds
multi_process cost : 35.869956254959106 seconds
也即，因为GIL，多线程相比单线程在CPU密集场景下，性能不升反降，因为多线程多了线程上下文切换的开销
而多进程因为能利用多核真正做到并行，所以性能更好，我的机器是双核，可以看到正好差不多提升2倍
"""

import math
import concurrent.futures
import time

primes = [112272535095293] * 100

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

#用单线程计算
def single_thread():
    for number in primes:
        is_prime(number)
        
#用多线程计算
def multi_thread():
    with concurrent.futures.ThreadPoolExecutor() as pool:
        pool.map(is_prime,primes)
        
#用多进程计算
def multi_process():
    with concurrent.futures.ProcessPoolExecutor() as pool:
        pool.map(is_prime,primes)

#实际运行一下，看看各自花费的时间
if __name__ == "__main__":
    start = time.time();
    single_thread()
    end = time.time();
    print("single_thread cost :",end - start,"seconds")
    
    start = time.time();
    multi_thread()
    end = time.time();
    print("multi_thread cost :",end - start,"seconds")
    
    start = time.time();
    multi_process()
    end = time.time();
    print("multi_process cost :",end - start,"seconds")

        



