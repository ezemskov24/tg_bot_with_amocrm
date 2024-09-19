## Краткое описание

Телеграм бот опрашивает пользователя о требованиях к банковской гарантии 
для исполнения контракта на участие в тендере. 
Ответы пользователя отправляются в подключенную amoCRM в виде сделок с задачами и тегом.

***

## Описание команд

### Команда /start

- Начать новый расчет

## Установка и запуск

Склонировать проект:

```
git clone https://github.com/ezemskov24/tg_bot_with_amocrm.git
```

Предварительно необходимо создать файл .py, в нем заполнить данные 
из установленной в amoCRM интеграции и выполнить его, создадутся 2 файла: 
refresh_token.txt и access_token.txt.
```
from amocrm.v2 import tokens

tokens.default_token_manager(
    client_id="xxx-xxx-xxxx-xxxx-xxxxxxx",
    client_secret="xxxx",
    subdomain="subdomain",
    redirect_url="https://xxxx/xx",
    storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
)
tokens.default_token_manager.init(code="..very long code...", skip_error=True)
```
В репозитории хранится файл .env.template. Надо на его основе создать и заполнить файл .env
***
### Запуск проекта через Docker
```
docker compose up --build
```
