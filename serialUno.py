import serial
import time

if __name__ =='__main__':
    ser=serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    count = 0
    while True:
        ser.write(b"Hello from Pi!\n")
        line=ser.readline().decode('utf-8').rstrip()
        print("Message from Arduino: ", line)
        time.sleep(1)
        count += 1