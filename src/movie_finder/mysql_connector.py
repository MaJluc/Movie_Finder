# Работа с MySQL: поиск фильмов и получение информации о жанрах и годах

import pymysql  # Для подключения к MySQL
from dotenv import load_dotenv  # Для чтения .env
import os
from decorators import handle_db_errors  # Импортируем декоратор для обработки ошибок

# Загружаем переменные окружения
load_dotenv()
MYSQL_HOST = os.getenv("MYSQL_HOST")       # Хост MySQL
MYSQL_USER = os.getenv("MYSQL_USER")       # Имя пользователя MySQL
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")  # Пароль пользователя
MYSQL_DB = os.getenv("MYSQL_DB")           # Имя базы данных

# =============================================
# Создание подключения к MySQL
# =============================================
@handle_db_errors
def get_connection():
    """
    Создает соединение с MySQL
    """
    return pymysql.connect(
        host=MYSQL_HOST,                      # Хост
        user=MYSQL_USER,                      # Пользователь
        password=MYSQL_PASSWORD,              # Пароль
        database=MYSQL_DB,                    # База данных
        cursorclass=pymysql.cursors.DictCursor  # Курсор возвращает словари
    )

# =============================================
# Получаем все жанры с минимальным и максимальным годом
# =============================================
@handle_db_errors
def get_genres_with_years():
    """
    Возвращает список кортежей (жанр, min_year, max_year)
    """
    conn = get_connection()  # Подключаемся
    with conn.cursor() as cur:  # Создаем курсор
        # SQL-запрос для получения жанров и диапазона годов
        cur.execute("""
            SELECT g.name AS genre,
                   MIN(f.release_year) AS min_year,
                   MAX(f.release_year) AS max_year
            FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category g ON fc.category_id = g.category_id
            GROUP BY g.name
            ORDER BY g.name
        """)
        result = cur.fetchall()  # Получаем все результаты
    conn.close()  # Закрываем соединение
    return [(r['genre'], r['min_year'], r['max_year']) for r in result]  # Возвращаем список кортежей

# =============================================
# Поиск фильмов по ключевому слову
# =============================================
@handle_db_errors
def search_by_keyword(keyword, limit, offset):
    """
    keyword: ключевое слово
    limit: количество результатов
    offset: смещение для пагинации
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT title, release_year
            FROM film
            WHERE title LIKE %s
            ORDER BY title
            LIMIT %s OFFSET %s
        """, (f"%{keyword}%", limit, offset))
        result = cur.fetchall()
    conn.close()
    return result

# =============================================
# Подсчет фильмов по ключевому слову
# =============================================
@handle_db_errors
def count_by_keyword(keyword):
    """
    Возвращает количество фильмов, подходящих под ключевое слово
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) AS cnt FROM film WHERE title LIKE %s", (f"%{keyword}%",))
        result = cur.fetchone()
    conn.close()
    return result['cnt'] if result else 0

# =============================================
# Поиск фильмов по жанру и диапазону годов
# =============================================
@handle_db_errors
def search_by_genre_and_year(genre, start, end, limit, offset):
    """
    genre: жанр
    start: начальный год
    end: конечный год
    limit: количество результатов
    offset: смещение
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT f.title, f.release_year
            FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category g ON fc.category_id = g.category_id
            WHERE g.name=%s AND f.release_year BETWEEN %s AND %s
            ORDER BY f.title
            LIMIT %s OFFSET %s
        """, (genre, start, end, limit, offset))
        result = cur.fetchall()
    conn.close()
    return result

# =============================================
# Подсчет фильмов по жанру и году
# =============================================
@handle_db_errors
def count_by_genre_and_year(genre, start, end):
    """
    Возвращает количество фильмов в жанре за выбранный диапазон
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*) AS cnt
            FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category g ON fc.category_id = g.category_id
            WHERE g.name=%s AND f.release_year BETWEEN %s AND %s
        """, (genre, start, end))
        result = cur.fetchone()
    conn.close()
    return result['cnt'] if result else 0