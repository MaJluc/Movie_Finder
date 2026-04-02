from mysql_connector import *
'''(
    search_by_keyword,
    search_by_genre_and_year,
    get_genres_with_years,
    count_by_keyword,
    count_by_genre_and_year
)'''
from log_writer import log_search
from log_stats import get_top_queries, get_last_queries
from formatter import print_table
from datetime import datetime

# Функция для печати главного меню
def print_menu():
    print("\n==============================")
    print("🎬 ПОИСК ФИЛЬМОВ")
    print("==============================")
    print("1. Поиск по ключевому слову")
    print("2. Поиск по жанру и году")
    print("3. Популярные запросы")
    print("4. Последние запросы")
    print("5. Выход")

# Вспомогательная функция безопасного ввода числа с ограничением попыток
def safe_int_input(text, min_val=None, max_val=None, max_attempts=3):
    attempts = 0
    while True:
        value = input(text)
        if not value.isdigit():
            attempts += 1
            print("❌ Введите число")
        else:
            value = int(value)
            if min_val is not None and value < min_val:
                attempts += 1
                print(f"❌ Минимум: {min_val}")
            elif max_val is not None and value > max_val:
                attempts += 1
                print(f"❌ Максимум: {max_val}")
            else:
                return value

        if attempts >= max_attempts:
            print("⚠️ Слишком много неверных попыток. Возврат в главное меню.")
            return None

# Функция пагинации результатов поиска
def paginate(results_func, count_func, params):
    offset = 0
    limit = 10
    total = count_func(*params)
    print(f"\nВсего найдено: {total}")

    while True:
        results = results_func(*params, limit, offset)
        if not results:
            print("Нет результатов")
            break

        table = []
        for r in results:
            table.append({
                'Название': r['title'],
                'Год релиза': r['release_year']
            })

        print_table(table)

        offset += limit
        if offset >= total:
            print("\nЭто были все результаты")
            break
        cont = input("Показать ещё? (y/n): ")
        if cont.lower() != 'y':
            break

# Функция вывода популярных запросов
def display_top_queries(queries):
    print("\n=== Популярные запросы ===")
    if not queries:
        print("Нет данных")
        return

    table = []
    for q in queries:
        if not isinstance(q, dict):
            continue

        _id = q.get('_id')
        if isinstance(_id, dict):
            keyword_val = _id.get('keyword', '-')
        elif isinstance(_id, str):
            keyword_val = _id
        else:
            keyword_val = '-'

        count_val = q.get('count', '-')
        table.append({'ключевое_слово': keyword_val, 'количество': count_val})

    print_table(table)

# Функция вывода последних запросов
def display_last_queries(queries):
    print("\n=== Последние запросы ===")
    if not queries:
        print("Нет данных")
        return
    table = []
    for q in queries:
        if not isinstance(q, dict):  # Пропускаем, если не словарь
            continue
        search_type = q.get('search_type', '-')
        raw_ts = q.get('timestamp', '-')

        # форматируем timestamp без микросекунд
        if isinstance(raw_ts, datetime):
            timestamp = raw_ts.strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp = str(raw_ts).split('.')[0]

        # Формируем читаемые параметры поиска
        if search_type == 'keyword':
            keyword_val = q.get('params', {}).get('keyword', '-')
            param_str = keyword_val
        elif search_type == 'genre_year':
            params = q.get('params', {})
            genre = params.get('genre', '-')
            start = params.get('start', '-')
            end = params.get('end', '-')
            param_str = f"{genre} ({start}-{end})"
        else:
            param_str = '-'

        count_val = q.get('results_count', '-')
        table.append({'тип_поиска': search_type, 'параметры': param_str, 'количество': count_val, 'время': timestamp})
    print_table(table)


def main():
    print("Проверка: программа запустилась")
    while True:
        print_menu()  # Показываем меню
        choice = input("Выберите пункт: ")

        if choice == '1':
            keyword = input("Введите ключевое слово: ")
            paginate(search_by_keyword, count_by_keyword, (keyword,))
            log_search("keyword", {"keyword": keyword}, count_by_keyword(keyword))


        elif choice == '2':
            genres_years = get_genres_with_years()  # получаем список жанров с годами
            print("\nДоступные жанры и диапазон годов:")
            for idx, (g, min_y, max_y) in enumerate(genres_years, start=1):
                print(f"{idx:2}. {g:<20} {min_y}-{max_y}")

            # Выбор жанра с ограничением на 3 попытки
            genre_number = safe_int_input("Выберите жанр по номеру: ", 1, len(genres_years))
            if genre_number is None:
                continue  # слишком много попыток, возвращаемся в меню

            genre, min_year, max_year = genres_years[genre_number - 1]
            print(f"Выбран жанр: {genre} ({min_year}-{max_year})")

            # Выбор года "от"
            start = safe_int_input(f"От года ({min_year}-{max_year}): ", min_year, max_year)
            if start is None:
                continue

            # Выбор года "до"
            end = safe_int_input(f"До года ({min_year}-{max_year}): ", min_year, max_year)
            if end is None:
                continue

            # Если пользователь перепутал годы, меняем местами
            if start > end:
                print("⚠️ Меняем местами годы")
                start, end = end, start

            # Пагинация поиска и логирование
            paginate(search_by_genre_and_year, count_by_genre_and_year, (genre, start, end))
            log_search("genre_year", {"genre": genre, "start": start, "end": end},
                       count_by_genre_and_year(genre, start, end))

        elif choice == '3':
            queries = get_top_queries(5)  # Получаем 5 популярных
            display_top_queries(queries)

        elif choice == '4':
            queries = get_last_queries(5)  # Получаем 5 последних
            display_last_queries(queries)

        elif choice == '5':  # Выход
            break

        else:
            print("❌ Неверный выбор")

# Точка входа
if __name__ == '__main__':
    main()