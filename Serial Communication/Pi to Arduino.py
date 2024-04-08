import serial
import time

#identifying USB port for arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()
while(1):
    send_string = ("Hi\n")
    ser.write(send_string.encode('utf-8'))
    time.sleep(0.5)
    #allows for feedback
    receive_string = ser.readline().decode('utf-8').rstrip()
    print(receive_string)
