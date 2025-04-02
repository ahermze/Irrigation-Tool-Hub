# https://api.openweathermap.org/data/2.5/weather?lat=40.8136&lon=96.7026&appid=5dce344bb5f7327c5c215b3aaa1a78c7
import requests
def get_weather(latitude, longitude):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid=5dce344bb5f7327c5c215b3aaa1a78c7&units=imperial'
    response = requests.get(url)
    try:
        data=response.json()
        # print(data)
        # print(data['name'])
        return data

    except Exception as e:
        print(f"error: {e}")
