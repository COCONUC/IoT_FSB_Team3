import paho.mqtt.client as mqtt
import time
import random

MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "group3"
MQTT_PASSWORD = "ngoansangdinh"
MQTT_TOPIC_PUB = MQTT_USERNAME + "/feeds/V1"
MQTT_TOPIC_SUB = MQTT_USERNAME + "/feeds/V1/+"


def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    client.subscribe(MQTT_TOPIC_SUB)

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")

def mqtt_message(client, userdata, message):
    print("Receive data from topic " + message.topic +": " + str(message.payload.decode('utf-8')))

mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)

#Register mqtt events
mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message = mqtt_message

mqttClient.loop_start()

stype = 0
while True:
    time.sleep(5)
    stype += 1
    match stype:
            case 1:
            # Update thermal stat
                value = random.randint(10, 70)
                print("Update thermal: ", value)
                mqttClient.publish(MQTT_TOPIC_PUB + '/sensor1', value)
            case 2:
            # Update light stat
                value = random.randint(0, 500)
                print("Update light: ", value)
                mqttClient.publish(MQTT_TOPIC_PUB + '/sensor2', value)
            case 3:
            # Update humidity stat
                value = random.randint(0, 100)
                print("Update humidity: ", value)
                mqttClient.publish(MQTT_TOPIC_PUB + '/sensor3', value)
                stype = 0
