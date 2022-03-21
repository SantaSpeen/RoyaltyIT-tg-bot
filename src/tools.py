import logging

import aiogram

from config import Config

static_log = logging.getLogger('static messages')


class Tools:

    def __init__(self, config: Config, dispatcher: aiogram.Dispatcher):
        self.log = logging.getLogger("bot tools")
        self.config = config
        self.dispatcher = dispatcher

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
