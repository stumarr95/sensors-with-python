#### script to get token from Phase IV leap gateway, 
#### then get last reading and publish that reading
#### to the mqtt broker

import paho.mqtt.client as mqtt
from doc_get_token_readings_v4 import get_reading
import json

# assign get_reading() method to json_lastReading variable
json_lastReading = get_reading()

# define send_payload method
def send_payload():
    message = json.dumps(json_lastReading) # converts json_lastReading, which comes in as a type(dict), to a json object
    print(f"This is the latest reading {message}") 
    client.publish("/edge/leap/data", message) # publish lastReading to mqtt broker topic 'edge/leap/data'
    client.loop()
    client.disconnect()

# define method on_connect; once connected, send payload
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    send_payload()

# define on_message
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# create an MQTT client instance
client = mqtt.Client()

# set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# connect to the MQTT broker
client.username_pw_set("gateway", "gateway")
client.connect("10.0.30.74", port=1883)
client.loop()