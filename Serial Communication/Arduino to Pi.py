import serial

#identifying the USB port for the arduino
ser = serial.Serial('/dev/ttyACM0',9600)  
s = [0,1]
while True:
    #have to decode string from the arduino
    read_serial=ser.readline().decode('utf-8')
    s[0] = str(read_serial)
    #print the string from the arduino
    print (s[0])
    print (read_serial)
