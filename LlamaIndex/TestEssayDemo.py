# My OpenAI Key
import logging
import os
import sys

from IPython.display import Markdown, display
from llama_index import GPTTreeIndex, SimpleDirectoryReader

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

documents = SimpleDirectoryReader("data").load_data()
index = GPTTreeIndex.from_documents(documents)

index.save_to_disk("index.json")

# try loading
new_index = GPTTreeIndex.load_from_disk("index.json")

# set Logging to DEBUG for more detailed outputs
response = new_index.query("What did the author do growing up?")

print(response)

# set Logging to DEBUG for more detailed outputs
response = new_index.query("What did the author do after his time at Y Combinator?")

print(response)
