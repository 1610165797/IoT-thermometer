import grovepi
from grove_rgb_lcd import *
from grovepi import *
import paho.mqtt.client as mqtt
import time
import threading
import requests
import json

sensor=0

port=4

detected=True



def vacc_init():
    params={'country':'US','ab':'US','continent':'North America',}
    response = requests.get('https://covid-api.mmediagroup.fr/v1/vaccines', params)
    if response.status_code == 200:
        data = response.json()
        vacc_partial=json.dumps(data["United States"]["All"]["people_partially_vaccinated"])
        setText_norefresh("US Vaccinated:  \n"+vacc_partial)
        return "US Vaccinated: "+vacc_partial
    else:
        setText_norefresh('error: got response code %d' % response.status_code)
        return None

def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code "+str(rc))

    client.subscribe("hospital/stop")
    client.message_callback_add("hospital/stop",stop_callback)

    client.subscribe("hospital/detected")
    client.message_callback_add("hospital/detected",detected_callback)



def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def stop_callback(client, userdata, msg):
    print("stop_callback: " + msg.topic + " " + str(msg.payload, "utf-8"))
    exit()

def detected_callback(client, userdata, msg):
    print("detected_callback: " + msg.topic + " " + str(msg.payload, "utf-8"))
    global detected
    if(str(msg.payload, "utf-8")=="True"):
        detected =True
    else:
        detected =False


if __name__ == '__main__':
    lock=threading.Lock()

    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    setRGB(0,255,0)
    detected=False
    while True:
        if(detected==True):
            with lock:
                temperature = grovepi.ultrasonicRead(port)
                time.sleep(0.5)
            if(temperature>5):
                setText_norefresh("Temerature High")
            else:
                setText_norefresh("Entry Granted")
                client.publish("hospital/population","One Person Entered")
        else:
            vacc_init()

