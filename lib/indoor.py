#! /usr/bin/env python3

# -*- coding: utf-8 -*-
import logging
import time
try:
    import pigpio
    import DHT22
except(ImportError) as e:
    print('import error:  ' + str(e)) #debug
    logging.info('import error:  ' + str(e))
    pass

logging.basicConfig(filename='indoor.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Indoor():
    degree_sign= '\N{DEGREE SIGN}'
    sleepTime = 4 # Time wait between indoor tempature readings
      
    def __init__(self):
        pass
        
    def readDHT22(self):
        try:
            # Intitiate GPIO for pigpio
            self.pi = pigpio.pi()
            # Setup the sensor
            self.dht22 = DHT22.sensor(self.pi, 27) # use the actual GPIO pin
        
            # Get a new reading
            for i in range(2):
                self.dht22.trigger()
                print('DHT22 sensor reading ' + str(self.dht22.temperature()))
                print('waiting  ' + str(self.sleepTime) + ' Seconds')

                
            # Save our values
            self.inside_hum_d ='%.1f' % (self.dht22.humidity())
            temp = float(self.dht22.temperature())
            self.inside_temp_f_conv = int(temp*1.8+32) # Convert to fahrenheit
            self.inside_temp_f = str(self.inside_temp_f_conv)
            print(self.inside_hum_d)
            
            
            # Indoor temp
            self.indoor_temp = self.inside_temp_f + '' + self.degree_sign
        except(NameError, AttributeError) as e:
            logging.info('No temp sensor found  ' + str(e))
            print('No temp sensor found  ' + str(e))
            pass
            
        
if __name__ == "__main__":
    app = Indoor()    

