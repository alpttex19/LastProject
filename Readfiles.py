import json

def national_city_info():
    # 从city_codes.txt文件中读入城市中文名、adcode和citycode
    city_info = {}
    with open('city_codes.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if len(line.split()) == 2:
                city_name, adcode = line.split()
                citycode = ''
            else:
                city_name, adcode, citycode = line.split()
            city_info[city_name] = {'adcode': adcode, 'citycode': citycode}
    return city_info

def national_citys_list(city_info):
    cn_citys = []
    for city_name in city_info:
        cn_citys.append(city_name)
    return cn_citys



def international_country_info():
    # 从national_city_list.txt读取国家名，并以国家名为字典键，城市各项信息为字典值构成字典
    national_country_list = {}
    with open('city.list.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for line in data:
            countryname = line['country']
            cityname = line['name']
            id = line['id']
            lat = line['coord']['lat']
            lon = line['coord']['lon']
            # if the countryname is none,then delete the line
            if countryname == '':
                continue
            if countryname not in national_country_list:
                national_country_list[countryname] = []
            national_country_list[countryname].append({'name': cityname, 'id': id, 'lat': lat, 'lon': lon})
        # sort by the name of city
        for countryname in national_country_list:
            national_country_list[countryname].sort(key=lambda x: x['name'])
    #print(national_country_list)
    return national_country_list

# national_country_list()

def citys_lat_lon(national_country_list, country, city):
    # country is the key of the national_country_list, city is the key of the national_city_list, return the lat and lon of the city
    for city_info in national_country_list[country]:
        if city_info['name'] == city:
            lat = city_info['lat']
            lon = city_info['lon']
            # print(lat, lon)
            return lat, lon

def countrys(national_country_list):
    # coutryname is the key of the national_city_list, make countryname as a list
    countrys = []
    for countryname in national_country_list:
        countrys.append(countryname)
    # print(countrys)
    return countrys

def national_citys(national_country_list, country):
    # country is the key of the national_country_list, make cityname as a list
    national_citys = []
    for city in national_country_list[country]:
        national_citys.append(city['name'])
    # duplicate removal
    national_citys = list(set(national_citys))
    national_citys.sort()
    # print(national_citys)
    return national_citys

# countrys(international_country_list())
# national_citys(international_country_list(), 'CN')


# return the city fullname of the city
# 读取national_city_list.txt文件，将每一行的城市信息以元组的形式保存在列表中
def national_city_list():
    national_city_list = {}
    with open('fullname.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            line = line.split()
            national_city_list[line[1]] = line[0]
    return national_city_list

# print(national_city_list()['IR'])

