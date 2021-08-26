import os, time, json, re
import tkinter as tk, threading
from tkinter import filedialog, PhotoImage, Image, messagebox
from pathlib import Path
from PIL import ImageTk, Image

firstRun = True
file_paths = [os.path.join(Path().absolute(), 'camera.jpg')]
syringeStatus = [None, None, None, None, None, None]


class TestGUI():

    def __init__(self):
        
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True) 
        # self.root.geometry("800x480")

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

        # New
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

        # end






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

        self.cleaningProcess()

    def cleaningProcess(self):
        # Refreshes GUI components to show the cleaning process
        self.lblProcessOne.lower()
        self.lblProcessTwo.lower()
        self.lblProcessOne = tk.Label(fg='#F0EFF5', image=self.cleaningProcessPhotoImage)
        self.lblProcessOne.place(x=300, y=170)
        self.lblProcessTwo = tk.Label(fg='#F0EFF5', image=self.checkingSyringePhotoImage)
        self.lblProcessTwo.place(x=300, y=290)

        self.dryingProcess()

    def dryingProcess(self):
        self.lblProcessOne.lower()
        self.lblProcessTwo.lower()
        self.lblProcessOne = tk.Label(fg='#F0EFF5', image=self.dryingProcessPhotoImage)
        self.lblProcessOne.place(x=300, y=170)
        self.lblProcessTwo = tk.Label(fg='#F0EFF5', image=self.cleaningProcessPhotoImage)
        self.lblProcessTwo.place(x=300, y=290)

        self.sterilisationProcess()

    def sterilisationProcess(self):
        self.lblProcessOne.lower()
        self.lblProcessTwo.lower()
        self.lblProcessOne = tk.Label(fg='#F0EFF5', image=self.sterilisationProcessPhotoImage)
        self.lblProcessOne.place(x=300, y=170)
        self.lblProcessTwo = tk.Label(fg='#F0EFF5', image=self.dryingProcessPhotoImage)
        self.lblProcessTwo.place(x=300, y=290)

        self.finalProcess()

    def finalProcess(self):
        self.lblProcessOne.lower()
        self.lblProcessTwo.lower()
        self.lblCleaningCompleted = tk.Label(fg='#F0EFF5', image=self.cleaningCompletedPhotoImage, borderwidth=0,
                                             highlightthickness=0)
        self.lblCleaningCompleted.place(x=320, y=185)
        messagebox.showinfo("Cleaning completed", "SMS sent to nurse.")

        self.reset()

    def reset(self):
        self.lblProcessOne.lower()
        self.lblProcessTwo.lower()
        self.lblCleaningCompleted.lower()
        self.lblNoUpdate.lift()
        self.btnStart.lift()
        self.lblStartText.lift()


app = TestGUI()
