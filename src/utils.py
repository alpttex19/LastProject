# Desc: 一些工具函数，如读取文件，写入文件等
# 用于前期处理网上提供城市信息等数据，将其转换为可用的数据
# Date: 2019-11-12
# Author: 阿拉帕提


import json

# 读取json文件
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 将json文件中的数据写入到txt文件中
def write_txt_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in data:
            # line = (line['id'], line['name'], line['state'], line['country'], line['coord']['lat'], line['coord']['lon'])
            f.write(str(line))
            f.write('\n')
        
# write_txt_file('national_city_list.txt', read_json_file('city.list.json'))


# 读取json文件，
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 只留下country为CN的城市信息， 并将state信息去掉
def sort_country_named_CN(data):
    # data = [line for line in data if line['country'] == 'CN']
    data.sort(key=lambda x: x['country'])
    for line in data:
        line.pop('state')
    return data


# 将排序后的数据写到text文件中 一行一个城市信息
def write_txt_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in data:
            f.write(str(line))
            f.write('\n')

# write_txt_file('national_city_list.txt', sort_country_named_CN((read_json_file('city.list.json'))))


# 按行读取Country.txt文件，只保留第一，第六列信息，并保存为元组
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return data

def write_txt_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in data:
            f.write(str(line))
            f.write('\n')

def sort_country_named(data):
    data = [line.split() for line in data]
    # data = [(line[0], line[5]) for line in data]
    data = [line[0] + ' ' + line[5] for line in data]
    return data

# write_txt_file('country2fullname.txt', sort_country_named(read_txt_file('Country.txt')))
from Readfiles import international_country_info

international_countrys = international_country_info()

def read_txt_file(file_path1, file_path2):
    returndata = []
    with open(file_path1, 'r', encoding='utf-8') as f1:
        data1 = f1.readlines()
    for line1 in data1:
        flag = False
        line1 = line1.strip()
        line1 = line1.split()
        for country in international_countrys.keys():
            print(line1[0], country)
            if line1[0] == country:
                flag = True
        if flag == True:
            line1 = line1[0] + ' ' + line1[1]
            returndata.append(line1)
        else:
            continue
    return returndata


def write_txt_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in data:
            f.write(str(line))
            f.write('\n')

# write_txt_file('fullname.txt', read_txt_file('country2fullname.txt', 'city.list.json'))

# 读取national_city_list.txt文件，并将每一行以第二列的字母顺讯排序后存取
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return data

def write_txt_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in data:
            f.write(str(line))
            f.write('\n')

def sort_city_name(data):
    data = [line.split() for line in data]
    data.sort(key=lambda x: x[1])
    data = [line[0] + ' ' + line[1] for line in data]
    return data

write_txt_file('fullname11.txt', sort_city_name(read_txt_file('fullname.txt')))