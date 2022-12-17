import datetime
import requests
import config
from config import TOKEN_WEATHER
from pprint import pprint
import pyowm
from pyowm.utils.config import get_default_config
from datetime import datetime


config_dict = get_default_config()
config_dict["language"] = "ru"


def my_weather(lat, lon, weather_token): #для местоположения
    req = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_token}&units=metric'
    )
    info = req.json()
    if info["cod"] == 404 or info["cod"] == "404":
        return []
    else:
        info = req.json()
        #pprint(info)
        cur_weather = info["main"]["temp"]
        humidity = info["main"]["humidity"]
        feels_like = info["main"]["feels_like"]
        temp_max = info["main"]["temp_max"]
        temp_min = info["main"]["temp_min"]
        wind_speed = info["wind"]["speed"]
        #sunrise = datetime.datetime.fromtimestamp(info["sys"]["sunrise"])
        #sunset = datetime.datetime.fromtimestamp(info["sys"]["sunset"])
        cloudiness = info["clouds"]["all"]
        des_weather = info["weather"][0]["main"]
        if des_weather in config.weather_des:
            weat_des = config.weather_des[des_weather]
        else:
            weat_des = "Выгляни на улицу, я не могу понять, что за осадки("
        return [cur_weather, feels_like, temp_min, temp_max, humidity, wind_speed, cloudiness, weat_des]


def city_weather(city_, weather_token): #для пооды на сейчас
    req = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city_}&appid={weather_token}&units=metric'
    )
    info = req.json()
    if info["cod"] == 404 or info["cod"] == "404":
        return []
    else:
        info = req.json()
        #pprint(info)
        city = city_
        cur_weather = info["main"]["temp"]
        humidity = info["main"]["humidity"]
        feels_like = info["main"]["feels_like"]
        temp_max = info["main"]["temp_max"]
        temp_min = info["main"]["temp_min"]
        wind_speed = info["wind"]["speed"]
        #sunrise = datetime.datetime.fromtimestamp(info["sys"]["sunrise"])
        #sunset = datetime.datetime.fromtimestamp(info["sys"]["sunset"])
        cloudiness = info["clouds"]["all"]
        des_weather = info["weather"][0]["main"]
        if des_weather in config.weather_des:
            weat_des = config.weather_des[des_weather]
        else:
            weat_des = "Выгляни на улицу, я не могу понять, что за осадки("

        # my_rec = "Вот, что мне удалось узнать про текущую погоду в городе " + city + ":" '\n' "" \
        #            "Текущая температура:" + cur_weather + '\n' + "Облачность: " + cloudiness + '\n' + "Давление: " + humidity + '\n' + "" \
        #            "" + "Скорость ветра: " + wind_speed + '\n' + "Температура ощущается как " + feels_like + '\n' + "" \
        #           "Минимальная температура за сегодня: " + temp_min + '\n' + "Минимальная температура за сегодня: " + temp_max + "" \
        # "Время восхода солнца: " + str(sunrise) + '\n' + "Время захода солнца: " + str(sunset)
        return [city, cur_weather, feels_like, temp_min, temp_max, humidity, wind_speed, weat_des]




def future_weather(city, token):    #для погоды на 3 дня
    req = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={token}&units=metric')
    info = req.json()
    if info["cod"] == 404 or info["cod"] == "404":
        return []
    else:
        lst = []
        for i in range(4, 21, 8):
            date = datetime.strptime(info["list"][i]["dt_txt"], "%Y-%m-%d %H:%M:%S")
            m = config.month[date.strftime("%B")]
            d = date.strftime("%d")
            y = date.strftime("%Y")
            dmy = str(d) + m + str(y)
            cur_weather = info["list"][i]["main"]["temp"]
            humidity = info["list"][i]["main"]["humidity"]
            feels_like = info["list"][i]["main"]["feels_like"]
            wind_speed = info["list"][i]["wind"]["speed"]
            #sunrise = datetime.datetime.fromtimestamp(info["list"][i]["sys"]["sunrise"])
            #sunset = datetime.datetime.fromtimestamp(info["list"][i]["sys"]["sunset"])
            cloudiness = info["list"][i]["clouds"]["all"]
            des_weather = info["list"][i]["weather"][0]["main"]
            if des_weather in config.weather_des:
                weat_des = config.weather_des[des_weather]
            else:
                weat_des = "Выгляни на улицу, я не могу понять, что за погода("
            lst.append([dmy, city, cur_weather, humidity, wind_speed, weat_des])
            #pprint(info["list"][i])
        return lst

#city = input()
#print(city_weather(city, config.TOKEN_WEATHER))



