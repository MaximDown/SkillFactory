import telebot
from telegram_bot.extensions import CurrencyConverter, APIException
from telegram_bot.config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_instructions(message):
    cmd_start = "Добро пожаловать в бот-конвертер валют!"
    bot.send_message(message.chat.id, cmd_start)


@bot.message_handler(commands=['help'])
def send_instructions(message):
    cmd_help = ("Чтобы узнать цену определенной валюты, отправьте сообщение в формате:\n"
                "<из какой валюты> <в какую валюту> <сумма>\n"
                "Например: USD EUR 100\n"
                "Вы также можете использовать команду /values, чтобы просмотреть все доступные валюты.")
    bot.send_message(message.chat.id, cmd_help)


@bot.message_handler(commands=['values'])
def send_currency_values(message):
    cmd_values = ("Доступные валюты:\n"
                  "1. USD - Доллар\n"
                  "2. EUR - Евро\n"
                  "3. RUB - Рубль")
    bot.send_message(message.chat.id, cmd_values)


@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        base, quote, amount = message.text.split()
        amount = float(amount)
        converted_amount = CurrencyConverter.get_price(base.upper(), quote.upper(), amount)
        bot.send_message(message.chat.id, f"{amount} {base.upper()} = {converted_amount} {quote.upper()}")
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка ввода. Обратитесь к /help и /values")
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка: {e.message}")


bot.polling()
