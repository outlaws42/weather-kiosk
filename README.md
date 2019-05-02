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

requires: python 3, tkinter 8.6, Dark Sky api key

### api.py
You will need to create a file called api.py in the lib dir. You can get a api key from https://darksky.net/dev 
```
#! /usr/bin/env python3

# -*- coding: utf-8 -*-
key = 'your_Dark_Sky_api_key'

```

### settings Dialog
You can either type in your address or zip code to get the weather for your area. 
The broker is for the IP address of the MQTT broker. This is only used for the indoor remote temp sensor. It is not required. If this is not setup the indoor temp will read E1.
As of version 3.0.4 settings.py is not used instead there is a settings dialog. 
There is a drop down menu from the current status image(Image located with the outside temp).


### Installing

Installing python 3, tkinter and pip on the raspberry pi.
```
sudo apt-get install python3 python3-pip python3-tk

```
Run this from a terminal in the dir you want. to clone the repo to your local computer

```
git clone https://github.com/outlaws42/weather-kiosk.git


```
Then run this command to install the modules needed

```
pip3 install -r requirements.txt

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
 
