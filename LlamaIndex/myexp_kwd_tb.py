# My OpenAI Key
import logging
import os
import sys

from IPython.display import Markdown, display
from llama_index import GPTKeywordTableIndex, SimpleDirectoryReader

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

documents = SimpleDirectoryReader("data").load_data()

# use GPTSimpleVectorIndex
kwd_tb_index = GPTKeywordTableIndex.from_documents(documents)
kwd_tb_index.save_to_disk("kwd_tb_index.json")
new_kwd_tb_index = GPTKeywordTableIndex.load_from_disk("kwd_tb_index.json")

v_response_ch = new_kwd_tb_index.query("作者叫什么名字?他的最高学历是？")
print(f"v中文问题答复：{v_response_ch}")

v_response_ch = new_kwd_tb_index.query("作者一共工作过几家公司，工作时间最长的公司是哪家？")
print(f"v中文问题答复：{v_response_ch}")
