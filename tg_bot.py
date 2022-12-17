import requests
from _datetime import datetime
import telebot
from telebot import types
import config
import main
from pyowm.utils.config import get_default_config

bot = telebot.TeleBot(config.Token_bot)

#т.к. сайт выдает все на английском, то он все переводит + время для функции ниже
config_dict = get_default_config()
config_dict["language"] = "ru"
time1 = datetime.now()
m = config.month[time1.strftime("%B")]
d = time1.strftime("%d")
y = time1.strftime("%Y")
ms = str(time1.hour) + ":" + time1.strftime("%H:%M")
time = str(d) + m + str(y) + ", " + ms


@bot.message_handler(commands=['start']) # кнопки
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup1, markup2 = types.KeyboardButton("Узнать текущую погоду", request_location=True), types.KeyboardButton("Узнать текущую погоду в каком-то городе")
    markup3 = types.KeyboardButton("Узнать погоду на ближайшие 3 дня")
    markup.add(markup1, markup2, markup3)
    bot.send_message(message.chat.id, text="Привет. Я бот, который может сказать, какая будет погода в любой точке мира.", reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['location'])
def loc(message):
    lat = message.location.latitude
    lon = message.location.longitude
    ans = main.my_weather(lat, lon, config.TOKEN_WEATHER)
    if len(ans):
        tex = "Температура: " + str(ans[0]) + "°C, " + ans[7] + '\n' + "\n" + "" \
                "Ощущается, как " + str(ans[1]) + "°C" + '\n' + "\n" + "" \
                "Минимальная температура за сегодня: " + str(ans[2]) + "°C" + '\n' + "\n" + "" \
                "Максимальная температура за сегодня: " + str(ans[3]) + "°C" + '\n' + "\n" + "" \
                "Влажность: " + str(ans[4]) + "%" + '\n' + "\n" + "" \
                "Ветер: " + str(ans[5]) + " км/ч" + '\n' + "\n" + ""
        bot.send_message(message.chat.id, text=tex)

@bot.message_handler(func=lambda message: True)
def bot_mes(message):
    if message.text == "Узнать текущую погоду в каком-то городе":
        bot.send_message(message.chat.id, "Напиши название города в формате <Погода 'название города'>, то есть: Погода Москва")
    elif message.text == "Узнать погоду на ближайшие 3 дня":
        bot.send_message(message.chat.id, "Напиши название города в формате <Город 'название города'>, например:Город Москва")
    elif message.text.split()[0] == "город" or message.text.split()[0] == "Город":
        print(message.text.split())
        ans = main.future_weather(' '.join(message.text.split()[1:]), config.TOKEN_WEATHER)
        #print(ans)
        if len(ans):
            for i in range(0, 3):
                tex = "Дата: " + ans[i][0] + "\n" + "\n" + "Температура: " + str(ans[i][2]) + "°C, " + ans[i][5] + '\n' + "\n" + "" \
                    "Влажность: " + str(ans[i][3]) + "%" + '\n' + "\n" + "" \
                    "Ветер: " + str(ans[i][4]) + " км/ч" + '\n' + "\n" + ""
                bot.send_message(message.chat.id, text=tex)
        else:
            bot.send_message(message.chat.id, "Название города введено неверно")
    elif (message.text.split()[0] == "Погода" or message.text.split()[0] == "погода"):
        #print(message.text.split())
        ans = main.city_weather(' '.join(message.text.split()[1:]), config.TOKEN_WEATHER)
        #print(ans)
        if len(ans):
            tex = str(time) + "\n" + "\n" + "Температура: " + str(ans[1]) + "°C, " + ans[7] + '\n' + "\n" + "" \
            "Ощущается, как " + str(ans[2]) + "°C" + '\n' + "\n" + "" \
            "Минимальная температура за сегодня: " + str(ans[3]) + "°C" + '\n' + "\n" + "" \
             "Максимальная температура за сегодня: " + str(ans[4]) + "°C" + '\n' + "\n" + "" \
             "Влажность: " + str(ans[5]) + "%" + '\n' + "\n" + "" \
              "Ветер: " + str(ans[6]) + " км/ч" + '\n' + ""
            bot.send_message(message.chat.id, text=tex)
        else:
            bot.send_message(message.chat.id, "Название города введено неверно")
    else:
        #print(message.text.split())
        bot.send_message(message.chat.id, "Я вас не понимаю(")




bot.polling(none_stop=True)