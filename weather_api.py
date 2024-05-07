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
    s = f"Город: {response['location']['name']}\n" \
        f"Температура: {response['current']['temp_c']}\n" \
        f"Как ощущается: {response['current']['feelslike_c']}\n" \
        f"Ветер: {response['current']['wind_kph']}\n" \
        f"Время: {datetime.fromtimestamp(response['current']['last_updated_epoch'])}"
    return s


def current_weather(lat, lon):
    """
    Описание функции, входных и выходных переменных
    """
    token = '9386fc7e-e6fc-482b-9847-c42f340390b3'  # Вставить ваш токен
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"  # Если вдруг используете тариф «Погода на
    # вашем сайте», то вместо forecast используйте informers. url = f"https://api.weather.yandex.ru/v2/informers?lat=
    # {lat}&lon={lon}"
    headers = {"X-Yandex-API-Key": f"{token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Данная реализация приведена для тарифа «Тестовый», если у вас Тариф «Погода на вашем сайте», то закомментируйте
    # пару строк указанных ниже
    result = {
        'city': data['geo_object']['locality']['name'],  # Если используете Тариф «Погода на вашем сайте», то
        # закомментируйте эту строку
        'time': datetime.fromtimestamp(data['fact']['uptime']).strftime("%H:%M"),  # Если используете Тариф «Погода на
        # вашем сайте», то закомментируйте эту строку
        'temp': data['fact']['temp'],  # TODO Реализовать вычисление температуры из данных полученных от API
        'feels_like_temp': data['fact']['feels_like'],  # TODO Реализовать вычисление ощущаемой температуры из данных
        # полученных от API
        'pressure': data['fact']['pressure_mm'],  # TODO Реализовать вычисление давления из данных полученных от API
        'humidity': data['fact']['humidity'],  # TODO Реализовать вычисление влажности из данных полученных от API
        'wind_speed': data['fact']['wind_speed'],  # TODO Реализовать вычисление скорости ветра из данных полученных от API
        'wind_gust': data['fact']['wind_gust'],  # TODO Реализовать вычисление скорости порывов ветка из данных полученных от API
        'wind_dir': DIRECTION_TRANSFORM.get(data['fact']['wind_dir']),  # Если используете Тариф «Погода на вашем
        # сайте», то закомментируйте эту строку
    }
    return result


if __name__ == "__main__":
    print("Данные Weatherapi:")
    print(current_weather_with_apiweather(59.93, 30.31))

    print("\nДанные Yandex_API:")
    print(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга
