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
# Create sqlite database from src/sl3.sql
# Then start the bot
$ python3 main.py
```

### config.json example

```json
{
  "bot_token": "BOT_TOKEN",
  "remote_chat": -123456789,
  "new_member_message": "new_member_message.txt",
  "start_message": "start message",
  "standart_start_message": "Привет, @%(username)-s!\nДобро пожаловать в наше IT - сообщество.\nЧтобы люди могли в будущем найти тебя, напиши вступительное сообщение о себе с хештегом %(<)-s#знакомство%(</)-s.\n\nПриятного времяпрепровождения!",
  "static_message": {
    "help": "Я бот, ничем не могу помочь, сорян...",
    "rules": "\uD83D\uDD16Правила чата:\n\n1. Политические и религиозные высказывания запрещены.\n2. Спам и флуд запрещён.\n3. Оскорбления запрещены.\n4. Запрещено скидывать вредоносное ПО и ссылки.\n5. Запрещено скидывать 18+ контент (порно, расчленёнку и т.д.).\n\nОтноситесь уважительно друг к другу. Чат создан для комфортного и уютного общения IT-шников. Здесь люди помогают друг другу, а не ругаются и высказываются по поводу политики. \n\nС уважением, администрация Royalty❤️"
  }
}
```

### License

License: MIT