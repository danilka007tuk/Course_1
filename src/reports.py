import datetime
import json
import logging
from typing import Any, Callable, Optional

import pandas as pd

from src.decorators import decorator_spending_by_category

logger = logging.getLogger("report.log")
file_handler = logging.FileHandler("report.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def log_spending_by_category(filename: Any) -> Callable:
    """Логирует результат функции в указанный файл"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs).to_dict("records")
            with open(filename, "w") as f:
                json.dump(result, f, indent=4)
            return result

        return wrapper

    return decorator


@decorator_spending_by_category
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None):
    """Функция возвращающая траты за последние 3 месяца по заданной категории"""
    logger.info("Начало работы")
    list_by_category = []
    final_list = []

    if date is None:
        logger.info("Обработка условия на отсутствие")
        date_start = datetime.datetime.now() - datetime.timedelta(days=90)
        for i in transactions:
            if i["Категория"] == category:
                list_by_category.append(i)
        for i in list_by_category:
            if i["Дата платежа"] == "nan" or type(i["Дата платежа"]) is float:
                continue
            elif (
                    date_start
                    <= datetime.datetime.strptime(str(i["Дата платежа"]), "%d.%m.%Y")
                    <= date_start + datetime.timedelta(days=90)
            ):
                final_list.append(i["Сумма платежа"])
        return final_list
    else:
        logger.info("Обработка условия на создание")
        day, month, year = date.split(".")
        date_obj = datetime.datetime(int(year), int(month), int(day))
        date_start = date_obj - datetime.timedelta(days=90)

        for i in transactions:
            if i["Категория"] == category:
                list_by_category.append(i)

        for i in list_by_category:
            if i["Дата платежа"] == "nan" or type(i["Дата платежа"]) is float:
                continue
            else:
                day_, month_, year_ = i["Дата платежа"].split(".")
                date_obj_ = datetime.datetime(int(year), int(month), int(day))
                if date_start <= date_obj_ <= date_start + datetime.timedelta(days=90):
                    final_list.append(i["Сумма платежа"])
        logger.info("Завершение работы функции")
        data_json = json.dumps(final_list, indent=4, ensure_ascii=False, )

        return data_json

# def log(filename: Optional[str] = None) -> Callable:
#     """Декоратор log который автоматически регистрирует детали выполнения функций,
#     имя функции, передаваемые аргументы,
#     результат выполнения и информация об ошибках"""
#
#     def my_decorators_error(function: Callable) -> Callable:
#         @wraps(function)
#         def wrapper(*args: tuple, **kwargs: dict) -> Any:
#             try:
#                 if filename:
#                     with open(filename, "a") as file:
#                         file.write(f"{function.__name__}: inputs: {args}, kwargs: {kwargs}\n")
#                 else:
#                     print(f"Запуск функции {function.__name__}, Inputs: {args}, kwargs: {kwargs}")
#
#                 result = function(*args, **kwargs)
#
#                 if filename:
#                     with open(filename, "a") as file:
#                         file.write(f"{function.__name__} ok: {result}\n")
#                 else:
#                     print(f"Результат: {result}")
#                     print(f"Функция {function.__name__} успешно выполнена.")
#
#                 return result
#
#             except Exception as e:
#                 error_message = f"Ошибка в функции {function.__name__}: {e}"
#                 if filename:
#                     with open(filename, "a") as file:
#                         file.write(error_message + "\n")
#                 else:
#                     print(error_message)
#                 raise
#             return result
#
#         return wrapper
#
#     return my_decorators_error
#
#
#
# def spending_by_category(transactions: pd.DataFrame,
#                          category: str,
#                          date: Optional[str] = None) -> pd.DataFrame:
#     transactions_1 = []
#     transactions = pd.read_excel("operations.xlsx")
#     for transactions in transactions_1:
#         if transactions:
#             print(transactions)
