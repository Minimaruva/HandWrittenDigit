from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np

model = load_model('mnist_model.h5')

def predict_digit(img):
    # A bunch of filters to achieve similar look to input data
    img = img.quantize(8)
    img = img.resize(img.size, Image.NEAREST)
    img = img.resize((20,20))
    img = img.convert('L') # Convert to grayscale
    img = ImageOps.invert(img)
    img = img.filter(ImageFilter.SHARPEN) 
    
    img = img.resize((28,28))
    # img.show()
    img = np.array(img)
    # Reshaping to support our model input and normalizing
    img = img.reshape(1,28,28,1)
    img = img/255.0

    res = model.predict([img])[0]
    return np.argmax(res), max(res)


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Handwritten Digit Recognition")
        self.geometry("600x400")
        self.resizable(False, False)
        self.x = self.y = 0
        self.configure(bg='#72BF78')
        
        # Creating elements
        self.canvas = tk.Canvas(self, width=356, height=356, bg = "white", cursor="circle")
        self.label = tk.Label(self, text="Draw..", font=("Helvetica", 48), bg='#72BF78', fg='black')
        self.classify_btn = tk.Button(self, text = "Recognise", command = self.classify_handwriting,bg="#FEFF9F", relief=tk.FLAT, activebackground="#FEFF9F")   
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all,bg="#FEFF9F", relief=tk.FLAT, activebackground="#FEFF9F")
       
        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        
        #self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)


    def clear_all(self):
        self.canvas.delete("all")


    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()  # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND)  # get the coordinate of the canvas
        a,b,c,d = rect
        rect=(a+4,b+4,c-4,d-4)
        im = ImageGrab.grab(rect)

        digit, acc = predict_digit(im)
        self.label.configure(text= str(digit)+', '+ str(int(acc*100))+'%')


    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=14 # brush size
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')


app = App()
mainloop()
