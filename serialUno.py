import serial
import time

def main():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

    command = int(input("Enter Choice: "))  # it takes user input

    if command == 1:
        sendCommand(1, ser)
    if command == 2:
        sendCommand(2, ser)
    if command == 3:
        sendCommand(3, ser)

    while True:
        line = ser.readline().decode('utf-8').rstrip()
        print("Message from Arduino: ", line)
        time.sleep(1)

def sendCommand(command, ser):
    ser.write(str(command).encode('utf-8'))

if __name__ == '__main__':
    main()