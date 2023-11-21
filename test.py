import requests
import json
import datetime

# exchage the localtime to utc mode
localtime = datetime.datetime.now()
utc_time = datetime.datetime.utcfromtimestamp(localtime.timestamp())
print(utc_time)

api = 'b81e53352899d219d96a6b1371b6929a'

geourl = 'http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid={}'.format(api)
url =    'http://api.openweathermap.org/data/2.5/forecast?q=beijing&appid={appid}'.format(appid=api)
responseweather = requests.get(url)
data = json.loads(responseweather.text)
# output the data to output.json
with open('output.json', 'w') as outfile:
    json.dump(data, outfile)

responsegeo = requests.get(geourl)
geodata = json.loads(responsegeo.text)
with open('geooutput.json', 'w') as outfile:
    json.dump(data, outfile)

