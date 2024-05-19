import matplotlib.pyplot as plt
import datetime
import requests
import io
import time

current_time = int(time.time())

# Определяем количество секунд в пяти годах
five_years_seconds = 5 * 365 * 24 * 60 * 60
three_month_seconds = 3 * 30 * 24 * 60 * 60

# Устанавливаем временные рамки для запросов данных
DATA_TO = int(time.time())
DATA_ONE_DAY = int(time.time()) - 86400
DATA_FIVE_DAY = int(time.time()) - 86400*5
DATA_ONE_MONTH = int(time.time()) - 2629743
DATA_THREE_MONTH = current_time - three_month_seconds
DATA_ONE_YEAR = int(time.time()) - 31556926
DATA_FIVE_YEAR = current_time - five_years_seconds
DATA_ALL_THE_TIME = 384693107

# Единицы измерения времени
MINUTE = 'M'
FIVE_MINUTE = '5'
THIRTY_MINUTE = '30'
HOURS = 'H'
DAYS = 'D'
WEEK = 'W'
MONTH = '40320'

def get_graph_wti_oil_price(resolution, from_time, to_time):
    # Получаем данные о ценах на нефть WTI
    data = f"https://api.bcs.ru/udfdatafeed/v1/history?symbol=LCROIL&resolution={resolution}&from={from_time}&to={to_time}"
    try:
        response = requests.get(data)
        if response.status_code == 200:
            content = response.text
            return content
    except Exception as e:
        return f"Ошибка: {str(e)}"
    

def create_plot(price_data):
    # Извлекаем данные
    timestamps = price_data["t"]  # временные метки
    closing_prices = price_data["c"]  # цены закрытия

    # Преобразуем временные метки в даты
    dates = [datetime.datetime.fromtimestamp(ts) for ts in timestamps]

    # Создаем график
    plt.figure(figsize=(12, 6))
    plt.plot(dates, closing_prices, linestyle='-')

    # Добавляем метки и заголовок
    plt.title('Brent')  # название графика
    plt.xlabel('Дата')  # метка оси X
    plt.ylabel('Цена, в $')  # метка оси Y

    # Поворачиваем метки дат для лучшей читаемости
    plt.xticks(rotation=65)

    # Создаем временный файл для сохранения графика   
    buffer = io.BytesIO()
    # Сохраняем график в буферном потоке в формате PNG
    plt.savefig(buffer, format='png')
    # Очищаем график из памяти
    plt.close()

    # Возвращаем содержимое буферного потока
    return buffer.getvalue()
