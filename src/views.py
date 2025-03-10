import datetime
import json
import os

import requests
from dotenv import load_dotenv

from src.utils import calculate_card_data, filter_data_by_date, get_greeting, load_operations_data, top_five_transact

# Загружаем переменные окружения из файла .env (если используете этот метод)
load_dotenv()

# Загружаем настройки пользователя
with open("../user_settings.json") as f:
    user_settings = json.load(f)

# Получаем API-ключ из переменной окружения
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API-ключ не найден. Установите переменную среды API_KEY.")


def get_currency_rates():
    rates = []

    # Обрабатываем каждую валюту из списка user_currencies
    for currency in user_settings["user_currencies"]:
        try:
            # Формируем URL для запроса к API
            url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"

            headers = {"apikey": api_key}

            # Делаем запрос к API
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Поднимет исключение для HTTP ошибок

            # Если запрос успешен
            data = response.json()

            if "rates" not in data:
                return {"error": "Курсы не обнаружены в данных ответа"}

            # Получаем курс для рубля относительно текущей базовой валюты
            rate = data["rates"].get("RUB")
            if rate:
                rates.append({"currency": currency, "rate": rate})
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}"}
        except requests.exceptions.RequestException as req_err:
            return {"error": f"Request error occurred: {req_err}"}
        except Exception as err:
            return {"error": f"An error occurred: {err}"}

    return {"currency_rates": rates}


def get_stock_prices() -> dict | str:
    """
    Возвращает стоимость акций из установленного списка, обращаясь
    к сайту `https://site.financialmodelingprep.com/`
    :return:
    """
    with open("../user_settings.json") as f:
        user_settings = json.load(f)
    user_stocks = user_settings["user_stocks"]

    results = {}
    apikey = os.getenv("NINJAS_APIKEY")

    for stock in user_stocks:
        url = f"https://financialmodelingprep.com/api/v3/quote-short/{stock}?apikey={apikey}"
        response = requests.get(url)

        if response.status_code == 200:
            result = response.json()
            for data in result:
                stock = data["symbol"]
                price = round(data["price"], 2)
                results[stock] = {"stock": stock, "price": price}

        else:
            return (
                f"Ошибка при получении данных для {user_stocks}: код статуса {response.status_code}, {response.reason}"
            )

    return results


def get_dashboard_data(target_date):
    if isinstance(target_date, str):
        try:
            target_date = datetime.datetime.strptime(target_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте формат 'YYYY-MM-DD HH:MM:SS'.")

    # Загружаем данные
    file_path = os.path.join(os.path.dirname(__file__), "../data/operations.xlsx")
    df = load_operations_data(file_path)

    # Фильтруем по дате
    filtered_df = filter_data_by_date(df, target_date)

    # Формируем JSON
    dashboard_data = {
        "greeting": get_greeting(),
        "cards": calculate_card_data(filtered_df),
        "top_transactions": top_five_transact(filtered_df),
        "currency_rates": get_currency_rates().get("currency_rates", []),
        "stock_prices": get_stock_prices().get("stock_prices", []),
    }

    return dashboard_data


if __name__ == "__main__":
    # target_date = datetime.datetime(2021, 12, 20)
    target_date = "2021-12-20 17:00:00"
    dashboard = get_dashboard_data(target_date)
    print(json.dumps(dashboard, ensure_ascii=False, indent=4))
