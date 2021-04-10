import grovepi
from grove_rgb_lcd import *
from grovepi import *
import paho.mqtt.client as mqtt
import time
import threading

sensor=0

port=4

def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code "+str(rc))

    client.subscribe("hospital/stop")
    client.message_callback_add("hospital/stop",entry_callback)

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def stop_callback(client, userdata, msg):
    print("stop_callback: " + msg.topic + " " + str(msg.payload, "utf-8"))

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
                temperature = grovepi.ultrasonicRead(sensor,'1.1')
                time.sleep(0.5)
                if(temperature>37):
                    setText_norefresh("Temerature High, Entry Denied")
                else:
                    setText_norefresh("Welcome")
                    client.publish("hospital/population",temperature)
