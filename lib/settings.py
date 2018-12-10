#! /usr/bin/env python3

# -*- coding: utf-8 -*-
pws = 'KINLARWI12' # Weather station for your area. You can get this at https://www.wunderground.com/ 
zip_code = '46764' # Your zip code. This is only used for the database.
icon_path = 'Images/65' # Icon dir in relation to main.py
api = 'yes' # Yes = use the api(Production). no = don't use the api and get info from saved file(Development). 
fullscreen = 'yes' # yes = fullscreen no = Windowed
unit = 'in' # metric = Metric, in = Inch
forecast_source = 2 # 1 = weather undergroound 2 = weather channel 
broker_add = '192.168.1.26' # mqtt broker address

