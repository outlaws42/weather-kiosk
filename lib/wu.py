#! /usr/bin/env python3

# -*- coding: utf-8 -*-
import os
import sys
import datetime
import base64
import tkinter as tk
import logging
import requests
import lib.tmod as tmod
import lib.pywapi as pywapi
from lib.settings import key
logging.basicConfig(filename='wu.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Wu():
    degree_sign= '\N{DEGREE SIGN}'
    zip_code = '46764'
    pws = 'KINLARWI5'
    api = 'yes'  # yes = use api, no = don't use api
    api_key = key

    def __init__(self):
        pass

    def get_resource_path(self,rel_path):
        dir_of_py_file = os.path.dirname(sys.argv[0])
        rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
        abs_path_to_resource = os.path.abspath(rel_path_to_resource)
        return abs_path_to_resource

    def get_weather_info(self):
        try:
            if self.api == 'yes':
                f = requests.get('http://api.wunderground.com/api/{}/forecast/conditions/q/pws:{}.json'.format(self.api_key,self.pws))
                weather = f.json()
                weatherch = pywapi.get_weather_from_weather_com(self.zip_code, units = 'imperial')
                tmod.save_pickle('weather.cm',weather,'home')
                tmod.save_pickle('weatherch.cm',weatherch,'home')
                self.weather = tmod.open_pickle('weather.cm','home')
                self.weatherch = tmod.open_pickle('weatherch.cm','home')
                self.warning = ''
            else:
                self.weather = tmod.open_pickle('weather.cm','home')
                self.weatherch = tmod.open_pickle('weatherch.cm','home')
                self.warning = 'Using Saved Data'
        except:
           self.weather = tmod.open_pickle('weather.cm','home')
           self.weatherch = tmod.open_pickle('weatherch.cm','home') 
           self.warning = 'Using Saved Data'
           pass

    def gleen_info(self):
        # weather service
        self.weather_service = 'Provided by:  The Weather Underground'
        now = datetime.datetime.now()
        today7am = now.replace(hour=6, minute=59, second=0, microsecond=0)
        today6pm = now.replace(hour=17, minute=59, second=0, microsecond=0)
        if today7am <= now <= today6pm:
            self.current_icon = self.icon_select(self.weather['current_observation']['icon'])
        else:
            self.current_icon = self.icon_select('nt_{}'.format(self.weather['current_observation']['icon']))

        try:    # left weather info
            #brief discription of the weather
            self.status =self.weather['current_observation']['weather']
        except(KeyError,ValueError) as e:
            print('Status weather error:  ' + str(e)) #debug
            logging.info('Status weather error:  ' + str(e))
            self.status = 'Status ER'
            pass

        try:
            # outside temp .
            self.outdoor_temp = round(self.weather['current_observation']['temp_f'])
        except(KeyError,ValueError) as e:
            print('Outdoor temp weather error:  ' + str(e)) #debug
            logging.info('Outdoor temp weather error:  ' + str(e))
            self.outdoor_temp = '0'
            pass
        
        
        try:
            # right weather info
            # wind
            self.wind_dir = self.weather['current_observation']['wind_dir']
            self.wind_string = self.weather['current_observation']['wind_string']
            if self.wind_string == 'Calm':
                self.wind = "0"
                self.wind_speed = 0
            else:
                self.wind = self.wind_dir + "  at  " + str(self.weather['current_observation']['wind_mph'])
                self.wind_speed = self.weather['current_observation']['wind_mph']
            self.wind_gust =  self.weather['current_observation']['wind_gust_mph']
        except(KeyError,ValueError) as e:
            print('Wind weather error:  ' + str(e)) #debug
            logging.info('Wind weather error:  ' + str(e))
            self.wind='0'
            self.wind_speed = 0
            self.wind_gust = 'Gust ER'
            pass

        try:
            # dewpoint
            self.dewpoint = self.weather['current_observation']['dewpoint_f']
        except(KeyError, ValueError) as e:
            print('Dewpoint weather error:  ' + str(e)) #debug
            logging.info('Dewpoint weather error:  ' + str(e))
            self.dewpoint = "0"
            pass

        try:
            # Humidity
            self.humidity = self.weather['current_observation']['relative_humidity']
        except(KeyError,ValueError) as e:
            print('Humidity weather error:  ' + str(e)) #debug
            logging.info('Humidity check_weather error:  ' + str(e))
            self.humidity = "0"
            pass

        try:
            # Feels Like
            self.windchill = self.weather['current_observation']['feelslike_f']
            if self.windchill == '':
                self.windchill = self.outdoor_temp
            else:
                self.windchill = self.weather['current_observation']['feelslike_f']
        except(KeyError,ValueError) as e:
            self.windchill = "0"
            print('Windchill weather error:  ' + str(e)) #debug
            logging.info('Windchill weather error:  ' + str(e))
            pass

        try:
            # uv index
            self.uv =  self.weather['current_observation']['uv']
        except(KeyError,ValueError) as e:
            print('UV weather error:  ' + str(e)) #debug
            logging.info('UV weather error:  ' + str(e))
            self.uv = "UV ER"
            pass

        try:
            # barometer
            self.barometer_p =  self.weather['current_observation']['precip_today_in']
        except(KeyError) as e:
            print('Barometer weather error:  ' + str(e)) #debug
            logging.info('Barometer weather error:  ' + str(e))
            self.barometer_p = "0.0"
            self.barometer_dir = "0.0"
            pass


        try:
            # visibility
            self.visibility =  self.weather['current_observation']['visibility_mi']
        except(KeyError) as e:
            print('Visibility weather error:  ' + str(e)) #debug
            logging.info('Visibility weather error:  ' + str(e))
            self.visibility = "0"
            pass

        try:
            # sunrise/sunset
            self.heat_index = self.weather['current_observation']['heat_index_f']
        except(KeyError) as e:
            print('Sunrise weather error:  ' + str(e)) #debug
            logging.info('Sunrise weather error:  ' + str(e))
            self.forcasts_0_sunrise = "Sunrise ER"
            self.forcasts_0_sunset = "Sunset ER"
            pass
    
    def forecast_days(self):
        # forecast day
        forecast_day = []
        for i in range(3):
            temp = self.weather['forecast']['simpleforecast']['forecastday'][i]['date']['weekday_short']
            forecast_day.append(temp)
        return forecast_day
        
    def forecast_temp(self):    
        forecast = []
        for i in range(3):
            temp = '{}{}/{}{}'.format(self.weather['forecast']['simpleforecast']['forecastday'][i]['high']['fahrenheit'],self.degree_sign,self.weather['forecast']['simpleforecast']['forecastday'][i]['low']['fahrenheit'],self.degree_sign)
            forecast.append(temp)
        return forecast
    
    def forecast_code(self):
        forecast_day_code = []
        for i in range(6):
            temp = self.weather['forecast']['txt_forecast']['forecastday'][i]['icon']
            forecast_day_code.append(temp)
        return forecast_day_code
        
    def forecast_precip_day(self):
        forecast_pr = []
        for i in range(3):
            temp = self.weatherch['forecasts'][i]['day']['chance_precip'] + '%'
            forecast_pr.append(temp)
        return forecast_pr
        
    def forecast_precip_night(self):
        forecast_pr = []
        for i in range(3):
            temp = self.weatherch['forecasts'][i]['night']['chance_precip'] + '%'
            forecast_pr.append(temp)
        return forecast_pr
        
    
    def forecast(self):
        
        day_code = self.forecast_code()
        # day 0   
        # weather condition icon
        self.forecast_0_day_icon=self.icon_select(day_code[0])
        self.forecast_0_night_icon=self.icon_select(day_code[1])

        # day 1       
        # weather condition icon
        self.forecast_1_day_icon=self.icon_select(day_code[2])
        self.forecast_1_night_icon=self.icon_select(day_code[3])

        # day 2
        # weather condition icon
        self.forecast_2_day_icon=self.icon_select(day_code[4])
        self.forecast_2_night_icon=self.icon_select(day_code[5])


    def icon_select(self,icon_code):
        try:

            icon= tk.PhotoImage(file=self.get_resource_path('Images/65/wu/{}.png'.format(icon_code)))
        except:
            icon = tk.PhotoImage(file=self.get_resource_path('Images/65/na.png'))
        return(icon)


if __name__ == "__main__":
    app = Wu()
