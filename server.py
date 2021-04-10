import paho.mqtt.client as mqtt
import time

count=0
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("hospital/population")
    client.message_callback_add("hospital/population",population_callback)

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def population_callback(client,userdata, msg):
    print("population_callback: "+msg.topic+ " "+ str(msg.payload, "utf-8"))
    global count
    count+=1

if __name__ == '__main__':

    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        if(count>10):
            client.publish("hospital/stop","Maximum occupancy has been reached")
        time.sleep(1)
            

