# Форматирование и вывод данных в виде таблиц

from tabulate import tabulate


def print_table(results):
    if not results:
        print("Нет данных для отображения")
        return
    print(tabulate(results, headers="keys", tablefmt="grid"))