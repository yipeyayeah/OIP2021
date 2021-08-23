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

        self.settingButton = Button(self, text="Setting", command = self.setting)
        self.settingButton.grid(row=2, column=3, pady=4)

        #hbtn = Button(self, text="Help")
        #hbtn.grid(row=5, column=0, padx=5)

        exitButton = Button(self, text="Exit", command = self.quit)
        exitButton.grid(row=4, column=3, pady=4)
        #root.mainloop()
    def startWork(self):
        print("Start working")
        #activate camera module to take pic of syringe
        #photo taken compare with slickk ai
        #dry, wet, dirty activate components
        
        camera = PiCamera()

        camera.start_preview()
        camera.annotate_text = "Hello world!"
        sleep(5)
        camera.capture('/home/pi/Desktop/text.jpg')
        camera.stop_preview()
        

    def setting(self):
        app = tk.Tk()
        newWindow = tk.Toplevel(app)
                
        newWindow.title("Settings")
        newWindow.geometry("500x300")
        #Label(newWindow, text ="This is a new window")
        

        confirmButton = Button(self, text="Confirm", command = self.quit)
        confirmButton.grid(row=5, column=3)
        

waterControl = [
                "Low",
                "Medium",
                "High"
        ]
fanSpeed = [
                "Low",
                "Medium",
                "High"
        ]

lab1 = Label(root, text="condition №1", font="Arial 8", anchor='w')
mymenu1 = OptionMenu(root, 'Low', *waterControl)
lab2 = Label(root, text="condition №2", font="Arial 8", anchor='w')
mymenu2 = OptionMenu(root, 'Low', *fanSpeed)

lab1.pack(side="top",fill = "x")
mymenu1.pack(side="top",fill = "y")
lab2.pack(side="top",fill = "x")
mymenu2.pack(side="top",fill = "y")

        #clicked = tk.StringVar()
        #clicked.set("Low")
        #drop = OptionMenu(root, clicked, *options)
        #drop.pack()  
            
def quit(self):
        self.root.destroy()
        
def main():


    app = Test()
    root.mainloop()


if __name__ == '__main__':
    main()