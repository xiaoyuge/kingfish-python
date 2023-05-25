import os
from langchain.llms import  OpenAI

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = OpenAI(model_name="text-davinci-003",max_tokens=1024)
result  = llm("怎么评价人工智能")
print(result)
