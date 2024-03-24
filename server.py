# pip install paho-mqtt==1.6.1
# pip install pyserial
import paho.mqtt.client as mqtt
import time
from uart import *
from uart_relays import *

MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "group3"
MQTT_PASSWORD = "ngoansangdinh"
MQTT_TOPIC_PUB = MQTT_USERNAME + "/feeds/V1"
MQTT_TOPIC_SUB = MQTT_USERNAME + "/feeds/V2"

relay_topics = ['/r1', '/r2', '/r3']

def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    for topic in relay_topics:
        client.subscribe(MQTT_TOPIC_SUB + topic)

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")

def mqtt_message(client, userdata, message):
    global relay_topics
    payload = str(message.payload.decode('utf-8'))
    print("Receive data from topic " + message.topic +": " + payload)
    match message.topic.split('/')[-1]:
        case 'r1':
            is_relay_set = True
            relay_number = 1
        case 'r2':
            is_relay_set = True
            relay_number = 2
        case 'r3':
            is_relay_set = True
            relay_number = 3

#Inint MQTT client
mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)
#Register mqtt events
mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message = mqtt_message

mqttClient.loop_start()

is_relay_set = False
relay_number = 0

while True:
    if isSensorConnected and ser != None:

        # Relays interact
        if is_relay_set == True:
            match relay_number:
                case 1:
                    response = setRelay(payload == '1', 1)
                    print('Response R1: ' + str(response))
                    mqttClient.publish(MQTT_TOPIC_PUB + relay_topics[0], str(response) == '255')
                case 2:
                    response = setRelay(payload == '1', 2)
                    print('Response R2: ' + str(response))
                    mqttClient.publish(MQTT_TOPIC_PUB + relay_topics[1], str(response) == '255')
                case 3:
                    response = setRelay(payload == '1', 3)
                    print('Response R3: ' + str(response))
                    mqttClient.publish(MQTT_TOPIC_PUB + relay_topics[2], str(response) == '255')
            is_relay_set = False
            relay_number = 0

        # Sensor read
        temp = round(readSensor(1) * 0.01, 2)
        if temp > 0:
            print(str(temp) + ' °C')
            mqttClient.publish(MQTT_TOPIC_PUB + '/temp', temp)
        humid = round(readSensor(2) * 0.01, 2)
        if humid > 0:
            print(str(humid) + ' %')
            mqttClient.publish(MQTT_TOPIC_PUB + '/humid', humid)
        
    time.sleep(1)
