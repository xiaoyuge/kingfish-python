from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI

# 设置环境变量
#export OPENAI_API_BASE=http://region-9.seetacloud.com:45277/v1
#export OPENAI_API_KEY=EMPTY

embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
# wget https://raw.githubusercontent.com/hwchase17/langchain/master/docs/modules/state_of_the_union.txt
loader = TextLoader('/Users/joyce/kingfish-python/kingfish-python/langchain/data/resume.txt')
#loader = DirectoryLoader('/Users/joyce/kingfish-python/kingfish-python/langchain/data', glob='**/*.docx')
index = VectorstoreIndexCreator(embedding=embedding).from_loaders([loader])

llm = OpenAI(model="text-embedding-ada-002") # select your faux openai model name
# llm = OpenAI(model="gpt-3.5-turbo")

questions = [
             "作者叫什么名字?他的最高学历是？", 
             "作者工作时间最长的公司是哪家？", 
             "作者擅长的技术有哪些？", 
            ]

for query in questions:
    print("Query: ", query)
    print("Ans: ",index.query(query,llm=llm))