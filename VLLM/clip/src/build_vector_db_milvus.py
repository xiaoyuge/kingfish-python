import os
import numpy as np
from PIL import Image
import torch
from transformers import ChineseCLIPModel, ChineseCLIPProcessor
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import time
from tqdm import tqdm

# 配置
IMAGE_DIR = "/root/autodl-tmp/"  # 图片目录
MODEL_PATH = "/opt/yueqian/model/chinese-clip-vit-huge-patch14/"  # 模型路径
MILVUS_HOST = 'localhost'  # Milvus 在同一台服务器
MILVUS_PORT = '19530'
COLLECTION_NAME = 'image_search'
VECTOR_DIMENSION = 1024  # Chinese-CLIP 模型的向量维度
BATCH_SIZE = 1024  # 批处理大小

# 初始化 Chinese-CLIP 模型
print("Loading Chinese-CLIP model...")
is_cuda=torch.cuda.is_available()
print(f"current device is cuda : {is_cuda}")
device = torch.device("cuda" if is_cuda else "cpu")
model = ChineseCLIPModel.from_pretrained(MODEL_PATH).to(device)
processor = ChineseCLIPProcessor.from_pretrained(MODEL_PATH,use_fast=True)
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
        # 确保图片是RGB格式
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
                abs_image_path = os.path.join(root, file)
                print(f"Found abs_image_path : {abs_image_path}")
                # 添加绝对路径到列表
                image_paths.append(abs_image_path)
    
    print(f"Found {len(image_paths)} images in {directory}")
    return image_paths

def process_images(collection, image_paths):
    """处理所有图片并存储到 Milvus"""
    vectors = []
    paths = []
    processed_count = 0
    failed_count = 0
    batch_count = 0
    
    # 使用 tqdm 显示进度条
    for image_path in tqdm(image_paths, desc="Processing images"):
        try:
            vectaor = extract_image_features(image_path)
            if vector is not None:
                # 检查向量维度是否正确
                if len(vector) != VECTOR_DIMENSION:
                    print(f"Warning: Invalid vector dimension {len(vector)} for {image_path}, expected {VECTOR_DIMENSION}")
                    failed_count += 1
                    continue
                vectors.append(vector.tolist())  # 转换为列表
                # 关键步骤：计算相对路径
                rel_image_path = os.path.relpath(image_path, IMAGE_DIR) 
                # 确保以 '/' 开头，保持和OSS路径一致
                rel_image_path = '/' + rel_image_path 
                print(f"get rel_image_path : {rel_image_path} from abs_img_path : {image_path}")
                paths.append(rel_image_path)
                processed_count += 1
            else:
                failed_count += 1
        except Exception as e:
            print(f"Failed to process {image_path}: {e}")
            failed_count += 1
        
        # 批处理插入
        if len(vectors) >= BATCH_SIZE:
            batch_count += 1
            print(f"Inserting batch {batch_count} with {len(vectors)} vectors")
            insert_batch(collection, paths, vectors)
            vectors = []
            paths = []
    
    # 插入最后一批数据
    if vectors:
        batch_count += 1
        print(f"Inserting final batch {batch_count} with {len(vectors)} vectors")
        insert_batch(collection, paths, vectors)
    
    # 将数据持久化
    collection.flush()
    print(f"Processing completed! Success: {processed_count}, Failed: {failed_count}, Total batches: {batch_count}")

def insert_batch(collection, paths, vectors):
    """插入一批数据到 Milvus"""
    try:
        # 确保路径和向量的数量一致
        if len(paths) != len(vectors):
            print(f"Warning: Mismatch between paths ({len(paths)}) and vectors ({len(vectors)})")
            # 取最小值，确保数量一致
            min_len = min(len(paths), len(vectors))
            paths = paths[:min_len]
            vectors = vectors[:min_len]
        # 插入Milvus
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