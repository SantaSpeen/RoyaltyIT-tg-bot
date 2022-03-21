import logging
import time

import aiogram
from peewee import DoesNotExist

from SqlModels import Users
from config import Config

static_log = logging.getLogger('static messages')


class Tools:

    def __init__(self, config: Config, dispatcher: aiogram.Dispatcher):
        self.log = logging.getLogger("bot tools")
        self.config = config
        self.dispatcher = dispatcher
        self.__admins: dict = {}

    @staticmethod
    async def __message_handler(msg: aiogram.types.Message, **kwargs):
        text = msg.text
        static_log.info(f"New message from {msg.from_user.id}({msg.from_user.username}) in {msg.chat.id}: '{text}'")
        for k, v in kwargs['__messages__'].items():
            if k.startswith(text[1:len(k)]):
                allow = v['allow']
                send = False
                if (allow == "all") or \
                    (allow == "private" and msg.chat.id > 0) or \
                    (allow == "chat" and msg.chat.id < 0):
                    send = True
                if send:
                    await msg.reply(v['msg'])
                break

    def bind_static_messages(self):
        __messages__: dict = self.config.raw_config['static_message']
        __messages_keys__ = list(__messages__.keys())
        l = lambda *x: self.__message_handler(*x, __messages__=__messages__)
        self.dispatcher.register_message_handler(l, commands=__messages_keys__)

    async def _update_admins_list(self):
        admins = await self.dispatcher.bot.get_chat_administrators(self.config.remote_chat)
        ids = list()
        for admin in admins:
            ids.append(admin['user']['id'])
        self.__admins = {
            "time": time.time()+60.0,
            "object": {"list": admins, "ids": ids}
        }

    @property
    async def admins(self):
        if not self.__admins:
            await self._update_admins_list()
        elif time.time() >= self.__admins.get("time"):
            await self._update_admins_list()

        return self.__admins['object']

    async def add_warn(self, user_id, user_username, chat_id):
        try:
            user = Users.get(Users.user_id == user_id)
        except DoesNotExist:
            user = Users(user_id=user_id)
        user.warns += 1
        user.save()
        if user.warns > 3:
            try:
                await self.dispatcher.bot.kick_chat_member(chat_id, user_id)
                message = f"@{user_username} вёл себя плохо, поэтому теперь он иключён!"
            except Exception as e:
                message = f"Ошибка при исключении @{user_username}.\nException: `{e}`"
        else:
            message = f"@{user_username}, вы получили {user.warns} из 3 предупреждений.\nВпредь ведите себя лучше!"

        return message

    @classmethod
    async def reset_warn(cls, user_id, username):
        try:
            user = Users.get(Users.user_id == user_id)
        except DoesNotExist:
            user = Users(user_id=user_id)

        if user.warns == 0:
            message = f"У пользователя @{username} нет предупреждений!"
        else:
            message = f"Извини @{username}...\nТеперь у тебя 0 из 3 предупреждений."
            user.warns = 0
            user.save()

        return message
