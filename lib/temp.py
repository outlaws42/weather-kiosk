#! /usr/bin/env python3

# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt

class Sensor(mqtt.Client):

	# Callback fires when conected to MQTT broker.
    def on_connect(self, client, userdata, flags, rc):
        print('Connected with result code {0}'.format(rc))
        # Subscribe (or renew if reconnect).
        
    
    # Callback fires when a published message is received.
    def on_message(self,client, userdata, msg):
        # Decode temperature and humidity values from binary message paylod.
        t,h = [float(x) for x in msg.payload.decode("utf-8").split(',')]
        t = round(t)
        print('{}'.format(t))

    def run(self):
        self.connect('localhost', 1883, 60)  # Connect to MQTT broker (also running on Pi)
        self.subscribe('temp_humidity')
        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc
 
if __name__ == "__main__":
    app = Sensor()   
    rc =app.run()
    print(rc)
           
