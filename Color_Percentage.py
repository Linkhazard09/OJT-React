import subprocess as sb
import tkinter
import tkinter as tk
from tkinter import messagebox as mbox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import numpy as np
import cv2

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.winfo_toplevel().title("Panama Disease Percentage")
        self.Img = tkinter.Canvas(self, height=300, width=550, bg="light gray")
        self.Img.pack(side="top")

        def choosefilepress():
            global fname
            fname = askopenfilename()
		

        openfile = tk.Button(self, height=2, width=35, command=choosefilepress)
        openfile["text"] = "Choose Picture"
        openfile.pack(side="left")

        def evaluatepress():
            CP = Color_Percent
            green,yellow,brown =CP.getcolorpercent(fname)
            percentages = "Green Pixels: {}%\nYellow Pixels: {}%\nBrown Pixels: {}%".format(green,yellow,brown) 
            mbox.showinfo(title="Warning", message=percentages)
            file = open("Percentages.txt",'a')
            file.write("{},{},{}\n".format(green,yellow,brown))
            file.close()


            

        evaluatebutton = tk.Button(self, height=2, width=35, command=evaluatepress)
        evaluatebutton["text"] = "Evaluate"
        evaluatebutton.pack(side="right")

        
            


   

class Color_Percent:
    def getcolorpercent(image:str):

        img = cv2.imread(image)#link

        brown = [145, 80, 45]  # RGB
        diff = 45
        boundaries = [([brown[2]-diff, brown[1]-diff, brown[0]-diff],
                [brown[2]+diff, brown[1]+diff, brown[0]+diff])]
        # in order BGR as opencv represents images as numpy arrays in reverse order

        for (lower, upper) in boundaries:
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)
            mask = cv2.inRange(img, lower, upper)
            

            ratio_brown = cv2.countNonZero(mask)/(img.size/3)
            

            
        yellow = [255, 255, 160]  # RGB
        diff = 160

        boundaries = [([yellow[2]-diff, yellow[1]-diff, yellow[0]-diff],
                [yellow[2]+diff, yellow[1]+diff, yellow[0]+diff])]
        # in order BGR as opencv represents images as numpy arrays in reverse order

        for (lower, upper) in boundaries:
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)
            mask = cv2.inRange(img, lower, upper)
            

            ratio_yellow = cv2.countNonZero(mask)/(img.size/3)
            

        green = [200, 255, 200]  # RGB
        diff = 200
        boundaries = [([green[2]-diff, green[1]-diff, green[0]-diff],
                [green[2]+diff, green[1]+diff, green[0]+diff])]
        # in order BGR as opencv represents images as numpy arrays in reverse order

        for (lower, upper) in boundaries:
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)
            mask = cv2.inRange(img, lower, upper)
            

            ratio_green = cv2.countNonZero(mask)/(img.size/3)
            

        greenpixels = np.round(ratio_green*100, 2)
        yellowpixels = np.round(ratio_yellow*100, 2)
        brownpixels = np.round(ratio_brown*100, 2)


        return greenpixels,yellowpixels,brownpixels


    

root = tk.Tk()
root.resizable(False,False)
app = Application(master=root)
app.mainloop()

