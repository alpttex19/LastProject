import tkinter as tk
from tkinter import ttk
import datetime
from tkinter import messagebox
from Weather import WeatherGet, MyFavoriteCity

# GUI界面
class WeatherGUI:
    # 初始化
    def __init__(self,city_code_data):
        self.root = tk.Tk()
        self.root.title('天气预报')
        self.root.geometry('500x400')
        self.root.resizable(False, False)
        self.root.update()
        self.city_code = city_code_data
        self.city = tk.StringVar()  # 用来存储用户选择的城市名
        self.city.set('北京市')
        self.date = tk.StringVar()
        self.date.set(datetime.datetime.now().strftime('%Y-%m-%d'))
        self.weather_get = WeatherGet(self.city_code[self.city.get()]['adcode'])
        self.weather = self.weather_get.get_weather(self.city.get(), self.date.get())
        self.my_favorite_city = MyFavoriteCity()
        self.create_widgets()  # 创建控件
        self.root.mainloop()  # 进入主循环

    def create_widgets(self):
        # 城市名称
        self.city_label = tk.Label(self.root, text='城市：')
        self.city_label.place(x=20, y=20, width=50, height=20)
        self.city_combobox = ttk.Combobox(self.root, textvariable=self.city, state='readonly')
        self.city_combobox['values'] = list(self.city_code.keys())
        self.city_combobox.place(x=80, y=20, width=100, height=20)
        self.city_combobox.bind('<<ComboboxSelected>>', self.city_combobox_selected)

        self.date_label = tk.Label(self.root, text='日期：')
        self.date_label.place(x=260, y=20, width=50, height=20)
        self.date_combobox = ttk.Combobox(self.root, textvariable=self.date, state='readonly')
        self.date_combobox['values'] = [datetime.datetime.now().strftime('%Y-%m-%d'), 
                                        (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'), 
                                        (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d'),
                                        (datetime.datetime.now() + datetime.timedelta(days=3)).strftime('%Y-%m-%d'),]
        self.date_combobox.place(x=320, y=20, width=100, height=20)
        self.date_combobox.bind('<<ComboboxSelected>>', self.date_combobox_selected)

        # 星期、温度、湿度、风力风向、白天天气、夜间天气
        self.week_label = tk.Label(self.root, text='星期：')
        self.week_label.place(x=20, y=60, width=50, height=20)
        self.week_entry = tk.Entry(self.root)
        self.week_entry.place(x=80, y=60, width=100, height=20)
        self.week_entry.insert(0, self.weather.week)

        self.temperature_label = tk.Label(self.root, text='温度：')
        self.temperature_label.place(x=260, y=60, width=50, height=20)
        self.temperature_entry = tk.Entry(self.root)
        self.temperature_entry.place(x=320, y=60, width=100, height=20)
        self.temperature_entry.insert(0, self.weather.temperature)  

        self.humidity_label = tk.Label(self.root, text='湿度：')
        self.humidity_label.place(x=20, y=100, width=50, height=20)
        self.humidity_entry = tk.Entry(self.root)
        self.humidity_entry.place(x=80, y=100, width=100, height=20)
        self.humidity_entry.insert(0, self.weather.humidity)

        self.wind_label = tk.Label(self.root, text='风力风向：')
        self.wind_label.place(x=260, y=100, width=60, height=20)
        self.wind_entry = tk.Entry(self.root)
        self.wind_entry.place(x=320, y=100, width=100, height=20)
        self.wind_entry.insert(0, self.weather.wind)

        self.dayweather_label = tk.Label(self.root, text='白天天气：')
        self.dayweather_label.place(x=20, y=140, width=60, height=20)
        self.dayweather_entry = tk.Entry(self.root)
        self.dayweather_entry.place(x=80, y=140, width=100, height=20)
        self.dayweather_entry.insert(0, self.weather.dayweather)

        self.nightweather_label = tk.Label(self.root, text='夜间天气：')
        self.nightweather_label.place(x=260, y=140, width=60, height=20)
        self.nightweather_entry = tk.Entry(self.root)
        self.nightweather_entry.place(x=320, y=140, width=100, height=20)
        self.nightweather_entry.insert(0, self.weather.nightweather)


        # select the city by inter city name
        self.citysearch_label = tk.Label(self.root, text='城市搜索：')
        self.citysearch_label.place(x=20, y=180, width=60, height=20)
        self.citysearch_entry = tk.Entry(self.root)
        self.citysearch_entry.place(x=80, y=180, width=120, height=20)
        self.citysearch_button = tk.Button(self.root, text='搜索', command=self.citysearch_button_clicked)
        self.citysearch_button.place(x=200, y=180, width=40, height=20)
        self.citysearch_entry.bind('<KeyRelease>', self.search)
        # 创建一个列表框来显示搜索结果
        self.search_results_listbox = tk.Listbox(self.root)
        self.search_results_listbox.place(x=80, y=200, width=120, height=40)
        self.search_results_listbox.bind('<<ListboxSelect>>', self.on_select)
        # 创建一个滚动条
        scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.search_results_listbox.yview)
        scrollbar.place(x=220, y=200, width=20, height=40)
        self.search_results_listbox['yscrollcommand'] = scrollbar.set

        # 菜单栏
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.favorite_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='我的收藏', menu=self.favorite_menu)
        self.favorite_menu.add_command(label='添加至收藏', command=self.add_favorite)
        self.favorite_menu.add_command(label='查看收藏', command=self.show_favorite)
        # 创建win1_city_combobox属性
        self.win1_city_combobox = ttk.Combobox()
        
        self.favorite_language = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label = '语言/language', menu = self.favorite_language)
        self.favorite_language.add_command(label='中文', command=self.chinese)
        self.favorite_language.add_command(label='English', command=self.english)


    # 城市下拉框选择事件
    def city_combobox_selected(self, event):
        self.citysearch_entry.delete(0, tk.END) # 清空搜索框中的内容
        selected_date = self.date.get()  # 获取当前选择的日期
        city_name = self.city.get()  # 获取用户选择的新城市名

        # 使用天气 API 获取新的天气信息
        self.weather_get = WeatherGet(self.city_code[city_name]['adcode'])
        new_weather = self.weather_get.get_weather(city_name, selected_date)

        # 更新 GUI 显示的天气信息
        self.update_weather_info(new_weather)

    # 日期下拉框选择事件
    def date_combobox_selected(self, event):
        selected_date = self.date.get()  # 获取当前选择的日期
        city_name = self.city.get()  # 获取用户选择的新城市名
        new_weather = self.weather_get.get_weather(city_name, selected_date)

        # 更新 GUI 显示的天气信息
        self.update_weather_info(new_weather)

    # 这个函数用来更新 GUI 上的天气信息显示，根据传入的天气信息（例如温度、湿度等）
    def update_weather_info(self, weather_info):
        self.temperature_entry.delete(0, tk.END)  # 清空温度 Entry 中的内容
        self.temperature_entry.insert(0, weather_info.temperature)  # 显示新的温度信息

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

    # 搜索框输入事件
    def search(self,event):
        # 获取输入框的内容
        content = self.citysearch_entry.get()
        # 在城市代码中搜索可能的城市
        possible_cities = [city for city in self.city_code.keys() if content in city]
        # 更新搜索结果标签
        #self.search_results_label['text'] = '\n'.join(possible_cities)
        self.search_results_listbox.delete(0, tk.END)
        for city in possible_cities:
            self.search_results_listbox.insert(tk.END, city)
    
    # 搜索结果列表框点击事件
    def on_select(self,event):
        selected_city = self.search_results_listbox.get(self.search_results_listbox.curselection())
        # 将选中的城市填充到输入框中
        self.citysearch_entry.delete(0, tk.END)
        self.citysearch_entry.insert(0, selected_city)

    # 搜索按钮点击事件
    def citysearch_button_clicked(self):
        self.search_results_listbox.delete(0, tk.END)
        city_name = self.citysearch_entry.get()
        if city_name in self.city_code.keys():
            self.city.set(city_name)
            self.city_combobox['values'] = list(self.city_code.keys())
            self.city_combobox.current(list(self.city_code.keys()).index(city_name))
            self.weather_get = WeatherGet(self.city_code[city_name]['adcode'])
            new_weather = self.weather_get.get_weather(city_name, self.date.get())
            self.update_weather_info(new_weather)
        else:
            messagebox.showinfo('错误', '无法获取天气信息')

    # 添加到收藏
    def add_favorite(self):
        self.cityweather = []
        for i in range(0,4):
            idate = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            self.weather = self.weather_get.get_weather(self.city.get(),idate)
            self.cityweather.append(self.weather)
        self.my_favorite_city.add_weather(self.city.get(), self.cityweather)
        messagebox.showinfo('提示', '添加成功')
        # 重新加载收藏夹中的城市
        self.win1_city_combobox['values'] = list(self.my_favorite_city.get_favor_cityls())

    # 从收藏中删除
    def delete_favorite(self):
        self.my_favorite_city.delete_weather(self.win1_city_combobox.get())
        # 如果收藏夹空的，则关掉my_favorite_window窗口
        if len(self.my_favorite_city.get_favor_cityls()) == 0:
            self.favorite_window.destroy()
            messagebox.showinfo('提示', '删除成功')
        else: 
            # 删除后清空 self.win1_city_combobox
            self.my_fav_city.set(list(self.my_favorite_city.get_favor_cityls())[0])
            # 重新加载收藏夹中的城市
            self.win1_city_combobox['values'] = list(self.my_favorite_city.get_favor_cityls())

    # 查看收藏
    def show_favorite(self):
        if len(self.my_favorite_city.get_favor_cityls()) == 0:
            messagebox.showinfo('提示', '收藏夹为空')
        else:  
            self.favorite_window = tk.Toplevel(self.root)
            self.favorite_window.title('我的收藏')
            self.favorite_window.geometry('500x400')
            self.favorite_window.resizable(False, False)
            self.favorite_window.update() # 刷新窗口
            self.create_favorite_widgets()
            self.favorite_window.mainloop() 
        

    # 创建收藏界面
    def create_favorite_widgets(self):
        # 城市名称
        self.cityinlist = list(self.my_favorite_city.get_favor_cityls())
        self.my_fav_city = tk.StringVar()  # 用来存储用户选择的城市名
        self.my_fav_city.set(list(self.cityinlist)[0])
        self.win1_city_label = tk.Label(self.favorite_window, text='城市：')
        self.win1_city_label.place(x=20, y=20, width=50, height=20)
        self.win1_city_combobox = ttk.Combobox(self.favorite_window, textvariable= self.my_fav_city, state='readonly')
        self.win1_city_combobox['values'] =  self.cityinlist
        self.win1_city_combobox.place(x=80, y=20, width=100, height=20)
        self.win1_city_combobox.bind('<<ComboboxSelected>>', self.win1_city_combobox_selected)

        self.win1_delete_button = tk.Button(self.favorite_window, text='删除', command=self.delete_favorite)
        self.win1_delete_button.place(x=200, y=20, width=40, height=20)
        
    # 收藏界面城市下拉框选择事件
    def win1_city_combobox_selected(self, event):
        self.fav_weath_info = self.my_favorite_city.get_weather(self.win1_city_combobox.get())
        xpos = 20
        ypos = 60
        for weather in self.fav_weath_info:
            self.win1_date_label = tk.Label(self.favorite_window, text='日期：'+ weather.date)
            self.win1_date_label.place(x=xpos, y=ypos, width=100, height=20)
            # 以label的形式显示天气信息
            self.win1_week_label = tk.Label(self.favorite_window, text='星期：'+ weather.week)
            self.win1_week_label.place(x=xpos, y=ypos+20, width=100, height=20)
            self.win1_temperature_label = tk.Label(self.favorite_window, text='温度：'+ weather.temperature)
            self.win1_temperature_label.place(x=xpos, y=ypos+40, width=100, height=20)
            self.win1_humidity_label = tk.Label(self.favorite_window, text='湿度：'+ weather.humidity)
            self.win1_humidity_label.place(x=xpos, y=ypos+60, width=100, height=20)
            self.win1_wind_label = tk.Label(self.favorite_window, text='风力风向：'+ weather.wind)
            self.win1_wind_label.place(x=xpos, y=ypos+80, width=100, height=20)
            self.win1_dayweather_label = tk.Label(self.favorite_window, text='白天天气：'+ weather.dayweather)
            self.win1_dayweather_label.place(x=xpos, y=ypos+100, width=100, height=20)
            self.win1_nightweather_label = tk.Label(self.favorite_window, text='夜间天气：'+ weather.nightweather)
            self.win1_nightweather_label.place(x=xpos, y=ypos+120, width=100, height=20)
            xpos += 120
            ypos = 60  



    
    def chinese(self):
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
        self.favorite_menu.entryconfigure(0, label='添加至收藏')
        self.favorite_menu.entryconfigure(1, label='从收藏中删除')
        self.favorite_menu.entryconfigure(2, label='查看收藏')
        self.favorite_language.entryconfigure(0, label='中文')
        self.favorite_language.entryconfigure(1, label='English')
    
    def english(self):
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
        self.favorite_menu.entryconfigure(0, label='Add to favorite')
        self.favorite_menu.entryconfigure(1, label='Delete from favorite')
        self.favorite_menu.entryconfigure(2, label='Show favorite')
        self.favorite_language.entryconfigure(0, label='中文')
        self.favorite_language.entryconfigure(1, label='English')
