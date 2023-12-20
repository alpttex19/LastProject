"""
Descriptions:
- this file is used to define the class of weather and globalweather
Module Name: 
- Weather: A class representing weather information for a specific city on a given date.
- WeatherGet: A class for fetching and managing weather information for a specific city using an external API.
- GlobalWeather: A class representing global weather information for a specific city.
- GlobalWeatherGet: A class for fetching and managing global weather information for a specific geographical location using an external API.
- MyFavoriteCity: A class for storing and managing information about favorite cities and their weather details.

Author: 阿拉帕提
Date: 2023-12-12

Usage:
- Import the module into another script or interactive session as needed.
- Instantiate the WeatherGet class with a city name to fetch weather information for that city.
- Instantiate the GlobalWeatherGet class with a latitude and longitude to fetch global weather information for that location.
- Instantiate the MyFavoriteCity class to manage favorite cities and their weather information.

NOTE: The WeatherGet and GlobalWeatherGet classes use external APIs to fetch data, and the fetched data is converted into Weather and GlobalWeather objects, respectively.
"""

import requests
import json
import os
import datetime
from tkinter import messagebox
# 天气类
class Weather:
    """
    A class representing weather information for a specific city on a given date.

    Attributes:
    - city (str): The name of the city for which weather information is recorded.
    - date (str): The date for which the weather information is applicable.
    - week (str): The day of the week corresponding to the date.
    - daytemperature (float): The daytime temperature in degrees Celsius.
    - nighttemperature (float): The nighttime temperature in degrees Celsius.
    - humidity (int): The humidity level as a percentage.
    - wind (str): The wind conditions for the day.
    - dayweather (str): The weather conditions during the day.
    - nightweather (str): The weather conditions during the night.

    Methods:
    - __init__(self, city, date, week, daytemperature, nighttemperature, humidity, wind, dayweather, nightweather):
        Initializes a Weather object with the provided weather details.

    NOTE: It is assumed that the temperature is in degrees Celsius, humidity is represented as a percentage,
    and wind is a descriptive string indicating wind conditions.

    """
    def __init__(self, city, date, week, daytemperature, nighttemperature, humidity, wind, dayweather, nightweather):
        self.city = city
        self.date = date
        self.daytemperature = daytemperature
        self.nighttemperature = nighttemperature
        self.humidity = humidity
        self.wind = wind
        self.dayweather = dayweather
        self.nightweather = nightweather
        self.week = week  


            
# 通过api获取天气信息
class WeatherGet:
    """
    A class for fetching and managing weather information for a specific city using an external API.

    Attributes:
    - weathers (list): A list to store Weather objects representing daily weather information.
    - city (str): The name of the city for which weather information is fetched.
    - api_key (str): The API key for accessing the weather API.
    - url (str): The URL for the weather API request, including the API key and city name.
    - date (datetime): The current date and time when the WeatherGet object is instantiated.

    Methods:
    - __init__(self, city): Initializes a WeatherGet object for the specified city, sets up API details, and fetches initial weather data.
    - update_weather(self): Fetches updated weather data from the API and populates the 'weathers' list with Weather objects.
    - add_weather(self, weather): Adds a Weather object to the 'weathers' list.
    - get_weather(self, date=None): Retrieves weather information for a specific date from the 'weathers' list.
                                    If no date is specified, returns the latest weather information.

    NOTE: The class uses an external weather API to fetch data, and the fetched data is converted into Weather objects.
    """
    def __init__(self, city):
        self.weathers = []
        self.datelist = []
        self.city = city
        self.api_key = '81509fdfa2136f8c873d16fd812cb8fc'
        self.url = 'https://restapi.amap.com/v3/weather/weatherInfo?key={}&city={}&extensions=all'.format(self.api_key, city)
        self.date = datetime.datetime.now()
        self.update_weather()
        

    def update_weather(self):
        print('---------------fetch the national weather data------------------')
        self.weathers.clear()
        response = requests.get(self.url)
        data = json.loads(response.text)
        # print(data)
        if data['status'] == '1':
            day_city = data['forecasts'][0]['city']
            for day in data['forecasts'][0]['casts']:
                weather = Weather(day_city, day['date'], day['week'], day['daytemp'], day['nighttemp'],
                                  day['daypower'], day['daywind'], day['dayweather'], day['nightweather'])
                self.datelist.append(day['date'])
                self.add_weather(weather)
        else:
            raise Exception('weather api error')
   
    def add_weather(self, weather):
        self.weathers.append(weather)
    
    def get_weather(self, date = None):
        for weather in self.weathers:
            # print('124', weather.date, date)
            if date == None:
                return weather
            if date == weather.date:
                return weather
        raise Exception('date not found in weather')
            
class GlobalWeather:
    """
    A class representing global weather information for a specific city.

    Attributes:
    - country (str): The country where the city is located.
    - city (str): The name of the city for which global weather information is recorded.
    - time (str): The time at which the weather information is applicable.
    - temp_max (float): The maximum temperature in degrees Celsius.
    - temp_min (float): The minimum temperature in degrees Celsius.
    - feels_like (float): The perceived temperature, or "feels like" temperature, in degrees Celsius.
    - pressure (int): The atmospheric pressure in hPa (hectopascals).
    - humidity (int): The humidity level as a percentage.
    - description (str): A description of the weather conditions.
    - wind (str): The wind conditions for the specified time.

    Methods:
    - __init__(self, country, city, time, temp_max, temp_min, feels_like, pressure, humidity, description, wind):
        Initializes a GlobalWeather object with the provided global weather details.

    NOTE: It is assumed that the temperature is in degrees Celsius, pressure is in hPa, and humidity is represented as a percentage.
    """
    def __init__(self, country, city, time, temp_max, temp_min, feels_like, pressure, humidity, description, wind):
        self.country = country
        self.city = city
        self.time = time
        self.temp_max = temp_max
        self.temp_min = temp_min
        self.feels_like = feels_like
        self.pressure = pressure
        self.humidity = humidity
        self.description = description
        self.wind = wind


class GlobalWeatherGet:
    """
    A class for fetching and managing global weather information for a specific geographical location using an external API.

    Attributes:
    - globalweathers (list): A list to store GlobalWeather objects representing global weather information for different times.
    - timelist (list): A list to store the timestamps of the retrieved global weather data.
    - lat (float): The latitude of the geographical location for which global weather information is fetched.
    - lon (float): The longitude of the geographical location for which global weather information is fetched.
    - api (str): The API key for accessing the global weather API.
    - url (str): The URL for the global weather API request, including latitude, longitude, and the API key.

    Methods:
    - __init__(self, lat, lon): Initializes a GlobalWeatherGet object for the specified geographical location, sets up API details, and fetches initial global weather data.
    - update_weather(self): Fetches updated global weather data from the API and populates the 'globalweathers' list with GlobalWeather objects.
    - add_weather(self, weather): Adds a GlobalWeather object to the 'globalweathers' list.
    - get_weather(self, time=None): Retrieves global weather information for a specific time from the 'globalweathers' list.
                                    If no time is specified, returns the latest global weather information.

    NOTE: The class uses an external global weather API to fetch data, and the fetched data is converted into GlobalWeather objects.
    """
    def __init__(self, lat, lon):
        self.globalweathers = []
        self.timelist = []
        self.lat = lat
        self.lon = lon
        self.api = 'b81e53352899d219d96a6b1371b6929a'
        self.url = 'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={appid}'.format(
                        lat = self.lat, lon = self.lon, appid=self.api)
        self.update_weather()
    
    def update_weather(self):
        # update the weather information
        print('---------------fetch the international weather data------------------')
        self.globalweathers.clear()
        responseweather = requests.get(self.url)
        data = json.loads(responseweather.text)
        # print(data)
        if data['cod'] == '200':
            countryname = data['city']['country']
            cityname = data['city']['name']
            for day in data['list']:
                weather = GlobalWeather(countryname, cityname, day['dt_txt'], round((day['main']['temp_max']-273.15), 2),
                                        round((day['main']['temp_min']-273.15), 2), round((day['main']['feels_like']-273.15), 2), day['main']['pressure'],
                                        day['main']['humidity'], day['weather'][0]['description'], str('deg:'+ str(day['wind']['deg'])+'~speed:'+str(day['wind']['speed'])))
                self.timelist.append(day['dt_txt'])
                self.add_weather(weather)
        else:
            raise Exception('globalweather api error')
        
    def add_weather(self, weather):
        # add the weather information to the list
        self.globalweathers.append(weather)

    def get_weather(self, time = None):
        # get the weather information and return it 
        for weather in self.globalweathers:
            if time == None:
                return weather
            if weather.time == time:
                return weather
        raise Exception('time not found in globalweather')

# 用来存储我喜爱的城市的天气信息
class MyFavoriteCity:
    """
    A class for storing and managing information about favorite cities and their weather details.

    Attributes:
    - weathers (list): A list to store dictionaries containing information about cities and their weather.
                       Each dictionary includes the city's class (Weather/GlobalWeather), name, and corresponding details.

    Methods:
    - __init__(): Initializes the MyFavoriteCity object, reads data from a file, and populates the 'weathers' list.
    - add(cityinfo): Adds a new city information dictionary to the 'weathers' list if the city is not already present.
    - delete(nameofcity): Deletes the city information dictionary with the given name from the 'weathers' list.
    - get_classofcity(city): Retrieves the class (Weather/GlobalWeather) of the specified city.
    - get_city_codes(city): Retrieves the weather code of the specified city.
    - get_city_latlon(city): Retrieves the latitude and longitude of the specified city.
    - get_favor_cityls(): Retrieves a list of all city names stored in the 'weathers' list.
    - __del__(): Writes the 'weathers' list data to a file when the class instance is deleted.

    NOTE: The data is stored in a file ('favorcity.txt') and is read during initialization and written during deletion.
    """
    def __init__(self):
        print('---------------initialize favorite city info------------------')
        self.weathers = []
        with open('./cityinfo/favorcity.txt', 'r', encoding='utf-8') as f:
            # if the file is empty, return directly
            if os.stat('./cityinfo/favorcity.txt').st_size == 0:
                pass
            else:
                for line in f.readlines():
                    cityinfo = {}
                    line = line.split()
                    classofcity = line[0]
                    nameofcity = line[1]
                    cityinfo['class'] = classofcity
                    cityinfo['cityname'] = nameofcity
                    if classofcity == 'Weather':
                        codeofcity = line[2]
                        cityinfo['code'] = codeofcity
                    elif classofcity == 'GlobalWeather':
                        lat = line[2]
                        lon = line[3]
                        cityinfo['lat'] = lat
                        cityinfo['lon'] = lon
                    self.weathers.append(cityinfo)
        # print('---------------------------------')
        # for cityinfo in self.weathers:
        #     print('weather.py', cityinfo)
        # print('---------------------------------')
    def add(self, cityinfo):
        for city in self.weathers:
            if city['cityname'] == cityinfo['cityname']:
                return
        self.weathers.append(cityinfo)
        
    def delete(self, nameofcity):
        for cityinfo in self.weathers:
            if cityinfo['cityname'] == nameofcity:
                self.weathers.remove(cityinfo)
                break

    def get_classofcity(self, city):
        for cityinfo in self.weathers:
            if cityinfo['cityname'] == city:
                return cityinfo['class']

    def get_city_codes(self, city):
        for cityinfo in self.weathers:
            if cityinfo['cityname'] == city:
                return cityinfo['code']
        raise Exception('national city not found in favorcitylists')
    
    def get_city_latlon(self, city):
        for cityinfo in self.weathers:
            # print(cityinfo['cityname'], city)
            if cityinfo['cityname'] == city:
                return cityinfo['lat'], cityinfo['lon']

        raise Exception('international city not found in favorcitylists')

    def get_favor_cityls(self):
        cityls = []
        for cityinfo in self.weathers:
            cityls.append(cityinfo['cityname'])
        return cityls    
    
    # 当类要销毁时，将数据写入文件
    def __del__(self):
        print('---------------saving the favorite city info------------------')
        with open('./cityinfo/favorcity.txt', 'w', encoding='utf-8') as f:
            for cityinfo in self.weathers:
                if cityinfo['class'] == 'Weather':
                    f.write(cityinfo['class'] + ' ' + cityinfo['cityname'] + ' ' + str(cityinfo['code']) + '\n')
                elif cityinfo['class'] == 'GlobalWeather':
                    f.write(cityinfo['class'] + ' ' + cityinfo['cityname'] + ' ' + str(cityinfo['lat']) + ' ' + str(cityinfo['lon']) + '\n')
