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
