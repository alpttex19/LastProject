import requests
import json
import datetime
from tkinter import messagebox
# 天气类
class Weather:
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

# 用来存储我喜爱的城市的天气信息
class MyFavoriteCity:
    def __init__(self):
        self.weathers = {}
    
    def add_weather(self,city, cityweather):
        self.weathers[city] = cityweather

    def add_global_weather(self, globalcity, cityweather):
        self.weathers[globalcity] = cityweather
        
    def delete_weather(self,city):
        self.weathers.pop(city)

    def delete_global_weather(self, globalcity):
        self.weathers.pop(globalcity)

    def get_weather(self, city):
        return self.weathers[city]

    def get_global_weather(self, globalcity):
        return self.weathers[globalcity]
    
    def get_favor_cityls(self):
        return self.weathers.keys()     
            
# 通过api获取天气信息
class WeatherGet:
    def __init__(self, city):
        self.weathers = []
        self.city = city
        self.api_key = '81509fdfa2136f8c873d16fd812cb8fc'
        self.url = 'https://restapi.amap.com/v3/weather/weatherInfo?key={}&city={}&extensions=all'.format(self.api_key, city)
        self.date = datetime.datetime.now()
        self.update_weather()
        

    def update_weather(self):
        self.weathers.clear()
        response = requests.get(self.url)
        data = json.loads(response.text)
        # print(data)
        if data['status'] == '1':
            day_city = data['forecasts'][0]['city']
            for day in data['forecasts'][0]['casts']:
                weather = Weather(day_city, day['date'], day['week'], day['daytemp'], day['nighttemp'],
                                  day['daypower'], day['daywind'], day['dayweather'], day['nightweather'])
                self.add_weather(weather)
        else:
            messagebox.showinfo('错误', '无法获取天气信息')
   
    def add_weather(self, weather):
        self.weathers.append(weather)
    
    def get_weather(self, city, date=None):
        for weather in self.weathers:
            if weather.city == city:
                # print(weather.date, date)
                if date == weather.date or (date is None) :
                    return weather
        else:
            print('city not found')
            
class GlobalWeather:
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
            messagebox.showinfo('错误', '无法获取天气信息')
        
    def add_weather(self, weather):
        self.globalweathers.append(weather)

    def get_weather(self, time):
        for weather in self.globalweathers:
            if weather.time == time:
                return weather
        else:
                print('global city not found')

