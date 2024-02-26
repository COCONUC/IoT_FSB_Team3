# pip install paho-mqtt==1.6.1
import sys
import time
# import random
from Adafruit_IO import MQTTClient
from simple_ai import *

AIO_FEED_ID = ["button1", "button2"]
AIO_USERNAME = ""
AIO_KEY = ""

def connected(client):
    print("Ket noi thanh cong ...")
    for feed in AIO_FEED_ID:
      client.subscribe(feed)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu " + feed_id + ": " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

count = 0
stype = 0

while True:
  if(count % 5 == 0):
    count = 0
    # stype += 1
    # match stype:
      # case 1:
      #   # Update thermal stat
      #   value = random.randint(10, 70)
      #   print("Update thermal: ", value)
      #   client.publish('sensor1', value)
      # case 2:
      #   # Update light stat
      #   value = random.randint(0, 500)
      #   print("Update light: ", value)
      #   client.publish('sensor2', value)
      # case 3:
      #   # Update humidity stat
      #   value = random.randint(0, 100)
      #   print("Update humidity: ", value)
      #   client.publish('sensor3', value)
      #   stype = 0
    
    # Send AI data
    aiResult = image_detector()
    print('AI result: ', aiResult)
    client.publish('ai', aiResult)
  count += 1
  
  time.sleep(1)
