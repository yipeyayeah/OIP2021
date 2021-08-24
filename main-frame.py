from tkinter import *
from tkinter.ttk import Frame, Button, Label, Style
from PIL import ImageTk, Image
import os, time, cv2
from tkinter import StringVar
from picamera import PiCamera
from time import sleep

root = Tk()
root.geometry("500x500")


try:
    import Tkinter as tk
except:
    import tkinter as tk

class Test(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.master.title("STERIDRY	2.0")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
        
        #display image
        #image1 = Image.open("syringe.jpg")
        #image2 = image1.resize((350, 350), Image.ANTIALIAS)
        #test = ImageTk.PhotoImage(image2)

        #label1 = tk.Label(image=test)
        #label1.image = test

        # Position image
        #label1.place(x=6, y=4)
        
        #text
        T = tk.Text(padx=1, pady=1, height=8, width=27)
        T.place(x=1, y=1)
        T.pack()
        T.insert(tk.END, "Group 31\n\nMuhammad Zulhusni Bin Jumat\nLim Boon Seong\nLee Alan\nGideon Yip Yue Onn\nLim Yi Wei, Ivan ")

        #lbl = Label(self, text="Windows")
        #lbl.grid(sticky=W, pady=4, padx=5)

        #area = Text(self)
        #area.grid(row=1, column=0, columnspan=2, rowspan=4,
            #padx=5, sticky=E+W+S+N)

        self.startButton = Button(self, text="Start", command = self.startWork)
        self.startButton.grid(row=1, column=3, pady=4)

        #self.pumpButton = Button(self, text="Pump", command = self.pump)
        #self.pumpButton.grid(row=2, column=3, pady=4)

        #self.dumpButton = Button(self, text="Dump", command = self.dump)
        #self.dumpButton.grid(row=3, column=3, pady=4)
        
        #hbtn = Button(self, text="Help")
        #hbtn.grid(row=5, column=0, padx=5)

        exitButton = Button(self, text="Exit", command = self.quit)
        exitButton.grid(row=4, column=3, pady=4)
        #root.mainloop()

    def startWork(self):
        
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

    def SendCommandToArdunio(self):




    #def pump(self):
            
    #def setting(self):
        #app = tk.Tk()
        #newWindow = tk.Toplevel(app)
                
        #newWindow.title("Settings")
        #newWindow.geometry("500x300")
        #Label(newWindow, text ="This is a new window")

        #confirmButton = Button(self, text="Confirm", command = self.quit)
        #confirmButton.grid(row=5, column=3)
        

            
def quit(self):
        self.root.destroy()
        
def main():

    app = Test()
    root.mainloop()


if __name__ == '__main__':
    main()
