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
    # portName = getPort()
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


