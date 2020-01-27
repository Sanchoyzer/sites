## Описание

Телеграм бот, который по пользовательскому вводу выполняет поиск в геокодере Яндекса.
Учитывает белый список областей поиска из БД, туда же сохраняет историю поисков.


### Технологии

Админка

python 3.7, Django, DRF, sqlite


Бот

python 3.7, telebot, aiohttp (веб-хуки)


### Установка

0. Убедиться, что есть docker и docker compose

1. Создать конфиги в `.env` файлах рядом с Dockerfile'ами

Для админки

    SECRET_KEY='jber8h43gljn394njb-3ph0'
    DEBUG='false'
    ALLOWED_HOSTS='127.0.0.1,0.0.0.0'

Для бота

    TELEGRAM_TOKEN='12345:hsdbfkjslkfnsdkfj'
    GEO_TOKEN='akjerfk-asdfjbd-dfgsdf-sadgadfg'
    YANDEX_GEO_URL='https://geocode-maps.yandex.ru/1.x?format=json&apikey={}&geocode={}'
    STORAGE_URL='http://127.0.0.1:12345/api/v1/geobot/{}/'
    #
    WEBHOOK_HOST = '1.2.3.4'
    WEBHOOK_PORT = 8443
    WEBHOOK_LISTEN = '1.2.3.4'
    WEBHOOK_SSL_CERT = 'certs/webhook_cert.pem'
    WEBHOOK_SSL_PRIV = 'certs/webhook_pkey.pem'
    WEBHOOK_URL = 'https://{}:{}/{}/'


2. `docker-compose up`
