# Логирование поисковых запросов в MongoDB

from pymongo import MongoClient  # Работа с MongoDB
from dotenv import load_dotenv
import os
from decorators import handle_db_errors
from datetime import datetime

# Загружаем переменные окружения
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

# =============================================
# Подключение к MongoDB
# =============================================
@handle_db_errors
def get_mongo_collection():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return db[MONGO_COLLECTION]

# =============================================
# Логирование поиска
# =============================================
@handle_db_errors
def log_search(search_type, params, results_count):
    collection = get_mongo_collection()
    doc = {
        "timestamp": datetime.now(),
        "search_type": search_type,
        "params": params,
        "results_count": results_count
    }
    collection.insert_one(doc)