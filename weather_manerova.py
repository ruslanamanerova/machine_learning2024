import requests

API_KEY = '5d972375ea4250da38654903f3ef9d49'  # API-ключ OpenWeatherMap
URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city_name):
    try:
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric',  # Температура в Цельсиях
            'lang': 'ru'  # Ответ на русском языке
        }

        response = requests.get(URL, params=params)
        data = response.json()

        city = data['name']
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']

        print(f"Погода в городе {city}:")
        print(f"Температура: {temp}°C")
        print(f"Описание: {description}")
        print(f"Влажность: {humidity}%")

    except Exception as e:
        print("Ошибка: что-то пошло не так, возможно, вы ввели неправильное название города")


if __name__ == "__main__":
    city = input("Введите город: ")
    get_weather(city)