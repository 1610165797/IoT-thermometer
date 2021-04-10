import requests
import sys
import time
import math

sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')

import grovepi
import grove_rgb_lcd as lcd
from grove_rgb_lcd import *

# Modules for my apps
import my_reddit
import my_weather
#import my_app  # TODO: Create my_app.py using another API, following the examples as a template
import my_app

PORT_BUZZER = 2     # D2
PORT_BUTTON = 4     # D4

LCD_LINE_LEN = 16

# Setup
grovepi.pinMode(PORT_BUZZER, "OUTPUT")
grovepi.pinMode(PORT_BUTTON, "INPUT")

lcd.setRGB(0, 128, 0)

# Installed Apps!
APPS = [
    my_weather.WEATHER_APP,
    my_reddit.QOTD_APP,
    # TODO: Add your new app here
    my_app.MY_APP,
]

# Cache to store values so we save time and don't abuse the APIs
CACHE = [''] * len(APPS)
for i in range(len(APPS)):
    # Includes a two space offset so that the scrolling works better
    CACHE[i] = '  ' + APPS[i]['init']()

app = 0     # Active app
ind = 0     # Output index

partition=CACHE[2].partition(',')

potentiometer = 0

grovepi.pinMode(potentiometer,"INPUT")

while True:
    try:
        # Check for input
        if grovepi.digitalRead(PORT_BUTTON):
            # BEEP!
            grovepi.digitalWrite(PORT_BUZZER, 1)

            # Switch app
            app = (app + 1) % len(APPS)
            ind = 0

        time.sleep(0.1)

        grovepi.digitalWrite(PORT_BUZZER, 0)
        
        # Display app name
        # Scroll output
        # TODO: Make the output scroll across the screen (should take 1-2 lines of code)
        sensor_value = grovepi.analogRead(potentiometer)
        state=math.ceil(sensor_value/204)
        bright=state*51
        if(state<=1):
            lcd.setText('')
            lcd.setRGB(0, 0, 0)
        else:
            setRGB(bright,225-bright,bright)
            lcd.setText_norefresh(APPS[app]['name'])
            if(app==2):
                if(partition[2].find(":")==-1):
                    lcd.setText_norefresh('\n' + partition[0])
                    partition=CACHE[2].partition(',')
                else:
                    lcd.setText_norefresh('\n' + partition[0])
                    partition=partition[2].partition(',')
            else:
                lcd.setText_norefresh('\n' + CACHE[app][ind:ind+LCD_LINE_LEN])
                if(ind<len(CACHE[app])):
                    ind+=16
                else:
                    ind=0
        
            
    except KeyboardInterrupt:
        # Gracefully shutdown on Ctrl-C
        lcd.setText('')
        lcd.setRGB(0, 0, 0)

        # Turn buzzer off just in case
        grovepi.digitalWrite(PORT_BUZZER, 0)

        break

    except IOError as ioe:
        if str(ioe) == '121':
            # Retry after LCD error
            time.sleep(0.25)

        else:
            raise
