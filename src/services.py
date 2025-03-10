# import pandas as pd
# import json
# import re
# from typing import Dict, List
# import os
# from src.my_logging import get_logger
#
# current_dir = os.path.dirname(os.path.abspath(__file__))
# file_path_1 = os.path.join(current_dir, "../logs", "simple_search.log")
# logger = get_logger("simple_search", file_path_1)
import json
import logging

# Настройка логгера для записи в файл app.search.log
logging.basicConfig(
    filename="app.search.log",  # Логи будут записываться в файл app.search.log
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат лог-сообщений
)

def search_transactions(df, query):
    """
    Ищет транзакции, содержащие запрос в описании или категории.
    Аргументы:
    df (pandas._DataFrame): Данные о транзакциях.
    _query (str): Поисковый запрос.
    Возвращает:
    str: JSON-ответ со списком найденных транзакций.
    """
    # Логгируем начало поиска
    logging.info(f"Начинаем поиск транзакций по запросу: {query}")

    query = query.lower()  # Приводим запрос к нижнему регистру

    # Приводим столбцы "Описание" и "Категория" к строковому типу и удаляем лишние пробелы
    df["Описание"] = df["Описание"].astype(str).str.strip()
    df["Категория"] = df["Категория"].astype(str).str.strip()

    # Преобразуем все столбцы с типом Timestamp в строку
    for column in df.select_dtypes(include=["datetime64"]).columns:
        df[column] = df[column].dt.strftime("%Y-%m-%d %H:%M:%S")

    # Фильтруем транзакции с помощью filter и lambda
    filtered_transactions = filter(
        lambda row: query in str(row["Описание"]).lower() or query in str(row["Категория"]).lower(),
        df.to_dict(orient="records"),
    )

    filtered_transactions_list = list(filtered_transactions)

    # Логгируем количество найденных транзакций
    logging.info(f"Найдено {len(filtered_transactions_list)} транзакций по запросу '{query}'.")

    # Если транзакции не найдены, записываем предупреждение
    if len(filtered_transactions_list) == 0:
        logging.warning(f"По запросу '{query}' не найдено ни одной транзакции.")

    # Преобразуем результат в JSON и возвращаем
    result = (
        json.dumps(filtered_transactions_list, ensure_ascii=False, indent=4) if filtered_transactions_list else "[]"
    )

    # Логгируем результат, который возвращается
    logging.info(f"Результат поиска: {result}")

    return result


#
#
# def simple_search() -> str:
#     """Основная функция поиска, отвечающая за взаимодействие с пользователем."""
#     logger.info(f"Данная функция {simple_search.__name__}
#     запрашивает у пользователя ввести строку для простого поиска")
#     print("Привет! Добро пожаловать в программу работы поиска строки.")
#     print("Выберите пункт меню:")
#     print("1. Получить информацию о транзакциях из XLSX-файла")
#     choice = input("Пользователь: ")
#     transactions_data = []
#     match choice:
#         case "1":
#             print("Для обработки выбран XLSX-файл.")
#             transactions_data = read_file("../data/operations.xlsx")
#     if not transactions_data:
#         print("Не удалось распознать транзакции из файла.")
#         return json.dumps({"error": "Не удалось распознать транзакции из файла."}, ensure_ascii=False, indent=4)
#
#     do_filter_by_description = False
#     user_input = input("Отфильтровать список транзакций по описанию? Да/Нет\nПользователь: ").lower()
#     if user_input == "да":
#         do_filter_by_description = True
#
#     if do_filter_by_description:
#         user_input = input(
#             "Какие именно операции отразить в списке транзакций?\n"
#             "(Введите любую строку из ключа 'описание' в файле operations.xlsx)\n"
#             "Пользователь: "
#         ).strip()
#         transactions_data = filter_transactions(transactions_data, user_input)
#
#     if not transactions_data:
#         print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
#         return json.dumps({"error": "Транзакции не найдены."}, ensure_ascii=False, indent=4)
#     else:
#         print("Распечатываем итоговый список транзакций...")
#         result = []
#         for transaction in transactions_data:
#             if transaction:
#                 description = transaction.get("Описание")
#                 if description:
#                     result.append(transaction)
#         return json.dumps(result, ensure_ascii=False, indent=4)
#
#
# def read_excel(xlsx_file: str) -> list:
#     """Читает данные из XLSX-файла и возвращает список словарей с транзакциями."""
#     try:
#         excel_data = pd.read_excel(xlsx_file).to_dict(orient="records")
#     except FileNotFoundError:
#         print(f"Файл {xlsx_file} не найден!")
#         return []
#     except Exception as e:
#         print(f"Произошла ошибка при чтении файла: {str(e)}")
#         return []
#     if not excel_data or not isinstance(excel_data, list):
#         print("Ошибочные данные из файла.")
#         return []
#     return excel_data
#
#
# def read_file(file_path: str) -> list:
#     """Читает данные из файла и возвращает список словарей с транзакциями."""
#     file_extension = file_path.rsplit('.', maxsplit=1)[-1].lower()  # Получаем расширение файла
#     content: list = []
#     match file_extension:
#         case "xlsx":
#             content = read_excel(file_path)
#         case _:
#             print(f"Формат файла '{file_extension}' не поддерживается.")
#             return []
#     return content
#
#
# def filter_transactions(transactions: List[Dict], search_string: str, field: str = "Описание") -> List[Dict]:
#     """Фильтрует список транзакций по указанной строке в заданном поле."""
#     pattern = re.compile(re.escape(search_string), re.IGNORECASE)  # Шаблон для поиска
#     filtered_transactions = [
#         transaction for transaction in transactions
#         if pattern.search(str(transaction.get(field, "")))
#     ]
#     return filtered_transactions
#
# if __name__ == "__main__":
#     result = simple_search()
#     print(result)
