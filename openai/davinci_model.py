import os
import openai
import requests
import json

#尝试请求一下api
openai_url = "https://api.openai.com/v1/completions"
headers = {
    'Content-Type':'application/json',
    'Authorization':f'Bearer {openai.api_key}'
}
datas = {
     "model": "code-davinci-002",
     "messages": [{"role": "user", "content": "可以用python写一个爬取安居客网站上的二手房数据的代码吗"}],
     "temperature": 0.7
}
json_data = json.dumps(datas)
r = requests.post(url=openai_url,data=json_data,headers=headers,timeout=200)
if r.status_code == 200:
    resp = r.text
    print(resp)
else:
    print(f'Error Code={r.status_code};message={r.text}')
    