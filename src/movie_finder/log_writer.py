# Логирование поисковых запросов в MongoDB

from pymongo import MongoClient  # Работа с MongoDB
from dotenv import load_dotenv
import os
from decorators import handle_db_errors  # Декоратор для обработки ошибок
from datetime import datetime  # Для timestamp

# Загружаем переменные окружения
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")  # Строка подключения
MONGO_DB = os.getenv("MONGO_DB")    # Имя базы данных
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")  # Коллекция

# =============================================
# Подключение к MongoDB
# =============================================
@handle_db_errors
def get_mongo_collection():
    """
    Возвращает объект коллекции MongoDB
    """
    client = MongoClient(MONGO_URI)  # Подключение к MongoDB
    db = client[MONGO_DB]            # Выбираем базу данных
    return db[MONGO_COLLECTION]      # Возвращаем коллекцию

# =============================================
# Логирование поиска
# =============================================
@handle_db_errors
def log_search(search_type, params, results_count):
    """
    search_type: 'keyword' или 'genre_year'
    params: словарь параметров поиска
    results_count: количество результатов
    """
    collection = get_mongo_collection()  # Получаем коллекцию
    doc = {
        "timestamp": datetime.now(),    # Текущее время
        "search_type": search_type,     # Тип поиска
        "params": params,               # Параметры поиска
        "results_count": results_count  # Количество результатов
    }
    collection.insert_one(doc)          # Вставляем документ в коллекцию