import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
import aioschedule

from dotenv import load_dotenv
import os

from habr_parser import what_new_on_habr as habr
from tass_parser import what_new_on_tass as tass
import json

load_dotenv()
TOKEN = os.getenv('TOKEN')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

sites = ['tass', 'habr']


def what_new():
    tass()
    habr()

# REPLACE JSON TO SQL
async def send_news():
    what_new()
    with open('chats.json', 'r') as file:
        IDs = json.loads(file.read())
    for site in sites:
        with open(f'data/{site}/{site}_new.json', 'r', encoding='utf-8') as file:
            data = json.loads(file.read())
        if len(data['urls']) != 0:
            for ID in IDs:
                await bot.send_message(chat_id=ID, text=f'News from <b>{site}</b>', parse_mode='HTML')
            for i in range(len(data['urls'])):
                answer = ''
                for key in data.keys():
                    answer += f"{data[key][i]}\n"
                for ID in IDs:
                    await bot.send_message(chat_id=ID, text=answer, parse_mode='HTML')


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

    # LOL, WTF is that? need to rewrite it
    with open('chats.json', 'r') as file:
        a = json.loads(file.read())
    if message.chat.id not in a:
        a.append(message.chat.id)
        with open('chats.json', 'w') as file:
            json.dump(a, file)

        # Yes, of course xD to database :))))
        await message.answer('You added to database')


async def scheduler():
    aioschedule.every(1).minutes.do(send_news)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
