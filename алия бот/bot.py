import telebot
import requests

TOKEN = '6744362006:AAESGusArX4TbvHl_S-7iamC0WfnMMYhlEE'
API_KEY = '8dced8b8ea77c1644ac5c1d6fe1bc15d'

weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот погоды. Чтобы получить погоду, отправь мне название города.")

@bot.message_handler(func=lambda message: True)
def get_weather(message):
    city_name = message.text
    try:
        response = requests.get(weather_url.format(city_name, API_KEY))
        data = response.json()
        if data["cod"] == "404":
            bot.reply_to(message, "Город не найден. Попробуйте ввести название города еще раз.")
        else:
            weather_description = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            response_message = f"Погода в городе {city_name}:\nОписание: {weather_description}\nТемпература: {temp}°C\nВлажность: {humidity}%\nСкорость ветра: {wind_speed} м/c"
            bot.reply_to(message, response_message)
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при получении погоды. Попробуйте позже.")


bot.polling()
