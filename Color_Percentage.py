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

            file.write("{},{},{},1\n".format(green,yellow,brown))
            file.close()


            

        evaluatebutton = tk.Button(self, height=2, width=35, command=evaluatepress)
        evaluatebutton["text"] = "Evaluate"
        evaluatebutton.pack(side="right")

        
            


   

class Color_Percent:
    def getcolorpercent(image:str):

        img = cv2.imread(image)#link

        lower = np.array([200, 200, 200])
        upper = np.array([255, 255, 255])

        # Create mask to only select black
        thresh = cv2.inRange(img, lower, upper)

        # apply morphology
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # invert morp image
        mask = 255 - morph
        # apply mask to image
        result = cv2.bitwise_and(img, img, mask=mask)
        cv2.imwrite('result.jpg', result) 

        img = cv2.imread('result.jpg')#link

        # Scale image to small :
        scalePercent = 0.35

        # Calculate the new dimensions
        width = int(img.shape[1] * scalePercent)
        height = int(img.shape[0] * scalePercent)
        newSize = (width, height)

        img = cv2.resize(img, newSize, None, None, None, cv2.INTER_AREA)

        brown = [145, 80, 47]  # RGB
        diff = 45
        boundaries = [([brown[2]-diff, brown[1]-diff, brown[0]-diff],
                [brown[2]+diff, brown[1]+diff, brown[0]+diff])]
        # in order BGR as opencv represents images as numpy arrays in reverse order

        for (lower, upper) in boundaries:
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)
            mask = cv2.inRange(img, lower, upper)
            
            ax = np.sum(img)
            ratio_brown = cv2.countNonZero(mask)/np.sum(img != 0)
           

            
        yellow = [255, 255, 168]  # RGB
        diff = 160

        boundaries = [([yellow[2]-diff, yellow[1]-diff, yellow[0]-diff],
                [yellow[2]+diff, yellow[1]+diff, yellow[0]+diff])]
        # in order BGR as opencv represents images as numpy arrays in reverse order

        for (lower, upper) in boundaries:
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)
            mask = cv2.inRange(img, lower, upper)
            

            ratio_yellow = cv2.countNonZero(mask)/np.sum(img != 0)
            
        green = [204, 255, 203]  # RGB
        diff = 200
        boundaries = [([green[2]-diff, green[1]-diff, green[0]-diff],
                [green[2]+diff, green[1]+diff, green[0]+diff])]
        # in order BGR as opencv represents images as numpy arrays in reverse order

        for (lower, upper) in boundaries:
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)
            mask = cv2.inRange(img, lower, upper)
            

            ratio_green = cv2.countNonZero(mask)/np.sum(img != 0)
           

        greenpixels = np.round((ratio_green*100) / scalePercent)
        yellowpixels = np.round((ratio_yellow*100) / scalePercent)
        brownpixels = np.round((ratio_brown*100) / scalePercent )


        return greenpixels,yellowpixels,brownpixels


    

root = tk.Tk()
root.resizable(False,False)
app = Application(master=root)
app.mainloop()

