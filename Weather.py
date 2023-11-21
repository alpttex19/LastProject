import requests
import json
import datetime
from tkinter import messagebox
# 天气类
class Weather:
    def __init__(self, city, date, week, temperature, humidity, wind, dayweather, nightweather):
        self.city = city
        self.date = date
        self.temperature = temperature
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
        
    def delete_weather(self,city):
        self.weathers.pop(city)

    def get_weather(self, city):
        return self.weathers[city]
    
    def get_favor_cityls(self):
        return self.weathers.keys()

        # for weather in self.weathers:
        #     favorite_list.setdefault(weather.city, {})[weather.date] = {
        #         'week': weather.week, 
        #         'temperature': weather.temperature,
        #         'humidity': weather.humidity, 
        #         'wind': weather.wind, 
        #         'dayweather': weather.dayweather,
        #         'nightweather': weather.nightweather
        #     }
        # print(json.dumps(favorite_list, indent=4, ensure_ascii=False))
        # return favorite_list
            


            
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
        print(data)
        if data['status'] == '1':
            day_city = data['forecasts'][0]['city']
            for day in data['forecasts'][0]['casts']:
                weather = Weather(day_city, day['date'], day['week'], day['daytemp'], 
                                  day['daypower'], day['daywind'], day['dayweather'], day['nightweather'])
                self.add_weather(weather)
        else:
            messagebox.showinfo('错误', '无法获取天气信息')
   
    def add_weather(self, weather):
        self.weathers.append(weather)
    
    def get_weather(self, city, date=None):
        for weather in self.weathers:
            if weather.city == city:
                if date is None or weather.date == date:
                    return weather
            else:
                print('city not found')
            
    