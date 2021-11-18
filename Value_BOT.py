import telebot
from config import keys, TOKEN
from extensions import APIException, ValueConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_start(message: telebot.types.Message):
    text = 'Чтобы перевести валюту введите команду боту в следующем формате:\n <имя валюты> \
           <в какую валюту перевести> \
           <количество переводимой валюты>\n Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values_ = list(map(str.lower, message.text.split(' ')))

        if len(values_) != 3:
            raise APIException("Неправильное количество параметров")

        quote, base, amount = values_
        text = ValueConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        reply = f'Цена {amount} {quote} в {base} - {text}'
        bot.send_message(message.chat.id, reply)


bot.polling(none_stop=True)
