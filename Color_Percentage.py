import subprocess as sb
import tkinter
import tkinter as tk
from tkinter import messagebox as mbox
from tkinter.filedialog import askopenfilename
import PIL
from PIL import Image, ImageTk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.winfo_toplevel().title("Panama Disease YoloV4")
        self.Img = tkinter.Canvas(self, height=300, width=550, bg="light gray")
        self.Img.pack(side="top")

        def takePicturePress():
            global fname
            fname = askopenfilename()
		

        takePicture = tk.Button(self, height=2, width=35, command=takePicturePress)
        takePicture["text"] = "Take Picture"
        takePicture.pack(side="left")

        def evaluatepress():
            dnet = sb.run(["python3", "detect.py", "--weights", "./checkpoints/custom-416.tflite", "--size","416","--model"
                              , "yolov4", "--images", fname, "--framework", "tflite", "-dont_show"
                           ])
            img = Image.open("./detections/detection1.png")
            img = img.resize((550,300), Image.ANTIALIAS)
            myimage = ImageTk.PhotoImage(img)
            self.Img.create_image(280, 0, image=myimage, anchor = "n")
            self.Img.itemconfig(self.Img, image=myimage)

        evaluateButton = tk.Button(self, height=2, width=35, command=evaluatepress)
        evaluateButton["text"] = "Evaluate"
        evaluateButton.pack(side="right")

        def imageGet():
            mbox.showinfo(title="Warning", message=fname)

        getImageButton = tk.Button(self, height=2, width=35, command=imageGet)
        getImageButton["text"] = "Save Image(s)"
        getImageButton.pack(side="top")

    canvas_width = 900
    canvas_height = 700

    def say_hi(self):
        print("hi there, everyone!")


root = tk.Tk()
root.resizable(False,False)
app = Application(master=root)
app.mainloop()
