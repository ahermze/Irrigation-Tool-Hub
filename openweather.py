import requests
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
def get_weather(latitude, longitude):
    # url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=imperial&appid='+os.getenv("weather_api_id")
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&exclude={"alerts"}&appid={"weather_api_id"}'
    response = requests.get(url)
    try:
        data=response.json()
        print(data)
        # print(data['name'])
        return data

    except Exception as e:
        print(f"error: {e}")
