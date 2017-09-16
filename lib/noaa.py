#! /usr/bin/env python3

# -*- coding: utf-8 -*-
import os
import tkinter as tk
import pywapi
import logging
logging.basicConfig(filename='noaa.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Noaa():
    degree_sign= '\N{DEGREE SIGN}'
    # Path variables
  
    # weather/forcast images
    icon_clear_night_65 = os.path.join(os.path.expanduser('~'),'Weather','Images','65','clear_night_65.png')
    icon_cloudy_65 = os.path.join(os.path.expanduser('~'),'Weather','Images','65','cloudy_65.png')
    icon_cloudy_day_65 = os.path.join(os.path.expanduser('~'),'Weather','Images','65','cloudy_day_65.png')
    icon_cloudy_night_65 = os.path.join(os.path.expanduser('~'),'Weather','Images','65','cloudy_night_65.png')
    icon_cold_65 = os.path.join(os.path.expanduser('~'),'Weather','Images','65','cold_65.png')
    icon_hot_65 = os.path.join(os.path.expanduser('~'),'Weather','Images','65','hot_65.png')
    icon_fog_65 = os.path.join(os.path.expanduser('~'),'Weather','Images','65','fog_65.png')
    icon_rain_65 = os.path.join(os.path.expanduser('~'),'Weather','Images','65','rain_65.png')
    icon_snow_65 = os.path.join(os.path.expanduser('~'),'Weather','Images','65','snow_65.png')
    icon_sunny_65 = os.path.join(os.path.expanduser('~'),'Weather','Images','65','sunny_65.png')
    icon_thunderstorms_65 = os.path.join(os.path.expanduser('~'),'Weather','Images','65','thunderstorms_65.png')
    icon_thunderstorms_severe_65 = os.path.join(os.path.expanduser('~'),'Weather','Images','65','thunderstorms_severe_65.png')
    icon_tornado_65 = os.path.join(os.path.expanduser('~'),'Weather','Images','65','tornado_65.png')
    icon_wind_65 = os.path.join(os.path.expanduser('~'),'Weather','Images','65','wind_65.png')
    
      
    def __init__(self):
        print('This is noaa weather')
        #self.get_weather_info() #debug
        #self.gleen_info() # debug

    def get_weather_info(self):
        self.weather = pywapi.get_weather_from_noaa('KFWA')
        #return self.weather
        
    def gleen_info(self):

        try:
            # noaa get info
            #self.weather = pywapi.get_weather_from_noaa('KFWA')
            self.weather_service = 'Provided by:  NOAA Weather'
        
            # wind
            self.wind_dir = self.weather['wind_dir']
            self.wind = self.wind_dir + "  at  " + self.weather['wind_mph'] + " mph "

            # Brings outside temp elements together.
            self.outdoor_temp = str(round(float(self.weather['temp_f']))) + self.degree_sign

            # brief discription of the weather
            self.status = self.weather['weather']

            # Last updated
            self.update = self.weather['observation_time']
            self.update_list = list(self.update) # convert to list
            self.update_list[11:-12] = [] # slice list to show what we want
            self.updated = "".join(self.update_list) # join back to a string

            # dewpoint
            self.dewpoint = self.weather['dewpoint_f'] + self.degree_sign

            # Humidity
            self.humidity = self.weather['relative_humidity'] +'%'

            try:
            # wind chill
                self.windchill = self.weather['windchill_f'] + self.degree_sign
            except(KeyError) as e:
                print('noaa check_weather error:  ' + str(e)) #debug
                logging.info('noaa check_weather error:  ' + str(e))
                self.windchill = self.outdoor_temp

            
            # pressure
            self.pressure = self.weather['pressure_in'] 
        except(KeyError) as e:
            print('check_weather error:  ' + str(e)) #debug
            logging.info('check_weather error:  ' + str(e))
            pass
        
        
    

if __name__ == "__main__":
    app = Noaa()    

