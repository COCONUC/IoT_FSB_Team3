# pip install paho-mqtt==1.6.1
# pip install pyserial
import paho.mqtt.client as mqtt
import time
from uart import *

MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "group3"
MQTT_PASSWORD = "ngoansangdinh"
MQTT_TOPIC_PUB = MQTT_USERNAME + "/feeds/V1"
MQTT_TOPIC_SUB = MQTT_USERNAME + "/feeds/V2"

def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    client.subscribe(MQTT_TOPIC_SUB)

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")

def mqtt_message(client, userdata, message):
    print("Receive data from topic " + message.topic +": " + str(message.payload.decode('utf-8')))

#Inint MQTT client
mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)
#Register mqtt events
mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message = mqtt_message

mqttClient.loop_start()

counter = False

while True:
    if isSensorConnected and ser != None:
        temp = readSensor() * 0.01
        if temp > 0:
            print(str(temp) + ' *C')
    setRelay(counter)
    counter = not counter
    time.sleep(1)
