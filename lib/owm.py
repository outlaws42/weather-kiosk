#! /usr/bin/env python3

# -*- coding: utf-8 -*-
import pyowm
import logging
logging.basicConfig(filename='owm.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Owm():
    degree_sign= '\N{DEGREE SIGN}'
    # Path variables
      
    def __init__(self):
        print('This is Open Weather Map weather')
        #self.get_weather_info() # debug
        #self.gleen_info() # debug
        
    def get_weather_info(self):
        try:
            self.owm = pyowm.OWM('e93b2d38cc9588ba0c007104e09f1420')
            self.obs = self.owm.weather_at_id(4919203) # Columbia City
        except:
            pass
    
    
    def gleen_info(self):

        # OWM get info
        
        try:
            self.weather_service = 'Provided by:  Open Weather Map'
            self.weather = self.obs.get_weather()
            self.windy = self.weather.get_wind()
            self.rain =  self.weather.get_rain()
            self.hum = self.weather.get_humidity()
            self.status = self.weather.get_detailed_status()
            self.temperature = self.weather.get_temperature('fahrenheit')
            self.press = self.weather.get_pressure()
            self.sunrise = self.weather.get_sunrise_time('iso')
            self.sunset = self.weather.get_sunset_time('iso')

            # Brings outside temp elements together.
            self.outdoor_temp = str(round(self.temperature['temp'])) + self.degree_sign

             # Humidity
            self.humidity = str(self.hum) +'%  '
        
            # wind
            self.wind = str(self.windy['speed']) + " mph "
            print(self.wind)

            # Sun Rise/set
            self.sun_rise = str(self.sunrise) + "\n" + str(self.sunset) + '  '

            # Pressure
            self.pressure = self.press['press'] 
        except(KeyError,AttributeError) as e:
            print('owm check_weather error:  ' + str(e)) #debug
            logging.info('owm check_weather error:  ' + str(e))
            pass
    

if __name__ == "__main__":
    app = Owm()    

