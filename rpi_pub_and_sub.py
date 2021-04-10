import grovepi
from grove_rgb_lcd import *
from grovepi import *
import paho.mqtt.client as mqtt
import time
import threading

sensor=0

def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code "+str(rc))

    client.subscribe("hospital/population")
    client.message_callback_add("hospital/population",population_callback)

    client.subscribe("hospital/entry")
    client.message_callback_add("hospital/entry",entry_callback)

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def population_callback(client, userdata, msg):
    print("population_callback: " + msg.topic + " " + str(msg.payload, "utf-8"))
    remain=1000-msg
    if(str(msg.payload, "utf-8")>=1000):
        setText_norefresh("Facility Full")
    else:
        setText_norefresh("Remaining Spaces: "+remain)

def entry_callback(client, userdata, msg):
    print("entry_callback: " + msg.topic + " " + str(msg.payload, "utf-8"))
        setText_norefresh("Temerature High")

if __name__ == '__main__':
    lock=threading.Lock()

    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    setRGB(0,255,0)
    while True:
        outfile=open('detected.txt','r')
        txt=outfile.read()
        if(txt=="detected"):
            outfile.close()
            open("filename", "w").close()
	        with lock:
	        	temperature = grovepi.temp(sensor,'1.1')
	            time.sleep(0.5)
            if(temperature>37):
                client.publish("hospital/population",temperature)
                setText_norefresh("Temerature High")
            else:
                setText_norefresh("Welcome")
       
            

