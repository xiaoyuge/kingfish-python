"""
@author kingfish
这是一个非线程安全的例子
尽管大部分时候它能够打印 100，但有时侯也会打印 99 或者 98。
这其实就是因为，n+=1这一句代码让线程并不安全。foo 这个函数实际上由下面四行 bytecode 组成
>>> import dis
>>> dis.dis(foo)
LOAD_GLOBAL              0 (n)
LOAD_CONST               1 (1)
INPLACE_ADD
STORE_GLOBAL             0 (n)
而这四行 bytecode 中间都是有可能被打断的
我们还是需要 lock 等工具，来确保线程安全，见下面的safe_foo函数
"""
import threading

n = 0

#非线程安全
def foo():
    global n
    n += 1

#线程安全的写法
lock = threading.Lock()
def safe_foo():
    global n
    with lock:
      n += 1  

threads = []
for i in range(100):
    t = threading.Thread(target=foo)
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print(n)