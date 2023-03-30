# My OpenAI Key
import logging
import os
import sys

from IPython.display import Markdown, display
from llama_index import GPTTreeIndex, SimpleDirectoryReader

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# use GPTTreeIndex
documents = SimpleDirectoryReader("data").load_data()
tree_index = GPTTreeIndex.from_documents(documents)

tree_index.save_to_disk("tree_index.json")

# try loading
new_tree_index = GPTTreeIndex.load_from_disk("tree_index.json")

# set Logging to DEBUG for more detailed outputs
response_ch = new_tree_index.query("作者叫什么名字?他的最高学历是？")

print(f"中文问题答复：{response_ch}")

# set Logging to DEBUG for more detailed outputs
response_ch = new_tree_index.query("作者一共工作过几家公司？工作时间最长的公司是哪家？")

print(f"中文问题答复：{response_ch}")
