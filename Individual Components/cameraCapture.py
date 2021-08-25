# Import libraries required
import time
import cv2

# Set the timer countdown to be 3 seconds
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
