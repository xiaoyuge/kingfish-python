"""
@author kingfish
python的thread
"""

import threading

def do_craw(a,b):
    return "do_craw"

def my_func(a,b):
    do_craw(a,b)
    
t = threading.Thread(target=my_func,args=(100,200))

t.start()

t.join()