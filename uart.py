import serial.tools.list_ports
import time

ser = None
def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

isSensorConnected = False
try:
    portName = "/dev/ttyUSB0"
    ser = serial.Serial(port=portName, baudrate=9600)
    print(ser)
    print("Open port successfully")
    isSensorConnected = True
except:
    print("Can not open the port")
    isSensorConnected = False

def processData(client, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "T":
        client.publish("sensor1", splitData[2])
    elif splitData[1] == "L":
        client.publish("sensor2", splitData[2])
    elif splitData[1] == "H":
        client.publish("sensor3", splitData[2])

mess = ""

def readSerial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        print(mess)
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]


def writeData(data):
    print(data)
    ser.write((str(data)).encode())


# RS485 protocol
def serial_read_data(ser):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
            return value
        else:
            return -1
    return 0

sensor_data = [1, 3, 0, 6, 0, 1, 100, 11]
def readSensor():
    serial_read_data(ser)
    ser.write(sensor_data)
    time.sleep(1)
    return serial_read_data(ser)


relay1_ON  = [2, 6, 0, 0, 0, 255, 201, 185]
relay1_OFF = [2, 6, 0, 0, 0, 0, 137, 249]
relay2_ON  = [3, 6, 0, 0, 0, 255, 200, 104]
relay2_OFF = [3, 6, 0, 0, 0, 0, 136, 40]
relay3_ON  = [4, 6, 0, 0, 0, 255, 201, 223]
relay3_OFF = [4, 6, 0, 0, 0, 0, 137, 159]

def setRelay(state):
    # Relay ID2
    if state == True:
        ser.write(relay1_ON)
    else:
        ser.write(relay1_OFF)
    time.sleep(1)
    print(serial_read_data(ser))
    # Relay ID3
    if state == True:
        ser.write(relay2_ON)
    else:
        ser.write(relay2_OFF)
    time.sleep(1)
    print(serial_read_data(ser))
    # Relay ID4
    if state == True:
        ser.write(relay3_ON)
    else:
        ser.write(relay3_OFF)
    time.sleep(1)
    print(serial_read_data(ser))
