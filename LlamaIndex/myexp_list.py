# My OpenAI Key
import logging
import os
import sys

from IPython.display import Markdown, display
from llama_index import GPTListIndex, SimpleDirectoryReader

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

documents = SimpleDirectoryReader("data").load_data()

# use GPTSimpleVectorIndex
list_index = GPTListIndex.from_documents(documents)
list_index.save_to_disk("list_index.json")
new_list_index = GPTListIndex.load_from_disk("list_index.json")

v_response_ch = new_list_index.query("作者叫什么名字?他的最高学历是？")
print(f"v中文问题答复：{v_response_ch}")

v_response_ch = new_list_index.query("作者一共工作过几家公司，工作时间最长的公司是哪家？")
print(f"v中文问题答复：{v_response_ch}")
