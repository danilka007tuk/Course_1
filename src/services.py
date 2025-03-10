import json
import logging

from src.decorators import decorator_search

logger = logging.getLogger("services.log")
file_handler = logging.FileHandler("services.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


@decorator_search
def simple_search(my_list: list, string_search: str):
    """Функция поиска по переданной строке"""
    result = []
    logger.info("Начало работы функции (simple_search)")
    for i in my_list:
        if string_search == '':
            return result
        elif (
                i["Описание"] == "nan"
                or type(i["Описание"]) is float
                or i["Категория"] == "nan"
                or type(i["Категория"]) is float
        ):
            continue
        elif string_search in i["Описание"] or string_search in i["Категория"]:
            result.append(i)

    logger.info("Конец работы функции (simple_search)")
    data_json = json.dumps(result,
                           indent=4,
                           ensure_ascii=False,
                           )

    return data_json


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
