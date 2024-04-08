import serial
import random



ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)


while True:
    position = random.uniform(0, 200)
    print(int(position))
    ser.write(int(position).to_bytes())
    read_serial=ser.readline()
    print(read_serial)
    ser.flush()   
