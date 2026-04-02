# Получение статистики запросов из MongoDB

from log_writer import get_mongo_collection
from decorators import handle_db_errors  # Для безопасного подключения и работы с MongoDB

# =============================================
# Получение популярных запросов по частоте
# =============================================
@handle_db_errors
def get_top_queries(limit=5):
    """
    Возвращает список популярных поисковых запросов (по частоте)
    """
    collection = get_mongo_collection()  # Получаем коллекцию
    pipeline = [
        {"$match": {"search_type": "keyword"}},  # Только ключевые слова
        {"$group": {"_id": "$params.keyword", "count": {"$sum": 1}}},  # Группировка и подсчет
        {"$sort": {"count": -1}},  # Сортировка по убыванию
        {"$limit": limit}           # Ограничение по количеству
    ]
    return list(collection.aggregate(pipeline))  # Возвращаем список результатов

# =============================================
# Получение последних поисковых запросов
# =============================================
@handle_db_errors
def get_last_queries(limit=5):
    """
    Возвращает список последних поисковых запросов
    """
    collection = get_mongo_collection()
    cursor = collection.find().sort("timestamp", -1).limit(limit)  # Сортировка по времени
    return list(cursor)  # Преобразуем курсор в список