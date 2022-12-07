"""
@author kingifsh
模拟访问api，拿到json数据返回
"""

import requests
import json

r = requests.get("http://127.0.0.1:5000/returnJson")

print(r.text)

jsonData = json.loads(r.text).encode()

print(jsonData)

datas = """{"username":"啊哈",
         "sex":"女",
         "age":18,
         "email":"12345@qq.com"
        }""".encode('utf8')
        
json.loads(datas)

resp = requests.post('http://localhost:5000/add_user',data = datas)
if resp.status_code == 200:
    print(resp.text)