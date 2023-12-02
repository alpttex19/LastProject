import requests
import json
import os
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
        self.weathers = []
        with open('favorcity.txt', 'r', encoding='utf-8') as f:
            # 如果文件内容为空，直接返回
            if os.stat('favorcity.txt').st_size == 0:
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
        print('---------------------------------')
        for cityinfo in self.weathers:
            print('weather.py', cityinfo)
        print('---------------------------------')
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
        with open('favorcity.txt', 'w', encoding='utf-8') as f:
            for cityinfo in self.weathers:
                if cityinfo['class'] == 'Weather':
                    f.write(cityinfo['class'] + ' ' + cityinfo['cityname'] + ' ' + str(cityinfo['code']) + '\n')
                elif cityinfo['class'] == 'GlobalWeather':
                    f.write(cityinfo['class'] + ' ' + cityinfo['cityname'] + ' ' + str(cityinfo['lat']) + ' ' + str(cityinfo['lon']) + '\n')
            
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
            raise Exception('globalweather api error')
        
    def add_weather(self, weather):
        self.globalweathers.append(weather)

    def get_weather(self, time = None):
        for weather in self.globalweathers:
            if time == None:
                return weather
            if weather.time == time:
                return weather
        raise Exception('time not found in globalweather')

