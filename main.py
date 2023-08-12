import requests
import json
import time
import openai
import os
from dotenv import dotenv_values
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage

"""Settings"""
config = dotenv_values(".env")
OPEN_AI_TOKEN = config.get("OPEN_AI_TOKEN")
os.environ["OPENAI_API_KEY"] = OPEN_AI_TOKEN
openai.api_key = OPEN_AI_TOKEN


def train_and_save(path: str):
    """Функція для тренування та зберігання індекса"""
    print(f"Start train model")
    if os.path.exists(path):
        documents = SimpleDirectoryReader(path).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir="./storage")
        print(f"Index was saved")


def get_index():
    """Функція отримання індексу"""
    print(f"Start loading index")
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)
    return index


def get_chat_engine():
    """функція створення чату"""
    print(f"Creating chat engine")
    index = get_index()
    chat_engine = index.as_chat_engine()
    return chat_engine


if __name__ == '__main__':
    train_and_save("input")
