import requests
import json
import datetime

# exchage the localtime to utc mode
localtime = datetime.datetime.now()
utc_time = datetime.datetime.utcfromtimestamp(localtime.timestamp())
print(utc_time)

api = 'b81e53352899d219d96a6b1371b6929a'

geourl = 'http://api.openweathermap.org/geo/1.0/direct?q=beijing&limit=1&appid={}'.format(api)
url =    'http://api.openweathermap.org/data/2.5/forecast?q=shanghai&appid={appid}'.format(appid=api)
responseweather = requests.get(url)
data = json.loads(responseweather.text)
# output the data to output.json
with open('output.json', 'w') as outfile:
    json.dump(data, outfile)

responsegeo = requests.get(geourl)
geodata = json.loads(responsegeo.text)
print(geodata[0]['name'])
print(geodata[0]['lat'])
print(geodata[0]['lon'])
print(geodata[0]['state'])
print(geodata[0]['country'])
with open('geooutput.txt', 'w') as outfile:
    outfile.write(geodata[0]['name']+'\n')
    outfile.write(str(geodata[0]['lat'])+'\n')
    outfile.write(str(geodata[0]['lon'])+'\n')
    outfile.write(geodata[0]['state']+'\n')
    outfile.write(geodata[0]['country']+'\n')

