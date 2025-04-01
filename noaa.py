import requests

def find_station(latitude, longitude):
    API_KEY = 'SOUDUwtaSdlzFVDIdPdUhpYeoKCXBbVR'
    headers = {
        'token': API_KEY
    }

    # url = f'https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?latitude={latitude}&longitude={longitude}&limit=1'
    url = f'https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?latitude=40.8136&longitude=96.7026&limit=5'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            print(data)
            # Get the nearest weather station
            nearest_station = data['results'][0]
            station_id = nearest_station['id']
            station_name = nearest_station['name']
            print(f'Nearest Weather Station ID: {station_id}, Name: {station_name}')
        else:
            print('No weather stations found near the specified location.')
    else:
        print(f'Error: {response.status_code} - {response.text}')






















































































# def get_weather(latitude, longitude):
#     try:
#         print(latitude)
#         print(longitude)
#         url = f"https://api.weather.gov/points/{latitude},{longitude}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             forecast_url = data['properties']['forecast']
    
#             # Send a GET request to the forecast URL
#             forecast_response = requests.get(forecast_url)
    
#             if forecast_response.status_code == 200:
#                 # Parse the forecast JSON response
#                 forecast_data = forecast_response.json()

#                 # Get the current weather information
#                 current_weather = forecast_data['properties']['periods'][0]

#                 # Print the current weather information
#                 print(f"Temperature: {current_weather['temperature']}°{current_weather['temperatureUnit']}")
#                 print(f"Short Forecast: {current_weather['shortForecast']}")
#                 print(f"Detailed Forecast: {current_weather['detailedForecast']}")

#                 # Check for rainfall information
#                 if 'rain' in current_weather['shortForecast'].lower():
#                     print("Rain is expected.")
#                 else:
#                     print("No rain expected.")
#                 return current_weather
#             else:
#                 print(f"Failed to retrieve forecast data: {forecast_response.status_code}")
#         else:
#             print(f"Failed to retrieve location data: {response.status_code}")

#     except Exception as e:
#         print("Requests exception")
#         print(e)
#         return False
