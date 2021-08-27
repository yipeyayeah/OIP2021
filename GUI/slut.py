import os, time, cv2, json, re, serial
import tkinter as tk, threading
from tkinter import filedialog, PhotoImage, Image, messagebox
from pathlib import Path
from PIL import ImageTk, Image
from twilio.rest import Client

firstRun = True
file_paths = [os.path.join(Path().absolute(), 'camera.jpg')]
syringeStatus = [None, None, None, None, None, None]


class TestGUI():

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x480")
        # self.root.attributes("-fullscreen", True)

        # Establish serial connection with Arduino
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.ser.flush()

        # Image constants that will be used throughout the GUI
        self.cleaningProcessImage = Image.open("resources/CleaningProcess.png")
        self.cleaningProcessPhotoImage = ImageTk.PhotoImage(self.cleaningProcessImage)

        self.dryingProcessImage = Image.open("resources/DryingProcess.png")
        self.dryingProcessPhotoImage = ImageTk.PhotoImage(self.dryingProcessImage)

        self.sterilisationProcessImage = Image.open("resources/SterilisationProcess.png")
        self.sterilisationProcessPhotoImage = ImageTk.PhotoImage(self.sterilisationProcessImage)

        self.homeScreenImage = Image.open("resources/HomeScreen.png")
        self.homeScreenPhotoImage = ImageTk.PhotoImage(self.homeScreenImage)

        self.startImage = Image.open("resources/HomeUpdatesNotFound.png")
        self.startPhotoImage = ImageTk.PhotoImage(self.startImage)

        self.startTextImage = Image.open("resources/StartText.png")
        self.startTextPhotoImage = ImageTk.PhotoImage(self.startTextImage)

        self.StartButtonPhotoImage = PhotoImage(file=r"resources/StartButton.png")

        self.cleaningCompletedImage = Image.open("resources/CleaningCompleted.png")
        self.cleaningCompletedPhotoImage = ImageTk.PhotoImage(self.cleaningCompletedImage)

        self.checkingSyringeImage = Image.open("resources/CheckingSyringe.png")
        self.checkingSyringePhotoImage = ImageTk.PhotoImage(self.checkingSyringeImage)

        self.settingsImage = Image.open("resources/settingsButton.png")
        self.settingsPhotoImage = ImageTk.PhotoImage(self.settingsImage)

        self.settingsImage = Image.open("resources/settingsButton.png")
        self.settingsPhotoImage = ImageTk.PhotoImage(self.settingsImage)

        self.settingsScreenImage = Image.open("resources/SettingScreen.png")
        self.settingsScreenPhotoImage = ImageTk.PhotoImage(self.settingsScreenImage)

        self.lblHomeScreen = tk.Label(fg='#F0EFF5', image=self.homeScreenPhotoImage, borderwidth=0,
                                      highlightthickness=0)
        self.lblHomeScreen.place(relwidth=1, relheight=1, relx=0, rely=0)

        self.btnSettings = tk.Button(image=self.settingsPhotoImage, borderwidth=0,
                                     highlightthickness=0, cursor="hand1", command=lambda: self.settingsPage())
        self.btnSettings.place(x=48, y=197)



        self.lblProcessOne = tk.Label()
        self.lblProcessTwo = tk.Label()
        self.lblNoUpdate = None
        self.lblCleaningCompleted = None

        self.lblNoUpdate = tk.Label(fg='#F0EFF5', image=self.startPhotoImage, borderwidth=0, highlightthickness=0)
        self.lblNoUpdate.place(x=420, y=165)

        self.startPhotoImageEditted = self.StartButtonPhotoImage.subsample(2, 2)
        self.btnStart = tk.Button(image=self.startPhotoImageEditted, bg='#FFFFFF', cursor="hand1", highlightthickness=0,
                                  bd=0, command=lambda: self.checkSyringes())
        self.btnStart.place(x=440, y=200)

        self.lblStartText = tk.Label(fg='#F0EFF5', image=self.startTextPhotoImage, borderwidth=0, highlightthickness=0)
        self.lblStartText.place(x=440, y=340)
        self.root.mainloop()

    def settingsPage(self):
        self.lblHomeScreen = tk.Label( image=self.settingsScreenPhotoImage, borderwidth=0,
                                      highlightthickness=0)
        self.lblHomeScreen.place(relwidth=1, relheight=1, relx=0, rely=0)

    def checkSyringes(self):
        # Refreshes GUI components to show the cleaning process
        self.lblNoUpdate.lower()
        self.btnStart.lower()
        self.lblStartText.lower()
        self.lblProcessOne.lower()
        self.lblProcessTwo.lower()
        self.lblProcessOne = tk.Label(fg='#F0EFF5', image=self.checkingSyringePhotoImage)
        self.lblProcessOne.place(x=300, y=170)
        self.root.update()
        
        # Send command '5' six times. For each command, wait for ack ['4']
        # Once '4' is received, execute capture image
        # After capture image, send to API
        count = 0
        check = True
        while count < 2:
            
            self.sendCommandToArduino(5, self.ser)
            print("inside")
            check = True
            while check:
                line = self.ser.readline().decode('utf-8').rstrip()
                print("[checkSyringes] Message from Arduino: ", line)
                if (line == '4'):
                    self.captureImage()
                    self.root.update()
                    rs = self.sendToAPI()
                    print('Count: ', count)
                    print('Results: ' + rs)
                    syringeStatus[count] = rs
                    check = False
                    count += 1

                # time.sleep(1)

        if 'Dirty' in syringeStatus:
            self.cleaningProcess()
        elif 'Wet' in syringeStatus:
            self.dryingProcess()
        else:
            self.sterilisationProcess()


    def cleaningProcess(self):
        # Refreshes GUI components to show the cleaning process
        self.lblProcessOne.lower()
        self.lblProcessTwo.lower()
        self.lblProcessOne = tk.Label(fg='#F0EFF5', image=self.cleaningProcessPhotoImage)
        self.lblProcessOne.place(x=300, y=170)
        self.lblProcessTwo = tk.Label(fg='#F0EFF5', image=self.checkingSyringePhotoImage)
        self.lblProcessTwo.place(x=300, y=290)
        self.root.update()

        self.sendCommandToArduino(1, self.ser)

        check = True
        while check:
            line = self.ser.readline().decode('utf-8').rstrip()
            print("[cleaningProcess] Message from Arduino: ", line)
            time.sleep(1)
            if (line == '4'):
                check = False

        self.dryingProcess()

    def dryingProcess(self):
        self.lblProcessOne.lower()
        self.lblProcessTwo.lower()
        self.lblProcessOne = tk.Label(fg='#F0EFF5', image=self.dryingProcessPhotoImage)
        self.lblProcessOne.place(x=300, y=170)
        self.lblProcessTwo = tk.Label(fg='#F0EFF5', image=self.cleaningProcessPhotoImage)
        self.lblProcessTwo.place(x=300, y=290)
        self.root.update()

        self.sendCommandToArduino(2, self.ser)

        check = True
        while check:
            line = self.ser.readline().decode('utf-8').rstrip()
            print("[dryingProcess] Message from Arduino: ", line)
            time.sleep(1)
            if (line == '4'):
                check = False

        self.sterilisationProcess()


    def sterilisationProcess(self):
        self.lblProcessOne.lower()
        self.lblProcessTwo.lower()
        self.lblProcessOne = tk.Label(fg='#F0EFF5', image=self.sterilisationProcessPhotoImage)
        self.lblProcessOne.place(x=300, y=170)
        self.lblProcessTwo = tk.Label(fg='#F0EFF5', image=self.dryingProcessPhotoImage)
        self.lblProcessTwo.place(x=300, y=290)
        self.root.update()

        self.sendCommandToArduino(3, self.ser)

        check = True
        while check:
            line = self.ser.readline().decode('utf-8').rstrip()
            print("[sterilisationProcess] Message from Arduino: ", line)
            time.sleep(1)
            if (line == '4'):
                check = False

        self.finalProcess()

    def finalProcess(self):
        self.lblProcessOne.lower()
        self.lblProcessTwo.lower()
        self.lblCleaningCompleted = tk.Label(fg='#F0EFF5', image=self.cleaningCompletedPhotoImage, borderwidth=0,
                                             highlightthickness=0)
        self.lblCleaningCompleted.place(x=320, y=185)
        self.root.update()
        messagebox.showinfo("Cleaning completed", "SMS sent to nurse.")

        self.reset()

    def reset(self):
        self.lblProcessOne.lower()
        self.lblProcessTwo.lower()
        self.lblCleaningCompleted.lower()
        self.lblNoUpdate.lift()
        self.btnStart.lift()
        self.lblStartText.lift()

    def captureImage(self):

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

    def sendToAPI(self):
        project_id = 'dfbb7979-773f-4b4e-b8b9-64331d6fd477'
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

    def sendCommandToArduino(self, command, ser):
        ser.write(str(command).encode('utf-8'))

    def sendSMS():
        account_sid = "AC35b622ad2fd3094dfd47f9b94e4ef723"
        auth_token = "a6bed858fc2a1c35ce4cbda258099701"
        client = Client(account_sid, auth_token)

        client.messages.create(
            to="+65" + str(96388495),
            from_="+16182081528",
            body="Cleaning Cycle Completed! Please check STERIDRY machine.")


app = TestGUI()
