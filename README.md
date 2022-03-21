# RoyaltyIT-tg-bot
<p align="center">
    <a href="https://github.com/SantaSpeen/RoyaltyIT-tg-bot/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/SantaSpeen/RoyaltyIT-tg-bot?style=for-the-badge"></a>    
    <a href="https://github.com/SantaSpeen/RoyaltyIT-tg-bot/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/SantaSpeen/RoyaltyIT-tg-bot?style=for-the-badge"></a>    
    <a href="https://github.com/SantaSpeen"><img src="https://img.santaspeen.ru/github/magic.svg" alt="magic"></a>
    <br/>
</p>

Этот бот создан специально для: [@RoyaltyProject](https://t.me/royaltyproject)

### Установка:

```shell
# Clone repository
$ git clone https://github.com/SantaSpeen/RoyaltyIT-tg-bot.git
# Change directory
$ cd src
# Install requirements
$ python3 -m pip install -r requirements.txt
# Create configuration file
# Then start the bot
$ python3 main.py
```

### config.json example

```json
{
  "bot_token": "BOT_TOKEN",
  "remote_chat": -1000,
  "static_message": {
    "start": {
      "allow": "private",
      "msg": "Привет, я бот \"Ял\".\nДля ознакомления с возможностями - /help"
    },
    "help": {
      "allow": "all",
      "msg": "Помощь уже в пути!"
    }
  }
}
```