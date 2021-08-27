import os, time, cv2, json, re
from pathlib import Path

file_paths = [os.path.join(Path().absolute(),'camera.jpg')]


def sendToAPI():
    #project_id = 'dfbb7979-773f-4b4e-b8b9-64331d6fd477' #OG undesirable api
    project_id = '53910905-2afc-430d-8f8e-e491ed97b4e8' #object detection (clearn, dirty, empty)
    #project_id = 'db06a0d9-66d8-4a25-8271-545c23db73d9' #backup classification
    code = """curl --silent --request POST \
    --url https://app.slickk.ai/api/project/entryPoint \
    --header 'Accept: */*' \
    --header 'Accept-Language: en-US,en;q=0.5' \
    --header 'Connection: keep-alive' \
    --header 'Content-Type: multipart/form-data' \
    --form "projectId={1}" \
    {0}""".format(''.join(["--form data=@{0}".format(path) for path in file_paths]), project_id)

    if project_id == 'dfbb7979-773f-4b4e-b8b9-64331d6fd477':
        print("OG")
    elif project_id == '53910905-2afc-430d-8f8e-e491ed97b4e8':
        print("object detection")
    elif project_id == 'db06a0d9-66d8-4a25-8271-545c23db73d9':
        print("backup")
        # execute code
    results = os.popen(code).read()
        # above return string, include progress, so remove
    results = re.sub(r'{"progress":\d+,"max":\d+}', "", results)
        # process using json library and load into program
    results = json.loads(results)
        # print text of the result
    return str(results[0]["text"])


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
    
    captureImage()
    rs = sendToAPI()
    print('Result from slickk.ai API: '+ rs)
    

main()

