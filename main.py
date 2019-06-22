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
requires: python 3, tkinter 8.6, pywapi
For indoor temp sensor DS18B20 the following need to be installed
Starting with 3.0 this gets the indoor temp  from a  wireless temp sensor
via MQTT. 

"""
import datetime
import logging
import time
import tkinter as tk
# user libraries
import lib.indoor as indr
import lib.ds as wu
import lib.db as dp
import lib.tmod as tmod
import lib.forecast as wc

logging.basicConfig(filename='weather_kiosk.log', level=logging.INFO, 
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class Main(tk.Frame):
    version = '3.0.14'
    software = 'Weather Kiosk'
    degree_sign = '\N{DEGREE SIGN}'  # Set Degree special character
    background = "black"
    foreground = "white"
    color_1 = "medium sea green" # NA
    color_2 = "yellow"  # status.
    color_3 = "deepskyblue2" # minus
    color_4 = "red"  # Indoor temp no sensor
    font_ws = ("ubuntu", 10, 'bold')
    font_cat = ("ubuntu", 13, 'bold') # 11
    font_q = ("ubuntu", 10, 'bold')
    font_general = ("ubuntu", 21, "bold")  # 19
    font_hum = ("ubuntu", 20, "bold")
    font_temp = ("ubuntu", 55, "bold")  # 55
    font_time = ("ubuntu", 36, "bold")  # 55
    font_set = ("ubuntu", 16, "bold")  # 55
    run_once = 1  # initiate variable to 1 for high low write to the DB
    refresh_type = '1'  # 1 = minutes 2 = Seconds
    refresh_rate_amount = 15
    
    if refresh_type == '1':
        refresh_rate = ((refresh_rate_amount*60)*1000)  # Minutes Refresh ((minutes*60)*1000) 1000 Miliseconds in a second
    else:
        refresh_rate = (refresh_rate_amount*1000)  # Seconds Refresh (seconds*1000) 1000 Miliseconds in a second

    def __init__(self):
        self.root = tk.Tk()
        self.read_config('config.json')
        self.root.title(self.software + ' ' + self.version)
        self.root.geometry('800x480')
        self.root.configure(bg = self.background)
        if self.fullscreen:
            self.root.overrideredirect(1) # Make the window borderless
        else:
            pass
        self.frame0 = tk.Frame(self.root, background=self.background)
        self.frame0.grid(column='0', row='0', sticky="ew")

        # create and instance of the external classes

        self.outdoor = wu.Wu()
        self.forecastwc = wc.WeatherCh()
        self.indoor = indr.Indoor()
        
        self.intial_past_db()
        
        # Call refresh of data
        self.refresh_info()

        # Call refresh of time
        try:
            self.update_timeText()
        except ValueError as e:
            print('timeText error:  ' + str(e))  # debug
            logging.info('timeText error:  ' + str(e))
            pass

        self.root.mainloop()


    def sign_plus(self):
        # self.city = self.outdoor.city
        self.outdoor_temp = '{}{}'.format(self.outdoor.outdoor_temp, self.degree_sign)
        self.wind = self.outdoor.wind
        self.windchill = '{}{}'.format(self.outdoor.windchill, self.degree_sign)
        self.precip = '{} {}'.format(self.outdoor.precip, self.outdoor.measure)
        self.humidity = '{}%'.format(self.outdoor.humidity)
        self.dewpoint = '{}{}'.format(self.outdoor.dewpoint, self.degree_sign)
        self.weather_service = '{}/ {} {}/ Location: {}'.format(self.outdoor.weather_service,
                                                                self.software, self.version, self.outdoor.city)
        self.past_temp = '{}{} / {}{}'.format(self.tempp, self.degree_sign, self.templ, self.degree_sign)

    #############################################
    # Info calls                                #
    #############################################

        # DATABASE CALLS

    def get_high_low_temp_db(self):
        now = datetime.datetime.now()
        today12am = now.replace(hour=0, minute=5, second=0, microsecond=0)
        today1230am = now.replace(hour=0, minute=35, second=0, microsecond=0)
        today1130pm = now.replace(hour=23, minute=30, second=0, microsecond=0)
        if now >= today1130pm and self.run_once == 1:
            conn, cur = dp.create_connection(self.database_path)
            high_low = dp.high_low_temp_today(cur, conn, 'weather')
            high = high_low[0]
            low = high_low[1]
            dp.close(conn)
            self.write_past_db('high', high)
            self.write_past_db('low', low)
            self.run_once = 0
        else:
            if today12am <= now <= today1230am:
                self.run_once = 1

    def db_config_wether(self):
        table = 'weather'
        condition = self.outdoor.status_icon
        otemp = self.outdoor.outdoor_temp
        windspeed = self.outdoor.wind_speed
        feelslike = self.outdoor.windchill
        dewpoint = self.outdoor.dewpoint
        relhumidity = self.outdoor.humidity
        precip = self.outdoor.precip
        zip_code = self.code
        self.write_db(table, condition, otemp,
                      windspeed, feelslike, dewpoint, relhumidity, precip, zip_code)

    def write_db(self, table, *args):

        # create a database connection
        conn, cur = dp.create_connection(self.database_path)
        
        # create projects table
        dp.create_table(cur, conn, table)
        
        if self.outdoor.status != 'Status ER':
            dp.add_row(cur, table, args[0], args[1], args[2], args[3], 
                args[4], args[5], args[6], args[7])
        else:
            print("This didn't get sent to the database")
        dp.close(conn)
    
    def write_past_db(self, tablename, past):
        id_, cond,temp, winspd, feels, dewpnt, relhum, precip, date, zip_ = past
        # create a database connection
        conn, cur = dp.create_connection(self.database_path)
        # create projects table
        dp.create_table(cur, conn, tablename)
        dp.add_row(cur, tablename, cond, temp, winspd, feels, 
                   dewpnt, relhum, precip, date, zip_)
        dp.close(conn)

    def read_past_db(self):
        today = datetime.date.today()
        if self.now_date != today:
            print('This is read_past_db: {}'.format(self.temp_past))
            conn, cur = dp.create_connection(self.database_path)
            high = dp.past_temp(cur, conn, 'high', self.temp_past)
            low = dp.past_temp(cur, conn, 'low', self.temp_past)
            self.now_date = datetime.date.today()
            try:
                self.idp, self.conp, self.tempp, self.windp, self.feelp, self.dewp, self.relp, self.barp, self.datep, \
                self.zipp = high
                self.idl, self.conl, self.templ, self.windl, self.feell, self.dewl, self.rell, self.barl, self.datel,\
                self.zipl = low
            except TypeError as e:
                print(e)
                self.tempp = 'ND'
                self.templ = 'ND'

    def intial_past_db(self):
        self.database_path = tmod.get_resource_path('lib/weather.db')
        self.now_date = datetime.date.today()
        conn, cur = dp.create_connection(self.database_path)

        # create projects table
        dp.create_table(cur, conn, 'high')
        dp.create_table(cur, conn, 'low')
        high = dp.past_temp(cur, conn,'high', self.temp_past)
        low = dp.past_temp(cur, conn,'low', self.temp_past)
        try:
            self.idp, self.conp, self.tempp, self.windp, self.feelp, self.dewp, self.relp, self.barp, self.datep, \
            self.zipp = high
            self.idl, self.conl, self.templ, self.windl, self.feell, self.dewl, self.rell, self.barl, self.datel, \
            self.zipl = low
        except TypeError as e:
            print(e)
            self.tempp = 'ND'
            self.templ = 'ND'
        # END DATABASE CALLS

    def refresh_info(self):
        # call indoor temp function
        self.read_config('config.json')
        self.indoor.run()
        
        self.frame0.destroy()
        try:
            self.frame0 = tk.Frame(self.root, background=self.background)
            self.frame0.grid(column='0', row='0', sticky="ew")

            # whole container frame
            self.f_all = tk.Frame(self.frame0, border='2', relief='sunken',
                                  background=self.background)
            self.f_all.grid(column='0', row='0', columnspan='2', rowspan='6',
                            padx=(85, 0), pady=(55, 0), sticky="new")  # 110,0 55,0

            # left container frame
            self.f_left = tk.Frame(self.f_all, background=self.background)
            self.f_left.grid(column='0', row='0', rowspan='7', padx=(0, 0),
                             pady=(0, 0), sticky="new")

            # left children frames
            self.f_top = tk.Frame(self.f_left, border='2', relief='sunken',
                                  background=self.background)
            self.f_top.grid(column='0', row='1', padx=(0, 0), pady=(0, 0), sticky="new")

            self.lef_center = tk.Frame(self.f_left, background=self.background)
            self.lef_center.grid(column='0', row='2', padx=(0, 0), pady=(0, 0), sticky='new')

            # sub of lef_center temp frames
            self.f_indoor_temp = tk.Frame(self.lef_center, border='2',
                                          relief='sunken', background=self.background)
            self.f_indoor_temp.grid(column='0', row='0', padx=(0, 0),
                                    pady=(0, 0), sticky='nsew')
            self.f_outdoor_temp = tk.Frame(self.lef_center, border='2',
                                           relief='sunken', background=self.background)
            self.f_outdoor_temp.grid(column='1', row='0', padx=(0, 0),
                                     pady=(0, 0), sticky='nsew')

            self.lef_bottom = tk.Frame(self.f_left, border='2',
                                       relief='sunken', background=self.background)
            self.lef_bottom.grid(column='0', row='3', padx=(0, 0), sticky="new")

            # middle container frame
            self.f_middle = tk.Frame(self.f_all, background=self.background)
            self.f_middle.grid(column='1', row='0', rowspan='7',
                               padx=(0, 0), pady=(0, 0), sticky="new")

            # middle children frames
            self.frame4 = tk.Frame(self.f_middle, border='2',
                                   relief='sunken', background=self.background)
            self.frame4.grid(column='0', row='0', rowspan='2', padx=(0, 0),
                             pady=(0, 0), sticky="new")

            self.f_wind = tk.Frame(self.f_middle, border='2',
                                   relief='sunken', background=self.background)
            self.f_wind.grid(column='0', row='2', padx=(0, 0),
                             pady=(0, 0), sticky="new")

            self.f_windchill = tk.Frame(self.f_middle, border='2',
                                        relief='sunken', background=self.background)
            self.f_windchill.grid(column='0', row='3', padx=(0, 0),
                                  pady=(0, 0), sticky="new")

            self.f_precip = tk.Frame(self.f_middle, border='2',
                                     relief='sunken', background=self.background)
            self.f_precip.grid(column='0', row='6', padx=(0, 0),
                               pady=(0, 0), sticky="new")

            self.f_hum = tk.Frame(self.f_middle, border='2',
                                  relief='sunken', background=self.background)
            self.f_hum.grid(column='0', row='5', padx=(0, 0),
                            pady=(0, 0), sticky="new")

            self.f_dp = tk.Frame(self.f_middle, border='2',
                                 relief='sunken', background=self.background)
            self.f_dp.grid(column='0', row='4', padx=(0, 0),
                           pady=(0, 0), sticky="new")

            # right container frame
            self.f_right = tk.Frame(self.frame0, background=self.background)
            self.f_right.grid(column='2', row='0', rowspan='7',
                              padx=(10, 0), pady=(55, 0), sticky="new")

            self.f_quit = tk.Frame(self.f_right, relief='sunken',
                                   background=self.background)
            self.f_quit.grid(column='0', row='1', padx=(0, 0), pady=(5,5),
                             sticky="new")
        except:
            logging.info('Frame refresh error: ')
            pass

        # get weather info from the internet
        self.outdoor.get_weather_info()
        if self.forecast_source == 2:
            self.forecastwc.get_weather_info()
        else:
            pass

        # populate the weather info from the net.
        self.outdoor.gleen_info()
        try:
            if self.forecast_source == 1:
                
                self.outdoor.forecast()
            else:
                self.forecastwc.forecast()
        except Exception as e:
            print('This is the forecast call {}'.format(e))
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
        except AttributeError as e:
            print('display_outdoor error:  ' + str(e))  # debug
            logging.info('display_outdoor error:  ' + str(e))
            pass
        self.get_high_low_temp_db()  # Get high low temp for the day
        self.display_refresh()
        self.frame0.after(self.refresh_rate, self.refresh_info)

    def update_timeText(self):

        # Get the current time, note you can change the format as you wish
        current = time.strftime("%l:%M")
        meridiem = time.strftime("%p")
        self.now = tk.StringVar()
        self.now2 = tk.StringVar()

        # Update the timeText Label box with the current time
        time_text = tk.Label(self.frame4, fg=self.foreground,
                             bg=self.background, font=self.font_cat, text='Time(%s)' % meridiem)
        time_text.grid(row='0', column='0', sticky='ew', padx=(0, 0))
        timeText = tk.Label(self.frame4, fg=self.foreground,
                            bg=self.background,font=self.font_time)
        timeText.grid(column ='0', row ='1', sticky='ew', columnspan='1',
                      rowspan='2', padx=(0, 0))
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
        except ValueError as e:
            print('display_refresh error:  ' + str(e))  # debug
            logging.info('display_refresh error:  ' + str(e))
            self.refresh = "Refresh:  Date"
        refresh = tk.Label(self.f_top, fg=self.foreground, bg=self.background,
                           font=self.font_general, text=self.refresh)
        refresh.grid(row='3', column='1', columnspan='1', sticky = 'w')

    def display_indoor(self):
        try:
            tempin = tmod.open_file('temp.txt')  # open temp.txt
            templist = tempin.split()  # put values in a list
            temp, tempdate, temptime = templist  # take values from the list put in variables
            now_time = datetime.datetime.now().strftime('%M.%S')  # Get current time min and Sec
            diff_time = round(float(now_time) - float(temptime))  # subtract time from file from current time the round should be 0
            temp_round = '{}{}'.format(round(float(temp)), self.degree_sign)  # temp together with degree sign
        except Exception as e:
            print('Issue with temp.txt: {}'.format(e))
            diff_time = 1
            
        if diff_time == 0:
            if temp > '0':
                message = 'Temp sensor working fine'
                indoor_temp = tk.Label(self.f_indoor_temp, fg=self.foreground,
                                       bg=self.background,
                                       font=self.font_temp, text=temp_round)
                indoor_temp.grid(row='1', column='0', sticky='w', rowspan='4',
                                 columnspan='2', padx=(50,50))
            else:
                temp_round = "-"
                message = 'Temp sensor working but negative value'
                indoor_temp = tk.Label(self.f_indoor_temp, fg=self.color_1,
                                       bg=self.background, font=self.font_temp, text= temp_round)
                indoor_temp.grid(row='1', column='0', sticky='w', rowspan='4',
                                 padx=(50,50))
        else:
            temp_round = "E1"
            message = 'Indoor Temp Communication ERROR'
            indoor_temp = tk.Label(self.f_indoor_temp, fg=self.color_4,
                                   bg=self.background, font=self.font_temp, text=temp_round)
            indoor_temp.grid(row='1', column='0', sticky='w', rowspan='4',
                             columnspan='2', padx=(50, 50))

        logging.info('{}: {}'.format(message,temp_round))

        # Indoor Temp label
        indoor_label = tk.Label(self.f_indoor_temp,fg=self.foreground,
                                bg=self.background,font=self.font_general,
                                text="Indoor({})".format(self.outdoor.temp_measure.upper()))
        indoor_label.grid(row='0', column='0', columnspan='2', padx=(50, 50))

    def display_outdoor(self):
        
        if self.temp_past == 'day':
            past_text = 'Yesterday\'s High/Low: '
        elif self.temp_past == 'month':
            past_text = 'Last Month\'s High/Low: '
        elif self.temp_past == 'year':
            past_text = 'Last Year\'s High/Low: '

        # Top center block
        # Status, Past, Warning(Cloudy/Sunny  etc)
        status_text = tk.Label(self.f_top, fg=self.foreground,
                               bg=self.background,font=self.font_hum, text='Current:')
        status_text.grid(row='1', column='1', sticky='w', pady=(0, 0), padx=(0, 0))
        status_info = tk.Label(self.f_top, fg=self.color_2,
                               bg=self.background, font=self.font_hum, text=self.outdoor.status)
        status_info.grid(row='1', column='1', sticky='w', pady=(0, 0), padx=(120, 0))
        past_h_text = tk.Label(self.f_top, fg=self.foreground,
                               bg=self.background, font=self.font_hum, text = past_text)
        past_h_text.grid(row='2', column='1', sticky='w', pady=(0, 0), padx=(0, 0))
        past_h_info = tk.Label(self.f_top, fg=self.color_2,
                               bg=self.background,font=self.font_hum, text=self.past_temp)
        past_h_info.grid(row='2',column='1', sticky='w', pady=(0, 0), padx=(290, 0))
        if self.outdoor.warning:
            warning_info = tk.Label(self.f_top, fg=self.color_4,
                                    bg=self.background, font=self.font_cat, text=self.outdoor.warning)
            warning_info.grid(row='3', column='1', sticky='w', pady=(0, 0), padx=(275, 0))
        else:
          pass
        
        # Middle Center
        # Outdoor Temp
        outdoor_label = tk.Label(self.f_outdoor_temp, fg=self.foreground,
                                 bg=self.background, font=self.font_general,
                                 text="Outdoor({})".format(self.outdoor.temp_measure.upper()))
        outdoor_label.grid(row='0',column='1', pady=(0, 0), padx=(0, 50))
        outdoor_temp = tk.Label(self.f_outdoor_temp, fg=self.foreground,
                                bg=self.background, font=self.font_temp, text=self.outdoor_temp)
        outdoor_temp.grid(row='1', column='0', rowspan='4', columnspan ='2',
                          padx=(0, 80))

        # Side info settings
        # Wind settings
        wind_label = tk.Label(self.f_wind, fg=self.foreground,
                              bg=self.background,justify ="center", font=self.font_cat, text="Wind")
        wind_label.grid(column ='0', row ='0')
        wind_ = tk.Label(self.f_wind, fg=self.foreground,
                         bg=self.background, justify ="center", font=self.font_general, text=self.wind)
        wind_.grid(row='2', column='0', pady=(0, 0), padx=(0, 0))
        self.f_wind.grid_columnconfigure(0, weight='1')

        # Humidity settings
        humidity_label = tk.Label(self.f_hum, fg=self.foreground,
                                  bg=self.background, font=self.font_cat, text="Rel. Humidity")
        humidity_label.grid(row='0', column='0', padx =(0, 0))
        humidity = tk.Label(self.f_hum, fg=self.foreground,
                            bg=self.background, font=self.font_general, text=self.outdoor.humidity)
        humidity.grid(row='1', column='0', padx=(0, 0))
        self.f_hum.grid_columnconfigure(0, weight='1')


        try: 

            # Dewpoint settings
            dewpoint_label = tk.Label(self.f_dp, fg=self.foreground,
                                      bg=self.background, font=self.font_cat, text="Dew Point")
            dewpoint_label.grid(row='0', column='0', padx =(0, 0))
            dewpoint = tk.Label(self.f_dp, fg=self.foreground,
                                bg=self.background, font=self.font_general, text=self.dewpoint)
            dewpoint.grid(row='1', column='0', pady=(0, 0), padx=(0, 5))
            self.f_dp.grid_columnconfigure(0, weight='1')

            # windchill settings
            windchill = tk.Label(self.f_windchill, fg=self.foreground,
                                 bg=self.background, font=self.font_general, text=self.windchill)
            windchill.grid(row='1', column='0', rowspan='1', pady=(0, 0), padx=(0, 0))
            windchill_label = tk.Label(self.f_windchill, fg=self.foreground,
                                       bg=self.background, font=self.font_cat, text="Feels Like")
            windchill_label.grid(row='0', column='0', padx =(0, 0), pady=(0, 0))
            self.f_windchill.grid_columnconfigure(0, weight='1')

        except AttributeError as e:
            print('display outdoor service,Dewpoint,windchill error:  ' + str(e))  # debug
            logging.info('display outdoor service,Dewpoint,windchill error:  ' + str(e))
            pass
        try:
            # Precip settings
            precip_label = tk.Label(self.f_precip, fg=self.foreground,
                                    bg=self.background, font=self.font_cat, text="Precip Today")
            precip_label.grid(row='0', column='0', padx =(0,0))
            precip = tk.Label(self.f_precip, fg=self.foreground,
                              bg=self.background, font=self.font_general, text=self.precip)
            precip.grid(row='1', column='0', pady=(0, 0), padx=(0, 5))
            self.f_precip.grid_columnconfigure(0, weight='1')

            # Bottom Center
            # Forcast settings
            if self.forecast_source == 1:
                days = self.outdoor.forecast_days()
                temps = self.outdoor.forecast_temp()
                precip_day = self.outdoor.forecast_precip_day()
                
            else:
                days = self.forecastwc.forecast_days()
                temps = self.forecastwc.forecast_temp()
                precip_day = self.forecastwc.forecast_precip_day('day')
                precip_night = self.forecastwc.forecast_precip_day('night')

            # icons
            if self.forecast_source == 1:
                icon_day_0 = self.outdoor.forecast_0_day_icon
                icon_day_1 = self.outdoor.forecast_1_day_icon
                icon_day_2 = self.outdoor.forecast_2_day_icon
            else:
                icon_day_0 = self.forecastwc.forecast_0_day_icon
                icon_day_1 = self.forecastwc.forecast_1_day_icon
                icon_day_2 = self.forecastwc.forecast_2_day_icon
                       
            # Day current
            forecast_0_day = tk.Label(self.lef_bottom, fg=self.foreground,
                                      bg=self.background, font=self.font_general, text=days[0])
            forecast_0_day.grid(row='1', column='1', padx=(0, 30), pady=(0, 0))

            forecast_0_icon = tk.Label(self.lef_bottom, fg=self.foreground,
                                           bg=self.background, font=self.font_general, image=icon_day_0)
            forecast_0_precip = tk.Label(self.lef_bottom, fg=self.foreground,
                                             bg=self.background, font=self.font_cat, text=precip_day[0])
                        
            forecast_0_icon.grid(row='2', column='1', padx=(0,10))
            forecast_0_temp = tk.Label(self.lef_bottom, fg=self.foreground,
                                       bg=self.background, font=self.font_general, text=temps[0])
            forecast_0_temp.grid(row='3', column='1', padx=(0, 10))
            forecast_0_precip.grid(row='1', column='1', padx=(95, 5), pady=(0, 0))
            # Day 1
            forecast_1_day = tk.Label(self.lef_bottom, fg=self.foreground,
                                      bg=self.background, font=self.font_general, text=days[1])
            forecast_1_day.grid(row='1', column='2', padx=(0, 10))
            forecast_1_icon = tk.Label(self.lef_bottom, fg=self.foreground,
                                       bg=self.background, font=self.font_general, image=icon_day_1)
            forecast_1_icon.grid(row='2', column='2', padx=(0, 10))
            forecast_1_temp = tk.Label(self.lef_bottom, fg=self.foreground,
                                       bg=self.background, font=self.font_general, text=temps[1])
            forecast_1_temp.grid(row='3', column='2', padx=(0, 10))
            
            if self.forecast_source == 1:
                forecast_1_precip = tk.Label(self.lef_bottom, fg=self.foreground,
                                             bg=self.background, font=self.font_cat, text=precip_day[1])
            else:
                forecast_1_precip = tk.Label(self.lef_bottom, fg=self.foreground,
                                             bg=self.background, font=self.font_cat,text=precip_day[2])
                
            forecast_1_precip.grid(row='1', column='2', padx=(105, 5), pady=(0, 0))
            # Day 2
            forecast_2_day = tk.Label(self.lef_bottom, fg=self.foreground,
                                      bg=self.background, font=self.font_general, text=days[2])
            forecast_2_day.grid(row='1', column='3', padx=(0, 0))
            forecast_2_icon = tk.Label(self.lef_bottom, fg=self.foreground,
                                       bg=self.background, font=self.font_general, image=icon_day_2)
            forecast_2_icon.grid(row='2', column='3')
            forecast_2_temp = tk.Label(self.lef_bottom, fg=self.foreground,
                                       bg=self.background,font=self.font_general, text=temps[2])
            forecast_2_temp.grid(row='3', column='3', padx=(0, 0))

            forecast_2_precip = tk.Label(self.lef_bottom, fg=self.foreground,
                                             bg=self.background,font=self.font_cat, text=precip_day[2])
            forecast_2_precip.grid(row='1', column='3', padx=(105, 0), pady=(0, 0))
        except Exception as e:
            print("display error: {}".format(e))  # debug
            logging.info('display outdoor Weather Ch only error: ')
            # pass
            
        # weather service indicator
        service_text = tk.Label(self.lef_bottom, fg=self.color_1,
                                bg=self.background, font=self.font_ws, text=self.weather_service)
        service_text.grid(row='4', column='1', columnspan='3', sticky='w',
                          pady=(0, 5), padx=(0, 5))

    def quit_button(self):
        # Quit button settings

        quit_image = self.outdoor.current_icon
        quitButton = tk.Menubutton(self.f_outdoor_temp, bg=self.background,
                                   fg=self.color_3, highlightthickness = 0, bd = 0, font=self.font_q,
                                   text = "X")  # command=self.root.quit
        menu = tk.Menu(quitButton, font=self.font_set, bg=self.background,
                       fg=self.foreground, bd = 0)
        quitButton.config(image=quit_image, menu = menu)  # image=quit_image,width="60",height="60"
        btnList = ['Settings', 'Refresh','Quit']
        for btn in btnList:
            menu.add_command(label=btn,  
                             command= lambda btn = btn: self.menuClicked(btn))
        quitButton.grid(column='1', row='4', sticky='sw', pady=(0, 5), padx=(130, 0))
        
    def menuClicked(self, btn):
        if btn == 'Settings':
            self.settings_dialog()
            print(btn)
            
        elif btn == 'Refresh':
            self.refresh_info()
            
        elif btn == 'Quit':
            self.root.quit()
            
    def settings_dialog(self):
        padradheadx = 20
        padradx = padradheadx + 10
        padradlabx = padradx + 40
        padgeny = 8
        self.settings_window = tk.Toplevel(master=self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry('700x430')
        self.settings_window.configure(bg = self.background)
        if self.fullscreen:
            self.root.withdraw()  # will leave the root alive, but only settings visible.
        self.settings_window.geometry("+%d+%d" % (self.root.winfo_rootx()+20, self.root.winfo_rooty()+10))

        zip_label = tk.Label(self.settings_window, bg=self.background, fg=self.foreground,
                             highlightthickness = 0, bd = 0, font=self.font_set, text="Address/Zip: ")
        zip_label.grid(column='1',row='1', sticky='w', padx=(10,0))
        self.zip_var = tk.StringVar(self.settings_window, value=self.code)
        input_zip=tk.Entry(self.settings_window, textvariable=self.zip_var, 
                           fg=self.background, font=self.font_set, width=20)
        input_zip.grid(column='1', row='1', sticky='w', pady=(padgeny, 0), padx=(175, 0))
        
        icon_label = tk.Label(self.settings_window, bg=self.background, fg=self.foreground, 
                              highlightthickness = 0, bd = 0, font=self.font_set, text="Icons Path: ")
        icon_label.grid(column='1',row='2', sticky='w', padx=(10, 0))
        self.icon_var = tk.StringVar(self.settings_window, value=self.icon_path)
        input_icon=tk.Entry(self.settings_window, textvariable=self.icon_var, 
                            fg=self.background, font=self.font_set, width=20)
        input_icon.grid(column='1', row='2', sticky='w', pady=(padgeny, 0), padx=(175, 0))
        
        ip_label = tk.Label(self.settings_window, bg=self.background, fg=self.foreground, 
                            highlightthickness = 0, bd = 0, font=self.font_set, text="Broker Host: ")
        ip_label.grid(column='1', row='3', sticky='w', padx=(10, 0))
        self.ip_var = tk.StringVar(self.settings_window, value=self.broker_add)
        input_ip=tk.Entry(self.settings_window, textvariable=self.ip_var,
                          fg=self.background, font=self.font_set, width=20)
        input_ip.grid(column='1', row='3', sticky='w', pady=(padgeny, 0), padx=(175, 0))
        
        api_label = tk.Label(self.settings_window, bg=self.background, fg=self.foreground, 
                             font=self.font_set, text="Check to use the API ")
        api_label.grid(column='1', row='4', sticky = 'w', pady=(padgeny, 0), padx=(30, 0))
        self.api_var = tk.BooleanVar()
        self.api_var.set(self.api)
        check_api = tk.Checkbutton(self.settings_window, bg=self.background,highlightthickness = 0, bd = 0,
                                   activebackground = self.background, var=self.api_var)
        check_api.grid(column='1', row='4', sticky='w', padx=(10, 0), pady=(padgeny, 0))
        
        # Full screen configure --------------------------------------
        fs_label = tk.Label(self.settings_window, bg=self.background, fg=self.foreground, 
                            font=self.font_set, text="Check for fullscreen")
        fs_label.grid(column='1', row='5', sticky='w', pady=(padgeny, 0), padx=(30, 0))
        self.fs_var = tk.BooleanVar()
        self.fs_var.set(self.fullscreen)
        check_fs = tk.Checkbutton(self.settings_window, bg=self.background,
                                  highlightthickness = 0, bd = 0, activebackground = self.background,
                                  var=self.fs_var) # onvalue="RGB", offvalue="YCbCr"
        check_fs.grid(column='1', row='5', sticky='w', pady=(padgeny, 0), padx=(10, 0))

        # Unit of measure configure --------------------------------------
        ms_label = tk.Label(self.settings_window, bg=self.background, fg=self.foreground, 
                            font=self.font_set, text="Unit of measure ")
        ms_label.grid(column='1',row='6', sticky='w', pady=(padgeny, 0), padx=(padradheadx, 0))
        self.ms_var = tk.StringVar()
        self.ms_var.set(self.unit)
        
        check_inlabel = tk.Label(self.settings_window, bg=self.background, fg=self.foreground, 
                                 font=self.font_set,text="Inch ")
        check_inlabel.grid(column='1', row='7', sticky='w', pady=(padgeny, 0), padx=(padradlabx, 0))
        check_in = tk.Radiobutton(self.settings_window, bg=self.background,
                                  highlightthickness = 0, bd = 0, activebackground = self.background,
                                  var=self.ms_var, value="in")
        check_in.grid(column='1', row='7', sticky='w', pady=(padgeny, 0),padx=(padradx, 0))
        
        check_mtlabel = tk.Label(self.settings_window, bg=self.background, fg=self.foreground, 
                                 font=self.font_set, text="Metric ")
        check_mtlabel.grid(column='1', row='8', sticky='w', pady=(padgeny, 0), padx=(padradlabx, 0))
        check_mt = tk.Radiobutton(self.settings_window, bg=self.background,
                                  highlightthickness = 0, bd = 0, activebackground = self.background,
                var=self.ms_var, value="metric")
        check_mt.grid(column='1', row='8', sticky='w', pady=(padgeny, 0), padx=(padradx, 0))
        
        # Forecast Source configure --------------------------------------
        padrightx = 40
        padrightradx = padrightx + 10
        padrightradlabx = padrightradx + 40
        fc_label = tk.Label(self.settings_window, bg=self.background, fg=self.foreground, 
                            font=self.font_set, text="Forecast source ")
        fc_label.grid(column='2', row='1', sticky='w', pady=(padgeny, 0), padx=(padrightx, 0))
        self.fc_var = tk.IntVar()
        self.fc_var.set(self.forecast_source)
        
        check_wulabel = tk.Label(self.settings_window, bg=self.background, fg=self.foreground, 
                                 font=self.font_set, text="Dark Sky")
        check_wulabel.grid(column='2', row='2', sticky='w', pady=(padgeny, 0), padx=(padrightradlabx, 0))
        check_wu = tk.Radiobutton(self.settings_window, bg=self.background,
                                  highlightthickness = 0, bd = 0, activebackground = self.background,
                                  var=self.fc_var, value=1)
        check_wu.grid(column='2', row='2', sticky='w', pady=(padgeny, 0), padx=(padrightradx, 0))
        
        check_wclabel = tk.Label(self.settings_window, bg=self.background, fg=self.foreground, 
                                 font=self.font_set, text="Weather Channel ")
        check_wclabel.grid(column='2', row='3', sticky='w', pady=(padgeny, 0), padx=(padrightradlabx, 0))
        check_wc = tk.Radiobutton(self.settings_window, bg=self.background,
                                  highlightthickness = 0, bd = 0, activebackground = self.background,
                                  var=self.fc_var, value=2)
        check_wc.grid(column='2', row='3', sticky='w', pady=(padgeny, 0), padx=(padrightradx, 0))
        
        # Past Temp configure --------------------------------------
        pst_label = tk.Label(self.settings_window, bg=self.background, fg=self.foreground, 
                             font=self.font_set, text="Past temp range ")
        pst_label.grid(column='2', row='4', sticky='w', pady=(padgeny, 0), padx=(padrightx, 0))
        self.pst_var = tk.StringVar()
        self.pst_var.set(self.temp_past)
        
        check_daylabel = tk.Label(self.settings_window, bg=self.background, fg=self.foreground,
                                  font=self.font_set, text="Day")
        check_daylabel.grid(column='2', row='5', sticky='w', pady=(padgeny,0), padx=(padrightradlabx, 0))
        check_day = tk.Radiobutton(self.settings_window, bg=self.background,
                                   highlightthickness = 0, bd = 0, activebackground = self.background,
                                   var=self.pst_var, value="day")
        check_day.grid(column='2', row='5', sticky='w', pady=(padgeny, 0), padx=(padrightradx, 0))
        
        check_monthlabel = tk.Label(self.settings_window, bg=self.background, fg=self.foreground, 
                                    font=self.font_set, text="Month")
        check_monthlabel.grid(column='2', row='6', sticky='w', pady=(padgeny, 0), padx=(padrightradlabx, 0))
        check_month= tk.Radiobutton(self.settings_window, bg=self.background,
                                    highlightthickness = 0, bd = 0, activebackground = self.background,
                                    var=self.pst_var, value="month")
        check_month.grid(column='2',row='6',sticky='w', pady=(padgeny, 0), padx=(padrightradx, 0))
        
        check_yearlabel = tk.Label(self.settings_window, bg=self.background, fg=self.foreground,
                                   font=self.font_set, text="Year")
        check_yearlabel.grid(column='2', row='7', sticky='w', pady=(padgeny, 0), padx=(padrightradlabx, 0))
        check_year= tk.Radiobutton(self.settings_window, bg=self.background,
                                   highlightthickness = 0, bd = 0, activebackground = self.background,
                                   var=self.pst_var, value="year")
        check_year.grid(column='2', row='7', sticky='w', pady=(padgeny, 0), padx=(padrightradx, 0))
        
        # Ok/Cancel configure --------------------------------------
        ok_button = tk.Button(self.settings_window, text="Ok",
                              bg=self.background, fg=self.foreground,
                              highlightthickness = 0, bd = 1, font=self.font_set,
                              command=lambda btn='ok_button': self.ok_cancel(btn))
        ok_button.grid(column='2',row='10', pady=(padgeny,0),padx=(195,0))
        cancel_button = tk.Button(self.settings_window, text="Cancel",
                                  bg=self.background, fg=self.foreground,
                                  highlightthickness = 0, bd = 1, font=self.font_set,
                                  command=lambda btn='cancel_button': self.ok_cancel(btn))
        cancel_button.grid(column='2',row='10', pady=(padgeny,0), padx=(20,0))

    def ok_cancel(self, btn):
        
        if btn == 'cancel_button':
            self.settings_window.destroy()
            print(btn)
        if btn == 'ok_button':
            zip_ = self.zip_var.get()
            icon = self.icon_var.get()
            ip = self.ip_var.get()
            api = self.api_var.get()
            fs = self.fs_var.get()
            ms = self.ms_var.get()
            fc = self.fc_var.get()
            pst = self.pst_var.get()

            output = {'code': zip_, 'icon_path': icon,
                      'broker_add': ip, 'api': api, 'fullscreen': fs,
                      'unit': ms, 'forecast_source': fc, 'temp_past': pst}
            self.write_config('config.json', output)
            self.settings_window.destroy()
            
        # if self.fullscreen == True:
        self.root.deiconify()  # returns root window when done with settings dialog

    def write_config(self, file_, dictionary,):
        tmod.save_json(file_, dictionary)
        self.read_config('config.json')
    
    def read_config(self, file_='config.json'):
            config = tmod.open_json(file_)
            config_value = [value for (key,value) in sorted(config.items())]           
            self.api, self.broker_add, self.code, self.forecast_source, self.fullscreen, self.icon_path, \
            self.temp_past, self.unit = config_value
            
        
if __name__ == "__main__":
    app = Main()
