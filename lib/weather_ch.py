#! /usr/bin/env python3

# -*- coding: utf-8 -*-
import os
import sys
import tkinter as tk
import configparser
import pywapi
import logging
import inspect
logging.basicConfig(filename='noaa.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class WeatherCh():
    degree_sign= '\N{DEGREE SIGN}'
    zip_code = '46764'

    def __init__(self):
        pass

    def get_resource_path(self,rel_path):
        dir_of_py_file = os.path.dirname(sys.argv[0])
        rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
        abs_path_to_resource = os.path.abspath(rel_path_to_resource)
        return abs_path_to_resource

    def get_weather_info(self):
        self.weather = pywapi.get_weather_from_weather_com(self.zip_code, units = 'imperial')

    def gleen_info(self):

        # weather service
        self.weather_service = 'Provided by:  The Weather Channel'

        try:    # left weather info
            # brief discription of the weather
            self.status =self.weather['current_conditions']['text']
        except(KeyError) as e:
            print('Status weather error:  ' + str(e)) #debug
            logging.info('Status weather error:  ' + str(e))
            self.status = 'Status ER'
            pass

        try:
            # outside temp .
            self.outdoor_temp = self.weather['current_conditions']['temperature']
        except(KeyError) as e:
            print('Outdoor temp weather error:  ' + str(e)) #debug
            logging.info('Outdoor temp weather error:  ' + str(e))
            self.outdoor_temp = '0'
            pass

        try:
            # write weather info
            # wind
            self.wind_dir = self.weather['current_conditions']['wind']['text']
            if self.wind_dir == 'CALM':
                self.wind = "0"
                self.wind_speed = 0
            else:
                self.wind = self.wind_dir + "  at  " + self.weather['current_conditions']['wind']['speed']
                self.wind_speed = self.weather['current_conditions']['wind']['speed']
            self.wind_gust =  self.weather['current_conditions']['wind']['gust']
        except(KeyError) as e:
            print('Wind weather error:  ' + str(e)) #debug
            logging.info('Wind weather error:  ' + str(e))
            self.wind='0'
            self.wind_speed = 0
            self.wind_gust = 'Gust ER'
            pass

        try:

            # Last updated
            self.update = "Updated:  " + self.weather['current_conditions']['last_updated']
            self.update_list = list(self.update) # convert to list
            self.update_list[9:-12] = [] # slice list to show what we want
            self.update_list[18:] = [] # slice list to show what we want
            self.updated ="".join(self.update_list) # join back to a string
        except(KeyError) as e:
            print('Update weather error:  ' + str(e)) #debug
            logging.info('Update weather error:  ' + str(e))
            self.update = "Updated: Error"
            pass

        try:
            # dewpoint
            self.dewpoint = self.weather['current_conditions']['dewpoint']
        except(KeyError) as e:
            print('Dewpoint weather error:  ' + str(e)) #debug
            logging.info('Dewpoint weather error:  ' + str(e))
            self.dewpoint = "0"
            pass

        try:
            # Humidity
            self.humidity = self.weather['current_conditions']['humidity']
        except(KeyError) as e:
            print('Humidity weather error:  ' + str(e)) #debug
            logging.info('Humidity check_weather error:  ' + str(e))
            self.humidity = "0"
            pass

        try:
            # Feels Like
            self.windchill = self.weather['current_conditions']['feels_like']
        except(KeyError) as e:
            print('Windchill weather error:  ' + str(e)) #debug
            logging.info('Windchill weather error:  ' + str(e))
            self.windchill = "0"
            pass

        try:
            # uv index
            self.uv =  self.weather['current_conditions']['uv']['text']
        except(KeyError) as e:
            print('UV weather error:  ' + str(e)) #debug
            logging.info('UV weather error:  ' + str(e))
            self.uv = "UV ER"
            pass

        try:
            # barometer
            self.barometer_p =  self.weather['current_conditions']['barometer']['reading']
            self.barometer_dir =  self.weather['current_conditions']['barometer']['direction']
        except(KeyError) as e:
            print('Barometer weather error:  ' + str(e)) #debug
            logging.info('Barometer weather error:  ' + str(e))
            self.barometer_p = "0.0"
            self.barometer_dir = "0.0"
            pass

        try:
            # moon phase
            self.moon_phase =  self.weather['current_conditions']['moon_phase']['text']
        except(KeyError) as e:
            print('Moon weather error:  ' + str(e)) #debug
            logging.info('Moon weather error:  ' + str(e))
            self.moon_phase = "Moon ER"
            pass

        try:
            # visibility
            self.visibility =  self.weather['current_conditions']['visibility']
        except(KeyError) as e:
            print('Visibility weather error:  ' + str(e)) #debug
            logging.info('Visibility weather error:  ' + str(e))
            self.visibility = "0"
            pass

        try:
            # sunrise/sunset
            self.forcasts_0_sunrise = self.weather['forecasts'][0]['sunrise']
            self.forcasts_0_sunset = self.weather['forecasts'][0]['sunset']
        except(KeyError) as e:
            print('Sunrise weather error:  ' + str(e)) #debug
            logging.info('Sunrise weather error:  ' + str(e))
            self.forcasts_0_sunrise = "Sunrise ER"
            self.forcasts_0_sunset = "Sunset ER"
            pass

    def forecast(self):
        try:
            # forecasts
            # day 0
            # weather conditon codes
            self.forecast_0_day_code = self.weather['forecasts'][0]['day']['icon']
            self.forecast_0_night_code = self.weather['forecasts'][0]['night']['icon']
            print(self.forecast_0_day_code)
            print(self.forecast_0_night_code)

            # Precip %
            self.forecast_0_night_precip = self.weather['forecasts'][0]['night']['chance_precip'] + '%'
            self.forecast_0_day_precip = self.weather['forecasts'][0]['day']['chance_precip'] + '%'

            # slice day 0
            self.forecast_0_day_long = self.weather['forecasts'][0]['day_of_week']
            self.forecast_0_list = list(self.forecast_0_day_long) # convert to list
            self.forecast_0_list[3:] = [] # slice list to show what we want
            self.forecast_0_day = "".join(self.forecast_0_list) # join back to a string

            # temp high/low
            self.forecast_0 = self.weather['forecasts'][0]['high'] + self.degree_sign + '/' + self.weather['forecasts'][0]['low'] + self.degree_sign

        except(KeyError) as e:
            print('day 1 weather error:  ' + str(e)) #debug
            logging.info('day 1 weather error:  ' + str(e))
            self.forecast_0_day_code = "99"
            self.forecast_0_night_code = "99"
            self.forecast_0_night_precip = "ER"
            self.forecast_0_day_precip = "ER"
            self.forecast_0_day = "ER"
            self.forecast_0 = "ER/ER"
            pass
        # weather condition icon
        self.forecast_0_day_icon=self.icon_select(self.forecast_0_day_code)
        self.forecast_0_night_icon=self.icon_select(self.forecast_0_night_code)

        try:
            # day 1
            # weather conditon codes
            self.forecast_1_day_code = self.weather['forecasts'][1]['day']['icon']
            self.forecast_1_night_code = self.weather['forecasts'][1]['night']['icon']

            # Precip %
            self.forecast_1_night_precip = self.weather['forecasts'][1]['night']['chance_precip'] + '%'
            self.forecast_1_day_precip = self.weather['forecasts'][1]['day']['chance_precip'] + '%'

            # slice day 1
            self.forecast_1_day_long = self.weather['forecasts'][1]['day_of_week']
            self.forecast_1_list = list(self.forecast_1_day_long) # convert to list
            self.forecast_1_list[3:] = [] # slice list to show what we want
            self.forecast_1_day = "".join(self.forecast_1_list) # join back to a string

            # temp high/low
            self.forecast_1 = self.weather['forecasts'][1]['high'] + self.degree_sign + '/' + self.weather['forecasts'][1]['low'] + self.degree_sign

        except(KeyError) as e:
            print('day 2 weather error:  ' + str(e)) #debug
            logging.info('day 2 weather error:  ' + str(e))
            self.forecast_1_day_code = "99"
            self.forecast_1_night_code = "99"
            self.forecast_1_night_precip = "ER"
            self.forecast_1_day_precip = "ER"
            self.forecast_1_day = "ER"
            self.forecast_1 = "ER/ER"
            pass
        # weather condition icon
        self.forecast_1_day_icon=self.icon_select(self.forecast_1_day_code)
        self.forecast_1_night_icon=self.icon_select(self.forecast_1_night_code)

        try:
            # day 2
            # weather conditon codes
            self.forecast_2_day_code = self.weather['forecasts'][2]['day']['icon']
            self.forecast_2_night_code = self.weather['forecasts'][2]['night']['icon']

            # Precip %
            self.forecast_2_night_precip = self.weather['forecasts'][2]['night']['chance_precip'] + '%'
            self.forecast_2_day_precip = self.weather['forecasts'][2]['day']['chance_precip'] + '%'

            # slice day 2
            self.forecast_2_day_long = self.weather['forecasts'][2]['day_of_week']
            self.forecast_2_list = list(self.forecast_2_day_long) # convert to list
            self.forecast_2_list[3:] = [] # slice list to show what we want
            self.forecast_2_day = "".join(self.forecast_2_list) # join back to a string

            # temp high/low
            self.forecast_2 = self.weather['forecasts'][2]['high'] + self.degree_sign + '/' + self.weather['forecasts'][2]['low'] + self.degree_sign

            # weather condition icon
            self.forecast_2_day_icon=self.icon_select(self.forecast_2_day_code)
            self.forecast_2_night_icon=self.icon_select(self.forecast_2_night_code)

        except(KeyError) as e:
            print('day 3 weather error:  ' + str(e)) #debug
            logging.info('day 3 weather error:  ' + str(e))
            self.forecast_2_day_code = "99"
            self.forecast_2_night_code = "99"
            self.forecast_2_night_precip = "ER"
            self.forecast_2_day_precip = "ER"
            self.forecast_2_day = "ER"
            self.forecast_2 = "ER/ER"
            pass
        # weather condition icon
        self.forecast_2_day_icon=self.icon_select(self.forecast_2_day_code)
        self.forecast_2_night_icon=self.icon_select(self.forecast_2_night_code)


    def icon_select(self,icon_code):
        source = inspect.stack()[1][3]
        if source == 'forcast':
            number = 65
        elif source == 'quit_button':
            number = 45
        else:
            number = 65

        if icon_code in '0': #Tornado
            file_='tornado.png'
        elif icon_code in ('5','6','7','8','9','10','11','12','17','18','35','40'): #rain
            file_='rain.png'
        elif icon_code in ('13','14','15','16','41','42','43','46'): #Snow
            file_='snow.png'
        elif icon_code in ('20','21'): #Foggy or Haze
            file_='fog.png'
        elif icon_code in ('23','24'): # Windy
            file_='wind.png'
        elif icon_code == '25': #Cold
            file_='cold.png'
        elif icon_code == '36': #Hot
            file_='hot.png'
        elif icon_code in ('26','44'): #Cloudy
            file_= 'cloudy.png'
        elif icon_code in ('27','29'): #Mostly Cloudy(Night)
            file_='cloudy_night.png'
        elif icon_code in ('28','30'): #Mostly Cloudy(Day)
            file_='cloudy_day.png'
        elif icon_code in ('31','33'): #Clear(Night),Fair(Night)
            file_='clear_night.png'
        elif icon_code in ('32','34'): #Sunny,Fair(day)
            file_='sunny.png'
        elif icon_code in ('4','37','38','39','45','47'): #Thunderstorms
            file_= 'thunderstorms_severe.png'
        elif icon_code == '3': #Severe Thunderstorms
            file_= 'thunderstorms.png'
        else:
            file_='x.png'
            
        icon= tk.PhotoImage(file=self.get_resource_path('Images/{}/{}'.format(number,file_)))
        return(icon)


if __name__ == "__main__":
    app = WeatherCh()
