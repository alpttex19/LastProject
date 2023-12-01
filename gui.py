import tkinter as tk
from tkinter import ttk
from tkinter import Canvas, Scrollbar, Frame
import datetime
from tkinter import messagebox
from Weather import WeatherGet, MyFavoriteCity, Weather, GlobalWeatherGet
from Readfiles import national_citys, citys_lat_lon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# GUI界面
class WeatherGUI:
    # 初始化
    def __init__(self,cn_citys, international_countrys, countryfullnames):
        self.root = tk.Tk()
        self.root.geometry('600x480')
        self.root.title('天气预报')
        self.maincanvas = tk.Canvas(self.root, width=600, height=480, bg='white')
        self.secondcanvas = tk.Canvas(self.root, width=600, height=480, bg='white')
        self.myfavcanvas = tk.Canvas(self.root, width=600, height=480, bg='white')
        self.city_code = cn_citys
        self.city = tk.StringVar()  # 用来存储用户选择的城市名
        self.city.set('北京市')
        self.date = tk.StringVar()
        self.date.set(datetime.datetime.now().strftime('%Y-%m-%d'))
        self.weather_get = WeatherGet(self.city_code[self.city.get()]['adcode'])
        self.weather = self.weather_get.get_weather(self.city.get(), self.date.get())

        self.international_countrys = international_countrys
        self.countryfullnames = countryfullnames
        self.country = tk.StringVar()  # 用来存储用户选择的国家名
        self.country.set('China')
        self.country2city = tk.StringVar()  # 用来存储用户选择的城市名
        self.country2city.set('Beijing')

        self.citylat, self.citylon = citys_lat_lon(self.international_countrys, self.countryfullnames[self.country.get()], self.country2city.get())
        self.globalweather_get = GlobalWeatherGet(self.citylat, self.citylon)
        self.international_time = tk.StringVar()
        self.international_time.set(self.globalweather_get.timelist[0])
        self.globweather = self.globalweather_get.get_weather(self.international_time.get())

        self.my_favorite_city = MyFavoriteCity()
        self.create_widgets()  # 创建控件
        self.root.mainloop()  # 进入主循环

    def create_widgets(self):
        # 默认窗口选择 国内
        self.national()
        # 菜单栏
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


    def national(self):
        self.secondcanvas.pack_forget()
        self.myfavcanvas.pack_forget()
        self.maincanvas.pack()
        self.maincanvas.update()
        # 城市名称
        self.city_label = tk.Label(self.maincanvas, text='城市：')
        self.city_label.place(x=20, y=20, width=50, height=20)
        self.city_combobox = ttk.Combobox(self.maincanvas, textvariable=self.city, state='readonly')
        self.city_combobox['values'] = list(self.city_code.keys())
        self.city_combobox.place(x=80, y=20, width=100, height=20)
        self.city_combobox.bind('<<ComboboxSelected>>', self.city_combobox_selected)

        # select the city by inter city name
        self.citysearch_label = tk.Label(self.maincanvas, text='城市搜索：')
        self.citysearch_label.place(x=320, y=20, width=60, height=20)
        self.citysearch_entry = tk.Entry(self.maincanvas)
        self.citysearch_entry.place(x=380, y=20, width=120, height=20)
        self.citysearch_button = tk.Button(self.maincanvas, text='搜索', command=self.citysearch_button_clicked)
        self.citysearch_button.place(x=500, y=20, width=40, height=20)
        self.citysearch_entry.bind('<KeyRelease>', self.search)
        # 创建一个列表框来显示搜索结果
        self.search_results_listbox = tk.Listbox(self.maincanvas)
        self.search_results_listbox.place(x=380, y=40, width=120, height=40)
        self.search_results_listbox.bind('<<ListboxSelect>>', self.on_select)
        # 创建一个滚动条
        scrollbar = ttk.Scrollbar(self.maincanvas, orient='vertical', command=self.search_results_listbox.yview)
        scrollbar.place(x=520, y=40, width=20, height=40)
        self.search_results_listbox['yscrollcommand'] = scrollbar.set

        self.date_label = tk.Label(self.maincanvas, text='日期：')
        self.date_label.place(x=20, y=60, width=50, height=20)
        self.date_combobox = ttk.Combobox(self.maincanvas, textvariable=self.date, state='readonly')
        self.date_combobox['values'] = [datetime.datetime.now().strftime('%Y-%m-%d'), 
                                        (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'), 
                                        (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d'),
                                        (datetime.datetime.now() + datetime.timedelta(days=3)).strftime('%Y-%m-%d'),]
        self.date_combobox.place(x=80, y=60, width=100, height=20)
        self.date_combobox.bind('<<ComboboxSelected>>', self.date_combobox_selected)

        # 星期、温度、湿度、风力风向、白天天气、夜间天气
        self.week_label = tk.Label(self.maincanvas, text='星期：')
        self.week_label.place(x=20, y=100, width=50, height=20)
        self.week_entry = tk.Entry(self.maincanvas)
        self.week_entry.place(x=80, y=100, width=100, height=20)
        self.week_entry.insert(0, self.weather.week)

        self.wind_label = tk.Label(self.maincanvas, text='风力风向：')
        self.wind_label.place(x=320, y=100, width=60, height=20)
        self.wind_entry = tk.Entry(self.maincanvas)
        self.wind_entry.place(x=380, y=100, width=100, height=20)
        self.wind_entry.insert(0, self.weather.wind)

        self.temperature_label = tk.Label(self.maincanvas, text='温度：')
        self.temperature_label.place(x=20, y=140, width=50, height=20)
        self.temperature_entry = tk.Entry(self.maincanvas)
        self.temperature_entry.place(x=80, y=140, width=100, height=20)
        self.temperature_entry.insert(0,  '{}~{}'.format(self.weather.nighttemperature, self.weather.daytemperature))  

        self.humidity_label = tk.Label(self.maincanvas, text='湿度：')
        self.humidity_label.place(x=320, y=140, width=50, height=20)
        self.humidity_entry = tk.Entry(self.maincanvas)
        self.humidity_entry.place(x=380, y=140, width=100, height=20)
        self.humidity_entry.insert(0, self.weather.humidity)

        self.dayweather_label = tk.Label(self.maincanvas, text='白天天气：')
        self.dayweather_label.place(x=20, y=180, width=60, height=20)
        self.dayweather_entry = tk.Entry(self.maincanvas)
        self.dayweather_entry.place(x=80, y=180, width=100, height=20)
        self.dayweather_entry.insert(0, self.weather.dayweather)

        self.nightweather_label = tk.Label(self.maincanvas, text='夜间天气：')
        self.nightweather_label.place(x=320, y=180, width=60, height=20)
        self.nightweather_entry = tk.Entry(self.maincanvas)
        self.nightweather_entry.place(x=380, y=180, width=100, height=20)
        self.nightweather_entry.insert(0, self.weather.nightweather)

        # 在画布中嵌入图片
        self.draw_tempreture()

    # 根据当前选择的城市天气信息，画出温度变化图
    def draw_tempreture(self):
        x_values = [datetime.datetime.now().strftime('%Y-%m-%d'), 
                        (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'), 
                        (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d'),
                        (datetime.datetime.now() + datetime.timedelta(days=3)).strftime('%Y-%m-%d'),]
        y1_values = []
        y2_values = []
        for x_value in x_values:
            y1_values.append(int(self.weather_get.get_weather(self.city.get(), x_value).daytemperature))
            y2_values.append(int(self.weather_get.get_weather(self.city.get(), x_value).nighttemperature))
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
        canvas = FigureCanvasTkAgg(fig, master=self.maincanvas)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().place(x=20, y=220, width=500, height=200)


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

        self.draw_tempreture()

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

    """
        名称：国际天气
        功能：显示国际天气
        参数：无
    """
    def international(self):
        self.maincanvas.pack_forget() 
        self.myfavcanvas.pack_forget() 
        self.secondcanvas.pack()
        self.secondcanvas.update()

        # 国家名称
        self.country_label = tk.Label(self.secondcanvas, text='国家：')
        self.country_label.place(x=20, y=20, width=50, height=20)
        self.country_combobox = ttk.Combobox(self.secondcanvas, textvariable=self.country, state='readonly')
        self.country_combobox['values'] = list(self.countryfullnames.keys())
        self.country_combobox.place(x=80, y=20, width=150, height=20)
        self.country_combobox.bind('<<ComboboxSelected>>', self.country_combobox_selected)
        # 国家对应的城市名称
        self.international_city_label = tk.Label(self.secondcanvas, text='城市：')
        self.international_city_label.place(x=320, y=20, width=50, height=20)
        self.international_city_combobox = ttk.Combobox(self.secondcanvas, textvariable=self.country2city, state='readonly')
        self.international_city_combobox['values'] = list(national_citys(self.international_countrys, self.countryfullnames[self.country.get()])) # 根据选定的城市列表更新城市下拉框
        self.international_city_combobox.place(x=380, y=20, width=100, height=20)
        self.international_city_combobox.bind('<<ComboboxSelected>>', self.international_city_combobox_selected)

        self.international_date_label = tk.Label(self.secondcanvas, text='日期：')
        self.international_date_label.place(x=20, y=60, width=50, height=20)
        self.international_date_combobox = ttk.Combobox(self.secondcanvas, textvariable=self.international_time, state='readonly')
        self.international_date_combobox['values'] = list(self.globalweather_get.timelist)
        self.international_date_combobox.place(x=80, y=60, width=150, height=20)
        self.international_date_combobox.bind('<<ComboboxSelected>>', self.international_time_combobox_selected)
        

        # 温度
        self.international_temperature_label = tk.Label(self.secondcanvas, text='温度：')
        self.international_temperature_label.place(x=20, y=100, width=50, height=20)
        self.international_temperature_entry = tk.Entry(self.secondcanvas)
        self.international_temperature_entry.place(x=80, y=100, width=100, height=20)
        self.international_temperature_entry.insert(0,  '{}~{}'.format(self.globweather.temp_min, self.globweather.temp_max))

        # 体感温度
        self.international_feels_like_label = tk.Label(self.secondcanvas, text='体感温度：')
        self.international_feels_like_label.place(x=320, y=100, width=60, height=20)
        self.international_feels_like_entry = tk.Entry(self.secondcanvas)
        self.international_feels_like_entry.place(x=380, y=100, width=100, height=20)
        self.international_feels_like_entry.insert(0, self.globweather.feels_like)

        # 压强
        self.international_pressure_label = tk.Label(self.secondcanvas, text='压强：')
        self.international_pressure_label.place(x=20, y=140, width=50, height=20)
        self.international_pressure_entry = tk.Entry(self.secondcanvas)
        self.international_pressure_entry.place(x=80, y=140, width=100, height=20)
        self.international_pressure_entry.insert(0, self.globweather.pressure)

        # 湿度
        self.international_humidity_label = tk.Label(self.secondcanvas, text='湿度：')
        self.international_humidity_label.place(x=320, y=140, width=50, height=20)
        self.international_humidity_entry = tk.Entry(self.secondcanvas)
        self.international_humidity_entry.place(x=380, y=140, width=100, height=20)
        self.international_humidity_entry.insert(0, self.globweather.humidity)

        # 天气描述
        self.international_description_label = tk.Label(self.secondcanvas, text='天气描述：')
        self.international_description_label.place(x=20, y=180, width=60, height=20)
        self.international_description_entry = tk.Entry(self.secondcanvas)
        self.international_description_entry.place(x=80, y=180, width=100, height=20)
        self.international_description_entry.insert(0, self.globweather.description)

        # 风向
        self.international_wind_label = tk.Label(self.secondcanvas, text='风向：')
        self.international_wind_label.place(x=320, y=180, width=50, height=20)
        self.international_wind_entry = tk.Entry(self.secondcanvas)
        self.international_wind_entry.place(x=380, y=180, width=150, height=20)
        self.international_wind_entry.insert(0, self.globweather.wind)

        # 在画布中嵌入图片
        self.draw_international_tempreture()

    def international_time_combobox_selected(self, event):
        selected_time = self.international_time.get()
        self.globweather = self.globalweather_get.get_weather(selected_time)
        self.international_temperature_entry.delete(0, tk.END)  # 清空温度 Entry 中的内容
        self.international_temperature_entry.insert(0,  '{}~{}'.format(self.globweather.temp_min, self.globweather.temp_max))  # 显示新的温度信息

        self.international_feels_like_entry.delete(0, tk.END)  # 清空体感温度 Entry 中的内容
        self.international_feels_like_entry.insert(0, self.globweather.feels_like)  # 显示新的体感温度信息

        self.international_pressure_entry.delete(0, tk.END)  # 清空压强 Entry 中的内容
        self.international_pressure_entry.insert(0, self.globweather.pressure)  # 显示新的压强信息

        self.international_humidity_entry.delete(0, tk.END)  # 清空湿度 Entry 中的内容
        self.international_humidity_entry.insert(0, self.globweather.humidity)  # 显示新的湿度信息

        self.international_description_entry.delete(0, tk.END)  # 清空天气描述 Entry 中的内容
        self.international_description_entry.insert(0, self.globweather.description)  # 显示新的天气描述信息

        self.international_wind_entry.delete(0, tk.END)  # 清空风向 Entry 中的内容
        self.international_wind_entry.insert(0, self.globweather.wind)  # 显示新的风向信息


    def country_combobox_selected(self, event): 
        self.international_city_combobox['values'] = list(national_citys(self.international_countrys, self.countryfullnames[self.country.get()])) # 根据选定的城市列表更新城市下拉框
        self.country2city.set(list(national_citys(self.international_countrys, self.countryfullnames[self.country.get()]))[0])
        self.draw_international_tempreture()

    def international_city_combobox_selected(self, event):
        self.citylat, self.citylon = citys_lat_lon(self.international_countrys, self.countryfullnames[self.country.get()], self.country2city.get())
        self.globalweather_get = GlobalWeatherGet(self.citylat, self.citylon)
        self.globweather = self.globalweather_get.get_weather(self.international_time.get())
        self.international_time_combobox_selected(0)
        self.draw_international_tempreture()

    # 根据当前选择的城市天气信息，画出温度变化图
    def draw_international_tempreture(self):
        x_values = list(self.globalweather_get.timelist)
        y1_values = []
        y2_values = []
        for x_value in x_values:
            y1_values.append(self.globalweather_get.get_weather(x_value).temp_max)
            y2_values.append(self.globalweather_get.get_weather(x_value).temp_min)
        fig = Figure(figsize=(40,2), dpi=100)
        a = fig.add_subplot(111)
        # 只显示x_values的形式是2023-12-1 18:00:00，只留下12:1 18
        x_values = [x_value[5:10] + '/' + x_value[11:13] for x_value in x_values]
        a.plot(x_values, y1_values, label='time')
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
        # canvas = FigureCanvasTkAgg(fig, master=self.secondcanvas)  # A tk.DrawingArea.
        # canvas.draw()
        # canvas.get_tk_widget().place(x=20, y=220, width=500, height=200)

        # 创建一个可滚动的画布
        scroll_canvas = Canvas(self.secondcanvas)
        scroll_canvas.place(x=20, y=220, width=500, height=200)

        # 创建一个滚动条
        scrollbar = Scrollbar(self.secondcanvas, orient="horizontal", command=scroll_canvas.xview, width = 30)
        scrollbar.place(x=20, y=430, width=500, height=20)
        #scrollbar.pack(side="bottom", fill="x")

        # 将滚动条连接到画布
        scroll_canvas.configure(xscrollcommand=scrollbar.set)

        # 创建一个Frame，将其添加到画布中
        frame = Frame(scroll_canvas)
        scroll_canvas.create_window((500,200), window=frame, anchor='nw')
        # 将FigureCanvasTkAgg添加到Frame中
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", fill="both", expand=True) # 将画布填充到Frame中

        # 更新画布的滚动区域
        frame.update_idletasks()
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox('all'))


    

    # 查看收藏
    def show_favorite(self):
        if len(self.my_favorite_city.get_favor_cityls()) == 0:
            messagebox.showinfo('提示', '收藏夹为空')
        else:  
            self.maincanvas.pack_forget()
            self.secondcanvas.pack_forget()
            self.myfavcanvas.pack()
            self.myfavcanvas.update() # 刷新窗口
            self.cityinlist = list(self.my_favorite_city.get_favor_cityls())
            self.my_fav_city = tk.StringVar()  # 用来存储用户选择的城市名
            self.my_fav_city.set(list(self.cityinlist)[0])
            self.fav_city_label = tk.Label(self.myfavcanvas, text='城市：')
            self.fav_city_label.place(x=20, y=20, width=50, height=20)
            self.fav_city_combobox = ttk.Combobox(self.myfavcanvas, textvariable= self.my_fav_city, state='readonly')
            self.fav_city_combobox['values'] =  self.cityinlist
            self.fav_city_combobox.place(x=80, y=20, width=100, height=20)
            self.fav_city_combobox_selected(0)
            self.fav_city_combobox.bind('<<ComboboxSelected>>', self.fav_city_combobox_selected)

            self.win1_delete_button = tk.Button(self.myfavcanvas, text='删除', command=self.delete_favorite)
            self.win1_delete_button.place(x=200, y=20, width=40, height=20)
        # 添加到收藏
    def add_favorite(self):
        self.cityweather = []
        #如果当前页面是self.maincanvas，则添加到收藏
        if self.maincanvas.winfo_ismapped():
            for i in range(0,4):
                idate = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
                self.weather = self.weather_get.get_weather(self.city.get(),idate)
                self.cityweather.append(self.weather)
            self.my_favorite_city.add_weather(self.city.get(), self.cityweather)
            messagebox.showinfo('提示', '添加成功')
        # 如果当前页面是self.secondcanvas，将国际类的天气信息添加到收藏
        elif self.secondcanvas.winfo_ismapped():
            for time in self.globalweather_get.timelist:
                self.globweather = self.globalweather_get.get_weather(time)
                self.cityweather.append(self.globweather)
            self.my_favorite_city.add_weather(self.country2city.get(), self.cityweather)
            messagebox.showinfo('提示', '添加成功')
        else:
            messagebox.showinfo('提示', '当前页面不是国内天气页面，无法添加')

    # 从收藏中删除
    def delete_favorite(self):
        self.my_favorite_city.delete_weather(self.fav_city_combobox.get())
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


    # 收藏界面城市下拉框选择事件
    def fav_city_combobox_selected(self, event):
        self.fav_weath_info = self.my_favorite_city.get_weather(self.fav_city_combobox.get())
        print(self.fav_weath_info)
        # 如果选择的城市是国内类的天气信息
        if self.fav_weath_info[0].__class__.__name__ == 'Weather':
            # 清空页面上的信息
            self.myfavcanvas.pack_forget()
            self.myfavcanvas.pack()
            xpos = 20
            ypos = 60
            for weather in self.fav_weath_info:
                self.win1_date_label = tk.Label(self.myfavcanvas, text='日期：'+ weather.date)
                self.win1_date_label.place(x=xpos, y=ypos, width=100, height=20)
                # 以label的形式显示天气信息
                self.win1_week_label = tk.Label(self.myfavcanvas, text='星期：'+ weather.week)
                self.win1_week_label.place(x=xpos, y=ypos+20, width=100, height=20)
                self.win1_temperature_label = tk.Label(self.myfavcanvas, text='温度：'+ weather.daytemperature)
                self.win1_temperature_label.place(x=xpos, y=ypos+40, width=100, height=20)
                self.win1_humidity_label = tk.Label(self.myfavcanvas, text='湿度：'+ weather.humidity)
                self.win1_humidity_label.place(x=xpos, y=ypos+60, width=100, height=20)
                self.win1_wind_label = tk.Label(self.myfavcanvas, text='风力风向：'+ weather.wind)
                self.win1_wind_label.place(x=xpos, y=ypos+80, width=100, height=20)
                self.win1_dayweather_label = tk.Label(self.myfavcanvas, text='白天天气：'+ weather.dayweather)
                self.win1_dayweather_label.place(x=xpos, y=ypos+100, width=100, height=20)
                self.win1_nightweather_label = tk.Label(self.myfavcanvas, text='夜间天气：'+ weather.nightweather)
                self.win1_nightweather_label.place(x=xpos, y=ypos+120, width=100, height=20)
                xpos += 120
                ypos = 60  
            
        # 如果选择的城市是国际类的天气信息
        elif self.fav_weath_info[0].__class__.__name__ == 'GlobalWeather':
            self.myfavcanvas.pack_forget()
            self.myfavcanvas.pack()
            xpos = 10
            ypos = 60
            i = 0
            for weather in self.fav_weath_info:
                i += 1
                self.win1_date_label = tk.Label(self.myfavcanvas, text='日期：'+ weather.time)
                self.win1_date_label.place(x=xpos, y=ypos, width=100, height=20)
                # 以label的形式显示天气信息
                self.win1_temperature_label = tk.Label(self.myfavcanvas, text='最高温度：'+ str(weather.temp_max))
                self.win1_temperature_label.place(x=xpos, y=ypos+20, width=100, height=20)
                self.win1_feels_like_label = tk.Label(self.myfavcanvas, text='体感温度：'+ str(weather.feels_like))
                self.win1_feels_like_label.place(x=xpos, y=ypos+40, width=100, height=20)
                self.win1_pressure_label = tk.Label(self.myfavcanvas, text='压强：'+ str(weather.pressure))
                self.win1_pressure_label.place(x=xpos, y=ypos+60, width=100, height=20)
                self.win1_humidity_label = tk.Label(self.myfavcanvas, text='湿度：'+ str(weather.humidity))
                self.win1_humidity_label.place(x=xpos, y=ypos+80, width=100, height=20)
                self.win1_description_label = tk.Label(self.myfavcanvas, text='天气描述：'+ weather.description)
                self.win1_description_label.place(x=xpos, y=ypos+100, width=100, height=20)
                self.win1_wind_label = tk.Label(self.myfavcanvas, text='风向：'+ weather.wind)
                self.win1_wind_label.place(x=xpos, y=ypos+120, width=100, height=20)
                if i <= 4:
                    xpos += 120
                    ypos = 60
                if i > 4:
                    ypos = 220
                    if i == 5: 
                        xpos = 10
                    else : 
                        xpos += 120



    
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
        # 国际类天气界面
        self.country_label['text'] = '国家：'
        self.international_city_label['text'] = '城市：'
        self.international_date_label['text'] = '日期：'
        self.international_temperature_label['text'] = '温度：'
        self.international_feels_like_label['text'] = '体感温度：'
        self.international_pressure_label['text'] = '压强：'
        self.international_humidity_label['text'] = '湿度：'
        self.international_description_label['text'] = '天气描述：'
        self.international_wind_label['text'] = '风向：'
        # 收藏界面
        self.fav_city_label['text'] = '城市：'
        self.win1_date_label['text'] = '日期：'
        self.win1_week_label['text'] = '星期：'
        self.win1_temperature_label['text'] = '温度：'
        self.win1_humidity_label['text'] = '湿度：'
        self.win1_wind_label['text'] = '风力风向：'
        self.win1_dayweather_label['text'] = '白天天气：'
        self.win1_nightweather_label['text'] = '夜间天气：'
        self.win1_delete_button['text'] = '删除'

    
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
        # 国际类天气界面
        self.country_label['text'] = 'Country：'
        self.international_city_label['text'] = 'City：'
        self.international_date_label['text'] = 'Date：'
        self.international_temperature_label['text'] = 'Temperature：'
        self.international_feels_like_label['text'] = 'Feels Like：'
        self.international_pressure_label['text'] = 'Pressure：'
        self.international_humidity_label['text'] = 'Humidity：'
        self.international_description_label['text'] = 'Description：'
        self.international_wind_label['text'] = 'Wind：'
        # 收藏界面
        self.fav_city_label['text'] = 'City：'
        self.win1_date_label['text'] = 'Date：'
        self.win1_week_label['text'] = 'Week：'
        self.win1_temperature_label['text'] = 'Temperature：'
        self.win1_humidity_label['text'] = 'Humidity：'
        self.win1_wind_label['text'] = 'Wind：'
        self.win1_dayweather_label['text'] = 'DayWeather：'
        self.win1_nightweather_label['text'] = 'NightWeather：'
        self.win1_delete_button['text'] = 'Delete'

