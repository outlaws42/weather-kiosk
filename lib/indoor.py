#! /usr/bin/env python3

# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import time
import datetime
import lib.tmod as tm
from lib.settings import broker_add

class Indoor(mqtt.Client):

	# Callback fires when conected to MQTT broker.
    def on_connect(self, client, userdata, flags, rc):
        #print('Connected with result code {0}'.format(rc))
        # Subscribe (or renew if reconnect).
        self.subscribe('room/living/temperature')
        self.looping_flag=0
        
    
    # Callback fires when a published message is received.
    def on_message(self,client, userdata, msg):
        in_temp = str(msg.payload.decode("utf-8"))
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %M.%S")
        t = '{} {}'.format(in_temp, time_now)
        print(t)
        tm.save_file('temp.txt',t)

    def run(self):
        try:
            self.connect(broker_add, 1883, 60)  # Connect to MQTT broker (also running on Pi)
            self.loop_start()
            self.looping_flag = 1
            counter=0
            while self.looping_flag == 1:
                #print('Waiting on callback to occur {}'.format(counter))
                time.sleep(4) #  Pause 1/100 second
                counter+=1
        except Exception as e:
            print(e)
            t = '-58'
            tm.save_file('temp.txt',t)
            pass

        self.disconnect()
        self.loop_stop()
        
 
if __name__ == "__main__":
    app = Indoor()   
    rc = app.run()
           
