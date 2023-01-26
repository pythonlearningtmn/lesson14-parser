import telebot
from telebot import apihelper
from datetime import datetime
from func_telebot import parser_html
from os.path import exists

TOKEN = '1324248990:AAFQmG6EQNGZLEkUw9wF4b6SQACp5Co51og'
proxies = {
    'http': 'http://5.9.94.91:3128',
    'https': 'http://5.9.94.91:3128',
}
apihelper.proxy = proxies
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_menu(message):
    name = message.from_user.username
    message_text = f'Здравствуйте, {name}!\nНаберите /help - для ' \
                   f'отображения списка доступных команд.'
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['help'])
def print_menu(message):
    message_text = f'Вот, что умеет этот бот:' \
                   f'\n/start - начало работы бота и приветствие ' \
                   f'\n/help - отображает список доступных команд' \
                   f'\n/date - отображает текущую дату' \
                   f'\n/time - отображает текущее время' \
                   f'\n/pars req - отображает результаты запроса по ключевому слову "req"' \
                   f'\n/file - присылает файл с результатами запроса'
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['time'])
def time_now(message):
    current_time = datetime.now()
    current_time_hour = current_time.hour
    current_time_minute = current_time.minute
    current_time_second = current_time.second
    bot.send_message(message.chat.id, f'{current_time_hour}:{current_time_minute}:{current_time_second}')


@bot.message_handler(commands=['date'])
def date_today(message):
    current_date = datetime.now()
    current_date_day = current_date.day
    current_date_month = current_date.month
    current_date_year = current_date.year
    bot.send_message(message.chat.id, f'{current_date_day}-{current_date_month}-{current_date_year}')


@bot.message_handler(commands=['pars'])
def pars_site(message):
    text = message.text.split()[1]
    chat_id = message.chat.id
    q = parser_html(text)
    for note in q[:5]:
        bot.send_message(chat_id, f'{note[1]} - {note[2]}')


@bot.message_handler(commands=['file'])
def send_file(message):
    chat_id = message.chat.id
    if not exists('news.csv'):
        bot.send_message(chat_id, 'Файл не сформирован. Используйте команду /pars для его формирования')
    else:
        with open('news.csv') as f:
            bot.send_document(chat_id, f)


@bot.message_handler(content_types=['text'])
def reverse_text(message):
    text = message.text[::-1]
    bot.reply_to(message, text)


if __name__ == '__main__':
    bot.infinity_polling()
