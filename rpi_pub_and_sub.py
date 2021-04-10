import grovepi
from grove_rgb_lcd import *
from grovepi import *
import paho.mqtt.client as mqtt
import time
import threading

sensor=0

port=4

detected=False

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

def detected_callback(client, userdata, msg):
    print("detected_callback: " + msg.topic + " " + str(msg.payload, "utf-8"))
    global detected
    detected =True

if __name__ == '__main__':
    lock=threading.Lock()

    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    setRGB(0,255,0)

    while True:
        if(detected==True):
            detected==False
            with lock:
                temperature = grovepi.ultrasonicRead(port)
                time.sleep(1)
            if(temperature>5):
                setText_norefresh("Temerature High, Entry Denied")
            else:
                setText_norefresh("Welcome")
                client.publish("hospital/population","One Person Entered")
