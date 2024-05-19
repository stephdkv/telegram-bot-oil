import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import BufferedInputFile



from bs4 import BeautifulSoup

from graph_oil_price import create_plot, get_graph_oil_price, io, DATA_FIVE_YEAR, DATA_THREE_MONTH, DATA_ONE_DAY, DATA_FIVE_DAY, DATA_ONE_MONTH, DATA_ONE_YEAR, DATA_ALL_THE_TIME, DATA_TO, MINUTE, HOURS, DAYS, WEEK, MONTH, THIRTY_MINUTE, FIVE_MINUTE

from graph_wti_price import create_plot, get_graph_wti_oil_price, io, DATA_FIVE_YEAR, DATA_THREE_MONTH, DATA_ONE_DAY, DATA_FIVE_DAY, DATA_ONE_MONTH, DATA_ONE_YEAR, DATA_ALL_THE_TIME, DATA_TO, MINUTE, HOURS, DAYS, WEEK, MONTH, THIRTY_MINUTE, FIVE_MINUTE



import requests

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчера
API_TOKEN = '7096859249:AAGwyR2SwoWyS6ylN7z7Q_nGnblXrP-d3iY'  # Замените на ваш API токен
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# URL для получения цен на нефть
OIL_PRICE_URL = "https://www.investing.com/commodities/brent-oil"

# Функция для получения цены на нефть
def get_oil_price():
    try:
        response = requests.get(OIL_PRICE_URL)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            price_element = soup.find("div", {"data-test": "instrument-price-last"})
            
            if price_element:
                return price_element.text
            else:
                return "Цена не найдена"
        else:
            return "Ошибка при получении цены на нефть"
    except Exception as e:
        return f"Ошибка: {str(e)}"
    
def get_wti_price():
    try:
        response = requests.get("https://www.investing.com/currencies/wti-usd")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            price_element = soup.find("div", {"data-test": "instrument-price-last"})
            
            if price_element:
                return price_element.text
            else:
                return "Цена не найдена"
        else:
            return "Ошибка при получении цены на нефть марки WTI"
    except Exception as e:
        return f"Ошибка: {str(e)}"

@dp.message(Command("choose_ticket"))
async def send_oil_price(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Нефть Brent"),
            types.KeyboardButton(text="Нефть WTI")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Цену чего ты хочешь узнать?"
    )
    await message.answer("Цену чего ты хочешь узнать?", reply_markup=keyboard)



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Нефть Brent"),
            types.KeyboardButton(text="Нефть WTI")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Цену чего ты хочешь узнать?"
    )
    await message.answer("Цену чего ты хочешь узнать?", reply_markup=keyboard)



@dp.message(F.text.lower() == "нефть brent")
async def with_puree(message: types.Message):
    oil_brent_price = get_oil_price()
    kb = [
        [
            types.KeyboardButton(text="Графики цен на нефть марки Brent"),
            types.KeyboardButton(text="Назад")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="График"
    )
    await message.answer(f"Цена на нефть: {oil_brent_price}$", reply_markup=keyboard)
    

@dp.message(F.text.lower() == "графики цен на нефть марки brent")
async def with_puree(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="График цены BRENT за день"),
            types.KeyboardButton(text="График цены BRENT за 5 дней"),
        ],
        [
            types.KeyboardButton(text="График цены BRENT за месяц"),
            types.KeyboardButton(text="График цены BRENT за 3 месяца"),
        ],
        [
            types.KeyboardButton(text="График цены BRENT за год"),
            types.KeyboardButton(text="График цены BRENT за 5 лет"),
        ],
        [
            types.KeyboardButton(text="График цены BRENT за все время"),
            types.KeyboardButton(text="Назад")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="График"
    )
    await message.answer('Выберите временной диапозон:',reply_markup=keyboard)
    

@dp.message(F.text.lower() == "график цены brent за год")
async def send_oil_price(message: types.Message):
    await message.answer(f"Подождите, генерирую график...")
    file_ids = []
    # Создаем график
    price_one_year = json.loads(get_graph_oil_price(DAYS, DATA_ONE_YEAR, DATA_TO))
    graph_content = create_plot(price_one_year)
    # Отправляем график в чат
    with open('graph.png', 'wb') as graph_file:
        graph_file.write(graph_content)
    
    with open("graph.png", "rb") as graph:
        result = await message.answer_photo(
            BufferedInputFile(
                graph.read(),
                filename="graph.png"
            ),
            caption="график цены BRENT за год"
        )
        file_ids.append(result.photo[-1].file_id)
       
    

@dp.message(F.text.lower() == "график цены brent за день")
async def send_oil_price(message: types.Message):
    await message.answer(f"Подождите, генерирую график...")
    file_ids = []
    # Создаем график
    price = json.loads(get_graph_oil_price(MINUTE, DATA_ONE_DAY, DATA_TO))
    graph_content = create_plot(price)
    # Отправляем график в чат
    with open('graph.png', 'wb') as graph_file:
        graph_file.write(graph_content)
    
    with open("graph.png", "rb") as graph:
        result = await message.answer_photo(
            BufferedInputFile(
                graph.read(),
                filename="graph.png"
            ),
            caption="График цены BRENT за день"
        )
        file_ids.append(result.photo[-1].file_id)
    

@dp.message(F.text.lower() == "график цены brent за 5 дней")
async def send_oil_price(message: types.Message):
    await message.answer(f"Подождите, генерирую график...")
    file_ids = []
    # Создаем график
    price = json.loads(get_graph_oil_price(FIVE_MINUTE, DATA_FIVE_DAY, DATA_TO))
    graph_content = create_plot(price)
    # Отправляем график в чат
    with open('graph.png', 'wb') as graph_file:
        graph_file.write(graph_content)
    
    with open("graph.png", "rb") as graph:
        result = await message.answer_photo(
            BufferedInputFile(
                graph.read(),
                filename="graph.png"
            ),
            caption="График цены BRENT за 5 дней"
        )
        file_ids.append(result.photo[-1].file_id)
    

@dp.message(F.text.lower() == "график цены brent за месяц")
async def send_oil_price(message: types.Message):
    await message.answer(f"Подождите, генерирую график...")
    file_ids = []
    # Создаем график
    price = json.loads(get_graph_oil_price(THIRTY_MINUTE, DATA_ONE_MONTH, DATA_TO))
    graph_content = create_plot(price)
    # Отправляем график в чат
    with open('graph.png', 'wb') as graph_file:
        graph_file.write(graph_content)
    
    with open("graph.png", "rb") as graph:
        result = await message.answer_photo(
            BufferedInputFile(
                graph.read(),
                filename="graph.png"
            ),
            caption="График цены BRENT за месяц"
        )
        file_ids.append(result.photo[-1].file_id)
    
@dp.message(F.text.lower() == "график цены brent за 3 месяца")
async def send_oil_price(message: types.Message):
    await message.answer(f"Подождите, генерирую график...")
    file_ids = []
    # Создаем график
    price = json.loads(get_graph_oil_price(HOURS, DATA_THREE_MONTH, DATA_TO))
    graph_content = create_plot(price)
    # Отправляем график в чат
    with open('graph.png', 'wb') as graph_file:
        graph_file.write(graph_content)
    
    with open("graph.png", "rb") as graph:
        result = await message.answer_photo(
            BufferedInputFile(
                graph.read(),
                filename="graph.png"
            ),
            caption="График цены BRENT за 3 месяца"
        )
        file_ids.append(result.photo[-1].file_id)
    

@dp.message(F.text.lower() == "график цены brent за 5 лет")
async def send_oil_price(message: types.Message):
    await message.answer(f"Подождите, генерирую график...")
    file_ids = []
    # Создаем график
    price = json.loads(get_graph_oil_price(WEEK, DATA_FIVE_YEAR, DATA_TO))
    graph_content = create_plot(price)
    # Отправляем график в чат
    with open('graph.png', 'wb') as graph_file:
        graph_file.write(graph_content)
    
    with open("graph.png", "rb") as graph:
        result = await message.answer_photo(
            BufferedInputFile(
                graph.read(),
                filename="graph.png"
            ),
            caption="График цены BRENT за 5 лет"
        )
        file_ids.append(result.photo[-1].file_id)
   


@dp.message(F.text.lower() == "график цены brent за все время")
async def send_oil_price(message: types.Message):
    await message.answer(f"Подождите, генерирую график...")
    file_ids = []
    # Создаем график
    price = json.loads(get_graph_oil_price(MONTH, DATA_ALL_THE_TIME, DATA_TO))
    graph_content = create_plot(price)
    # Отправляем график в чат
    with open('graph.png', 'wb') as graph_file:
        graph_file.write(graph_content)
    
    with open("graph.png", "rb") as graph:
        result = await message.answer_photo(
            BufferedInputFile(
                graph.read(),
                filename="graph.png"
            ),
            caption="График цены на BRENT за все время"
        )
        file_ids.append(result.photo[-1].file_id)





@dp.message(F.text.lower() == "графики цен на нефть марки wti")
async def with_puree(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="График цены WTI за день"),
            types.KeyboardButton(text="График цены WTI за 5 дней"),
        ],
        [
            types.KeyboardButton(text="График цены WTI за месяц"),
            types.KeyboardButton(text="График цены WTI за 3 месяца"),
        ],
        [
            types.KeyboardButton(text="График цены WTI за год"),
            types.KeyboardButton(text="График цены WTI за 5 лет"),
        ],
        [
            types.KeyboardButton(text="График цены WTI за все время"),
            types.KeyboardButton(text="Назад")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="График"
    )
    await message.answer('Выберите временной диапозон:',reply_markup=keyboard)
    

@dp.message(F.text.lower() == "график цены wti за год")
async def send_oil_price(message: types.Message):
    await message.answer(f"Подождите, генерирую график...")
    file_ids = []
    # Создаем график
    price_one_year = json.loads(get_graph_wti_oil_price(DAYS, DATA_ONE_YEAR, DATA_TO))
    graph_content = create_plot(price_one_year)
    # Отправляем график в чат
    with open('graph.png', 'wb') as graph_file:
        graph_file.write(graph_content)
    
    with open("graph.png", "rb") as graph:
        result = await message.answer_photo(
            BufferedInputFile(
                graph.read(),
                filename="graph.png"
            ),
            caption="график цены WTI за год"
        )
        file_ids.append(result.photo[-1].file_id)
       
    

@dp.message(F.text.lower() == "график цены wti за день")
async def send_oil_price(message: types.Message):
    await message.answer(f"Подождите, генерирую график...")
    file_ids = []
    # Создаем график
    price = json.loads(get_graph_wti_oil_price(MINUTE, DATA_ONE_DAY, DATA_TO))
    graph_content = create_plot(price)
    # Отправляем график в чат
    with open('graph.png', 'wb') as graph_file:
        graph_file.write(graph_content)
    
    with open("graph.png", "rb") as graph:
        result = await message.answer_photo(
            BufferedInputFile(
                graph.read(),
                filename="graph.png"
            ),
            caption="График цены WTI за день"
        )
        file_ids.append(result.photo[-1].file_id)
    

@dp.message(F.text.lower() == "график цены wti за 5 дней")
async def send_oil_price(message: types.Message):
    await message.answer(f"Подождите, генерирую график...")
    file_ids = []
    # Создаем график
    price = json.loads(get_graph_wti_oil_price(FIVE_MINUTE, DATA_FIVE_DAY, DATA_TO))
    graph_content = create_plot(price)
    # Отправляем график в чат
    with open('graph.png', 'wb') as graph_file:
        graph_file.write(graph_content)
    
    with open("graph.png", "rb") as graph:
        result = await message.answer_photo(
            BufferedInputFile(
                graph.read(),
                filename="graph.png"
            ),
            caption="График цены WTI за 5 дней"
        )
        file_ids.append(result.photo[-1].file_id)
    

@dp.message(F.text.lower() == "график цены wti за месяц")
async def send_oil_price(message: types.Message):
    await message.answer(f"Подождите, генерирую график...")
    file_ids = []
    # Создаем график
    price = json.loads(get_graph_wti_oil_price(THIRTY_MINUTE, DATA_ONE_MONTH, DATA_TO))
    graph_content = create_plot(price)
    # Отправляем график в чат
    with open('graph.png', 'wb') as graph_file:
        graph_file.write(graph_content)
    
    with open("graph.png", "rb") as graph:
        result = await message.answer_photo(
            BufferedInputFile(
                graph.read(),
                filename="graph.png"
            ),
            caption="График цены WTI за месяц"
        )
        file_ids.append(result.photo[-1].file_id)
    
@dp.message(F.text.lower() == "график цены wti за 3 месяца")
async def send_oil_price(message: types.Message):
    await message.answer(f"Подождите, генерирую график...")
    file_ids = []
    # Создаем график
    price = json.loads(get_graph_wti_oil_price(HOURS, DATA_THREE_MONTH, DATA_TO))
    graph_content = create_plot(price)
    # Отправляем график в чат
    with open('graph.png', 'wb') as graph_file:
        graph_file.write(graph_content)
    
    with open("graph.png", "rb") as graph:
        result = await message.answer_photo(
            BufferedInputFile(
                graph.read(),
                filename="graph.png"
            ),
            caption="График цены WTI за 3 месяца"
        )
        file_ids.append(result.photo[-1].file_id)
    

@dp.message(F.text.lower() == "график цены wti за 5 лет")
async def send_oil_price(message: types.Message):
    await message.answer(f"Подождите, генерирую график...")
    file_ids = []
    # Создаем график
    price = json.loads(get_graph_wti_oil_price(WEEK, DATA_FIVE_YEAR, DATA_TO))
    graph_content = create_plot(price)
    # Отправляем график в чат
    with open('graph.png', 'wb') as graph_file:
        graph_file.write(graph_content)
    
    with open("graph.png", "rb") as graph:
        result = await message.answer_photo(
            BufferedInputFile(
                graph.read(),
                filename="graph.png"
            ),
            caption="График цены WTI за 5 лет"
        )
        file_ids.append(result.photo[-1].file_id)
   


@dp.message(F.text.lower() == "график цены wti за все время")
async def send_oil_price(message: types.Message):
    await message.answer(f"Подождите, генерирую график...")
    file_ids = []
    # Создаем график
    price = json.loads(get_graph_wti_oil_price(MONTH, DATA_ALL_THE_TIME, DATA_TO))
    graph_content = create_plot(price)
    # Отправляем график в чат
    with open('graph.png', 'wb') as graph_file:
        graph_file.write(graph_content)
    
    with open("graph.png", "rb") as graph:
        result = await message.answer_photo(
            BufferedInputFile(
                graph.read(),
                filename="graph.png"
            ),
            caption="График цены на WTI за все время"
        )
        file_ids.append(result.photo[-1].file_id)






    
@dp.message(F.text.lower() == "нефть wti")
async def with_puree(message: types.Message):
    oil_wti_price = get_wti_price()
    kb = [
        [
            types.KeyboardButton(text="Графики цен на нефть марки WTI"),
            types.KeyboardButton(text="Назад")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="График"
    )
    await message.answer(f"Цена на Нефть марки Wti: {oil_wti_price}$", reply_markup=keyboard)


@dp.message(F.text.lower() == "назад")
async def go_back(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Нефть Brent"),
            types.KeyboardButton(text="Нефть WTI")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Цену чего ты хочешь узнать?"
    )
    await message.answer("Цену чего ты хочешь узнать?", reply_markup=keyboard)
# Функция для запуска бота
async def main():
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
