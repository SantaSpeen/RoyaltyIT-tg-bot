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
    log.info(f"New message from {msg.from_user.id}({msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    message = "Администраторы нашего сообщества:\n%(owner)-s"
    admins = await tools.admins
    i = 1
    for admin_object in admins['list']:
        user = admin_object['user']
        status = admin_object['status'].replace("administrator", "Администратор").replace("creator", "Создатель:")
        if status == "Администратор":
            if not user['is_bot']:
                message += f"`{i}. {status + ':'}` `@{user['username']}`\n"
                i += 1
        else:
            message %= {"owner": f"`0. {status:14}` `@{user['username']}`\n"}

    await msg.reply(message, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(regexp=r"\A(?:.|\/)(?:warn|пред)", is_chat_admin=True)
async def wanrs(msg: types.Message):
    log.info(f"New message from {msg.from_user.id}({msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    reply_message = msg.reply_to_message

    if reply_message:
        warn_user = reply_message.from_user
        user_id = warn_user.id
        user_username = warn_user.username

        message = await tools.add_warn(user_id, user_username, msg.chat.id)

    else:
        message = "Сначала надо выбрать пользователя."

    await msg.reply(message, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(regexp=r"\A(?:.|\/)(?:reset|прости)", is_chat_admin=True)
async def unwarn(msg):
    log.info(f"New message from {msg.from_user.id}({msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    reply_message = msg.reply_to_message

    if reply_message:
        warn_user = reply_message.from_user
        user_id = warn_user.id
        user_username = warn_user.username

        message = await tools.reset_warn(user_id, user_username)
    else:
        message = "Сначала надо выбрать пользователя."

    await msg.reply(message, parse_mode=ParseMode.MARKDOWN)


tools.bind_static_messages()

if __name__ == '__main__':
    executor.start_polling(dp)
