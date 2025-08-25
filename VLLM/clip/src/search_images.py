import os
import numpy as np
from PIL import Image
import torch
from transformers import ChineseCLIPModel, ChineseCLIPProcessor
from pymilvus import connections, Collection
import argparse

# 配置
MODEL_PATH = "/opt/yueqian/model/chinese-clip-vit-huge-patch14/"
MILVUS_HOST = 'localhost'
MILVUS_PORT = '19530'
COLLECTION_NAME = 'image_search'
TOP_K = 10  # 返回最相似的前K个结果

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

def extract_image_features(image_path):
    """从本地图像文件提取特征向量"""
    try:
        image = Image.open(image_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        inputs = processor(images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        return image_features.cpu().numpy()[0]
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def extract_text_features(text):
    """从文本提取特征向量"""
    try:
        inputs = processor(text=text, return_tensors="pt", padding=True).to(device)
        with torch.no_grad():
            text_features = model.get_text_features(**inputs)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        
        return text_features.cpu().numpy()[0]
    except Exception as e:
        print(f"Error processing text: {e}")
        return None

def search_similar_images(query_vector, top_k=TOP_K):
    """在 Milvus 中搜索相似图像"""
    try:
        # 加载集合
        collection = Collection(COLLECTION_NAME)
        collection.load()
        
        # 搜索参数
        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10}
        }
        
        # 执行搜索
        results = collection.search(
            data=[query_vector],
            anns_field="vector",
            param=search_params,
            limit=top_k,
            output_fields=["image_path"]
        )
        
        # 处理结果
        similar_images = []
        for hits in results:
            for hit in hits:
                similar_images.append({
                    "image_path": hit.entity.get("image_path"),
                    "score": hit.score
                })
        
        return similar_images
    except Exception as e:
        print(f"Search failed: {e}")
        return []

def search_by_image(image_path):
    """通过图像搜索"""
    print(f"Searching by image: {image_path}")
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return
    
    query_vector = extract_image_features(image_path)
    if query_vector is None:
        return
    
    results = search_similar_images(query_vector)
    print("\nSearch results:")
    for i, result in enumerate(results):
        print(f"{i+1}. {result['image_path']} (score: {result['score']:.4f})")

def search_by_text(text):
    """通过文本搜索"""
    print(f"Searching by text: {text}")
    query_vector = extract_text_features(text)
    if query_vector is None:
        return
    
    results = search_similar_images(query_vector)
    print("\nSearch results:")
    for i, result in enumerate(results):
        print(f"{i+1}. {result['image_path']} (score: {result['score']:.4f})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search similar images")
    parser.add_argument("--image", help="Path to query image")
    parser.add_argument("--text", help="Text query")
    
    args = parser.parse_args()
    
    # 连接 Milvus
    connect_milvus()
    
    # 执行搜索
    if args.image:
        search_by_image(args.image)
    elif args.text:
        search_by_text(args.text)
    else:
        print("Please provide either --image or --text argument")
        print("Example:")
        print("  python search_images.py --image /path/to/query.jpg")
        print("  python search_images.py --text \"清华学堂前穿着汉服的美女\"")