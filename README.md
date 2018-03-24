# weather-kiosk

The reason for writing this program was for 2 reasons.
    1) I wanted learn more about programming in python. I did learn alot
        while working on this I still have alot to learn.
    2) I wanted take a raspberry pi B that I had laying around and added a  5"
        display to create a weather display. Getting the outside weather from a online
        service and providing inside temp with a sensor DHT22.
        I know this isn't the most accurate  vs a outside sensor at your location.
        I had some failed devices like that. so I decided to do a project
        getting that info from the internet.

## Prerequisites

requires: python 3, tkinter 8.6, weather underground api key

For indoor temp sensor DHT22 the following need to be installed

pigpio

### api.py
You will need to create a file called api.py in the lib dir. You can get a api key from https://www.wunderground.com/weather/api/ 
```
#! /usr/bin/env python3

# -*- coding: utf-8 -*-
key = 'your_weather_underground_api_key'

```

### settings.py
 The zip code is only used to insert into the
database. You can find the pws code for your area by going to https://www.wunderground.com/ and then search location 
by zip code or city. 

```
#! /usr/bin/env python3

# -*- coding: utf-8 -*-
pws = 'pws_for_your_location'
zip_code = 'your_zip_code'
icon_path = 'Images/65'
api = 'yes' # Yes = use the api(Production). no = don't use the api and get info from saved file(Development). 
fullscreen = 'yes' # yes = fullscreen no = Windowed
unit = 'in' # metric = Metric, in = Inch

```

### Installing

Installing python 3 and pip on the raspberry pi.
```
sudo apt-get install python3 python3-pip

```
Run this from a terminal in the dir you want. to clone the repo to your local computer

```
git clone https://github.com/outlaws42/weather-kiosk.git


```
Then run this command to install the modules needed

```
pip3 install -r requirements.txt

```
Installing pigpio for reading the GPIO pins on the raspberry pi. Note this is not needed if you are not
going to use the indoor temp sensor.
```
rm master.zip
sudo rm -rf pigpio-master
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make
sudo make install

```
pigpiod needs to be started at os start as root

put the following line in sudo crontab -e

```
@reboot              /usr/local/bin/pigpiod

```

You will have to make the python files executedable.

```
chmod u+x *.py

```

To run

```
main.py

```


    
 Note: The minimum that has to be install is python 3 and tkinter. if you don't have a temp
    sensor for the indoor temp it will just insert a static number of 70 degrees.
    
## Raspbery Pi
In the OS dir there is a file called weather.desktop to add a menu item as well as a image.
Add the image to:
```
/usr/share/pixmaps/

```

Add the weather.desktop file to:
```
/usr/share/applications/

```

## Author

Troy Franks

## License

GPL
 
