# My OpenAI Key
import os
import openai

from llama_index import GPTTreeIndex, SimpleDirectoryReader,LLMPredictor,ServiceContext

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# use GPTTreeIndex
documents = SimpleDirectoryReader("data").load_data()

#define llm
llm_predictor = LLMPredictor(llm=openai(temperature=0, model_name="gpt-3.5-turbo"))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

tree_index = GPTTreeIndex.from_documents(documents,service_context=service_context)

tree_index.save_to_disk("tree_index.json")

# try loading
new_tree_index = GPTTreeIndex.load_from_disk("tree_index.json")

# set Logging to DEBUG for more detailed outputs
response_ch = new_tree_index.query("作者叫什么名字?他的最高学历是？")

print(f"中文问题答复：{response_ch.get_formatted_sources()}")

# set Logging to DEBUG for more detailed outputs
response_ch = new_tree_index.query("作者一共工作过几家公司？工作时间最长的公司是哪家？")

print(f"中文问题答复：{response_ch.get_formatted_sources()}")
