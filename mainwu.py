#! /usr/bin/env python3

# -*- coding: utf-8 -*-
#
#  Title: Weather kiosk
#
#  Copyright 2016 Troy Franks <outlaws42@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
"""
requires: python 3, tkinter 8.6, pywapi, pyowm
For indoor temp sensor DHT22 the following need to be installed
pigpio, DHT22
pigpiod needs to be started at os start as root
put the following line in sudo crontab -e
@reboot              /usr/local/bin/pigpiod
need to compile pigpio
Files in main dir: DHT22.py, main.py
Libraries in lib dir: indoor.py, noaa.py, owm.py weather_ch.py
"""
import configparser
import datetime
import logging
import os
import sys
import time
import tkinter as tk

logging.basicConfig(filename='weather_kiosk.log', level=logging.INFO, 
    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# user libraries
import lib.indoor as indr
#import lib.owm as ow
import lib.noaa as no
#import lib.weather_ch as wc
import lib.wu as wu
import lib.db as dp



class Main():
    version = '2.1.9'
    software = 'Weather Kiosk'
    #Set Degree special character
    degree_sign= '\N{DEGREE SIGN}'
    background = "black"
    foreground = "white"
    color_1 = "medium sea green" # NA
    color_2 = "yellow"  # status.
    color_3 = "deepskyblue2" # minus
    color_4 = "red" # Indoor temp no sensor
    font_ws = ("ubuntu",7,'bold')
    font_cat = ("ubuntu",13,'bold') # 11
    font_q = ("ubuntu",10,'bold')
    font_general = ("ubuntu",21,"bold") # 19
    font_hum = ("ubuntu",20,"bold")
    font_temp = ("ubuntu",55,"bold") # 55
    font_time = ("ubuntu",36,"bold") # 55
    refresh_type='1' # 1 = minutes 2 = Seconds
    refresh_rate_amount = 30
    service = 'wu' # noaa = noaa weather, ch = Weather Channel


    if refresh_type =='1':
        refresh_rate =((refresh_rate_amount*60)*1000) # Minutes Refresh ((minutes*60)*1000) 1000 Miliseconds in a second
    else:
        refresh_rate =(refresh_rate_amount*1000) # Seconds Refresh (seconds*1000) 1000 Miliseconds in a second

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(self.software + ' ' + self.version)
        self.root.geometry('800x480')
        self.root.configure(bg = self.background)
        #self.root.overrideredirect(1) # Make the window borderless
        self.frame0 = tk.Frame(self.root,background=self.background)
        self.frame0.grid(column='0',row='0',sticky="ew")

        # create and instance of the external classes
        if self.service == 'noaa':
            self.outdoor = no.Noaa()
        elif self.service == 'owm':
            self.outdoor = ow.Owm()
        elif self.service == 'wu':
            self.outdoor = wu.Wu()
        else:
            self.outdoor = wc.WeatherCh()
        self.indoor = indr.Indoor()
        self.intial_past_db()
        # Call refresh of data
        self.refresh_info()

        # Call refresh of time
        try:
            self.update_timeText()
        except(ValueError) as e:
            print('timeText error:  ' + str(e)) #debug
            logging.info('timeText error:  ' + str(e))
            pass

        self.root.mainloop()


    def get_resource_path(self,rel_path):
        dir_of_py_file = os.path.dirname(sys.argv[0])
        rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
        abs_path_to_resource = os.path.abspath(rel_path_to_resource)
        return abs_path_to_resource

    def sign_plus(self):
        self.outdoor_temp = self.outdoor.outdoor_temp , self.degree_sign
        self.wind = self.outdoor.wind + ' mph '
        self.windchill = self.outdoor.windchill , self.degree_sign
        self.barometer = self.outdoor.barometer_p + ' in'
        self.humidity = self.outdoor.humidity , '%'
        self.dewpoint = self.outdoor.dewpoint , self.degree_sign
        #self.visibility = self.outdoor.visibility + ' mi'
        self.weather_service = self.outdoor.weather_service + '/    ' + self.software + ' ' + self.version
        self.past_temp = '{}{}/{}{}'.format(self.tempp,self.degree_sign,self.templ,self.degree_sign)

    #############################################
    # Info calls                                #
    #############################################

        # DATABASE CALLS

    def get_high_low_temp_db(self):
        now = datetime.datetime.now()
        today1130pm = now.replace(hour=23, minute=30, second=0, microsecond=0)
        if now >= today1130pm:
            conn, cur = dp.create_connection(self.database_path)
            high_low = dp.high_low_temp_today(cur, conn,'weather')
            high = high_low[0]
            low = high_low[1]
            dp.close(conn)
            self.db_config_past('high',high)
            self.db_config_past('low', low)
        else:
            pass

    def db_config_past(self, tablename, past):
        idr,con,tem,win,feel,dew,rel,bar,da,zi= past
        
        create_table = "CREATE TABLE IF NOT EXISTS " + tablename + """ (
                                                            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                                            Condition TEXT NOT NULL,
                                                            OTemp INTEGER NOT NULL,
                                                            WindSpeed INTEGER NOT NULL,
                                                            FeelsLike REAL,
                                                            DewPoint REAL,
                                                            RelHumidity REAL,
                                                            Barometer REAL,
                                                            TDate,
                                                            Zip TEXT
                                                    ); """

        prin = """SELECT ID, Condition, OTemp, WindSpeed,
                    FeelsLike, DewPoint, RelHumidity, Barometer,
                    TDate, Zip FROM """ + tablename

        database_loc = 'lib/weather.db'
        condition = con
        otemp = tem
        windspeed = win
        feelslike = feel
        dewpoint = dew
        relhumidity = rel
        barometer = bar
        date_today= da
        zip_code = zi
        self.write_past_db(tablename,database_loc,create_table,prin,condition,otemp, 
            windspeed,feelslike,dewpoint,relhumidity,barometer,date_today,zip_code)

    def db_config_wether(self):
        create_table = """CREATE TABLE IF NOT EXISTS weather(
                                                            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                                            Condition TEXT NOT NULL,
                                                            OTemp INTEGER NOT NULL,
                                                            WindSpeed INTEGER NOT NULL,
                                                            FeelsLike REAL,
                                                            DewPoint REAL,
                                                            RelHumidity REAL,
                                                            Barometer REAL,
                                                            TDate,
                                                            Zip TEXT
                                                    ); """

        prin = """SELECT ID, Condition, OTemp, WindSpeed,
                    FeelsLike, DewPoint, RelHumidity, Barometer,
                    TDate, Zip FROM weather """
        database_loc = 'lib/weather.db'
        condition = self.outdoor.status
        otemp = self.outdoor.outdoor_temp
        windspeed = self.outdoor.wind_speed
        feelslike = self.outdoor.windchill
        dewpoint = self.outdoor.dewpoint
        relhumidity = self.outdoor.humidity
        barometer = self.outdoor.barometer_p
        zip_code = self.outdoor.zip_code
        self.write_db(database_loc,create_table,prin,condition,otemp, 
            windspeed,feelslike,dewpoint,relhumidity,barometer,zip_code)

    def write_db(self, *args):
        #self.database_path = self.get_resource_path(args[0])

        # create a database connection
        conn, cur = dp.create_connection(self.database_path)
        if conn is not None:
            # create projects table
            dp.create_table(cur, conn, args[1])
        else:
            print("Error! cannot create the database connection.")
        if self.outdoor.status != 'Status ER':
            dp.add_row(cur, 'weather',args[3], args[4], args[5], args[6], 
                args[7], args[8], args[9], args[10])
        else:
            print("This didn't get sent to the database")
        dp.close(conn)

    def write_past_db(self, tablename, *args):

        # create a database connection
        conn, cur = dp.create_connection(self.database_path)
        # create projects table
        dp.create_table(cur, conn, args[1])
        dp.add_row(cur, tablename, args[3], args[4], args[5], args[6], 
            args[7], args[8], args[9], args[10], args[11])
        dp.close(conn)

    def read_past_db(self):
        today = datetime.date.today()
        if self.now_date != today:
            conn, cur = dp.create_connection(self.database_path)
            high = dp.past_temp(cur, conn,'high')
            low = dp.past_temp(cur,conn, 'low')
            self.now_date = datetime.date.today()
            try:
                self.idp,self.conp,self.tempp,self.windp,self.feelp,self.dewp,self.relp,self.barp,self.datep,self.zipp = high
                self.idl,self.conl,self.templ,self.windl,self.feell,self.dewl,self.rell,self.barl,self.datel,self.zipl = low
            except TypeError as e:
                print(e)
                self.tempp = 'ND'
                self.templ = 'ND'


    def intial_past_db(self):
        self.database_path = self.get_resource_path('lib/weather.db')
        self.now_date = datetime.date.today()
        conn, cur = dp.create_connection(self.database_path)
        high = dp.past_temp(cur, conn,'high')
        low = dp.past_temp(cur, conn,'low')
        try:
            self.idp,self.conp,self.tempp,self.windp,self.feelp,self.dewp,self.relp,self.barp,self.datep,self.zipp = high
            self.idl,self.conl,self.templ,self.windl,self.feell,self.dewl,self.rell,self.barl,self.datel,self.zipl = low
        except TypeError as e:
            print(e)
            self.tempp = 'ND'
            self.templ = 'ND'
        # END DATABASE CALLS

    def refresh_info(self):

        self.frame0.destroy()
        try:
            self.frame0 = tk.Frame(self.root,background=self.background)
            self.frame0.grid(column='0',row='0',sticky="ew")

            # whole container frame
            self.f_all = tk.Frame(self.frame0,border='2',relief='sunken',
                background=self.background)
            self.f_all.grid(column='0',row='0',columnspan='2',rowspan='6', 
                padx=(45,0),pady=(55,0),sticky="new") # 110,0 55,0

            # left container frame
            self.f_left = tk.Frame(self.f_all,background=self.background)
            self.f_left.grid(column='0',row='0',rowspan='7', padx=(0,0),
                pady=(0,0),sticky="new")

            # left children frames
            self.f_top = tk.Frame(self.f_left,border='2',relief='sunken',
                background=self.background)
            self.f_top.grid(column='0',row='1',padx=(0,0),pady=(0,0),sticky="new")

            self.lef_center = tk.Frame(self.f_left,background=self.background)
            self.lef_center.grid(column='0',row='2',padx=(0,0),pady=(0,0),sticky='new')

            # sub of lef_center temp frames
            self.f_indoor_temp = tk.Frame(self.lef_center,border='2',
                relief='sunken',background=self.background)
            self.f_indoor_temp.grid(column='0',row='0',padx=(0,0),
                pady=(0,0),sticky='nsew')
            self.f_outdoor_temp = tk.Frame(self.lef_center,border='2',
                relief='sunken',background=self.background)
            self.f_outdoor_temp.grid(column='1',row='0',padx=(0,0),
                pady=(0,0),sticky='nsew')

            self.lef_bottom = tk.Frame(self.f_left,border='2',
                relief='sunken',background=self.background)
            self.lef_bottom.grid(column='0',row='3',padx=(0,0),sticky="new")

            # middle container frame
            self.f_middle = tk.Frame(self.f_all,background=self.background)
            self.f_middle.grid(column='1',row='0',rowspan='7', 
                padx=(0,0),pady=(0,0),sticky="new")

            # middle children frames
            self.frame4 = tk.Frame(self.f_middle,border='2',
                relief='sunken',background=self.background)
            self.frame4.grid(column='0',row='0',rowspan='2', padx=(0,0),
                pady=(0,0),sticky="new")

            self.f_wind = tk.Frame(self.f_middle,border='2',
                relief='sunken',background=self.background)
            self.f_wind.grid(column='0',row='2', padx=(0,0),
                pady=(0,0),sticky="new")

            self.f_windchill = tk.Frame(self.f_middle,border='2',
                relief='sunken',background=self.background)
            self.f_windchill.grid(column='0',row='3', padx=(0,0),
                pady=(0,0),sticky="new")

            self.f_uv = tk.Frame(self.f_middle,border='2',
                relief='sunken',background=self.background)
            self.f_uv.grid(column='0',row='6', padx=(0,0),
                pady=(0,0),sticky="new")

            self.f_hum = tk.Frame(self.f_middle,border='2',
                relief='sunken',background=self.background)
            self.f_hum.grid(column='0',row='5', padx=(0,0),
                pady=(0,0),sticky="new")

            self.f_dp = tk.Frame(self.f_middle,border='2',
                relief='sunken',background=self.background)
            self.f_dp.grid(column='0',row='4', padx=(0,0),
                pady=(0,0),sticky="new")

            # right container frame
            self.f_right = tk.Frame(self.frame0,background=self.background)
            self.f_right.grid(column='2',row='0',rowspan='7', 
                padx=(10,0),pady=(55,0),sticky="new")

            self.f_quit = tk.Frame(self.f_right,relief='sunken',
                background=self.background)
            self.f_quit.grid(column='0',row='1', padx=(0,0),pady=(5,5),
                sticky="new")
        except:
            logging.info('Frame refresh error: ')
            pass

        # call indoor temp function
        self.indoor.readDHT22()


        # get weather info from the internet
        self.outdoor.get_weather_info()

        # populate the weather info from the net.
        self.outdoor.gleen_info()
        try:
            self.outdoor.forecast()
        except:
            pass

        # write info
        self.db_config_wether()

        # read from db
        self.read_past_db()

        # Add sign for display
        self.sign_plus()

        # display quit button
        self.quit_button()

        self.check_current_hour()

        # disply functions
        self.display_indoor()

        try:
            self.display_outdoor()
        except(AttributeError) as e:
            print('display_outdoor error:  ' + str(e)) #debug
            logging.info('display_outdoor error:  ' + str(e))
            pass
        self.get_high_low_temp_db()  # Get high low temp for the day
        self.display_refresh()
        self.frame0.after(self.refresh_rate,self.refresh_info)


    def update_timeText(self):


        # Get the current time, note you can change the format as you wish
        current = time.strftime("%l:%M")
        meridiem = time.strftime("%p")
        self.now = tk.StringVar()
        self.now2 = tk.StringVar()

        # Update the timeText Label box with the current time
        time_text = tk.Label(self.frame4,fg=self.foreground,
            bg=self.background,font=self.font_cat,text='Time(%s)'%meridiem)
        time_text.grid(row='0',column='0',sticky='ew',padx=(0,0))
        timeText = tk.Label(self.frame4,fg=self.foreground,
            bg=self.background,font=self.font_time)
        timeText.grid(column ='0',row ='1',sticky='ew',columnspan='1',
            rowspan='2', padx=(0,0))
        timeText["textvariable"] = self.now

        # Call the update_timeText() function after 5 second
        self.now.set(current)
        self.now2.set(meridiem)
        self.frame4.grid_columnconfigure(0,weight='1')
        self.root.after(5000, self.update_timeText)

    def check_current_hour(self):
        self.date_now = datetime.datetime.now()
        self.time_now = self.date_now.time()
        return self.time_now.hour

    def display_refresh(self):
        try:
            self.refresh = "Refresh:  " + time.strftime('%l:%M %p')
        except(ValueError) as e:
            print('display_refresh error:  ' + str(e)) #debug
            logging.info('display_refresh error:  ' + str(e))
            self.refresh = "Refresh:  Date"
        refresh = tk.Label(self.f_top,fg=self.foreground,bg=self.background,
                font=self.font_general,text=self.refresh)
        refresh.grid(row='3',column='1',columnspan='3',sticky = 'w')

    def display_indoor(self):
        try:
            if self.indoor.inside_temp_f >'0':
                indoor_temp =tk.Label(self.f_indoor_temp,fg=self.foreground,
                    bg=self.background,
                    font=self.font_temp,text=self.indoor.indoor_temp)
                indoor_temp.grid(row='1',column='0',sticky='w',rowspan='4',
                    columnspan='2',padx=(50,50))
                indoor_hum = tk.Label(self.f_indoor_temp,fg=self.color_3,
                    bg=self.background,
                    font=self.font_general,text=self.indoor.indoor_hum)
                indoor_hum.grid(row='4',column='0',padx=(145,0))
            else:
                indoor_temp =tk.Label(self.f_indoor_temp,fg=self.color_1,
                    bg=self.background,font=self.font_temp,text='70')
                indoor_temp.grid(row='1',column='0',sticky='w',rowspan='4',
                    padx=(50,50))
                indoor_hum = tk.Label(self.f_indoor_temp,fg=self.color_3,
                    bg=self.background,font=self.font_general,text='??%')
                indoor_hum.grid(row='3',column='0',padx=(145,0))
        except (NameError, AttributeError) as e:
            print('display_indoor error:  ' + str(e)) #debug
            logging.info('display_indoor error:  ' + str(e))
            indoor_temp = tk.Label(self.f_indoor_temp,fg=self.color_4,
                bg=self.background,font=self.font_temp,text='70')
            indoor_temp.grid(row='1',column='0', sticky='w', rowspan='4', 
                columnspan='2',padx=(50,50))
            indoor_hum = tk.Label(self.f_indoor_temp,fg=self.color_3,
                bg=self.background,font=self.font_general,text='??%')
            indoor_hum.grid(row='3',column='0',padx=(145,0))

        # Indoor Temp label
        indoor_label = tk.Label(self.f_indoor_temp,fg=self.foreground,
            bg=self.background,font=self.font_general,text="Indoor(F)")
        indoor_label.grid(row='0',column='0', columnspan='2', padx=(50,50))


    def display_outdoor(self):
        # Outdoor Temp
        outdoor_label = tk.Label(self.f_outdoor_temp,fg=self.foreground,
            bg=self.background,font=self.font_general,text="Outdoor(F)")
        outdoor_label.grid(row='0',column='1',pady=(0,0),padx=(0,70))
        outdoor_temp = tk.Label(self.f_outdoor_temp,fg=self.foreground,
            bg=self.background,font=self.font_temp,text=self.outdoor_temp) # noaa no sky conditon icon.
        outdoor_temp.grid(row='1',column='0',rowspan='4',columnspan ='2',
            padx=(0,80))


        # weather status (Cloudy/Sunny  etc)
        status_text = tk.Label(self.f_top,fg=self.foreground,
            bg=self.background,font=self.font_hum,text='Current:')
        status_text.grid(row='1',column='1',sticky='w',pady=(0,0),padx=(0,0))
        status_info = tk.Label(self.f_top,fg=self.color_2,
            bg=self.background,font=self.font_hum,text=self.outdoor.status)
        status_info.grid(row='1',column='1',sticky='w',pady=(0,0),padx=(120,0))
        past_h_text = tk.Label(self.f_top,fg=self.foreground,
            bg=self.background,font=self.font_hum,text='Yesterday H/L: ')
        past_h_text.grid(row='2',column='1',sticky='w',pady=(0,0),padx=(0,0))
        past_h_info = tk.Label(self.f_top,fg=self.color_2,
            bg=self.background,font=self.font_hum,text=self.past_temp)
        past_h_info.grid(row='2',column='1',sticky='w',pady=(0,0),padx=(200,0))
        if self.outdoor.warning:
            warning_info = tk.Label(self.f_top,fg=self.color_4,
               bg=self.background,font=self.font_cat,text=self.outdoor.warning)
            warning_info.grid(row='2',column='3',sticky='w',pady=(0,0),padx=(30,0))
        else:
          pass

         # weather sevice indicator
        service_text = tk.Label(self.lef_bottom,fg=self.foreground,
            bg=self.background,font=self.font_ws,text=self.weather_service)
        service_text.grid(row='4',column='1',columnspan='2', sticky='w',
            pady=(0,5),padx=(0,5))


        # Side info settings
        # Wind settings
        wind_label = tk.Label(self.f_wind,fg=self.foreground,
            bg=self.background,justify ="center",font=self.font_cat,text="Wind")
        wind_label.grid(column ='0', row ='0')
        wind_ = tk.Label(self.f_wind,fg=self.foreground,
            bg=self.background,justify ="center",font=self.font_general,text=self.wind)
        wind_.grid(row='2',column='0',pady=(0,0),padx=(0,0))
        self.f_wind.grid_columnconfigure(0,weight='1')

        # Humidity settings
        humidity_label = tk.Label(self.f_hum,fg=self.foreground,
            bg=self.background, font=self.font_cat,text="Rel. Humidity")
        humidity_label.grid(row='0',column='0',padx =(0,0))
        humidity = tk.Label(self.f_hum,fg=self.foreground,
            bg=self.background,font=self.font_general,text=self.outdoor.humidity)
        humidity.grid(row='1',column='0',padx=(0,0))
        self.f_hum.grid_columnconfigure(0,weight='1')


        try: 

            # Dewpoint settings
            dewpoint_label = tk.Label(self.f_dp,fg=self.foreground,
                bg=self.background,font=self.font_cat,text="Dew Point")
            dewpoint_label.grid(row='0',column='0',padx =(0,0))
            dewpoint = tk.Label(self.f_dp,fg=self.foreground,
                bg=self.background,font=self.font_general,text=self.dewpoint)
            dewpoint.grid(row='1',column='0',pady=(0,0),padx=(0,5))
            self.f_dp.grid_columnconfigure(0,weight='1')

            # windchill settings
            windchill = tk.Label(self.f_windchill,fg=self.foreground,
                bg=self.background,font=self.font_general,text=self.windchill)
            windchill.grid(row='1',column='0',rowspan='1',pady=(0,0),padx=(0,0))
            windchill_label = tk.Label(self.f_windchill,fg=self.foreground,
                bg=self.background,font=self.font_cat,text="Feels Like")
            windchill_label.grid(row='0',column='0',padx =(0,0), pady=(0,0))
            self.f_windchill.grid_columnconfigure(0,weight='1')

        except(AttributeError) as e:
            print('display outdoor service,Dewpoint,windchill error:  ' + str(e)) #debug
            logging.info('display outdoor service,Dewpoint,windchill error:  ' + str(e))
            pass
        try:
            # weather.com only
            # Barometer settings
            baro_label = tk.Label(self.f_uv,fg=self.foreground,
                bg=self.background,font=self.font_cat,text="Precip Today")
            baro_label.grid(row='0',column='0',padx =(0,0))
            baro = tk.Label(self.f_uv,fg=self.foreground,
                bg=self.background,font=self.font_general,text=self.barometer)
            baro.grid(row='1',column='0',pady=(0,0),padx=(0,5))
            self.f_uv.grid_columnconfigure(0,weight='1')

            # Forcast settings
            days = self.outdoor.forecast_days()
            temps = self.outdoor.forecast_temp()
            precip_day = self.outdoor.forecast_precip_day()
            precip_night = self.outdoor.forecast_precip_night()
                        
            # Day current
            forecast_0_day = tk.Label(self.lef_bottom,fg=self.foreground,
                bg=self.background,font=self.font_general,text=days[0])
            forecast_0_day.grid(row='1',column='1',padx=(0,30),pady=(0,0))
            now = datetime.datetime.now()
            today4pm = now.replace(hour=17, minute=59, second=0, microsecond=0)
            if now <= today4pm:
                forecast_0_icon = tk.Label(self.lef_bottom,fg=self.foreground,
                    bg=self.background,font=self.font_general,image=self.outdoor.forecast_0_day_icon)
                forecast_0_precip = tk.Label(self.lef_bottom,fg=self.foreground,
                    bg=self.background,font=self.font_cat,text=precip_day[0] )
            else:
                forecast_0_icon = tk.Label(self.lef_bottom,fg=self.foreground,
                    bg=self.background,font=self.font_general,image=self.outdoor.forecast_0_night_icon)
                forecast_0_precip = tk.Label(self.lef_bottom,fg=self.foreground,
                   bg=self.background,font=self.font_cat,text=precip_night[0] )
            forecast_0_icon.grid(row='2',column='1',padx=(0,20))
            forecast_0_temp = tk.Label(self.lef_bottom,fg=self.foreground,
                bg=self.background,font=self.font_general,text=temps[0])
            forecast_0_temp.grid(row='3',column='1',padx=(0,20))
            forecast_0_precip.grid(row='1',column='1',padx=(90,20),pady=(0,0))
            # Day 1
            forecast_1_day = tk.Label(self.lef_bottom,fg=self.foreground,
                bg=self.background,font=self.font_general,text=days[1] )
            forecast_1_day.grid(row='1',column='2',padx=(0,30))
            forecast_1_icon = tk.Label(self.lef_bottom,fg=self.foreground,
                bg=self.background,font=self.font_general,image=self.outdoor.forecast_1_day_icon )
            forecast_1_icon.grid(row='2',column='2',padx=(0,20))
            forecast_1_temp = tk.Label(self.lef_bottom,fg=self.foreground,
                bg=self.background,font=self.font_general,text=temps[1])
            forecast_1_temp.grid(row='3',column='2',padx=(0,20))
            forecast_1_precip = tk.Label(self.lef_bottom,fg=self.foreground,
                bg=self.background,font=self.font_cat,text=precip_day[1] )
            forecast_1_precip.grid(row='1',column='2',padx=(90,20),pady=(0,0))
            # Day 2
            forecast_2_day = tk.Label(self.lef_bottom,fg=self.foreground,
                bg=self.background,font=self.font_general,text=days[2] )
            forecast_2_day.grid(row='1',column='3',padx=(0,30))
            forecast_2_icon = tk.Label(self.lef_bottom,fg=self.foreground,
                bg=self.background,font=self.font_general,image=self.outdoor.forecast_2_day_icon )
            forecast_2_icon.grid(row='2',column='3')
            forecast_2_temp = tk.Label(self.lef_bottom,fg=self.foreground,
                bg=self.background,font=self.font_general,text=temps[2])
            forecast_2_temp.grid(row='3',column='3',padx=(0,0))
            forecast_2_precip = tk.Label(self.lef_bottom,fg=self.foreground,
                bg=self.background,font=self.font_cat,text=precip_day[2] )
            forecast_2_precip.grid(row='1',column='3',padx=(90,20),pady=(0,0))
        except:
            print('display outdoor Weather Ch only error:  ') #debug
            logging.info('display outdoor Weather Ch only error: ')
            pass

    def quit_button(self):
        # Quit button settings

        quit_image=self.outdoor.current_icon
        quitButton = tk.Button(self.f_outdoor_temp, bg=self.background,
                    fg=self.color_3, highlightthickness = 0, bd = 0, font=self.font_q,
                    text = "X",command=self.root.quit)
        quitButton.config(image=quit_image,width="70",height="55")
        quitButton.grid(column='1',row='4',sticky='sw',pady=(0,5),padx=(150,40))


if __name__ == "__main__":
    app = Main()
