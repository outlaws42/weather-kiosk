#! /usr/bin/env python3

# -*- coding: utf-8 -*-
import datetime
import math
import tkinter as tk
import logging
import requests
import lib.pywapi as pywapi
import lib.tmod as tmod
from lib.api import key
logging.basicConfig(filename='wu.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class Wu():
    degree_sign = '\N{DEGREE SIGN}'

    def __init__(self):
        # self.get_weather_info()
        pass

    def get_weather_info(self):
        self.read_config()
        try:
            if self.api == True:
                
                f = requests.get('https://api.darksky.net/forecast/{}/{}'.format(key,self.pws))
                weather = f.json()
                tmod.save_json('weather.json',weather,'home')
                self.weather = tmod.open_json('weather.json','home')
                self.warning = ''
            else:
                self.weather = tmod.open_json('weather.json', 'home')
                self.warning = 'NAPI Using Saved Data'
                print(self.weather['daily']['data'][0]['apparentTemperatureHigh'])
        except Exception as e:
           self.weather = tmod.open_json('weather.json', 'home')
           self.warning = 'ER Using Saved Data'
           logging.info('Collect weather error:  ' + str(e))
           pass
        self.units_of_measure()
    
    def units_of_measure(self):
        if self.unit == 'metric':
            self.temp_measure = 'c' 
            self.speed = 'kph'
            self.measure = 'mm'
        else:
            self.temp_measure = 'f' 
            self.speed = 'mph'
            self.measure = 'in'
        
    def gleen_info(self):
        # weather service
        self.weather_service = "Provided by:   Dark Sky"  # https://darksky.net/poweredby/
        
        try:    # left weather info
            # brief description of the weather
            self.status = self.weather['currently']['summary']
            print("status: {}".format(self.status))
        except(KeyError, ValueError) as e:
            print('Status weather error:  ' + str(e)) #debug
            logging.info('Status weather error:  ' + str(e))
            self.status = 'Status ER'
            pass

        try:
            # outside temp .
            self.outdoor_temp = round(self.weather['currently']['temperature'])
            print("Temp: {}{}".format(self.outdoor_temp, self.degree_sign))
        except(KeyError,ValueError) as e:
            print('Outdoor temp weather error:  ' + str(e)) #debug
            logging.info('Outdoor temp weather error:  ' + str(e))
            self.outdoor_temp = '0'
            pass
        
        
        try:
            # right weather info
            # wind
            self.wind_dir = self.weather['currently']['windBearing']
            print("wind Direction: {}".format(math.radians(self.wind_dir)))
            self.wind_speed = self.weather['currently']['windSpeed']
            print("Wind Speed: {}".format(self.wind_speed))
            if self.wind_speed == 0:
                self.wind = "Calm"
            else:
                self.wind = '{} at {}{}'.format(self.wind_dir, str(round(self.wind_speed)), self.speed)
            self.wind_gust = self.weather['currently']['windGust']
            print("wind Gust: {}".format(self.wind_gust))
        except(KeyError, ValueError) as e:
            print('Wind weather error:  ' + str(e)) #debug
            logging.info('Wind weather error:  ' + str(e))
            self.wind='Calm'
            self.wind_speed = 0
            self.wind_gust = 0
            pass

        try:
            # dewpoint
            self.dewpoint = round(self.weather['currently']['dewPoint'])
            print("Dewpoint: {}".format(self.dewpoint))
        except(KeyError, ValueError) as e:
            print('Dewpoint weather error:  ' + str(e)) #debug
            logging.info('Dewpoint weather error:  ' + str(e))
            self.dewpoint = "0"
            pass

        try:
            # Humidity
            self.humidity = self.weather['currently']['humidity']
            print("Humidity: {}".format(self.humidity))
        except(KeyError,ValueError) as e:
            print('Humidity weather error:  ' + str(e)) #debug
            logging.info('Humidity check_weather error:  ' + str(e))
            self.humidity = "0"
            pass

        try:
            # Feels Like
            self.windchill = round(float(self.weather['currently']['apparentTemperature']))
            print("windchill: {}".format(self.windchill))
            # print('This is float {}'.format(self.windchill))
            # self.windchill = self.weather['current_observation']['feelslike_{}'.format(self.temp_measure)]
            # print('This int {}'.format(self.windchill))
        except(KeyError,ValueError) as e:
            self.windchill = self.outdoor_temp
            print('This is outdoor temp {}'.format(self.windchill))
            print('Windchill weather error:  ' + str(e)) #debug
            logging.info('Windchill weather error:  ' + str(e))
            pass

        try:
            # Precip Today
            self.precip =  self.weather['currently']['precipIntensity']
            print("Precip: {}".format(self.precip))
        except(KeyError) as e:
            print('Precip weather error:  ' + str(e)) #debug
            logging.info('Precip weather error:  ' + str(e))
            self.precip = "0.0"
            self.barometer_dir = "0.0"
            pass

        # Current Icon      
        try:
            now_morn_eve = self.day_night()
            now, morning, evening = now_morn_eve
            if morning <= now <= evening:
                self.current_icon = self.icon_select(self.weather['currently']['icon'])
            else:
                self.current_icon = self.icon_select(self.weather['currently']['icon'])
        except(Exception) as e:
            print('current Icon error {}'.format(e))
            self.current_icon = self.icon_select('na')
                
    def day_night(self):
        try:
            sunrise_hour =self.weather['sun_phase']['sunrise']['hour']
            sunrise_min =self.weather['sun_phase']['sunrise']['minute']
            sunset_hour =self.weather['sun_phase']['sunset']['hour']
            sunset_min =self.weather['sun_phase']['sunset']['minute']
        except(Exception) as e:
            print('sunrise-Set error {}'.format(e))
            sunrise_hour = "6"
            sunrise_min = "18"
            sunset_hour = "20"
            sunset_min = "59"
            
        now = datetime.datetime.now()
        morning = now.replace(hour=int(sunrise_hour), 
            minute=int(sunrise_min), second=0, microsecond=0)
        evening = now.replace(hour=int(sunset_hour), 
            minute=int(sunset_min), second=0, microsecond=0)
        return now, morning, evening
        
    def forecast_days(self, days =3):
        # forecast day for 3 days
        forecast_day = []
        for i in range(days):
            tstamp = self.weather['daily']['data'][i]['time']
            day = datetime.datetime.utcfromtimestamp(tstamp).strftime('%a')
            print("forcastdays: {}".format(day))

            forecast_day.append(day)
        print(forecast_day)
        return forecast_day
        
    def forecast_temp(self, days = 3):
        # forecast high / low temp for 3 days    
        forecast = []
        if self.temp_measure == 'c':
            measure = 'celsius'
        else:
            measure = 'fahrenheit'
        
        for i in range(days):
            temp = '{}{}/{}{}'.format(round(self.weather['daily']['data'][i]['apparentTemperatureHigh']),
                                      self.degree_sign, round(self.weather['daily']['data'][i]['apparentTemperatureLow']),
                                      self.degree_sign)
            forecast.append(temp)
        print(forecast)
        return forecast
    
    def forecast_code(self, days = 3):
        # forecast code is day / night key word starting at index 0 for 3 days
        forecast_day_code = []
        for i in range(days):
            temp = self.weather['daily']['data'][i]['icon']
            forecast_day_code.append(temp)
        return forecast_day_code
        
    def forecast_precip_day(self, days=3):
        # pop is day night chance of precip starting at index 0 for 3 days
        forecast_pr = []
        for i in range(days):

            temp = self.weather['daily']['data'][i]['precipProbability']
            temp_calc = (float(temp)*100)
            forecast_pr.append('{}%'.format(int(temp_calc)))
        print(forecast_pr)
        return forecast_pr

    def forecast(self):
        day_code = self.forecast_code()
        # day 0   
        # weather condition icon
        self.forecast_0_day_icon=self.icon_select(day_code[0])

        # day 1       
        # weather condition icon
        self.forecast_1_day_icon=self.icon_select(day_code[1])
       
        # day 2
        # weather condition icon
        self.forecast_2_day_icon=self.icon_select(day_code[2])
 

    def icon_select(self,icon_code):
        try:
            icon= tk.PhotoImage(file=tmod.get_resource_path('{}/{}.png'.format(self.icon_path,icon_code)))
        except:
            icon = tk.PhotoImage(file=tmod.get_resource_path('{}/na.png'.format(self.icon_path)))
        return(icon)
        
    def read_config(self,file_='config.json'):
            config = tmod.open_json(file_)
            config_value = [value for (key,value) in sorted(config.items())]
            # pws icon_path api unit code
            self.api = config_value[0]
            #self.code = config_value[2]
            self.icon_path = config_value[5]
            self.pws = config_value[6]
            self.unit = config_value[8]

            
            


if __name__ == "__main__":
    app = Wu()
