import asyncio
import logging
import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode, ChatType
from aiogram.utils import executor

from config import Config
from tools import Tools

config = Config("config.json")
log = logging.getLogger("bot core")

bot = Bot(token=config.bot_token)
dp = Dispatcher(bot)
tools = Tools(config, dp)
mute_all = False
mute_perm = types.ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False
        )
unmute_perm = types.ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True
        )


@dp.message_handler(commands=["start"], chat_type=ChatType.PRIVATE)
async def start(msg: types.Message):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    user_id = msg.from_user.id
    registered = tools.register_user(user_id)
    if not registered:
        await msg.reply(config.start_message)


@dp.message_handler(commands=['admins'])
async def bot_admins(msg: types.Message):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
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


@dp.message_handler(regexp=r"\A(?:.|\/)(?:warn|пред)", is_chat_admin=True, chat_type=ChatType.SUPERGROUP)
async def wanr(msg: types.Message):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    reply_message = msg.reply_to_message

    if reply_message:
        warn_user = reply_message.from_user
        user_id = warn_user.id
        user_username = warn_user.username

        message = await tools.add_warn(user_id, user_username, msg.chat.id)

    else:
        message = "Сначала надо выбрать пользователя."

    if message:
        await msg.reply(message)


@dp.message_handler(regexp=r"\A(?:.|\/)(?:reset|прости)", is_chat_admin=True, chat_type=ChatType.SUPERGROUP)
async def unwarn(msg: types.Message):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    reply_message = msg.reply_to_message

    if reply_message:
        warn_user = reply_message.from_user
        user_id = warn_user.id
        user_username = warn_user.username

        message = tools.reset_warn(user_id, user_username)
    else:
        message = "Сначала надо выбрать пользователя."

    await msg.reply(message, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(regexp=r"\A(?:.|\/)(?:mute|тсс)", is_chat_admin=True, chat_type=ChatType.SUPERGROUP)
async def mute(msg: types.Message):
    reply_message = msg.reply_to_message

    if reply_message:
        warn_user = reply_message.from_user
        user_id = warn_user.id
        splt = msg.text.split(" ")[1:]
        if len(splt) > 0:
            c = time.time()
            try:
                for word in splt:
                    word: str
                    if word.endswith("d"):
                        c += int(word[:len(word)-1]) * 24 * 60 * 60
                    elif word.endswith("h"):
                        c += int(word[:len(word)-1]) * 60 * 60
                    elif word.endswith("m"):
                        c += int(word[:len(word)-1]) * 60
                    elif word.endswith("s"):
                        c += int(word[:len(word)-1])
                tools.set_mute(user_id, c)
                await tools.set_user_permissions(user_id, msg.chat.id, mute_perm)
            except Exception as e:
                await msg.reply(f"Exception:  <code>{e}</code>", parse_mode=ParseMode.HTML)
        else:
            await msg.reply("Укажи время:  <code>/mute 1d 5h 10m 30s</code>", parse_mode=ParseMode.HTML)
    else:
        await msg.reply("Сначала надо выбрать пользователя.")


@dp.message_handler(regexp=r"\A(?:.|\/)(?:unmute|говори)", is_chat_admin=True, chat_type=ChatType.SUPERGROUP)
async def unmute(msg: types.Message):
    reply_message = msg.reply_to_message

    if reply_message:
        warn_user = reply_message.from_user
        user_id = warn_user.id
        await tools.set_user_permissions(user_id, msg.chat.id, unmute_perm)

    else:

        await msg.reply("Сначала надо выбрать пользователя.")


@dp.message_handler(regexp=r"\A(?:.|\/)(?:ban|бан)", is_chat_admin=True, chat_type=ChatType.SUPERGROUP)
async def ban(msg: types.Message):
    reply_message = msg.reply_to_message

    if reply_message:

        if len(msg.text.split(" ")) > 1:

            message = await tools.ban_user(msg)

        else:
            message = "Укажи причину бана:  `/ban [причина]`"
    else:
        message = "Сначала надо выбрать пользователя."
    if message:
        await msg.reply(message, parse_mode=ParseMode.HTML)


@dp.message_handler(content_types=['new_chat_members'], chat_type=ChatType.SUPERGROUP)
async def new_chat_member(msg: types.Message):
    for user in msg.new_chat_members:
        user_id = user['id']
        log.info(f"New member: {user['id']}(@{user['username']})")
        banned, ban_msg, ban_by = tools.is_banned(user_id)
        if banned:
            await bot.send_message(msg.chat.id,
                                   f'@{user["username"]}, вы забанены <a href="tg://user?id={ban_by}">Администратором</a>.\n'
                                   f'Причина: <code>{ban_msg}</code>',
                                   parse_mode=ParseMode.HTML)
            await bot.kick_chat_member(msg.chat.id, user_id)
        else:
            message = config.new_member_message % {
                "username": user['username'],
                "<": "<code>",  # Start codeblock
                "</": "</code>"  # Close codeblock
            }
            await bot.send_message(msg.chat.id, message, parse_mode=ParseMode.HTML)


@dp.message_handler(content_types=['text', 'photo', 'document', 'audio', 'sticker', 'animation', 'voice', 'video_note'])
async def all_messages(msg: types.Message):
    global mute_all
    text = msg.text
    user_id = msg.from_user.id
    log.info(f"New message from {user_id}(@{msg.from_user.username}) in {msg.chat.id}: '{text}'; "
             f"Type: {msg.content_type}")

    if msg.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:  # Если сообщение пришло из группы
        asyncio.create_task(tools.fix_muted(unmute_perm))
        admins = await tools.admins
        if user_id in admins['ids']:
            if text == "суд идёт":
                mute_all = True
                await msg.reply("Да прибудет тишина!")
            elif text == "суд окончен":
                mute_all = False
                await msg.reply("Говорить разрешено.")

        elif mute_all:
            await msg.delete()

    for k, v in config.static_message.items():
        if k == text[1:len(k) + 1]:
            await msg.reply(config.static_message[k], parse_mode=ParseMode.MARKDOWN)
            return


if __name__ == '__main__':
    executor.start_polling(dp)
