# My OpenAI Key
import logging
import os
import sys

from IPython.display import Markdown, display
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

documents = SimpleDirectoryReader("data").load_data()

# use GPTSimpleVectorIndex
v_index = GPTSimpleVectorIndex.from_documents(documents)
v_index.save_to_disk("v_index.json")
new_v_index = GPTSimpleVectorIndex.load_from_disk("v_index.json")

v_response_ch = new_v_index.query("作者叫什么名字?他的最高学历是？")
print(f"v中文问题答复：{v_response_ch}")

v_response_ch = new_v_index.query("作者一共工作过几家公司，工作时间最长的公司是哪家？")
print(f"v中文问题答复：{v_response_ch}")
