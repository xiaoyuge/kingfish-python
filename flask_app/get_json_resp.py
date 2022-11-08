"""
@author kingifsh
模拟访问api，拿到json数据返回
"""

import requests
import json

r = requests.get("http://127.0.0.1:5000/returnJson")

print(r.text)

jsonData = json.loads(r.text)

print(jsonData)