#! /usr/bin/env python3

# -*- coding: utf-8 -*-
import datetime
import tkinter as tk
import logging
import requests
import lib.tmod as tmod
from lib.settings import key, pws
logging.basicConfig(filename='wu.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Wu():
    degree_sign= '\N{DEGREE SIGN}'
    pws = pws
    api = 'no'  # yes = use api, no = don't use api
    api_key = key

    def __init__(self):
        pass

    def get_weather_info(self):
        try:
            if self.api == 'yes':
                f = requests.get('http://api.wunderground.com/api/{}/astronomy/forecast/conditions/q/pws:{}.json'.format(self.api_key,self.pws))
                weather = f.json()
                tmod.save_pickle('weather.cm',weather,'home')
                self.weather = tmod.open_pickle('weather.cm','home')
                self.warning = ''
            else:
                self.weather = tmod.open_pickle('weather.cm','home')
                self.warning = 'Using Saved Data'
        except:
           self.weather = tmod.open_pickle('weather.cm','home') 
           self.warning = 'Using Saved Data'
           pass

    def gleen_info(self):
        # weather service
        self.weather_service = 'Provided by:  The Weather Underground'
        
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
                self.wind = "Calm"
                self.wind_speed = 0
            else:
                self.wind_speed = self.weather['current_observation']['wind_mph']
                self.wind = '{} at {}mph'.format(self.wind_dir,str(round(self.wind_speed)))
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
        except(KeyError,ValueError) as e:
            self.windchill = "0"
            print('Windchill weather error:  ' + str(e)) #debug
            logging.info('Windchill weather error:  ' + str(e))
            pass

        try:
            # Precip Today
            self.precip =  self.weather['current_observation']['precip_today_in']
        except(KeyError) as e:
            print('Barometer weather error:  ' + str(e)) #debug
            logging.info('Barometer weather error:  ' + str(e))
            self.precip = "0.0"
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

        # Current Icon      
        now_morn_eve = self.day_night()
        now, morning, evening = now_morn_eve
        if morning <= now <= evening:
            self.current_icon = self.icon_select(self.weather['current_observation']['icon'])
        else:
            self.current_icon = self.icon_select('nt_{}'.format(self.weather['current_observation']['icon']))
    
    def day_night(self):
        sunrise_hour =self.weather['sun_phase']['sunrise']['hour']
        sunrise_min =self.weather['sun_phase']['sunrise']['minute']
        sunset_hour =self.weather['sun_phase']['sunset']['hour']
        sunset_min =self.weather['sun_phase']['sunset']['minute']
        now = datetime.datetime.now()
        morning = now.replace(hour=int(sunrise_hour), 
            minute=int(sunrise_min), second=0, microsecond=0)
        evening = now.replace(hour=int(sunset_hour), 
            minute=int(sunset_min), second=0, microsecond=0)
        return now, morning, evening
        
    def forecast_days(self):
        # forecast day for 3 days
        forecast_day = []
        for i in range(3):
            temp = self.weather['forecast']['simpleforecast']['forecastday'][i]['date']['weekday_short']
            forecast_day.append(temp)
        return forecast_day
        
    def forecast_temp(self):
        # forecast high / low temp for 3 days    
        forecast = []
        for i in range(3):
            temp = '{}{}/{}{}'.format(self.weather['forecast']['simpleforecast']['forecastday'][i]['high']['fahrenheit'],self.degree_sign,self.weather['forecast']['simpleforecast']['forecastday'][i]['low']['fahrenheit'],self.degree_sign)
            forecast.append(temp)
        print(forecast)
        return forecast
    
    def forecast_code(self):
        # forecast code is day / night key word starting at index 0 for 3 days
        forecast_day_code = []
        for i in range(6):
            temp = self.weather['forecast']['txt_forecast']['forecastday'][i]['icon']
            forecast_day_code.append(temp)
        return forecast_day_code
        
    def forecast_precip_day(self):
        # pop is day night chance of precip starting at index 0 for 3 days
        forecast_pr = []
        for i in range(6):
            temp = self.weather['forecast']['txt_forecast']['forecastday'][i]['pop'] + '%'
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
            icon= tk.PhotoImage(file=tmod.get_resource_path('Images/65/wu/{}.png'.format(icon_code)))
        except:
            icon = tk.PhotoImage(file=tmod.get_resource_path('Images/65/na.png'))
        return(icon)


if __name__ == "__main__":
    app = Wu()
