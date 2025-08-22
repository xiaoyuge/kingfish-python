import os
import numpy as np
from PIL import Image
import torch
from transformers import ChineseCLIPModel, ChineseCLIPProcessor
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import time
from tqdm import tqdm

# 配置
IMAGE_DIR = "/img"  # 图片目录
MODEL_PATH = "/model/chinese-clip-vit-large-patch14-336px"  # 模型路径
MILVUS_HOST = 'localhost'  # Milvus 在同一台服务器
MILVUS_PORT = '19530'
COLLECTION_NAME = 'image_search'
VECTOR_DIMENSION = 768  # Chinese-CLIP 模型的向量维度
BATCH_SIZE = 64  # 批处理大小

# 初始化 Chinese-CLIP 模型
print("Loading Chinese-CLIP model...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = ChineseCLIPModel.from_pretrained(MODEL_PATH).to(device)
processor = ChineseCLIPProcessor.from_pretrained(MODEL_PATH)
print("Model loaded successfully!")

def connect_milvus():
    """连接 Milvus 数据库"""
    try:
        connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
        print("Connected to Milvus successfully!")
    except Exception as e:
        print(f"Failed to connect to Milvus: {e}")
        raise

def create_collection():
    """创建 Milvus 集合"""
    if utility.has_collection(COLLECTION_NAME):
        print(f"Collection {COLLECTION_NAME} already exists, dropping it...")
        utility.drop_collection(COLLECTION_NAME)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="image_path", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=VECTOR_DIMENSION)
    ]
    
    schema = CollectionSchema(fields, "Image feature vectors")
    collection = Collection(COLLECTION_NAME, schema)
    
    # 创建索引
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 1024}
    }
    collection.create_index("vector", index_params)
    print(f"Created collection: {COLLECTION_NAME}")
    return collection

def extract_image_features(image_path):
    """提取图像特征向量"""
    try:
        image = Image.open(image_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 预处理图像并提取特征
        inputs = processor(images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
            # 归一化特征向量
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        return image_features.cpu().numpy()[0]
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def get_all_image_paths(directory):
    """获取目录下所有图片路径"""
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')
    image_paths = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(image_extensions):
                image_paths.append(os.path.join(root, file))
    
    print(f"Found {len(image_paths)} images in {directory}")
    return image_paths

def process_images(collection, image_paths):
    """处理所有图片并存储到 Milvus"""
    vectors = []
    paths = []
    processed_count = 0
    failed_count = 0
    
    # 使用 tqdm 显示进度条
    for image_path in tqdm(image_paths, desc="Processing images"):
        try:
            vector = extract_image_features(image_path)
            if vector is not None:
                vectors.append(vector.tolist())  # 转换为列表
                paths.append(image_path)
                processed_count += 1
            else:
                failed_count += 1
        except Exception as e:
            print(f"Failed to process {image_path}: {e}")
            failed_count += 1
        
        # 批处理插入
        if len(vectors) >= BATCH_SIZE:
            insert_batch(collection, paths, vectors)
            vectors = []
            paths = []
    
    # 插入最后一批数据
    if vectors:
        insert_batch(collection, paths, vectors)
    
    # 将数据持久化
    collection.flush()
    print(f"Processing completed! Success: {processed_count}, Failed: {failed_count}")

def insert_batch(collection, paths, vectors):
    """插入一批数据到 Milvus"""
    try:
        entities = [paths, vectors]
        collection.insert(entities)
        print(f"Inserted batch of {len(vectors)} vectors")
    except Exception as e:
        print(f"Failed to insert batch: {e}")

if __name__ == "__main__":
    # 连接 Milvus
    connect_milvus()
    
    # 创建集合
    collection = create_collection()
    
    # 获取所有图片路径
    image_paths = get_all_image_paths(IMAGE_DIR)
    
    if not image_paths:
        print("No images found! Please check your IMAGE_DIR configuration.")
        exit(1)
    
    # 处理图片并存储特征向量
    print("Starting feature extraction...")
    start_time = time.time()
    process_images(collection, image_paths)
    end_time = time.time()
    
    print(f"Feature extraction completed in {end_time - start_time:.2f} seconds")
    
    # 打印集合统计信息
    print(f"Collection statistics: {collection.num_entities} entities")