import logging
import json
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)-29s - %(levelname)-5s - %(message)s")


class Config:

    # noinspection PyTypeChecker
    def __init__(self, config_file):
        self.log = logging.getLogger(__name__)
        self.debug = self.log.debug

        self.config_file = config_file
        self.raw_config: dict = None

        self.bot_token: str = None
        self.remote_chat: int = None

        self.messages_object: str = None
        self.start_message: str = None
        self.static_message: dict = None

        self.__new_member_message: dict = None

        self._read_config()

    def _read_config(self):
        self.debug("_read_config(self)")
        if os.path.isfile(self.config_file):
            self.log.info(f"Config file: %s - found" % self.config_file)
            with open(self.config_file, 'r') as f:
                self.raw_config = json.load(f)
        else:
            raise FileNotFoundError("Cannot found config file at %s." % self.config_file)

        self.bot_token = self.raw_config.get("bot_token")
        self.remote_chat = self.raw_config.get("remote_chat")
        self.messages_object = self.raw_config.get("messages")
        self.start_message = self.raw_config.get("start_message")
        self.static_message = self.raw_config.get("static_message")

    @property
    def new_member_message(self) -> str:
        if not self.__new_member_message:
            with open(self.raw_config['new_member_message']) as f:
                self.__new_member_message = f.read()
        return self.__new_member_message

    @new_member_message.setter
    def new_member_message(self, v):
        with open(self.raw_config['new_member_message'], "w") as f:
            f.write(v)
        self.__new_member_message = v