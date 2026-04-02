# Декораторы для обработки ошибок и валидации ввода

import functools  # Импортируем functools для сохранения имени и docstring функции

# =============================
# Декоратор для проверки ввода числа пользователем
# =============================
'''
def validate_int(min_val=None, max_val=None):
    def decorator(func):
        @functools.wraps(func)  # Сохраняем имя и описание исходной функции
        def wrapper(*args, **kwargs):
            while True:
                val = func(*args, **kwargs)
                if not val.isdigit():
                    print("❌ Введите число")
                    continue
                val = int(val)  # Преобразуем строку в число
                if min_val is not None and val < min_val:
                    print(f"❌ Минимум: {min_val}")
                    continue
                if max_val is not None and val > max_val:
                    print(f"❌ Максимум: {max_val}")
                    continue
                return val
        return wrapper
    return decorator
'''
# =============================
# Декоратор для обработки ошибок баз данных
# =============================
def handle_db_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"❌ Ошибка при работе с базой данных: {e}")
            return None
    return wrapper