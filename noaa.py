import requests

def get_weather(latitude, longitude):
    try:
        url = f"https://api.weather.gov/points/{latitude},{longitude}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            forecast_url = data['properties']['forecast']
    
            # Send a GET request to the forecast URL
            forecast_response = requests.get(forecast_url)
    
            if forecast_response.status_code == 200:
                # Parse the forecast JSON response
                forecast_data = forecast_response.json()

                # Get the current weather information
                current_weather = forecast_data['properties']['periods'][0]

                # Print the current weather information
                print(f"Temperature: {current_weather['temperature']}°{current_weather['temperatureUnit']}")
                print(f"Short Forecast: {current_weather['shortForecast']}")
                print(f"Detailed Forecast: {current_weather['detailedForecast']}")

                # Check for rainfall information
                if 'rain' in current_weather['shortForecast'].lower():
                    print("Rain is expected.")
                else:
                    print("No rain expected.")
            else:
                print(f"Failed to retrieve forecast data: {forecast_response.status_code}")
        else:
            print(f"Failed to retrieve location data: {response.status_code}")

    except Exception as e:
        print("Requests exception")
        print(e)
        return False

# latitude = 38.4247341
# longitude = -86.9624086

# url = f"https://api.weather.gov/points/{latitude},{longitude}"
# # Send a GET request to get the forecast URL
# response = requests.get(url)
# # Check if the request was successful
# if response.status_code == 200:
#     # Parse the JSON response
#     data = response.json()
    
#     # Get the forecast URL from the response
#     forecast_url = data['properties']['forecast']
    
#     # Send a GET request to the forecast URL
#     forecast_response = requests.get(forecast_url)
    
#     if forecast_response.status_code == 200:
#         # Parse the forecast JSON response
#         forecast_data = forecast_response.json()
        
#         # Get the current weather information
#         current_weather = forecast_data['properties']['periods'][0]
        
#         # Print the current weather information
#         print(f"Temperature: {current_weather['temperature']}°{current_weather['temperatureUnit']}")
#         print(f"Short Forecast: {current_weather['shortForecast']}")
#         print(f"Detailed Forecast: {current_weather['detailedForecast']}")
        
#         # Check for rainfall information
#         if 'rain' in current_weather['shortForecast'].lower():
#             print("Rain is expected.")
#         else:
#             print("No rain expected.")
#     else:
#         print(f"Failed to retrieve forecast data: {forecast_response.status_code}")
# else:
#     print(f"Failed to retrieve location data: {response.status_code}")
