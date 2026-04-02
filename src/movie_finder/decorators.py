# Декораторы для обработки ошибок и валидации ввода

import functools  # Импортируем functools для сохранения имени и docstring функции

# =============================
# Декоратор для проверки ввода числа пользователем
# =============================
def validate_int(min_val=None, max_val=None):
    """
    Декоратор для проверки числового ввода.
    min_val - минимальное допустимое значение
    max_val - максимальное допустимое значение
    """
    def decorator(func):
        @functools.wraps(func)  # Сохраняем имя и описание исходной функции
        def wrapper(*args, **kwargs):
            while True:  # Бесконечный цикл до корректного ввода
                val = func(*args, **kwargs)  # Вызываем исходную функцию input()
                if not val.isdigit():  # Проверяем, что введено число
                    print("❌ Введите число")
                    continue
                val = int(val)  # Преобразуем строку в число
                if min_val is not None and val < min_val:  # Проверка минимального значения
                    print(f"❌ Минимум: {min_val}")
                    continue
                if max_val is not None and val > max_val:  # Проверка максимального значения
                    print(f"❌ Максимум: {max_val}")
                    continue
                return val  # Возвращаем корректное число
        return wrapper
    return decorator

# =============================
# Декоратор для обработки ошибок баз данных
# =============================
def handle_db_errors(func):
    """
    Ловим ошибки при работе с базой данных
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)  # Выполняем функцию
        except Exception as e:  # Ловим любое исключение
            print(f"❌ Ошибка при работе с базой данных: {e}")
            return None  # Возвращаем None при ошибке
    return wrapper