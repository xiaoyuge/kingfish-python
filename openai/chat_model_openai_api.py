import os
import openai

#openai.organization = "org-EB9Hewj27svx8CRq6TB0RKa3"
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)

response = openai.Completion.create(model='text-davinci-003',prompt='我想训练一个法律行业的基于chatGPT的微调模型，应该怎么做',temperature=0,max_tokens=700)

result = response.choices[0].text

print(result)

    