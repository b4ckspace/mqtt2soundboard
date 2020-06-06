#!/usr/bin/env python
import time
import os

import paho.mqtt.client as mqtt


mqtt_host = os.environ.get('MQTT_HOST', 'localhost')
mqtt_user = os.environ.get('MQTT_USER', None)
mqtt_pass = os.environ.get('MQTT_PASS', None)
mqtt_port = os.environ.get('MQTT_PORT', 1883)

if mqtt_user is not None:
    mqtt.username_pw_set(mqtt_user, mqtt_pass)

def on_connect(client, userdata, flags, rc):
    client.subscribe("psa/alarm")
    client.subscribe("sensor/door/frame")
    client.subscribe("sensor/door/bell")
    print("Connected to mqtt with result code " + str(rc))

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    soundfile = None
    if topic == "psa/alarm":
        soundfile = "space/ALARM"
        client.publish('psa/sound', soundfile)
    elif topic == "sensor/door/frame" and payload == "open":
        soundfile = "door-louder"
        client.publish('psa/sound', soundfile)
    elif topic == "sensor/door/bell" and payload == "pressed":
        soundfile = "door-bell"
        client.publish('psa/sound', soundfile)
    print("RECEIVED: " + topic + '  ' + payload)

client = mqtt.Client()
client.on_connect = on_connect

client.connect(mqtt_host, mqtt_port, 60)
client.on_message = on_message
client.loop_start()

while True:
    time.sleep(2)
