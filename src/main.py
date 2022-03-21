import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
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
    message = "%(owner)-s"
    admin_list = await bot.get_chat_administrators(config.remote_chat)
    i = 1
    for admin_object in admin_list:
        user = admin_object['user']
        status = admin_object['status'].replace("administrator", "Администратор").replace("creator", "Создатель")
        if status == "Администратор":
            if not user['is_bot']:
                message += f"{i}. {status:13} @{user['username']}\n"
                i += 1
        else:
            message %= {"owner": f"0. {status:13} @{user['username']}\n"}

    await msg.reply(message, disable_notification=True)


# @dp.message_handler(content_types=['text'])
# async def msg_logger(msg: types.Message):
#     log.info(f"New message from {msg.from_user.id}({msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")


tools.bind_static_messages()

if __name__ == '__main__':
    executor.start_polling(dp)
