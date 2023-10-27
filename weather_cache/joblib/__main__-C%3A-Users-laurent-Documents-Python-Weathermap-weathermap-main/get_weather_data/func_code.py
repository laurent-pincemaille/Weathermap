# first line: 33
@cache_weather_data
def get_weather_data(city):
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(base_url)
    data = response.json()
    save_icon(data['weather'][0]['icon'])
    return data
