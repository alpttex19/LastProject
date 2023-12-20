"""
Descriptions:
- This file is used to read the files of city information
Author: 阿拉帕提
Date: 2023-12-12
functions:
- national_city_info: read the file city_codes.txt, save the city information of each line in the dict in the form of tuple
- national_citys_list: read the file city_codes.txt, save the city information of each line in the list in the form of tuple
- international_country_info: read the file national_city_list.txt, save the city information of each line in the dict in the form of tuple
- citys_lat_lon: read the file national_city_list.txt, save the city information of each line in the list in the form of tuple
- countrys: read the file national_city_list.txt, save the city information of each line in the list in the form of tuple
- national_citys: read the file national_city_list.txt, save the city information of each line in the list in the form of tuple
- national_city_list: read the file national_city_list.txt, save the city information of each line in the list in the form of tuple
"""

import json

def national_city_info()->dict:
    """
    :return: a dict, the key is the city name, the value is the city code
    """
    city_info = {}
    # read the city name, adcode and citycode from the file city_codes.txt
    with open('./cityinfo/city_codes.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if len(line.split()) == 2:
                city_name, adcode = line.split()
                citycode = ''
            else:
                city_name, adcode, citycode = line.split()
            city_info[city_name] = {'adcode': adcode, 'citycode': citycode}
    return city_info

def national_citys_list(city_info)->list:
    """
    :param city_info: the dict of the national city list
    :return: a list, the elements are the city name
    """
    cn_citys = []
    for city_name in city_info:
        cn_citys.append(city_name)
    return cn_citys



def international_country_info()->dict:
    """
    :return: a dict, the key is the country name, the value is the country code
    """
    national_country_list = {}
    # read the country name and country code from the file national_city_list.txt
    with open('./cityinfo/city.list.json', 'r', encoding='utf-8') as f:
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

def citys_lat_lon(national_country_list, country, city)->tuple:
    """
    :param national_country_list: the dict of the national country list
    :param country: the country name
    :param city: the city name
    :return: the lat and lon of the city
    """
    # country is the key of the national_country_list, city is the key of the national_city_list, return the lat and lon of the city
    for city_info in national_country_list[country]:
        if city_info['name'] == city:
            lat = city_info['lat']
            lon = city_info['lon']
            # print(lat, lon)
            return lat, lon

def countrys(national_country_list)->list:
    """
    :param national_country_list: the dict of the national country list
    """
    # coutryname is the key of the national_city_list, make countryname as a list
    countrys = []
    for countryname in national_country_list:
        countrys.append(countryname)
    # print(countrys)
    return countrys

def national_citys(national_country_list, country)->list:
    """
    :param national_country_list: the dict of the national country list
    """
    # country is the key of the national_country_list, make cityname as a list
    national_citys = []
    for city in national_country_list[country]:
        national_citys.append(city['name'])
    # duplicate removal
    national_citys = list(set(national_citys))
    national_citys.sort()
    # print(national_citys)
    return national_citys

# read the file national_city_list.txt, save the city information of each line in the list in the form of tuple
def national_city_list()->dict:
    """
    :return: a dict, the key is the fullname of the city, the value is the city name
    """
    national_city_list = {}
    with open('./cityinfo/fullname.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            line = line.split()
            national_city_list[line[1]] = line[0]
    return national_city_list