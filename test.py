import requests
import json
import datetime

# exchage the localtime to utc mode
localtime = datetime.datetime.now()
utc_time = datetime.datetime.utcfromtimestamp(localtime.timestamp())
print(utc_time)
api1 = '30fbfb28f58b3ac00dadfc75aa78b790'
api = 'b81e53352899d219d96a6b1371b6929a'
# url =    'https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={}'.format(api1)
url = 'http://api.openweathermap.org/data/2.5/forecast?lat=44.34&lon=10.99&appid={appid}'.format(appid=api)
responseweather = requests.get(url)
data = json.loads(responseweather.text)
print(data)

# api_key = '81509fdfa2136f8c873d16fd812cb8fc'
# url = 'https://restapi.amap.com/v3/weather/weatherInfo?key={}&city={}&extensions=all'.format(api_key, '北京市')
# response = requests.get(url)
# data = json.loads(response.text)
# print(data)
 