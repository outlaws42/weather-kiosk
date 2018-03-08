#! /usr/bin/env python3

# -*- coding: utf-8 -*-
import os
import tkinter as tk
import lib.pywapi as pywapi
import logging
logging.basicConfig(filename='noaa.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Noaa():
    degree_sign= '\N{DEGREE SIGN}'
    zip_code = '46764'

    def __init__(self):
        print('This is noaa weather')
        #self.get_weather_info() #debug
        #self.gleen_info() # debug

    def get_weather_info(self):
        self.weather = pywapi.get_weather_from_noaa('KFWA')
        #for i,b in self.weather.items():
            #print(i,": ",b)

        #return self.weather

    def gleen_info(self):


            # noaa get info
            #self.weather = pywapi.get_weather_from_noaa('KFWA')
            self.weather_service = 'Provided by:  NOAA Weather'

            try:    # left weather info
                # brief discription of the weather
                self.status =self.weather['weather']
                print(self.status)
            except(KeyError) as e:
                print('Status weather error:  ' + str(e)) #debug
                logging.info('Status weather error:  ' + str(e))
                self.status = 'Status ER'
                pass

            try:
                # Outside Temp
                self.outdoor_temp = str(round(float(self.weather['temp_f'])))
                print(self.outdoor_temp)
            except(KeyError) as e:
                print('Outdoor temp weather error:  ' + str(e)) #debug
                logging.info('Outdoor temp weather error:  ' + str(e))
                self.outdoor_temp = '0'
                pass
            try:
                # wind
                self.wind_dir = self.weather['wind_dir']
                self.wind_speed = str(round(float(self.weather['wind_mph'])))
                if self.wind_speed == '0':
                    self.wind = "0"
                else:
                    if self.wind_dir == 'Southwest':
                        self.wind = "SW  at  " + self.wind_speed
                    elif self.wind_dir == 'South':
                        self.wind = "S  at  " + self.wind_speed
                    elif self.wind_dir == 'Southeast':
                        self.wind = "SE  at  " + self.wind_speed
                    elif self.wind_dir == 'Northwest':
                        self.wind = "NW  at  " + self.wind_speed
                    elif self.wind_dir == 'North':
                        self.wind = "N  at  " + self.wind_speed
                    elif self.wind_dir == 'Northeast':
                        self.wind = "NE  at  " + self.wind_speed
                    elif self.wind_dir == 'East':
                        self.wind = "E  at  " + self.wind_speed
                    elif self.wind_dir == 'West':
                        self.wind = "W  at  " + self.wind_speed
                    else:
                        self.wind = "?  at  " + self.wind_speed
            except(KeyError) as e:
                print('Wind weather error:  ' + str(e)) #debug
                logging.info('Wind weather error:  ' + str(e))
                self.wind='0'
                self.wind_speed = 0
                self.wind_gust = 'Gust ER'
                pass

            try:
                # Last updated
                self.update = self.weather['observation_time']
                self.update_list = list(self.update) # convert to list
                self.update_list[:-12] = [] # slice list to show what we want
                self.update_list[6:] = [] # slice list to show what we want
                self.updated = "Updated: " + "".join(self.update_list) + 'AM' # join back to a string
            except(KeyError) as e:
                print('Update weather error:  ' + str(e)) #debug
                logging.info('Update weather error:  ' + str(e))
                self.update = "Updated: Error"
                pass

            try:
                # dewpoint
                self.dewpoint = str(round(float(self.weather['dewpoint_f'])))
            except(KeyError) as e:
                print('Dewpoint weather error:  ' + str(e)) #debug
                logging.info('Dewpoint weather error:  ' + str(e))
                self.dewpoint = "0"
                pass

            try:
                # Humidity
                self.humidity = self.weather['relative_humidity']
            except(KeyError) as e:
                print('Humidity weather error:  ' + str(e)) #debug
                logging.info('Humidity check_weather error:  ' + str(e))
                self.humidity = "0"
                pass

            try:
                # Feels Like
                self.windchill = self.weather['windchill_f']
            except(KeyError) as e:
                print('Windchill weather error:  ' + str(e)) #debug
                logging.info('Windchill weather error:  ' + str(e))
                self.windchill = "0"
                pass

            try:
                # pressure
                self.barometer_p = self.weather['pressure_in']
            except(KeyError) as e:
                print('Barometer weather error:  ' + str(e)) #debug
                logging.info('Barometer weather error:  ' + str(e))
                self.barometer_p = "0.0"
                self.barometer_dir = "0.0"
                pass




if __name__ == "__main__":
    app = Noaa()
