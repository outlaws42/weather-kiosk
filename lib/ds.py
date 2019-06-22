#! /usr/bin/env python3

# -*- coding: utf-8 -*-
import datetime
import geopy.geocoders
from geopy.geocoders import Nominatim
import tkinter as tk
import logging
import requests
import lib.tmod as tmod
from lib.api import key
logging.basicConfig(filename='wu.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class Wu():
    degree_sign = '\N{DEGREE SIGN}'

    def __init__(self):
        # self.get_weather_info()
        pass

    def geolocation(self, address):
        try:
            geolocator = Nominatim(user_agent = "weather kiosk")
            # location = geolocator.reverse("41.232921, -85.649106")
            location = geolocator.geocode(address)
            print(len(address))
            addressout = location.address
            addresslist = addressout.split(',')
            if len(address) <= 5:
                self.city = addresslist[0]
            else:
                self.city = addresslist[2]
            print(self.city)
            print(addresslist)
            print(addressout)
            return location.latitude, location.longitude
        except Exception as e:
            print(e)
            return 41.232921, -85.649106

    def get_weather_info(self):
        self.read_config()
        location = self.geolocation(self.code)
        lat, long = location
        print(location)
        try:
            if self.api == True:
                f = requests.get('https://api.darksky.net/forecast/{}/{},{}'.format(key, lat, long))
                weather = f.json()
                tmod.save_json('weather.json', weather, 'home')
                self.weather = tmod.open_json('weather.json','home')
                self.warning = ''
            else:
                self.weather = tmod.open_json('weather.json', 'home')
                self.warning = 'NAPI Using Saved Data'
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
        except(KeyError, ValueError) as e:
            print('Status weather error:  ' + str(e)) #debug
            logging.info('Status weather error:  ' + str(e))
            self.status = 'Status ER'
            pass

        try:
            # outside temp .
            self.outdoor_temp = round(self.weather['currently']['temperature'])
        except(KeyError,ValueError) as e:
            print('Outdoor temp weather error:  ' + str(e)) #debug
            logging.info('Outdoor temp weather error:  ' + str(e))
            self.outdoor_temp = '0'
            pass
        
        
        try:
            # right weather info
            # wind
            import_wind_dir = self.weather['currently']['windBearing']
            self.wind_dir = self.degtocompass(import_wind_dir)
            self.wind_speed = self.weather['currently']['windSpeed']
            if self.wind_speed == 0:
                self.wind = "Calm"
            else:
                self.wind = '{} at {}{}'.format(self.wind_dir, str(round(self.wind_speed)), self.speed)
            self.wind_gust = self.weather['currently']['windGust']
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
        except(KeyError, ValueError) as e:
            print('Dewpoint weather error:  ' + str(e)) #debug
            logging.info('Dewpoint weather error:  ' + str(e))
            self.dewpoint = "0"
            pass

        try:
            # Humidity
            self.humidity = '{}%'.format(round(self.weather['currently']['humidity']*100))
        except(KeyError,ValueError) as e:
            print('Humidity weather error:  ' + str(e)) #debug
            logging.info('Humidity check_weather error:  ' + str(e))
            self.humidity = "0"
            pass

        try:
            # Feels Like
            self.windchill = round(float(self.weather['currently']['apparentTemperature']))
        except(KeyError,ValueError) as e:
            self.windchill = self.outdoor_temp
            print('This is outdoor temp {}'.format(self.windchill))
            print('Windchill weather error:  ' + str(e)) #debug
            logging.info('Windchill weather error:  ' + str(e))
            pass

        try:
            # Precip Today
            self.precip =  self.weather['currently']['precipIntensity']
        except(KeyError) as e:
            print('Precip weather error:  ' + str(e)) #debug
            logging.info('Precip weather error:  ' + str(e))
            self.precip = "0.0"
            self.barometer_dir = "0.0"
            pass

        # Current Icon 
        self.status_icon =  self.weather['currently']['icon']    
        self.current_icon = self.icon_select(self.status_icon)
                
    def degtocompass(self, degrees):
        direction = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
                     "N"]
        val = int((degrees / 22.5) + .5)
        return direction[(val % 16)]

    def forecast_days(self, days =3):
        # forecast day for 3 days
        forecast_day = []
        for i in range(days):
            tstamp = self.weather['daily']['data'][i]['time']
            day = datetime.datetime.utcfromtimestamp(tstamp).strftime('%a')
            forecast_day.append(day)
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

    def write_config(self, file_, dictionary,):
        tmod.save_json(file_, dictionary)
        self.read_config('config.json')
        
    def read_config(self, file_='config.json'):
            config = tmod.open_json(file_)
            config_value = [value for (key,value) in sorted(config.items())]
            # pws icon_path api unit code
            self.api = config_value[0]
            self.code = config_value[2]
            self.icon_path = config_value[5]
            self.pws = config_value[6]
            self.unit = config_value[7]

            
            


if __name__ == "__main__":
    app = Wu()
