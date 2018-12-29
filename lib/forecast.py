#! /usr/bin/env python3

# -*- coding: utf-8 -*-
import inspect
import tkinter as tk
import lib.pywapi as pywapi
import logging
import inspect
import lib.tmod as tmod
logging.basicConfig(filename='weatherch.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class WeatherCh():
    degree_sign= '\N{DEGREE SIGN}'
    
    

    def __init__(self):
        pass

    def get_weather_info(self):
        self.read_config()
        if self.unit == "metric":
            forecast_unit = 'metric'
        else:
            forecast_unit = 'imperial'
        
        try:
            if self.api == True:
                weather = pywapi.get_weather_from_weather_com(self.code, units = self.forecast_unit)
                tmod.save_pickle('weatherch.cm',weather,'home')
                self.forecastw = tmod.open_pickle('weatherch.cm','home')
                self.warning = ''
            else:
                self.forecastw = tmod.open_pickle('weatherch.cm','home')
                self.warning = 'Using Saved Data'
        except:
           self.forecastw = tmod.open_pickle('weatherch.cm','home') 
           self.warning = 'Using Saved Data'
           pass
        
    def forecast_days(self):
        # forecast day for 3 days
        forecast_day = []
        for i in range(3):
            temp = self.forecastw['forecasts'][i]['day_of_week']
            temp_list = list(temp) # convert to list
            temp_list[3:] = [] # slice list to show what we want
            temp_day = "".join(temp_list) # join back to a string
            forecast_day.append(temp_day)
        return forecast_day
        
        
    def forecast_temp(self):
        # forecast high / low temp for 3 days    
        forecast = []
        for i in range(3):
            temp = '{}{}/{}{}'.format(self.forecastw['forecasts'][i]['high'],self.degree_sign,self.forecastw['forecasts'][i]['low'],self.degree_sign)
            forecast.append(temp)
        return forecast
    
    def forecast_code(self,time_):
        # forecast code is day / night key word starting at index 0 for 3 days
        forecast_day_code = []
        for i in range(3):
            temp = self.forecastw['forecasts'][i]['{}'.format(time_)]['icon']
            forecast_day_code.append(temp)
        return forecast_day_code
        
    def forecast_precip_day(self,time_):
        # pop is day night chance of precip starting at index 0 for 3 days
        forecast_pr = []
        for i in range(3):
            temp = self.forecastw['forecasts'][i]['{}'.format(time_)]['chance_precip'] + '%'
            forecast_pr.append(temp)
        return forecast_pr

    def forecast(self):
        
        day_code = self.forecast_code('day')
        night_code = self.forecast_code('night')
        # day 0   
        # weather condition icon
        self.forecast_0_day_icon=self.icon_select(day_code[0])
        self.forecast_0_night_icon=self.icon_select(night_code[0])

        # day 1       
        # weather condition icon
        self.forecast_1_day_icon=self.icon_select(day_code[1])

        # day 2
        # weather condition icon
        self.forecast_2_day_icon=self.icon_select(day_code[2])


    def icon_select(self,icon_code):
        source = inspect.stack()[1][3]
        #print('{} = {}'.format(source,icon_code))
        try:
            icon= tk.PhotoImage(file=tmod.get_resource_path('{}/{}.png'.format(self.icon_path,icon_code)))
        except:
            icon = tk.PhotoImage(file=tmod.get_resource_path('{}/na.png'.format(self.icon_path)))
        return(icon)

    def read_config(self,file_='config.json'):
            config = tmod.open_json(file_)
            config_value = [value for (key,value) in sorted(config.items())]
            # icon_path api unit code
            self.api = config_value[0]
            self.code = config_value[2]
            self.icon_path = config_value[5]
            self.unit = config_value[8]

if __name__ == "__main__":
    app = WeatherCh()
