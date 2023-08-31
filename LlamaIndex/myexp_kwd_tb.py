# My OpenAI Key
import logging
import os
import sys

from IPython.display import Markdown, display
from llama_index import GPTKeywordTableIndex, SimpleDirectoryReader

# 设置日志级别
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# 设置环境变量
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# 加载文档
documents = SimpleDirectoryReader("data").load_data()

# use GPTSimpleVectorIndex
# 使用GPTKeywordTableIndex
# 使用GPTKeywordTableIndex，从文档中加载关键词表
kwd_tb_index = GPTKeywordTableIndex.from_documents(documents)
# 保存关键词表到文件中
kwd_tb_index.save_to_disk("kwd_tb_index.json")
# 加载新的关键词表
new_kwd_tb_index = GPTKeywordTableIndex.load_from_disk("kwd_tb_index.json")

# 查询中文问题答复
v_response_ch = new_kwd_tb_index.query("作者叫什么名字?他的最高学历是？")
print(f"v中文问题答复：{v_response_ch}")

v_response_ch = new_kwd_tb_index.query("作者一共工作过几家公司，工作时间最长的公司是哪家？")
print(f"v中文问题答复：{v_response_ch}")