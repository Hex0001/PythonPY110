import json
from datetime import datetime
import requests


# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}


def current_weather_with_apiweather(lat, lon):
    key = '429aa38b8a3748a5b2c221901240705'
    url = 'https://api.weatherapi.com/v1/current.json'
    params = {'key': key, 'q': f'{lat}, {lon}'}
    response = requests.get(url, params=params).json()

    # s = f"Город: {response['location']['name']}\n" \
    #     f"Температура: {response['current']['temp_c']}\n" \
    #     f"Как ощущается: {response['current']['feelslike_c']}\n" \
    #     f"Ветер: {response['current']['wind_kph']}\n" \
    #     f"Время: {datetime.fromtimestamp(response['current']['last_updated_epoch'])}"
    # return s

    result = {'city': response['location']['name'],
              'time': datetime.fromtimestamp(response['current']['last_updated_epoch']).strftime("%H:%M"),
              'temp': response['current']['temp_c'],
              'feels_like_temp': response['current']['feelslike_c'],
              'pressure': response['current']['pressure_mb'],
              'humidity': response['current']['humidity'],
              'wind_speed': response['current']['wind_kph'],
              'wind_gust': response['current']['gust_kph'],
              'wind_dir': DIRECTION_TRANSFORM.get(response['current']['wind_dir'].lower())}
    return result


# def current_weather(lat, lon):
#     """
#     Описание функции, входных и выходных переменных
#     """
#     token = '9386fc7e-e6fc-482b-9847-c42f340390b3'  # Вставить ваш токен
#     url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"  # Если вдруг используете тариф «Погода на
#     # вашем сайте», то вместо forecast используйте informers. url = f"https://api.weather.yandex.ru/v2/informers?lat=
#     # {lat}&lon={lon}"
#     headers = {"X-Yandex-API-Key": f"{token}"}
#     response = requests.get(url, headers=headers)
#     data = response.json()
#
#     result = {
#         'city': data['geo_object']['locality']['name'],
#         'time': datetime.fromtimestamp(data['fact']['uptime']).strftime("%H:%M"),
#         'temp': data['fact']['temp'],
#         'feels_like_temp': data['fact']['feels_like'],
#         'pressure': data['fact']['pressure_mm'],
#         'humidity': data['fact']['humidity'],
#         'wind_speed': data['fact']['wind_speed'],
#         'wind_gust': data['fact']['wind_gust'],
#         'wind_dir': DIRECTION_TRANSFORM.get(data['fact']['wind_dir']),
#     }
#     return result


if __name__ == "__main__":
    print("Данные Weatherapi:")
    print(current_weather_with_apiweather(59.93, 30.31))

    # print("\nДанные Yandex_API:")
    # print(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга
