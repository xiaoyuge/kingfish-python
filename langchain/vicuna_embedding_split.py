from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI,VectorDBQA
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA

# 设置环境变量
#export OPENAI_API_BASE=http://region-9.seetacloud.com:45277/v1
#export OPENAI_API_KEY=EMPTY

# 加载文件夹中的所有txt类型的文件
#loader = DirectoryLoader('/Users/joyce/kingfish-python/kingfish-python/langchain/data', glob='**/*.docx')
loader = DirectoryLoader('/Users/joyce/kingfish-python/kingfish-python/langchain/data', glob='**/*.txt')
# 将数据转成 document 对象，每个文件会作为一个 document
documents = loader.load()

# 初始化加载器
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
# 切割加载的 document
split_docs = text_splitter.split_documents(documents)

# 初始化 openai 的 embeddings 对象
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
# 将 document 通过 openai 的 embeddings 对象计算 embedding 向量信息并临时存入 Chroma 向量数据库，用于后续匹配查询
docsearch = Chroma.from_documents(split_docs, embeddings)

# 创建问答对象
qa = VectorDBQA.from_chain_type(llm=OpenAI(model="text-embedding-ada-002"), chain_type="refine", vectorstore=docsearch,return_source_documents=False)
# 进行问答
result = qa({"query": "王兴渝工作时间最长的公司是哪家？"})
print(result)