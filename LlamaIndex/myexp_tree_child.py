# My OpenAI Key
import logging
import os

from llama_index import GPTTreeIndex, SimpleDirectoryReader

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# use GPTTreeIndex
documents = SimpleDirectoryReader("data").load_data()
tree_index_child = GPTTreeIndex.from_documents(documents)

tree_index_child.save_to_disk("tree_index_child.json")

# try loading
new_tree_index_child = GPTTreeIndex.load_from_disk("tree_index_child.json")

# set Logging to DEBUG for more detailed outputs
response_ch = new_tree_index_child.query("作者叫什么名字?他的最高学历是？", child_branch_factor=2)

print(f"中文问题答复：{response_ch}")

# set Logging to DEBUG for more detailed outputs
response_ch = new_tree_index_child.query("作者工作时间最长的公司是哪家？", child_branch_factor=2)

print(f"中文问题答复：{response_ch}")

# set Logging to DEBUG for more detailed outputs
response_ch = new_tree_index_child.query("作者擅长的技术有哪些？", child_branch_factor=2)

print(f"中文问题答复：{response_ch}")
