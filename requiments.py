import requests
from datetime import datetime

class FishingForecast:
    def __init__(self, api_key, lat, lon, lang='bg'):
        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        self.lang = lang
        self.weather_url = (
            f"https://api.openweathermap.org/data/2.5/forecast?"
            f"lat={lat}&lon={lon}&appid={api_key}&units=metric&lang={lang}"
        )

    def fetch_forecast(self):
        try:
            response = requests.get(self.weather_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Грешка при извличане на данни: {e}")
            return None

    def analyze_forecast(self, data):
        forecasts = []

        for forecast in data['list']:
            dt = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M')
            temp = forecast['main']['temp']
            pressure = forecast['main']['pressure']
            clouds = forecast['clouds']['all']
            wind_speed = forecast['wind']['speed']
            wind_deg = forecast['wind'].get('deg', 'N/A')
            desc = forecast['weather'][0]['description']
            rain = forecast.get('rain', {}).get('3h', 0)

            # 🎣 Условия за риболов
            if wind_speed > 6 or rain > 3:
                fish_hint = "🔴 Лоши условия"
            elif pressure < 1010:
                fish_hint = "🟡 Умерени условия"
            else:
                fish_hint = "🟢 Добри условия"

            forecasts.append({
                "datetime": dt,
                "temperature": temp,
                "pressure": pressure,
                "clouds": clouds,
                "wind_speed": wind_speed,
                "wind_deg": wind_deg,
                "rain": rain,
                "description": desc,
                "fishing_hint": fish_hint
            })

        return forecasts

    def print_forecast(self, forecasts):
        print("=== Рибарска прогноза ===\n")
        for f in forecasts:
            print(f"{f['datetime']} | Темп: {f['temperature']}°C | "
                  f"Налягане: {f['pressure']} hPa | Облаци: {f['clouds']}% | "
                  f"Вятър: {f['wind_speed']} м/с ({f['wind_deg']}°) | "
                  f"Валеж: {f['rain']} мм | Време: {f['description']} | 👉 {f['fishing_hint']}")

# 🔧 Настройки за село Златитрап
API_KEY = 'c9245afed767732b196728d13f30d7b6'
LAT = 42.1167
LON = 24.6333

# 🚀 Изпълнение
if __name__ == "__main__":
    ff = FishingForecast(api_key=API_KEY, lat=LAT, lon=LON)
    data = ff.fetch_forecast()

    if data:
        forecasts = ff.analyze_forecast(data)
        ff.print_forecast(forecasts)
    else:
        print("❌ Няма налични данни.")
