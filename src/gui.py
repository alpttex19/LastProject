"""
Description:
- This module is used to create the GUI of all the weather related information
Module Name:
- WeatherGUI(self, cn_citys, international_countrys, countryfullnames): create the GUI of all the weather related information
Author: 阿拉帕提
Date: 2023-12-12
Usage:
- import the class WeatherGUI from the module gui and specify the parameters
NOTE: the GUI is based on the tkinter
"""
import tkinter as tk
from tkinter import ttk, font as tkFont
from tkinter import Canvas, Scrollbar, Frame
import datetime
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# import from my own modules
from Weather import WeatherGet, GlobalWeatherGet, MyFavoriteCity
from Readfiles import national_citys, citys_lat_lon

# GUI界面
class WeatherGUI:
    """
    A class used to represent a WeatherGUI.

    Attributes
    ----------
    - cn_citys : dict of the national city list
    - international_countrys : dict of the international country list
    - countryfullnames : dict of the international country full name list

    Methods
    -------
    - init(self, cn_citys, international_countrys, countryfullnames) : init the GUI
    - update_weather(self) : update the weather information every 10 minutes
    - create_widgets(self) : create the widgets
    - national(self) : show the national weather information
        - city_combobox_selected(self, event) : the city combobox selected event
        - date_combobox_selected(self, event) : the date combobox selected event
        - update_weather_info(self, weather_info) : update the weather information
        - search(self,event) : the search event
        - on_select(self,event) : the search result listbox select event
        - citysearch_button_clicked(self) : the search button clicked event
        - draw_tempreture(self, tmp_canvas, weather_get) : draw the temperature change graph
    - international(self) : show the international weather information
        - country_combobox_selected(self, event) : the country combobox selected event
        - international_city_combobox_selected(self, event) : the international city combobox selected event
        - international_time_combobox_selected(self, event) : the international time combobox selected event
        - international_weather_update(self) : update the international weather information
        - draw_international_tempreture(self, tmp_canvas, weather_get) : draw the international temperature change graph
    - add_favorite(self) : add the city to the favorite list
    - show_favorite(self) : show the favorite list
    - delete_favorite(self) : delete the city from the favorite list
    - chinese(self) : show the chinese language
    - english(self) : show the english language

    NOTE: the GUI is based on the tkinter 
    """
    # 初始化
    def __init__(self,cn_citys, international_countrys, countryfullnames):
        """
        Parameters
        ----------
        - cn_citys : dict of the national city list
        - international_countrys : dict of the international country list
        - countryfullnames : dict of the international country full name list
        """
        self.root = tk.Tk()
        self.root.geometry('600x500')
        self.root.title('天气预报')
        self.maincanvas = tk.Canvas(self.root, width=600, height=500, bg='white')
        self.secondcanvas = tk.Canvas(self.root, width=600, height=500, bg='white')
        self.myfavcanvas = tk.Canvas(self.root, width=600, height=500, bg='white')
        self.city_code = cn_citys
        self.city = tk.StringVar()  # 用来存储用户选择的城市名
        self.city.set('北京市')
        self.date = tk.StringVar()

        self.international_countrys = international_countrys
        self.countryfullnames = countryfullnames
        self.country = tk.StringVar()  # 用来存储用户选择的国家名
        self.country.set('China')
        self.country2city = tk.StringVar()  # 用来存储用户选择的城市名
        self.country2city.set('Beijing')

        self.language = 'chinese' # 默认语言为中文

        self.international_time = tk.StringVar()
        self.last_update_time = None
        self.last_update_time_label = tk.Label()

        self.my_favorite_city = MyFavoriteCity()
        self.update_weather() # 每隔一段时间更新天气信息
        self.create_widgets()  # 创建控件
        self.root.mainloop()  # 进入主循环

    def update_weather(self):
        """
        update the weather information every 10 minutes
        """
        self.weather_get = WeatherGet(self.city_code[self.city.get()]['adcode'])
        self.date.set(self.weather_get.datelist[0])
        self.weather = self.weather_get.get_weather(self.date.get())

        self.citylat, self.citylon = citys_lat_lon(self.international_countrys, self.countryfullnames[self.country.get()], self.country2city.get())
        self.globalweather_get = GlobalWeatherGet(self.citylat, self.citylon)
        self.international_time.set(self.globalweather_get.timelist[0])
        self.globalweather = self.globalweather_get.get_weather(self.international_time.get())
        # 更新数据后，设置一个定时器在1小时后再次更新数据
        self.root.after(600000, self.update_weather)  # 600000毫秒 = 10 min
        # 更新上次更新的时间
        self.last_update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.last_update_time_label.config(text = self.last_update_time)


    def create_widgets(self):
        """
        create the menu bar and call the window of national weather
        """
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.favorite_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='收藏', menu=self.favorite_menu)
        self.favorite_menu.add_command(label='添加至收藏', command=self.add_favorite)
        self.favorite_menu.add_command(label='我的收藏', command=self.show_favorite)
        
        self.favorite_language = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label = '语言/language', menu = self.favorite_language)
        self.favorite_language.add_command(label='中文', command=self.chinese)
        self.favorite_language.add_command(label='English', command=self.english)

        self.na_interna = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label = '国内/国际', menu = self.na_interna)
        self.na_interna.add_command(label='国内', command=self.national)
        self.na_interna.add_command(label='国际', command=self.international)
        # 默认窗口选择 国内
        self.national()

    # NOTE: the following functions are used for the national weather window
    def national(self):
        """
        show the window of the national weather information
        """
        self.secondcanvas.pack_forget()
        self.myfavcanvas.pack_forget()
        self.maincanvas.pack()
        self.maincanvas.update()
        # 城市名称
        self.city_label = tk.Label(self.maincanvas, text='城市：', bg='white')
        self.city_label.place(x=20, y=20, width=100, height=20)
        self.city_combobox = ttk.Combobox(self.maincanvas, textvariable=self.city, state='readonly')
        self.city_combobox['values'] = list(self.city_code.keys())
        self.city_combobox.place(x=120, y=20, width=100, height=20)
        self.city_combobox.bind('<<ComboboxSelected>>', self.city_combobox_selected)

        # select the city by inter city name
        self.citysearch_label = tk.Label(self.maincanvas, text='城市搜索：', bg='white')
        self.citysearch_label.place(x=280, y=20, width=100, height=20)
        self.citysearch_entry = tk.Entry(self.maincanvas)
        self.citysearch_entry.place(x=380, y=20, width=120, height=20)
        self.citysearch_button = tk.Button(self.maincanvas, text='搜索',bg='white', command=self.citysearch_button_clicked)
        self.citysearch_button.place(x=500, y=20, width=50, height=20)
        self.citysearch_entry.bind('<KeyRelease>', self.search)
        # 创建一个列表框来显示搜索结果
        self.search_results_listbox = tk.Listbox(self.maincanvas)
        self.search_results_listbox.place(x=380, y=40, width=120, height=40)
        self.search_results_listbox.bind('<<ListboxSelect>>', self.on_select)
        # 创建一个滚动条
        scrollbar = ttk.Scrollbar(self.maincanvas, orient='vertical', command=self.search_results_listbox.yview)
        scrollbar.place(x=520, y=40, width=20, height=40)
        self.search_results_listbox['yscrollcommand'] = scrollbar.set

        self.date_label = tk.Label(self.maincanvas, text='日期：', bg='white')
        self.date_label.place(x=20, y=60, width=100, height=20)
        self.date_combobox = ttk.Combobox(self.maincanvas, textvariable=self.date, state='readonly')
        self.date_combobox['values'] = self.weather_get.datelist
        self.date_combobox.place(x=120, y=60, width=100, height=20)
        self.date_combobox.bind('<<ComboboxSelected>>', self.date_combobox_selected)

        # 星期、温度、湿度、风力风向、白天天气、夜间天气
        self.week_label = tk.Label(self.maincanvas, text='星期：', bg='white')
        self.week_label.place(x=20, y=100, width=100, height=20)
        self.week_entry = tk.Entry(self.maincanvas)
        self.week_entry.place(x=120, y=100, width=100, height=20)
        self.week_entry.insert(0, self.weather.week)

        self.wind_label = tk.Label(self.maincanvas, text='风力风向：', bg='white')
        self.wind_label.place(x=280, y=100, width=100, height=20)
        self.wind_entry = tk.Entry(self.maincanvas)
        self.wind_entry.place(x=380, y=100, width=100, height=20)
        self.wind_entry.insert(0, self.weather.wind)

        self.temperature_label = tk.Label(self.maincanvas, text='温度：', bg='white')
        self.temperature_label.place(x=20, y=140, width=100, height=20)
        self.temperature_entry = tk.Entry(self.maincanvas)
        self.temperature_entry.place(x=120, y=140, width=100, height=20)
        self.temperature_entry.insert(0,  '{}~{}'.format(self.weather.nighttemperature, self.weather.daytemperature))  

        self.humidity_label = tk.Label(self.maincanvas, text='湿度：', bg='white')
        self.humidity_label.place(x=280, y=140, width=100, height=20)
        self.humidity_entry = tk.Entry(self.maincanvas)
        self.humidity_entry.place(x=380, y=140, width=100, height=20)
        self.humidity_entry.insert(0, self.weather.humidity)

        self.dayweather_label = tk.Label(self.maincanvas, text='白天天气：', bg='white')
        self.dayweather_label.place(x=20, y=180, width=100, height=20)
        self.dayweather_entry = tk.Entry(self.maincanvas)
        self.dayweather_entry.place(x=120, y=180, width=100, height=20)
        self.dayweather_entry.insert(0, self.weather.dayweather)

        self.nightweather_label = tk.Label(self.maincanvas, text='夜间天气：', bg='white')
        self.nightweather_label.place(x=280, y=180, width=100, height=20)
        self.nightweather_entry = tk.Entry(self.maincanvas)
        self.nightweather_entry.place(x=380, y=180, width=100, height=20)
        self.nightweather_entry.insert(0, self.weather.nightweather)

        # 在画布中嵌入图片
        self.draw_tempreture(self.maincanvas, self.weather_get)

        # 在最底部显示上次更新时间
        self.last_update_label = tk.Label(self.maincanvas, text='上次更新: ')
        self.last_update_label.place(x=100, y=470, width=100, height=20)
        self.last_update_time_label = tk.Label(self.maincanvas, text=(self.last_update_time if self.last_update_time else '未更新'))
        self.last_update_time_label.place(x=200, y=470, width=200, height=20)

        # 选择的语言
        if self.language == 'chinese':
            self.chinese()
        else:
            self.english()

    # 根据当前选择的城市天气信息，画出温度变化图
    def draw_tempreture(self, tmp_canvas, weather_get):
        """
        draw the temperature change graph, and put it in the canvas
        """
        x_values = self.weather_get.datelist
        y1_values = []
        y2_values = []
        for x_value in x_values:
            y1_values.append(int(weather_get.get_weather(x_value).daytemperature))
            y2_values.append(int(weather_get.get_weather(x_value).nighttemperature))
        fig = Figure(figsize=(5,2), dpi=100)
        a = fig.add_subplot(111)
        a.plot(x_values, y1_values, label='day')
        a.plot(x_values, y2_values, label='night')

        # 在每个点上显示温度数值
        for i, txt in enumerate(y1_values):
            a.annotate(txt, (x_values[i], y1_values[i]))
        for i, txt in enumerate(y2_values):
            a.annotate(txt, (x_values[i], y2_values[i]))
        a.set_xlabel('date')
        a.set_ylabel('temperature/℃')
        a.set_axis_on()
        a.grid(True, axis='y')
        canvas = FigureCanvasTkAgg(fig, master=tmp_canvas)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().place(x=20, y=220, width=500, height=200)


    # 城市下拉框选择事件
    def city_combobox_selected(self, event):
        """
        the city combobox selected event, update the weather information according to the selected city
        """
        self.citysearch_entry.delete(0, tk.END) # 清空搜索框中的内容
        selected_date = self.date.get()  # 获取当前选择的日期
        city_name = self.city.get()  # 获取用户选择的新城市名
        # 使用天气 API 获取新的天气信息
        self.weather_get = WeatherGet(self.city_code[city_name]['adcode'])
        new_weather = self.weather_get.get_weather(selected_date)
        # 更新 GUI 显示的天气信息
        self.update_weather_info(new_weather)
    
    # 日期下拉框选择事件
    def date_combobox_selected(self, event):
        """
        the date combobox selected event, update the weather information according to the selected date
        """
        selected_date = self.date.get()  # 获取当前选择的日期
        new_weather = self.weather_get.get_weather(selected_date)
        # 更新 GUI 显示的天气信息
        self.update_weather_info(new_weather)

    # 更新 GUI 上的天气信息显示，根据传入的天气信息（例如温度、湿度等）
    def update_weather_info(self, weather_info):
        """
        the function is called to update the weather information
        """
        self.temperature_entry.delete(0, tk.END)  # 清空温度 Entry 中的内容
        self.temperature_entry.insert(0,  '{}~{}'.format(weather_info.nighttemperature, weather_info.daytemperature))  # 显示新的温度信息

        self.humidity_entry.delete(0, tk.END)  # 清空湿度 Entry 中的内容
        self.humidity_entry.insert(0, weather_info.humidity)  # 显示新的湿度信息

        self.wind_entry.delete(0, tk.END)  # 清空风力风向 Entry 中的内容
        self.wind_entry.insert(0, weather_info.wind)

        self.dayweather_entry.delete(0, tk.END)  # 清空白天天气 Entry 中的内容
        self.dayweather_entry.insert(0, weather_info.dayweather)

        self.nightweather_entry.delete(0, tk.END)  # 清空夜间天气 Entry 中的内容
        self.nightweather_entry.insert(0, weather_info.nightweather)

        self.week_entry.delete(0, tk.END)  # 清空星期 Entry 中的内容
        self.week_entry.insert(0, weather_info.week)

        self.draw_tempreture(self.maincanvas, self.weather_get)

        # 更新上次更新的时间
        self.last_update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.last_update_time_label.config(text = self.last_update_time)

    # 搜索框输入事件
    def search(self,event):
        """
        the search event, update the search result listbox according to the input
        """
        # 获取输入框的内容
        content = self.citysearch_entry.get()
        # 在城市代码中搜索可能的城市
        possible_cities = [city for city in self.city_code.keys() if content in city]
        # 更新搜索结果标签
        self.search_results_listbox.delete(0, tk.END)
        for city in possible_cities:
            self.search_results_listbox.insert(tk.END, city)
    
    # 搜索结果列表框点击事件
    def on_select(self,event):
        """
        if the user select the city in the search result listbox, the city name will be filled in the search entry
        """
        selected_city = self.search_results_listbox.get(self.search_results_listbox.curselection())
        # 将选中的城市填充到输入框中
        self.citysearch_entry.delete(0, tk.END)
        self.citysearch_entry.insert(0, selected_city)

    # 搜索按钮点击事件
    def citysearch_button_clicked(self):
        """
        the search button clicked event, update the weather information according to the input
        """
        self.search_results_listbox.delete(0, tk.END)
        city_name = self.citysearch_entry.get()
        if city_name in self.city_code.keys():
            self.city.set(city_name)
            self.city_combobox['values'] = list(self.city_code.keys())
            self.city_combobox.current(list(self.city_code.keys()).index(city_name))
            self.weather_get = WeatherGet(self.city_code[city_name]['adcode'])
            new_weather = self.weather_get.get_weather(self.date.get())
            self.update_weather_info(new_weather)
        else:
            messagebox.showinfo('错误', '无法获取天气信息')

    # NOTE: the following functions are used for the international weather window
    def international(self):
        """
        show the window of the international weather information
        """
        self.maincanvas.pack_forget() 
        self.myfavcanvas.pack_forget() 
        self.secondcanvas.pack()
        self.secondcanvas.update()

        # 国家名称
        self.country_label = tk.Label(self.secondcanvas, text='国家：', bg='white')
        self.country_label.place(x=20, y=20, width=100, height=20)
        self.country_combobox = ttk.Combobox(self.secondcanvas, textvariable=self.country, state='readonly')
        self.country_combobox['values'] = list(self.countryfullnames.keys())
        self.country_combobox.place(x=120, y=20, width=150, height=20)
        self.country_combobox.bind('<<ComboboxSelected>>', self.country_combobox_selected)
        # 国家对应的城市名称
        self.international_city_label = tk.Label(self.secondcanvas, text='城市：', bg='white')
        self.international_city_label.place(x=280, y=20, width=100, height=20)
        self.international_city_combobox = ttk.Combobox(self.secondcanvas, textvariable=self.country2city, state='readonly')
        self.international_city_combobox['values'] = list(national_citys(self.international_countrys, self.countryfullnames[self.country.get()])) # 根据选定的城市列表更新城市下拉框
        self.international_city_combobox.place(x=380, y=20, width=100, height=20)
        self.international_city_combobox.bind('<<ComboboxSelected>>', self.international_city_combobox_selected)

        self.international_date_label = tk.Label(self.secondcanvas, text='日期：', bg='white')
        self.international_date_label.place(x=20, y=60, width=100, height=20)
        self.international_date_combobox = ttk.Combobox(self.secondcanvas, textvariable=self.international_time, state='readonly')
        self.international_date_combobox['values'] = list(self.globalweather_get.timelist)
        self.international_date_combobox.place(x=120, y=60, width=150, height=20)
        self.international_date_combobox.bind('<<ComboboxSelected>>', self.international_time_combobox_selected)
        # 温度
        self.international_temperature_label = tk.Label(self.secondcanvas, text='温度：', bg='white')
        self.international_temperature_label.place(x=20, y=100, width=100, height=20)
        self.international_temperature_entry = tk.Entry(self.secondcanvas)
        self.international_temperature_entry.place(x=120, y=100, width=100, height=20)
        self.international_temperature_entry.insert(0,  '{}~{}'.format(self.globalweather.temp_min, self.globalweather.temp_max))
        # 体感温度
        self.international_feels_like_label = tk.Label(self.secondcanvas, text='体感温度：', bg='white')
        self.international_feels_like_label.place(x=280, y=100, width=100, height=20)
        self.international_feels_like_entry = tk.Entry(self.secondcanvas)
        self.international_feels_like_entry.place(x=380, y=100, width=100, height=20)
        self.international_feels_like_entry.insert(0, self.globalweather.feels_like)
        # 压强
        self.international_pressure_label = tk.Label(self.secondcanvas, text='压强：', bg='white')
        self.international_pressure_label.place(x=20, y=140, width=100, height=20)
        self.international_pressure_entry = tk.Entry(self.secondcanvas)
        self.international_pressure_entry.place(x=120, y=140, width=100, height=20)
        self.international_pressure_entry.insert(0, self.globalweather.pressure)
        # 湿度
        self.international_humidity_label = tk.Label(self.secondcanvas, text='湿度：', bg='white')
        self.international_humidity_label.place(x=280, y=140, width=100, height=20)
        self.international_humidity_entry = tk.Entry(self.secondcanvas)
        self.international_humidity_entry.place(x=380, y=140, width=100, height=20)
        self.international_humidity_entry.insert(0, self.globalweather.humidity)
        # 天气描述
        self.international_description_label = tk.Label(self.secondcanvas, text='天气描述：', bg='white')
        self.international_description_label.place(x=20, y=180, width=100, height=20)
        self.international_description_entry = tk.Entry(self.secondcanvas)
        self.international_description_entry.place(x=120, y=180, width=100, height=20)
        self.international_description_entry.insert(0, self.globalweather.description)
        # 风向
        self.international_wind_label = tk.Label(self.secondcanvas, text='风向：', bg='white')
        self.international_wind_label.place(x=280, y=180, width=100, height=20)
        self.international_wind_entry = tk.Entry(self.secondcanvas)
        self.international_wind_entry.place(x=380, y=180, width=150, height=20)
        self.international_wind_entry.insert(0, self.globalweather.wind)
        # 在画布中嵌入图片
        self.draw_international_tempreture(self.secondcanvas, self.globalweather_get)

        self.last_update_label = tk.Label(self.secondcanvas, text='上次更新: ' + (self.last_update_time if self.last_update_time else '未更新'))
        self.last_update_label.place(x=100, y=470, width=100, height=20)
        self.last_update_time_label = tk.Label(self.secondcanvas, text=(self.last_update_time if self.last_update_time else '未更新'))
        self.last_update_time_label.place(x=200, y=470, width=200, height=20)

        # 选择的语言
        if self.language == 'chinese':
            self.chinese()
        else:
            self.english()

    def country_combobox_selected(self, event): 
        """
        the country combobox selected event, update the international city combobox according to the selected country
        """
        self.international_city_combobox['values'] = list(national_citys(self.international_countrys, self.countryfullnames[self.country.get()])) # 根据选定的城市列表更新城市下拉框
        self.country2city.set(list(national_citys(self.international_countrys, self.countryfullnames[self.country.get()]))[0])
        self.citylat, self.citylon = citys_lat_lon(self.international_countrys, self.countryfullnames[self.country.get()], self.country2city.get())
        self.globalweather_get = GlobalWeatherGet(self.citylat, self.citylon)
        self.globalweather = self.globalweather_get.get_weather(self.international_time.get())
        self.international_weather_update()
        self.draw_international_tempreture(self.secondcanvas, self.globalweather_get)

    def international_city_combobox_selected(self, event):
        """
        the international city combobox selected event, update the weather information according to the selected international city
        """
        self.citylat, self.citylon = citys_lat_lon(self.international_countrys, self.countryfullnames[self.country.get()], self.country2city.get())
        self.globalweather_get = GlobalWeatherGet(self.citylat, self.citylon)
        self.globalweather = self.globalweather_get.get_weather(self.international_time.get())
        self.international_weather_update()
        self.draw_international_tempreture(self.secondcanvas, self.globalweather_get)
    
    def international_time_combobox_selected(self, event):
        """
        the international time combobox selected event, update the weather information according to the selected international time 
        """
        selected_time = self.international_time.get()
        self.globalweather = self.globalweather_get.get_weather(selected_time)
        self.international_weather_update()

    def international_weather_update(self):
        """
        the function is called to update the international weather information
        """
        self.international_temperature_entry.delete(0, tk.END)  # 清空温度 Entry 中的内容
        self.international_temperature_entry.insert(0,  '{}~{}'.format(self.globalweather.temp_min, self.globalweather.temp_max))  # 显示新的温度信息

        self.international_feels_like_entry.delete(0, tk.END)  # 清空体感温度 Entry 中的内容
        self.international_feels_like_entry.insert(0, self.globalweather.feels_like)  # 显示新的体感温度信息

        self.international_pressure_entry.delete(0, tk.END)  # 清空压强 Entry 中的内容
        self.international_pressure_entry.insert(0, self.globalweather.pressure)  # 显示新的压强信息

        self.international_humidity_entry.delete(0, tk.END)  # 清空湿度 Entry 中的内容
        self.international_humidity_entry.insert(0, self.globalweather.humidity)  # 显示新的湿度信息

        self.international_description_entry.delete(0, tk.END)  # 清空天气描述 Entry 中的内容
        self.international_description_entry.insert(0, self.globalweather.description)  # 显示新的天气描述信息

        self.international_wind_entry.delete(0, tk.END)  # 清空风向 Entry 中的内容
        self.international_wind_entry.insert(0, self.globalweather.wind)  # 显示新的风向信息

        # 更新上次更新的时间
        self.last_update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.last_update_time_label.config(text = self.last_update_time)

    # 根据当前选择的城市天气信息，画出温度变化图
    def draw_international_tempreture(self, tmp_canvas, globalweather_get):
        """
        draw the international temperature change graph, and put it in the canvas
        """
        x_values = list(globalweather_get.timelist)
        y1_values = []
        # y2_values = []
        for x_value in x_values:
            y1_values.append(globalweather_get.get_weather(x_value).temp_max)
            # y2_values.append(globalweather_get.get_weather(x_value).temp_min)
        fig = Figure(figsize=(35,2), dpi=100)
        a = fig.add_subplot(111)
        # 只显示x_values的形式是2023-12-1 18:00:00，只留下12:1 18
        x_values = [x_value[8:10] + '/' + x_value[11:13]+'' for x_value in x_values]
        a.plot(x_values, y1_values, label='time')
        # a.plot(x_values, y2_values, label='night')

        # 在每个点上显示温度数值
        for i, txt in enumerate(y1_values):
            a.annotate(txt, (x_values[i], y1_values[i]))
        # for i, txt in enumerate(y2_values):
        #     a.annotate(txt, (x_values[i], y2_values[i]))
        a.set_xlabel('date')
        a.set_ylabel('temperature/℃')
        a.set_axis_on()
        a.grid(True, axis='y')
        # 创建一个可滚动的画布
        scroll_canvas = Canvas(tmp_canvas)
        scroll_canvas.place(x=20, y=220, width=500, height=200)

        # 创建一个滚动条
        scrollbar = Scrollbar(tmp_canvas, orient="horizontal", command=scroll_canvas.xview, width = 30)
        scrollbar.place(x=20, y=430, width=500, height=20)
        #scrollbar.pack(side="bottom", fill="x")

        # 将滚动条连接到画布
        scroll_canvas.configure(xscrollcommand=scrollbar.set)

        # 创建一个Frame，将其添加到画布中
        frame = Frame(scroll_canvas)
        scroll_canvas.create_window((500,200), window=frame, anchor='center')
        # 将FigureCanvasTkAgg添加到Frame中
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", fill="both", expand=True) # 将画布填充到Frame中

        # 更新画布的滚动区域
        frame.update_idletasks()
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox('all'))

    # NOTE: the following functions are used for the favorite weather window
    # 查看收藏
    def show_favorite(self):
        """
        show the window of the favorite weather information
        """
        if len(self.my_favorite_city.get_favor_cityls()) == 0:
            messagebox.showinfo('提示', '收藏夹为空')
        else:  
            self.maincanvas.pack_forget()
            self.secondcanvas.pack_forget()
            self.myfavcanvas.pack()
            self.myfavcanvas.update() # 刷新窗口
            self.cityinlist = self.my_favorite_city.get_favor_cityls()
            self.my_fav_city = tk.StringVar()  # 用来存储用户选择的城市名
            self.my_fav_city.set(self.cityinlist[0])
            self.fav_city_label = tk.Label(self.myfavcanvas, text='城市：', bg='white')
            self.fav_city_label.place(x=20, y=20, width=50, height=20)
            self.fav_city_combobox = ttk.Combobox(self.myfavcanvas, textvariable= self.my_fav_city, state='readonly')
            self.fav_city_combobox['values'] =  self.cityinlist
            self.fav_city_combobox.place(x=80, y=20, width=100, height=20)
            self.win1_delete_button = tk.Button(self.myfavcanvas, text='删除', command=self.delete_favorite)
            self.win1_delete_button.place(x=200, y=20, width=40, height=20)
            self.fav_city_combobox_selected(0)
            self.fav_city_combobox.bind('<<ComboboxSelected>>', self.fav_city_combobox_selected)
    
    # 添加到收藏
    def add_favorite(self):
        """
        add the city to the favorite city list
        """
        #如果当前页面是self.maincanvas，则添加到收藏
        if self.maincanvas.winfo_ismapped():
            cityinfo = {}
            cityinfo['class'] = self.weather.__class__.__name__
            cityinfo['cityname'] = self.city.get()
            cityinfo['code'] = self.city_code[self.city.get()]['adcode']
            self.my_favorite_city.add(cityinfo)
            messagebox.showinfo('提示', '添加成功')
        # 如果当前页面是self.secondcanvas，将国际类的天气信息添加到收藏
        elif self.secondcanvas.winfo_ismapped():
            self.citylat, self.citylon = citys_lat_lon(self.international_countrys, self.countryfullnames[self.country.get()], self.country2city.get())
            cityinfo = {}
            cityinfo['class'] = self.globalweather.__class__.__name__
            cityinfo['cityname'] = self.country2city.get()
            cityinfo['lat'] = self.citylat
            cityinfo['lon'] = self.citylon
            self.my_favorite_city.add(cityinfo)
            messagebox.showinfo('提示', '添加成功')
        else:
            messagebox.showinfo('提示', '当前页面天气页面，无法添加')

    # 从收藏中删除
    def delete_favorite(self):
        """
        delete the city from the favorite city list
        """
        self.my_favorite_city.delete(self.fav_city_combobox.get())
        # 如果收藏夹空的，则关掉my_favorite_window窗口
        if len(self.my_favorite_city.get_favor_cityls()) == 0:
            self.myfavcanvas.pack_forget()
            self.maincanvas.pack()
            messagebox.showinfo('提示', '删除成功')
        else: 
            # 删除后清空 self.win1_city_combobox
            self.my_fav_city.set(list(self.my_favorite_city.get_favor_cityls())[0])
            # 重新加载收藏夹中的城市
            self.fav_city_combobox['values'] = list(self.my_favorite_city.get_favor_cityls())
            self.fav_city_combobox_selected(0)


    # 收藏界面城市下拉框选择事件
    def fav_city_combobox_selected(self,event):
        """
        the favorite city combobox selected event, update the weather information according to the selected favorite city
        """
        # 清空页面上的信息, y = 60及以上的信息保留
        for widget in self.myfavcanvas.winfo_children():
            if widget.winfo_y() > 50:
                widget.destroy()
        # print(self.fav_city_combobox.get())
        # 如果选择的城市是国内类的天气信息
        if self.my_favorite_city.get_classofcity(self.my_fav_city.get()) == 'Weather':
            # 获取城市代码
            citycode = self.my_favorite_city.get_city_codes(self.my_fav_city.get())
            # 获取天气信息
            weatherget = WeatherGet(citycode)
            weather = weatherget.get_weather()
            # 将当天温度信息用大字显示在x = 20，y = 60的位置
            self.win1_temperature_label0 = tk.Label(self.myfavcanvas, text='温度',bg='white')
            self.win1_temperature_label0['font'] = tkFont.Font(size=15)
            self.win1_temperature_label0.place(x=10, y=60, width=120, height=30)
            self.win1_temperature = tk.Label(self.myfavcanvas,text='{}'.format(weather.daytemperature),bg='white')
            self.win1_temperature['font'] = tkFont.Font(size=100)
            self.win1_temperature.place(x=20, y=90, width=100, height=115)
            # 在x = 140处画一条黑线，分割左右
            self.win1_line = tk.Label(self.myfavcanvas, text=' ',bg='black')
            self.win1_line.place(x=140, y=60, width=1, height=145)
            # 将天气信息用label的形式显示在x = 140，y = 60的位置
            self.win1_week_label = tk.Label(self.myfavcanvas, text='星期：', bg='white',anchor='w')
            self.win1_week_label['font'] = tkFont.Font(size=15)
            self.win1_week_label.place(x=180, y=60, width=100, height=25)
            self.win1_week = tk.Label(self.myfavcanvas,text='{}'.format(weather.week),bg='white')
            self.win1_week['font'] = tkFont.Font(size=20)
            self.win1_week.place(x=280, y=60, width=300, height=25)
            # 温度信息
            self.win1_temperature_label = tk.Label(self.myfavcanvas, text='温度：', anchor='w',bg='white')
            self.win1_temperature_label['font'] = tkFont.Font(size=15)
            self.win1_temperature_label.place(x=180, y=90, width=100, height=25)
            self.win1_temperature = tk.Label(self.myfavcanvas,text='H: '+ weather.daytemperature+'℃'+' L: '+ weather.nighttemperature+'℃',bg='white')
            self.win1_temperature['font'] = tkFont.Font(size=20)
            self.win1_temperature.place(x=280, y=90, width=300, height=25)
            # 湿度信息
            self.win1_humidity_label = tk.Label(self.myfavcanvas, text='湿度：'+ weather.humidity, anchor='w',bg='white')
            self.win1_humidity_label['font'] = tkFont.Font(size=15)
            self.win1_humidity_label.place(x=180, y=120, width=100, height=25)
            self.win1_humidity = tk.Label(self.myfavcanvas,text='{}'.format(weather.humidity),bg='white')
            self.win1_humidity['font'] = tkFont.Font(size=20)
            self.win1_humidity.place(x=280, y=120, width=300, height=25)
            # 风力风向信息 
            self.win1_wind_label = tk.Label(self.myfavcanvas, text='风向：', anchor='w',bg='white')
            self.win1_wind_label['font'] = tkFont.Font(size=15)
            self.win1_wind_label.place(x=180, y=150, width=100, height=25)
            self.win1_wind = tk.Label(self.myfavcanvas,text='{}'.format(weather.wind),bg='white')
            self.win1_wind['font'] = tkFont.Font(size=20)
            self.win1_wind.place(x=280, y=150, width=300, height=25)
            # 白天天气信息
            self.win1_dayweather_label = tk.Label(self.myfavcanvas, text='天气：', anchor='w',bg='white')
            self.win1_dayweather_label['font'] = tkFont.Font(size=15)
            self.win1_dayweather_label.place(x=180, y=180, width=100, height=25)
            self.win1_dayweather = tk.Label(self.myfavcanvas,text='{}'.format(weather.dayweather),bg='white')
            self.win1_dayweather['font'] = tkFont.Font(size=20)
            self.win1_dayweather.place(x=280, y=180, width=300, height=25)
            # 画气温变化图
            self.draw_tempreture(self.myfavcanvas, weatherget)

        # 如果选择的城市是国际类的天气信息
        elif self.my_favorite_city.get_classofcity(self.my_fav_city.get()) == 'GlobalWeather':
            # 获取城市代码
            citylat, citylon = self.my_favorite_city.get_city_latlon(self.my_fav_city.get())
            # 获取天气信息
            weatherget = GlobalWeatherGet(citylat, citylon)
            weather = weatherget.get_weather()
            # 将当天温度信息用大字显示在x = 20，y = 60的位置
            self.win1_temperature_label0 = tk.Label(self.myfavcanvas, text='温度',bg='white')
            self.win1_temperature_label0['font'] = tkFont.Font(size=20)
            self.win1_temperature_label0.place(x=20, y=60, width=160, height=25)
            self.win1_temperature = tk.Label(self.myfavcanvas,text='{}'.format(weather.temp_max),bg='white')
            self.win1_temperature['font'] = tkFont.Font(size=50)
            self.win1_temperature.place(x=20, y=90, width=160, height=115)
            # 在x = 140处画一条黑线，分割左右
            self.win1_line = tk.Label(self.myfavcanvas, text='‘',bg='black')
            self.win1_line.place(x=200, y=60, width=1, height=145)
            # 将天气信息用label的形式显示在x = 140，y = 60的位置
            self.win1_date_label = tk.Label(self.myfavcanvas, text='日期：', anchor='w',bg='white')
            self.win1_date_label['font'] = tkFont.Font(size=15)
            self.win1_date_label.place(x=220, y=60, width=100, height=20)
            self.win1_date = tk.Label(self.myfavcanvas,text='{}'.format(weather.time),bg='white')
            self.win1_date['font'] = tkFont.Font(size=15)
            self.win1_date.place(x=320, y=60, width=280, height=20)
            # 温度信息
            self.win1_temperature_label = tk.Label(self.myfavcanvas, text='温度：', anchor='w',bg='white')
            self.win1_temperature_label['font'] = tkFont.Font(size=10)
            self.win1_temperature_label.place(x=220, y=80, width=100, height=20)
            self.win1_temperature = tk.Label(self.myfavcanvas,text=str(weather.temp_min)+'℃'+'~'+ str(weather.temp_max)+'℃',bg='white')
            self.win1_temperature['font'] = tkFont.Font(size=15)
            self.win1_temperature.place(x=320, y=80, width=280, height=20)
            # 体感温度信息
            self.win1_feels_like_label = tk.Label(self.myfavcanvas, text='体感温度：', anchor='w',bg='white')
            self.win1_feels_like_label['font'] = tkFont.Font(size=10)
            self.win1_feels_like_label.place(x=220, y=100, width=100, height=20)
            self.win1_feels_like = tk.Label(self.myfavcanvas,text=str(weather.feels_like)+'℃',bg='white')
            self.win1_feels_like['font'] = tkFont.Font(size=15)
            self.win1_feels_like.place(x=320, y=100, width=280, height=20)
            # 压强信息
            self.win1_pressure_label = tk.Label(self.myfavcanvas, text='压强：', anchor='w',bg='white')
            self.win1_pressure_label['font'] = tkFont.Font(size=15)
            self.win1_pressure_label.place(x=220, y=120, width=100, height=20)
            self.win1_pressure = tk.Label(self.myfavcanvas,text=str(weather.pressure),bg='white')
            self.win1_pressure['font'] = tkFont.Font(size=15)
            self.win1_pressure.place(x=320, y=120, width=280, height=20)
            # 湿度信息
            self.win1_humidity_label = tk.Label(self.myfavcanvas, text='湿度：', anchor='w',bg='white')
            self.win1_humidity_label['font'] = tkFont.Font(size=15)
            self.win1_humidity_label.place(x=220, y=140, width=100, height=20)
            self.win1_humidity = tk.Label(self.myfavcanvas,text=str(weather.humidity),bg='white')
            self.win1_humidity['font'] = tkFont.Font(size=15)
            self.win1_humidity.place(x=320, y=140, width=280, height=20)
            # 天气描述信息
            self.win1_description_label = tk.Label(self.myfavcanvas, text='天气：', anchor='w',bg='white')
            self.win1_description_label['font'] = tkFont.Font(size=10)
            self.win1_description_label.place(x=220, y=160, width=100, height=20)
            self.win1_description = tk.Label(self.myfavcanvas,text='{}'.format(weather.description),bg='white')
            self.win1_description['font'] = tkFont.Font(size=15)
            self.win1_description.place(x=320, y=160, width=280, height=20)
            # 风向信息
            self.win1_wind_label = tk.Label(self.myfavcanvas, text='风向：', anchor='w',bg='white')
            self.win1_wind_label['font'] = tkFont.Font(size=15)
            self.win1_wind_label.place(x=220, y=180, width=100, height=20)
            self.win1_wind = tk.Label(self.myfavcanvas,text='{}'.format(weather.wind),bg='white')
            self.win1_wind['font'] = tkFont.Font(size=15)
            self.win1_wind.place(x=320, y=180, width=280, height=20)
            # 画气温变化图
            self.draw_international_tempreture(self.myfavcanvas, weatherget)
        else:
            messagebox.showinfo('提示', '无法获取天气信息')

        # 选择的语言
        if self.language == 'chinese':
            self.chinese()
        else:
            self.english()

    # NOTE: the following functions are used for the language selection
    def chinese(self):
        """
        the chinese language option
        """
        # 全局变量用于存储语言选项
        self.language = 'chinese'
        # 菜单栏
        self.favorite_menu.entryconfigure(0, label='添加至收藏')
        self.favorite_menu.entryconfigure(1, label='从收藏中删除')
        self.favorite_menu.entryconfigure(2, label='查看收藏')
        self.favorite_language.entryconfigure(0, label='中文')
        self.favorite_language.entryconfigure(1, label='English')

        if self.maincanvas.winfo_ismapped():
            self.city_label['text'] = '城市：'
            self.date_label['text'] = '日期：'
            self.week_label['text'] = '星期：'
            self.temperature_label['text'] = '温度：'
            self.humidity_label['text'] = '湿度：'
            self.wind_label['text'] = '风力风向：'
            self.dayweather_label['text'] = '白天天气：'
            self.nightweather_label['text'] = '夜间天气：'
            self.citysearch_label['text'] = '城市搜索：'
            self.citysearch_button['text'] = '搜索'
            self.last_update_label['text'] = '上次更新: '
        # 国际类天气界面
        elif self.secondcanvas.winfo_ismapped():
            self.country_label['text'] = '国家：'
            self.international_city_label['text'] = '城市：'
            self.international_date_label['text'] = '日期：'
            self.international_temperature_label['text'] = '温度：'
            self.international_feels_like_label['text'] = '体感温度：'
            self.international_pressure_label['text'] = '压强：'
            self.international_humidity_label['text'] = '湿度：'
            self.international_description_label['text'] = '天气描述：'
            self.international_wind_label['text'] = '风向：'
            self.last_update_label['text'] = '上次更新: '
        # 收藏界面
        elif self.myfavcanvas.winfo_ismapped():
            self.fav_city_label['text'] = '城市：'
            self.win1_delete_button['text'] = '删除'
            if self.my_favorite_city.get_classofcity(self.my_fav_city.get()) == 'Weather':  
                self.win1_temperature_label0['text'] = '温度'
                self.win1_week_label['text'] = '星期：'
                self.win1_temperature_label['text'] = '温度：'
                self.win1_humidity_label['text'] = '湿度：'
                self.win1_wind_label['text'] = '风向：'
                self.win1_dayweather_label['text'] = '天气：'
            elif self.my_favorite_city.get_classofcity(self.my_fav_city.get()) == 'GlobalWeather':
                self.win1_temperature_label0['text'] = '温度'
                self.win1_date_label['text'] = '日期：'
                self.win1_temperature_label['text'] = '温度：'
                self.win1_feels_like_label['text'] = '体感温度：'
                self.win1_pressure_label['text'] = '压强：'
                self.win1_humidity_label['text'] = '湿度：'
                self.win1_description_label['text'] = '天气描述：'
                self.win1_wind_label['text'] = '风向：'

    
    def english(self):
        """
        the english language option
        """
        # 全局变量用于存储语言选项
        self.language = 'english'
        self.favorite_menu.entryconfigure(0, label='Add to favorite')
        self.favorite_menu.entryconfigure(1, label='Delete from favorite')
        self.favorite_menu.entryconfigure(2, label='Show favorite')
        self.favorite_language.entryconfigure(0, label='中文')
        self.favorite_language.entryconfigure(1, label='English')
        self.na_interna.entryconfigure(0, label='National')
        self.na_interna.entryconfigure(1, label='International')
        # 国内类天气界面
        if self.maincanvas.winfo_ismapped():
            self.city_label['text'] = 'City：'
            self.date_label['text'] = 'Date：'
            self.week_label['text'] = 'Week：'
            self.temperature_label['text'] = 'Temperature：'
            self.humidity_label['text'] = 'Humidity：'
            self.wind_label['text'] = 'Wind：'
            self.dayweather_label['text'] = 'DayWeather：'
            self.nightweather_label['text'] = 'NightWeather：'
            self.citysearch_label['text'] = 'CitySearch：'
            self.citysearch_button['text'] = 'Search'
            self.last_update_label['text'] = 'Last Update: '
        # 国际类天气界面
        elif self.secondcanvas.winfo_ismapped():
            self.country_label['text'] = 'Country：'
            self.international_city_label['text'] = 'City：'
            self.international_date_label['text'] = 'Date：'
            self.international_temperature_label['text'] = 'Temperature：'
            self.international_feels_like_label['text'] = 'Feels Like：'
            self.international_pressure_label['text'] = 'Pressure：'
            self.international_humidity_label['text'] = 'Humidity：'
            self.international_description_label['text'] = 'Description：'
            self.international_wind_label['text'] = 'Wind：'
            self.last_update_label['text'] = 'Last Update: '
        # 收藏界面
        elif self.myfavcanvas.winfo_ismapped():
            self.fav_city_label['text'] = 'City：'
            self.win1_delete_button['text'] = 'Delete'
            if self.my_favorite_city.get_classofcity(self.my_fav_city.get()) == 'Weather':
                self.win1_temperature_label0['text'] = 'Temperature'
                self.win1_week_label['text'] = 'Week：'
                self.win1_temperature_label['text'] = 'Temperature：'
                self.win1_humidity_label['text'] = 'Humidity：'
                self.win1_wind_label['text'] = 'Wind：'
                self.win1_dayweather_label['text'] = 'DayWeather：'
            elif self.my_favorite_city.get_classofcity(self.my_fav_city.get()) == 'GlobalWeather':
                self.win1_temperature_label0['text'] = 'Temperature'
                self.win1_date_label['text'] = 'Date：'
                self.win1_temperature_label['text'] = 'Temperature：'
                self.win1_feels_like_label['text'] = 'Feels Like：'
                self.win1_pressure_label['text'] = 'Pressure：'
                self.win1_humidity_label['text'] = 'Humidity：'
                self.win1_description_label['text'] = 'Description：'
                self.win1_wind_label['text'] = 'Wind：'