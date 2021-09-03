import os, time, cv2, json, re, serial
from pathlib import Path

file_paths = [os.path.join(Path().absolute(),'camera.jpg')]
# Establish serial connection with Arduino


def cleaningProcess(ser):

    sendCommandToArduino(1, ser)

    check = True
    while check:
        line = ser.readline().decode('utf-8').rstrip()
        if len(line) != 0:
            print("[cleaningProcess] Message from Arduino: ", line)
        time.sleep(1)
        if (line == '4'):
            check = False

    dryingProcess(ser)


def dryingProcess(ser):
    sendCommandToArduino(2, ser)

    check = True
    while check:
        line = ser.readline().decode('utf-8').rstrip()
        if len(line) != 0:
            print("[dryingProcess] Message from Arduino: ", line)
        time.sleep(1)
        if (line == '4'):
            check = False

    sterilisationProcess(ser)


def sterilisationProcess(ser):
    sendCommandToArduino(3, ser)

    check = True
    while check:
        line = ser.readline().decode('utf-8').rstrip()
        if len(line) != 0:
            print("[sterilisationProcess] Message from Arduino: ", line)
        time.sleep(1)
        if (line == '4'):
            check = False

def sendToAPI():
    project_id = '53910905-2afc-430d-8f8e-e491ed97b4e8'
    code = """curl --silent --request POST \
    --url https://app.slickk.ai/api/project/entryPoint \
    --header 'Accept: */*' \
    --header 'Accept-Language: en-US,en;q=0.5' \
    --header 'Connection: keep-alive' \
    --header 'Content-Type: multipart/form-data' \
    --form "projectId={1}" \
    {0}""".format(''.join(["--form data=@{0}".format(path) for path in file_paths]), project_id)

        # execute code
    results = os.popen(code).read()
        # above return string, include progress, so remove
    results = re.sub(r'{"progress":\d+,"max":\d+}', "", results)
        # process using json library and load into program
    results = json.loads(results)
        # print text of the result
    return str(results[0]["text"])

def sendCommandToArduino(command, ser):
    ser.write(str(command).encode('utf-8'))

def captureImage():
    
    TIMER = int(3)
    window_name = "STERIDRY 2.0"

    print("[INFO] Starting camera stream.")

    # Open the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Read and display each frame
        ret, img = cap.read()
        cv2.imshow(window_name, img)

        # Check for the key pressed
        k = cv2.waitKey(125)

        # Trigger key is q to start the countdown to take JPG
        if k == ord('q'):
            prev = time.time()

            while TIMER >= 0:
                ret, img = cap.read()

                # Display countdown on each frame
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str(TIMER),
                            (225, 325), font,
                            10, (0, 255, 255),
                            4, cv2.LINE_AA)
                cv2.imshow(window_name, img)
                cv2.waitKey(125)

                # current time
                cur = time.time()

                # Update and keep track of Countdown
                # if time elapsed is one second
                # than decrease the counter
                if cur - prev >= 1:
                    prev = cur
                    TIMER = TIMER - 1

            else:
                ret, img = cap.read()

                # Display the clicked frame for 2
                # sec.You can increase time in
                # waitKey also
                cv2.imshow(window_name, img)

                # time for which image displayed
                cv2.waitKey(2000)

                # Save the frame as a jpg
                cv2.imwrite('camera.jpg', img)

                # Reset the countdown
                TIMER = 3
                break

        # Press Esc to exit
        elif k == 27:
            break

    # close the camera
    cap.release()

    # close all the opened windows
    cv2.destroyAllWindows()
    
def main():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()


    captureImage()
    rs = sendToAPI()
    print('Result from slickk.ai API: '+ rs)
    if rs == 'Dirty':
        cleaningProcess(ser)
        
    
    

main()

