import serial

ser = serial.Serial('/dev/ttyACM0',9600)
s = [0,1]
while True:
    read_serial=ser.readline().decode('utf-8')
    s[0] = str(read_serial)
    print (s[0])
    print (read_serial)
