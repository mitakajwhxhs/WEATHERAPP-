import requests
from datetime import datetime

# 🔧 Константи и настройки
API_KEY = 'c9245afed767732b196728d13f30d7b6'
LAT = 42.1167  # Ширина за село Златитрап
LON = 24.6333  # Дължина за село Златитрап

# 🌦️ URL за прогноза
weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang=bg"

# ⛅ Извличане на данни
response = requests.get(weather_url)
data = response.json()

print("=== Рибарска прогноза за село Златитрап (следващите 5 дни) ===\n")

# 🎣 Обработване и показване на прогноза
for forecast in data['list']:
    dt = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M')
    temp = forecast['main']['temp']
    pressure = forecast['main']['pressure']
    clouds = forecast['clouds']['all']
    wind_speed = forecast['wind']['speed']
    wind_deg = forecast['wind'].get('deg', 'N/A')
    desc = forecast['weather'][0]['description']
    rain = forecast.get('rain', {}).get('3h', 0)  # валежи за 3 часа

    # 💡 Малко логика за рибарите
    fish_hint = "🟢 Добри условия"
    if wind_speed > 6 or rain > 3:
        fish_hint = "🔴 Лоши условия"
    elif pressure < 1010:
        fish_hint = "🟡 Умерени условия"

    # 🖨️ Печат на резултатите
    print(f"{dt} | Темп: {temp}°C | Налягане: {pressure} hPa | "
          f"Облаци: {clouds}% | Вятър: {wind_speed} м/с ({wind_deg}°) | "
          f"Валеж: {rain} мм | Време: {desc} | 👉 {fish_hint}")
