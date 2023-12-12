"""
Project Name: Weather Forecast
Author: 阿拉帕提
Date: 2023-12-12
Function Description:
You need to implement at least the following basic functions:
    1. City search: Users can enter the city name to search for weather information.
    2. Weather display:
        (1) Display the weather conditions of the next 24 hours (or 24 hours of the day), including temperature, humidity, wind power and direction, etc.
        (2) Display the weather conditions of different dates (including the past few days, today and the next few days) of the selected city, including temperature, humidity, wind power and direction, etc.
    3. Data update: The application should be able to get the latest data from the API regularly to keep the information up-to-date.
    4. Error handling: When the relevant city cannot be searched or the API service is not available, the application should be able to give users appropriate feedback.

If you can achieve the following advanced functions, it will be an extra point. The general principle is that the richer the function, the higher the score:
    1. Multi-location save: Users can save the weather information of multiple locations for quick switching and viewing.
    2. Weather warning: The application can send warnings based on weather data, such as strong wind warning, heavy rain warning, high temperature warning and heavy snow warning.
    3. Weather trend chart: Use charts to show historical and forecast weather data trends, such as temperature curves, precipitation bar charts, etc. This function may be related to the functions that the specific public weather API can provide, and students need to study the corresponding API interface they choose.
    4. Multi-language support: Switch the application between Chinese and English display according to user preferences.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
项目名称: 天气预报
作者：阿拉帕提
时间： 2023-12-12
功能描述:
你需要至少实现以下基本功能:
    1.城市搜索:用户可以自行输入城市名称来搜索天气信息。
    2.天气显示:
        (1)显示当日未来 24h (或者当日 24h)的天气状况，包括温度、湿度、风力风向等。
        (2) 展示所选城市的不同日期(包括过去几日、今日和未来几日)对应的天气状况，包括温度、湿度、风力风向等。
    3.数据更新:应用应能够定时从 API 获取最新数据，保持信息的实时性。
    4.错误处理:当搜索不到相关城市或者API 服务不可用时，应用应能够给用户合适的反馈。

如果能实现以下高级功能，则作为加分项，总的原则就是功能越丰富分数越高:
    1.多地点保存:用户可以保存多个地点的天气信息，便于快速切换查看。
    2.天气预警:应用可以综合根据天气数据发送预警，例如大风预警、暴雨预警、高温预警和大雪预警等。
    3.天气趋势图表:利用图表展示历史和预测的天气数据趋势，如温度曲线、降水量柱状图等。这一功能可能和具体公开的天气 API 所能提供的功能有关，需要同学们自行研究对应选择的 API 接口。
    4.多语言支持：课根据用户偏好，切换应用中英文显示。
"""


from gui import WeatherGUI
from Readfiles import *


def main():
    try:
        international_countrys = international_country_info() # international city list
        cn_citys = national_city_info()                       # china city list
        countryfullnames = national_city_list()               # china city full name list
        WeatherGUI(cn_citys, international_countrys, countryfullnames)

    except Exception as e:
        print(e)
        print('Error: unable to start thread')

if __name__ == '__main__':
    main()