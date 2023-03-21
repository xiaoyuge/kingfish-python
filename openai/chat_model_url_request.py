import os
import openai
import requests
import json

"""
Temperature is a value between 0 and 1 that essentially lets you control how confident the model should be 
when making these predictions. Lowering temperature means it will take fewer risks, and completions will 
be more accurate and deterministic. Increasing temperature will result in more diverse completions.
"""

openai.organization = "org-EB9Hewj27svx8CRq6TB0RKa3"
openai.api_key = os.getenv("OPENAI_API_KEY")
model_list = openai.Model.list()
## print(model_list)

#尝试请求一下api
openai_url = "https://api.openai.com/v1/chat/completions"
headers = {
    'Content-Type':'application/json',
    'Authorization':f'Bearer {openai.api_key}'
}
datas = {
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "我想训练一个法律行业的基于chatGPT的微调模型，应该怎么做"}],
     "temperature": 1
}
json_data = json.dumps(datas)
r = requests.post(url=openai_url,data=json_data,headers=headers,timeout=200)
if r.status_code == 200:
    resp = r.text
    print(resp)
else:
    print(f'Error Code={r.status_code};message={r.text}')
    