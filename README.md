<div style="text-align: center;vertical-align: middle;">
    <h1>RoyaltyIT-tg-bot</h1>
    <a href="https://github.com/sssr-dev/api-server/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/sssr-dev/api-server?style=for-the-badge"></a>    
    <a href="https://github.com/sssr-dev/api-server/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/sssr-dev/api-server?style=for-the-badge"></a>    
    <a href="https://github.com/SantaSpeen"><img src="https://img.santaspeen.ru/github/magic.svg" alt="magic"></a>
    <br/>
</div>

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