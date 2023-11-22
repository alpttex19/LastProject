# 读取city.list.json文件，将每一个个城市信息输出为一行，分别为id, name, state, country, lat, lon

import json
import os

# # 读取json文件
# def read_json_file(file_path):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#     return data

# # 将json文件中的数据写入到txt文件中
# def write_txt_file(file_path, data):
#     with open(file_path, 'w', encoding='utf-8') as f:
#         for line in data:
#             # line = (line['id'], line['name'], line['state'], line['country'], line['coord']['lat'], line['coord']['lon'])
#             f.write(str(line))
#             f.write('\n')
        
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

write_txt_file('national_city_list.txt', sort_country_named_CN((read_json_file('city.list.json'))))