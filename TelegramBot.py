import telebot
import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()

token = os.getenv('TOKEN')

bot = telebot.TeleBot(token)
API = os.getenv('API')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Погода в каком городе Вас интересует?')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message,f'Сейчас погода в городе {city}: {temp} градуса')

        image ='images/sun.png' if temp > 5.0 else 'images/sun of weather.png'
        file = open("./" + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'Город не найден, проверте правильность написания.')

bot.polling(non_stop=True)

