# Получение статистики запросов из MongoDB

from log_writer import get_mongo_collection
from decorators import handle_db_errors  # Для безопасного подключения и работы с MongoDB

# =============================================
# Получение популярных запросов по частоте
# =============================================
@handle_db_errors
def get_top_queries(limit=5):
    collection = get_mongo_collection()
    pipeline = [
        {"$match": {"search_type": "keyword"}},
        {"$group": {"_id": "$params.keyword", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    return list(collection.aggregate(pipeline))

# =============================================
# Получение последних поисковых запросов
# =============================================
@handle_db_errors
def get_last_queries(limit=5):
    collection = get_mongo_collection()
    cursor = collection.find().sort("timestamp", -1).limit(limit)
    return list(cursor)