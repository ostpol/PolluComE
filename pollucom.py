#!/usr/bin/python

### original script by 93schlucko
### https://forum-raspberrypi.de/forum/thread/57389-sensus-pollucom-e-ueber-pymeterbus-auslesen/?postID=543096#post543096 ###

# -*- coding: utf-8 -*-
import serial, time
import meterbus
import requests
import paho.mqtt.client as paho
import os
import subprocess

#esp-link Settings
esp_ip = '192.168.1.123'

#MQTT Settings
mqtt_broker = '192.168.1.163'
mqtt_port = int(1883)
mqtt_topic = 'hzg/meter'
mqtt_client = 'PolluComE'

#Serial Settings
serial_port = './ttyV666'

address = 0
#Check if socat is connected to esp-link, if not connect
if os.path.exists(serial_port):
    print("socat is connected")
else:
    print("socat not connected")
    cmd_str = "socat pty,link={} tcp:{}:23 &".format(serial_port,esp_ip)
    subprocess.run(cmd_str, shell=True)
    time.sleep(0.5)
# start communication with 8N1, DTR enabled
url = 'http://{}/console/fmt?fmt=8N1'.format(esp_ip) #tell esp-link to use 8N1
requests.get(url)
ser =  serial.Serial(serial_port, 2400, 8, 'N', 1, 0.5)
ser.dsrdtr=True
# send wake up sequence
ser.write(b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55")
time.sleep(0.130)
ser.read()
response = ser.readline()
# switch to 8E1
url = 'http://{}/console/fmt?fmt=8E1'.format(esp_ip) #tell esp-link to use 8E1
requests.get(url)
ser.parity = serial.PARITY_EVEN
# SND_NKE to reset the communication
meterbus.send_ping_frame(ser, address)
frame = meterbus.load(meterbus.recv_frame(ser, 1))
assert isinstance(frame, meterbus.TelegramACK)
# request data from meter
meterbus.send_request_frame(ser, address)
frame = meterbus.load(meterbus.recv_frame(ser, meterbus.FRAME_DATA_LENGTH))
assert isinstance(frame, meterbus.TelegramLong)
# print data, todo: save it to file
print(frame.to_JSON())
#publish via MQTT
msg = frame.to_JSON()
def on_publish(client,userdata,result):           #create function for callback
    print("data published \n")
    pass
client1= paho.Client(mqtt_client)                  #create client object
client1.on_publish = on_publish                   #assign function to callback
client1.connect(mqtt_broker,mqtt_port)                 #establish connection
ret= client1.publish(mqtt_topic,msg)                   #publish