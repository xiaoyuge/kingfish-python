"""
@author kingfish
多线程加锁
"""
import threading
import time

lock = threading.Lock()

class Account:
    def __init__(self,balance):
        self.balance = balance
        
def draw(account,amount):
    with lock:
        if account.balance >= amount:
            time.sleep(0.1)
            print(threading.current_thread().name,"取钱成功")
            account.balance -= amount
            print(f"余额{account.balance}")
        else:
            print(threading.current_thread().name,"取钱失败，余额不足")
            print("余额%d" %account.balance)
        
if __name__ == "__main__":
    account = Account(1000)
    ta = threading.Thread(target=draw,args=(account,800),name="ta")
    tb = threading.Thread(target=draw,args=(account,800),name="tb")
    
    ta.start()
    tb.start()