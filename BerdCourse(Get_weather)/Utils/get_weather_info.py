import requests
from datetime import datetime, timezone

import sys
sys.path.append("..")
from config.global_config import API_KEY

class GetWeather:
    def get_weather_info(self, city):

        URL = f'http://api.openweathermap.org/data/2.5/weather?q={str(city)}&lang=ru&units=metric&appid={str(API_KEY)}'

        r = requests.get(URL)

        result = r.json()

        # Конвертируем timestamp в формат YYYY-MM-DD
        date_formatted = datetime.fromtimestamp(result["dt"], timezone.utc).strftime("%Y-%m-%d")

        weather_data = {
            "date": date_formatted,
            "city": result["name"],
            "temperature": result["main"]["temp"]
        }

        return (weather_data)


#
# gw = GetWeather()
# weather_1 = gw.get_weather_info('Москва')
# print(weather_1)
# write_csv(weather_1, '../dz_currency/weather_1.csv')

