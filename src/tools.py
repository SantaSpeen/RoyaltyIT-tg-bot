import logging
import time

import aiogram
from aiogram.types import ParseMode
from peewee import DoesNotExist

from SqlModels import Users, Mailing
from config import Config


class Tools:

    def __init__(self, config: Config, dispatcher: aiogram.Dispatcher):
        self.log = logging.getLogger("bot tools")
        self.config = config
        self.dispatcher = dispatcher
        self.__admins: dict = {}

    async def _update_admins_list(self):
        admins = await self.dispatcher.bot.get_chat_administrators(self.config.remote_chat)
        ids = list()
        for admin in admins:
            ids.append(admin['user']['id'])
        self.__admins = {
            "time": time.time() + 60.0,
            "object": {"list": admins, "ids": ids}
        }

    @property
    async def admins(self):
        if not self.__admins:
            await self._update_admins_list()
        elif time.time() >= self.__admins.get("time"):
            await self._update_admins_list()

        return self.__admins['object']

    @staticmethod
    def get_user(user_id):
        try:
            user = Users.get(Users.user_id == user_id)
        except DoesNotExist:
            user = Users(user_id=user_id)
        return user

    async def set_user_permissions(self, user_id, chat_id, permissions):
        try:
            await self.dispatcher.bot.restrict_chat_member(chat_id, user_id, permissions=permissions)
            return True
        except Exception as e:
            await self.dispatcher.bot.send_message(chat_id,
                                                   f"Ошибка при изменении прав на [пользователе](tg://user?id={user_id}).\n"
                                                   f"Exception: `{e}`",
                                                   parse_mode=ParseMode.MARKDOWN)
            return False

    async def kick_chat_member(self, chat_id, user_id):
        try:
            await self.dispatcher.bot.kick_chat_member(chat_id, user_id)
            return True
        except Exception as e:
            await self.dispatcher.bot.send_message(chat_id,
                                                   f"Ошибка при исключении [пользователя](tg://user?id={user_id}).\n"
                                                   f"Exception: `{e}`",
                                                   parse_mode=ParseMode.MARKDOWN)
            return False

    async def add_warn(self, user_id, user_username, chat_id):
        user = self.get_user(user_id)
        user.warns += 1
        user.save()
        if user.warns > 3:

            if await self.kick_chat_member(chat_id, user_id):
                message = f"@{user_username} вёл себя плохо, поэтому теперь он иключён!"
            else:
                message = None
                user.warns = 0
                user.save()

        else:
            message = f"@{user_username}, вы получили {user.warns} из 3 предупреждений.\nВпредь ведите себя лучше!"

        return message

    @classmethod
    def reset_warn(cls, user_id, username):
        user = cls.get_user(user_id)
        if user.warns == 0:
            message = f"У пользователя @{username} нет предупреждений!"
        else:
            message = f"Извини @{username}...\nТеперь у тебя 0 из 3 предупреждений."
            user.warns = 0
            user.save()

        return message

    @classmethod
    def is_banned(cls, user_id):
        user = cls.get_user(user_id)
        return user.banned, user.ban_msg, user.ban_by

    async def ban_user(self, msg: aiogram.types.Message):
        user = self.get_user(msg.reply_to_message.from_user.id)

        if await self.kick_chat_member(msg.chat.id, user.user_id):
            user.banned = True
            user.ban_msg = " ".join(msg.text.split(" ")[1:])
            user.ban_by = msg.from_user.id
            user.save()
            return f"@{msg.reply_to_message.from_user.username} был забанен.\nПричина: <code>{user.ban_msg}</code>."

    @classmethod
    def register_user(cls, user_id):
        registered = False
        cls.get_user(user_id).save()
        try:
            Mailing.get(Mailing.user_id == user_id)
            registered = True
        except DoesNotExist:
            Mailing(user_id=user_id).save()

        return registered
