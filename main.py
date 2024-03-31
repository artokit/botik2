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
        user_id, sub_id, status = message.text.split(":")
        db_api.add_user_status(user_id, sub_id, status)


@dp.message(Command("get"))
async def get_user(message: Message):
    if message.chat.id in ADMINS:
        user_id = int(message.text.split(" ")[1])
        user = db_api.get_user(user_id)
        statuses = db_api.get_all_status(user[0])
        url = json.load(open("settings.json"))['domain']
        await message.answer(
            markdown.text(f"UTM метка: {user[1]}\n") +
            f"Ссылка: {url}?sub_id={user[1]}&user_id={user[0]}\n\n".replace("_", "\_") +
            markdown.text("Все совпадения в группе: \n") +
            "".join([f"`[{i[3]}]` %s\n" % markdown.bold(i[2]).replace('\-', '-') for i in statuses]),
            parse_mode="markdown"
        )


asyncio.run(dp.start_polling(bot))
