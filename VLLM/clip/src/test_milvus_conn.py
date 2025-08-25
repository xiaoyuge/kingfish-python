# 使用 Python 测试连接（需要安装 pymilvus）
from pymilvus import connections, utility

try:
    connections.connect(host='localhost', port='19530')
    print("成功连接到 Milvus")
    print(f"版本: {utility.get_server_version()}")
    collections = utility.list_collections()
    print(f"现有集合: {collections}")
except Exception as e:
    print(f"连接失败: {e}")