import serial
import time

def main():
    check = True
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

    command = int(input("Enter command to execute: "))  

    if command == 1:
        sendCommand(1, ser)
    if command == 2:
        sendCommand(2, ser)
    if command == 3:
        sendCommand(3, ser)
    if command == 5:
        sendCommand(5, ser)
    if command == 6:
        sendCommand(6, ser)
    if command == 7:
        sendCommand(7, ser)
    
    while check:
        line = ser.readline().decode('utf-8').rstrip()
        print("Message from Arduino: ", line)
        time.sleep(1)
        if (line == '4'):
            check = False
            
       

def sendCommand(command, ser):
    ser.write(str(command).encode('utf-8'))

if __name__ == '__main__':
    main()