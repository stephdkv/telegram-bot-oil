from aiogram.types import Message, BufferedInputFile
from aiogram import F, Router
import json
from graph_oil_price import create_plot, get_graph_oil_price, io, DATA_FIVE_YEAR, DATA_THREE_MONTH, DATA_ONE_DAY, DATA_FIVE_DAY, DATA_ONE_MONTH, DATA_ONE_YEAR, DATA_ALL_THE_TIME, DATA_TO, MINUTE, HOURS, DAYS, WEEK, MONTH, THIRTY_MINUTE, FIVE_MINUTE

route = Router()


@route.message(F.text.lower() == "график цены за год")
async def send_oil_price(message: Message):
   
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
            caption="График цены на нефть"
        )
        file_ids.append(result.photo[-1].file_id)

@route.message(F.text.lower() == "график цены за день")
async def send_oil_price(message: Message):
   
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
            caption="График цены на нефть"
        )
        file_ids.append(result.photo[-1].file_id)

@route.message(F.text.lower() == "график цены за 5 дней")
async def send_oil_price(message: Message):
   
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
            caption="График цены на нефть"
        )
        file_ids.append(result.photo[-1].file_id)

@route.message(F.text.lower() == "график цены за месяц")
async def send_oil_price(message: Message):
   
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
            caption="График цены на нефть"
        )
        file_ids.append(result.photo[-1].file_id)

@route.message(F.text.lower() == "график цены за 3 месяца")
async def send_oil_price(message: Message):
   
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
            caption="График цены на нефть"
        )
        file_ids.append(result.photo[-1].file_id)

@route.message(F.text.lower() == "график цены за 5 лет")
async def send_oil_price(message: Message):
   
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
            caption="График цены на нефть"
        )
        file_ids.append(result.photo[-1].file_id)


@route.message(F.text.lower() == "график цены за все время")
async def send_oil_price(message: Message):
   
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
            caption="График цены на нефть"
        )
        file_ids.append(result.photo[-1].file_id)