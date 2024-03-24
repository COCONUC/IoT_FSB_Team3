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

portName = "/dev/ttyUSB0"
baudrate=9600
try:
    ser = serial.Serial(port=portName, baudrate=baudrate)
    print("Open port successfully: " + str(ser))
except:
    print("Can not open the port")

# RS485 protocol
def serial_read_data(ser):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        # print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
            return value
        else:
            return -1
    return 0

sensor_temp = [1, 3, 0, 6, 0, 1, 100, 11]
sensor_humid = [1, 3, 0, 7, 0, 1, 53, 203]
def readSensor(type):
    if type == 1:
        serial_read_data(ser)
        ser.write(sensor_temp)
        time.sleep(1)
        return serial_read_data(ser)
    if type == 2:
        serial_read_data(ser)
        ser.write(sensor_humid)
        time.sleep(1)
        return serial_read_data(ser)

relay1_ON  = [2, 6, 0, 0, 0, 255, 201, 185]
relay1_OFF = [2, 6, 0, 0, 0, 0, 137, 249]
relay2_ON  = [3, 6, 0, 0, 0, 255, 200, 104]
relay2_OFF = [3, 6, 0, 0, 0, 0, 136, 40]
relay3_ON  = [4, 6, 0, 0, 0, 255, 201, 223]
relay3_OFF = [4, 6, 0, 0, 0, 0, 137, 159]

def setRelay(state, relay_index):
    # Relay ID2
    if relay_index == 1:
        print('Set relay 1: ' + str(state))
        if state == True:
            ser.write(relay1_ON)
        else:
            ser.write(relay1_OFF)
        
    # Relay ID3
    if relay_index == 2:
        print('Set relay 2: ' + str(state))
        if state == True:
            ser.write(relay2_ON)
        else:
            ser.write(relay2_OFF)

    # Relay ID4
    if relay_index == 3:
        print('Set relay 3: ' + str(state))
        if state == True:
            ser.write(relay3_ON)
        else:
            ser.write(relay3_OFF)

    # Wait 1s and read relay's response
    time.sleep(1)
    return(serial_read_data(ser))
