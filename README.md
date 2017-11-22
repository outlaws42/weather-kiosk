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

requires: python 3, tkinter 8.6, pywapi, pyowm(only if you use pyowm)

For indoor temp sensor DHT22 the following need to be installed

pigpio, DHT22

### Installing

Run this from a terminal in the Dir you want.

```
git clone https://github.com/outlaws42/weather-kiosk.git

```

pigpiod needs to be started at os start as root

put the following line in sudo crontab -e

```
@reboot              /usr/local/bin/pigpiod

```

need to compile pigpio from source 


You will have to make the python files executedable.

```
chmod u+x *.py

```

To run

```
main.py

```

The weather channel is used by default and the one I use so it is the most up to date. It has the most info avaliable to you.
    
 Note: The minimum that has to be install is python 3 and tkinter. pywapi is included in the repo. if you don't have a temp
    sensor for the indoor temp it will just insert a static number of 70 degrees.

## Author

Troy Franks

## License

GPL
 
