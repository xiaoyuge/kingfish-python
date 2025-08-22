import os
import numpy as np
from PIL import Image
import torch
from transformers import ChineseCLIPModel, ChineseCLIPProcessor
import chromadb  # 导入 Chroma DB
from chromadb.config import Settings

# 配置
IMAGE_DIR = "../img"
MODEL_PATH = "../model/chinese-clip-vit-large-patch14-336px"
CHROMA_PERSIST_DIRECTORY = "../chroma_db"  # Chroma数据持久化目录
CHROMA_COLLECTION_NAME = "image_embeddings"

# 初始化 Chinese-CLIP 模型
print("Loading Chinese-CLIP model...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = ChineseCLIPModel.from_pretrained(MODEL_PATH).to(device)
processor = ChineseCLIPProcessor.from_pretrained(MODEL_PATH)
print("Model loaded successfully!")

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

def extract_image_features(image_path):
    """提取图像特征向量"""
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

def main():
    # 初始化 Chroma 客户端，采用持久化模式
    chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIRECTORY) 

    # 创建或获取一个集合（Collection）。Chroma 会自动处理嵌入的存储和索引。
    # 因为我们自己用 Chinese-CLIP 模型生成向量，所以不需要 Chroma 的嵌入函数，设置 `embedding_function` 为 None。
    collection = chroma_client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME,
        embedding_function=None # 我们提供预计算的向量，所以不需要Chroma的嵌入函数
    )

    image_paths = get_all_image_paths(IMAGE_DIR)
    if not image_paths:
        print("No images found!")
        return

    batch_size = 100  # 批处理大小
    ids_batch = []
    embeddings_batch = []
    metadatas_batch = []
    processed_count = 0

    for i, img_path in enumerate(image_paths):
        try:
            embedding = extract_image_features(img_path)
            if embedding is not None:
                # 构建批次数据
                ids_batch.append(f"id_{i}")
                embeddings_batch.append(embedding.tolist()) 
                metadatas_batch.append({"source": img_path}) 

                processed_count += 1
        except Exception as e:
            print(f"Failed on {img_path}: {e}")

        # 批量添加数据到 Chroma
        if len(ids_batch) >= batch_size:
            collection.add(
                embeddings=embeddings_batch,
                metadatas=metadatas_batch,
                ids=ids_batch
            )
            print(f"Added batch of {len(ids_batch)} embeddings. Total processed: {processed_count}")
            # 重置批次
            ids_batch = []
            embeddings_batch = []
            metadatas_batch = []

    # 添加最后一批数据
    if ids_batch:
        collection.add(
            embeddings=embeddings_batch,
            metadatas=metadatas_batch,
            ids=ids_batch
        )
        print(f"Added final batch of {len(ids_batch)} embeddings. Total processed: {processed_count}")

    print(f"All done! Total {processed_count} image embeddings stored in ChromaDB.")

if __name__ == "__main__":
    main()