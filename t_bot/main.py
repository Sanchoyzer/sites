import ssl

import telebot as tb
from aiohttp import web
from dotenv import dotenv_values
from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update

import controller


env = dotenv_values().get
bot = tb.TeleBot(token=env('TELEGRAM_TOKEN'))
app = web.Application()


async def handle(request: web.Request) -> web.Response:
    if request.match_info.get('token') != bot.token:
        return web.Response(status=403)

    request_body_dict = await request.json()
    update = Update.de_json(request_body_dict)
    bot.process_new_updates([update])
    return web.Response(status=200)


app.router.add_post('/{token}/', handle)


def callback_geo(message: Message) -> None:
    controller.get_geo_step(bot=bot, message=message)


@bot.message_handler(commands=['start'])
def input_command_start(message: Message) -> None:
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row('Search', 'History')
    bot.send_message(chat_id=message.chat.id, text='What do you want?',
                     reply_markup=markup)


@bot.message_handler(commands=['search'])
def input_command_start(message: Message) -> None:
    text = message.text.split(' ', maxsplit=1)
    if len(text) < 2:
        bot.send_message(chat_id=message.chat.id, text='Need "/search %address%"')
        return
    message.text = text[1]
    controller.get_geo_step(bot=bot, message=message)


@bot.message_handler(commands=['history'])
def input_command_start(message: Message) -> None:
    controller.show_history(bot=bot, message=message)


@bot.message_handler(content_types=['text'])
def input_text(message: Message) -> None:
    text = message.text
    markup = ReplyKeyboardRemove()
    if text == 'Search':
        msg = bot.send_message(chat_id=message.chat.id, text='Enter geo',
                               reply_markup=markup)
        bot.register_next_step_handler(message=msg, callback=callback_geo)
    elif text == 'History':
        controller.show_history(bot=bot, message=message, markup=markup)
    else:
        bot.send_message(chat_id=message.chat.id, text='Unknown command. Use /start',
                         reply_markup=markup)


def main() -> None:
    bot.remove_webhook()

#    url = env('WEBHOOK_URL').format(env('WEBHOOK_HOST'),
#                                    env('WEBHOOK_PORT'), bot.token)
#    bot.set_webhook(url=url, certificate=open(env('WEBHOOK_SSL_CERT'), 'r'))
#
#    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#    context.load_cert_chain(certfile=env('WEBHOOK_SSL_CERT'),
#                            keyfile=env('WEBHOOK_SSL_PRIV'))
#
#    web.run_app(app=app, host=env('WEBHOOK_LISTEN'),
#                port=env('WEBHOOK_PORT'), ssl_context=context)

    bot.polling()


if __name__ == '__main__':
    main()
