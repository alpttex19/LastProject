# 功能描述
# 你需要至少实现以下基本功能:
# 1.城市搜索:用户可以自行输入城市名称来搜索天气信息。
# 2.天气显示:(1)显示当日未来 24h (或者当日 24h)的天气状况，包括温度、湿度、风力风向等。
#           (2) 展示所选城市的不同日期(包括过去几日、今日和未来几日)对应的天气状况，
#               包括温度、湿度、风力风向等。
# 3.数据更新:应用应能够定时从 API 获取最新数据，保持信息的实时性。
# 4.错误处理:当搜索不到相关城市或者API 服务不可用时，应用应能够给用户合适的反馈。
#
# 如果能实现以下高级功能，则作为加分项，总的原则就是功能越丰富分数越高:
#1.多地点保存:用户可以保存多个地点的天气信息，便于快速切换查看。
# 2.天气预警:应用可以综合根据天气数据发送预警，例如大风预警、暴雨预警、高温预警和大雪预警等。
# 3.天气趋势图表:利用图表展示历史和预测的天气数据趋势，如温度曲线、降水量柱状图等。这一功能可能和具体公开的天气 API 所能提供的功能有关，需要同学们自行研究对应选择的 API 接口。
# 4.多语言支持：课根据用户偏好，切换应用中英文显示。


from gui import WeatherGUI
from Readfiles import *

# 读取城市代码
# def get_city_code():
#     try:
#         df = pd.read_excel('D:\VS_code\Python_Pro\LastProject\AMap_adcode_citycode.xlsx', 
#                            usecols=range(3), dtype=str, nrows=3242)
        
#         city_codes = {}
#         for index, row in df.iterrows():
#             city_name = row['中文名']
#             adcode = row['adcode']
#             citycode = row['citycode']
#             city_codes[city_name] = {'adcode': adcode, 'citycode': citycode}
#         return city_codes
#     except FileNotFoundError:
#         print("File not found. Please check the file path.")
#         return {}
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return {}

def main():
    international_countrys_list = international_country_info() # international city list
    city_code_data = national_city_info()              # china city list
    GUI = WeatherGUI(city_code_data, )

    # city_code = get_city_code()
    # city = input('请输入城市名称：')
    # while city not in city_code:
    #     print('输入城市名称有误')
    #     city = input('请重新输入：')
    
    # cityadcode = city_code[city].get('adcode')
    # citycitycode = city_code[city].get('citycode')
    # print(cityadcode)
    # print(citycitycode)
    # weather_api = WeatherAPI(cityadcode)
    # weather = weather_api.get_weather(city, weather_api.date)
    # print('城市：{}\n日期：{}\n温度：{}\n湿度：{}\n风力风向：{}'
    #       .format(weather.city, weather.date, weather.temperature, weather.humidity, weather.wind))


if __name__ == '__main__':
    main()