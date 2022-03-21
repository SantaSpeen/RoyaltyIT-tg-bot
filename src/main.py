import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor

from config import Config
from tools import Tools

config = Config("config.json")
log = logging.getLogger("bot core")

bot = Bot(token=config.bot_token)
dp = Dispatcher(bot)
tools = Tools(config, dp)


@dp.message_handler(commands=['admins'])
async def bot_admins(msg: types.Message):
    message = "Администраторы нашего сообщества:\n%(owner)-s"
    admin_list = await bot.get_chat_administrators(config.remote_chat)
    i = 1
    for admin_object in admin_list:
        user = admin_object['user']
        status = admin_object['status'].replace("administrator", "Администратор").replace("creator", "Создатель:")
        if status == "Администратор":
            if not user['is_bot']:
                message += f"`{i}. {status+':'}` `@{user['username']}`\n"
                i += 1
        else:
            message %= {"owner": f"`0. {status:14}` `@{user['username']}`\n"}

    await msg.reply(message, parse_mode=ParseMode.MARKDOWN)

tools.bind_static_messages()

if __name__ == '__main__':
    executor.start_polling(dp)
