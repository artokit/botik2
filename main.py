import json
from aiogram import Dispatcher, Bot
import asyncio
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils import markdown

import db_api

CHANNEL_ID = -1001968382463
ADMINS = [5833820044, 6143457652]
bot = Bot(token='6549593881:AAELHuVb0dfJMtUZ-Q2QPwXytnKCG2YZZ-s')
dp = Dispatcher()


@dp.channel_post()
async def handle_message(message: Message):
    if message.chat.id == CHANNEL_ID:
        print(message.text)
        user_id, sub_id, data = message.text.split(":", maxsplit=2)
        db_api.add_user_status(user_id, sub_id, data)


@dp.message(Command("get"))
async def get_user(message: Message):
    if message.chat.id in ADMINS:
        user_id = int(message.text.split(" ")[1])
        user = db_api.get_user(user_id)
        try:
            statuses = db_api.get_all_status(user[0])
        except TypeError:
            return await message.answer("Человека с таким ID нету в БД :(")
        url = json.load(open("settings.json"))['domain']

        user_casino_id = ""
        for i in statuses:
            if "reg" in i[2]:
                user_casino_id = i[2].split(":")[1]

        casino_id = f"&casino_user_id={user_casino_id}" if user_casino_id else ""

        await message.answer(
            markdown.text(f"UTM метка: {user[1]}\n") +
            f"Ссылка: {url}?sub_id={user[1]}&user_id={user[0]}{casino_id}\n\n".replace("_", "\_") +
            markdown.text("Все совпадения в группе: \n") +
            "".join([f"`[{i[3]}]` %s\n" % markdown.bold(i[2]).replace('\-', '-').replace("reg:", "reg").replace(user_casino_id, "").replace("::", ":") for i in statuses]),
            parse_mode="markdown"
        )


asyncio.run(dp.start_polling(bot))
