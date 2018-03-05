# Import all relevant packages
from tkinter import *
from tkinter import filedialog
import pyfirmata as f
import threading as th
import warnings
import serial
import serial.tools.list_ports as ports
import sys
import cv2
from PIL import Image,ImageTk
import numpy as np
import datetime,os,sys,platform
class lighting_GUI(Tk): # Inherit from Tk class (main window)

    def __init__(self):
        super().__init__()
        # Set up the main window
        self.title("Lighting GUI") # Set GUI title
        self.screen_width = int(self.winfo_screenwidth() * 0.75)
        self.screen_height = int(self.winfo_screenheight() * 0.75)
        self.geometry(str(self.screen_width) + "x" + 
                      str(self.screen_height)) # Set GUI main window size
        self.config(bg = "#2f4f4f")
        self.output_path = os.getcwd() + '/'
        # Create GUI variables for lighting
        self.redvalue = 50
        self.greenvalue = 50
        self.bluevalue = 50        
        self.intensityvalue = 0      
        
        self.saved_bluevalue = self.bluevalue
        self.saved_redvalue = self.redvalue
        self.saved_greenvalue = self.greenvalue
        self.saved_intensity = self.intensityvalue
        
        # Create GUI-Arduino connection
        for serial_port in ports.comports():
            if 'Arduino' in serial_port.description:
                arduino_serial_port = serial_port
                print("Found Arduino Serial Port: {}".format(arduino_serial_port.description))
                print("Lighting System Status: Activated")
        try:
            self.board = f.Arduino(str(arduino_serial_port.device))
            self.redpin = self.board.get_pin('d:5:p')
            self.greenpin = self.board.get_pin('d:3:p')
            self.bluepin = self.board.get_pin('d:6:p')
        except:
            print("No Arduino connected to computer. Lighting System Status: Deactivated")
            pass       
        
        # Set GUI spacing format
        self.grid()
        
        # Create GUI widgets e.g. red/green/blue light control
        self.create_widgets()
        
        # Create safe exit from GUI
        self.protocol("WM_DELETE_WINDOW",self._delete_window)
        
        # Create GUI-Video Feed Connection
        self.cap = cv2.VideoCapture(1) # 0 for laptop camera, 1 for
                                       # external webcam
        if self.cap:
            print("Found camera")
        else:
            print("No camera detected")
        self.video_loop() # Receive video feed
        
    def create_widgets(self):
        #Create colour control widgets
        
        # Label for Colour Control
        self.Color = Label(self, text = "Color Control", font=("Arial",16))
        self.Color.grid()   
        
        # Add menubar
        self.menubar = Menu(self)
        self.menubar.add_command(label="Quit", command = self._delete_window)
        self.config(menu=self.menubar)
#----------Red Colour Control Widget------------------------------------
        self.red_Label = Label(self, text = "     Red:")
        self.red_Label.grid(sticky=W)
        self.red_Label.grid(row=2, column=0)  
        self.redpercentlabel = Label(self, text = "Enter") 
        self.redpercentlabel.grid(row=2, column=9)
        self.redpercent = Entry(self, width=4)
        self.redpercent.grid(row=2, column=11)        
        self.redpercent.bind("<Return>", self.update_redpercent)
        
        self.reddecrease = Button(self, text = "-",command=self.decrease_redvalue)
        self.reddecrease.grid(row=2, column=2)
        self.redscale = Scale(self, from_=0, to=100, orient=HORIZONTAL, command=self.update_redscale, activebackground="red")
        self.redscale.set(self.redvalue)
        self.redscale.grid(row=2, column=3)
        self.redincrease = Button(self, text = "+", command=self.increase_redvalue)
        self.redincrease.grid(row=2, column=8)        
        
#----------Green Colour Control Widget------------------------------------     
        self.green = Label(self, text = "     Green:")
        self.green.grid(sticky=W)
        self.greenpercentlabel = Label(self, text = "Enter") 
        self.greenpercentlabel.grid(row=3, column=9)
        self.greenpercent = Entry(self, width=4)
        self.greenpercent.grid(row=3, column=11)        
        self.greenpercent.bind("<Return>", self.update_greenpercent)    
        self.green.grid(row=3, column=0)
        self.greendecrease = Button(self, text = "-",command=self.decrease_greenvalue)
        self.greendecrease.grid(row=3, column=2)
        self.greenscale = Scale(self, from_=0, to=100, orient=HORIZONTAL, command=self.update_greenscale, activebackground="green")
        self.greenscale.set(self.greenvalue)
        self.greenscale.grid(row=3, column=3)
        self.greenincrease = Button(self, text = "+", command=self.increase_greenvalue)
        self.greenincrease.grid(row=3, column=8)
        
#----------Blue Colour Control Widget------------------------------------  
        self.blue = Label(self, text = "     Blue:")
        self.blue.grid(sticky=W)
        self.bluepercentlabel = Label(self, text = "Enter") 
        self.bluepercentlabel.grid(row=4, column=9)
        self.bluepercent = Entry(self, width=4)
        self.bluepercent.grid(row=4, column=11)        
        self.bluepercent.bind("<Return>", self.update_bluepercent) 
        self.blue.grid(row=4, column=0)
        self.bluedecrease = Button(self, text = "-",command=self.decrease_bluevalue)
        self.bluedecrease.grid(row=4, column=2)
        self.bluescale = Scale(self, from_=0, to=100, orient=HORIZONTAL, command=self.update_bluescale,activebackground="blue")
        self.bluescale.set(self.bluevalue)
        self.bluescale.grid(row=4, column=3)
        self.blueincrease = Button(self, text = "+", command=self.increase_bluevalue)
        self.blueincrease.grid(row=4, column=8)        
        
#----------Intensity Control Widget------------------------------------  
        self.intensity = Label(self, text = "     Intensity:")
        self.intensity.grid(sticky=W)
        self.intensitypercentlabel = Label(self, text = "Enter") 
        self.intensitypercentlabel.grid(row=5, column=9)
        self.intensitypercent = Entry(self, width=4)
        self.intensitypercent.grid(row=5, column=11)        
        self.intensitypercent.bind("<Return>", self.update_intensitypercent)
        self.intensity.grid(row=5, column=0)
        self.intensitydecrease = Button(self, text = "-",command=self.decrease_intensityvalue)
        self.intensitydecrease.grid(row=5, column=2)
        self.intensityscale = Scale(self, from_=0, to=100, orient=HORIZONTAL, command=self.update_intensityvalue)
        self.intensityscale.set(0)
        self.intensityscale.grid(row=5, column=3)
        self.intensityincrease = Button(self, text = "+", command=self.increase_intensityvalue)
        self.intensityincrease.grid(row=5, column=8)        

#-------Lighting Pre-set Control Buttons-----------------------------
        self.lightset1 = Button(self, text = "Aged Oil Optimized Light", command=self.set_optimized_light)
        self.lightset1.grid(row=7, column=2, columnspan =3, sticky=W,pady = 10)
        self.lightsave = Button(self, text = "Save Current Lighting", command=self.save_light)
        self.lightsave.grid(row=9, column =2, columnspan =3, sticky=W,pady = 10)
        self.lightrestore = Button(self, text = "Restore Saved Lighting", command=self.restore_light)
        self.lightrestore.grid(row=11, column = 2, columnspan =3, sticky=W, pady = 10)
        
#-------Video Feed Frame-----------------------------
        self.video_frame = Frame(self,height=self.screen_height/2, width=self.screen_width/1.5)
        self.video_frame.grid(row=2, column=16,padx = 20,rowspan = 9)
        self.video_feed = Label(self.video_frame)
        self.video_feed.grid(row=0, column=0)
        self.snapshot_btn = Button(self, text="Take Snapshot", command=self.take_snapshot)
        self.snapshot_btn.grid(row=12, column=16, sticky=W, padx=15)
      

#========================================================================================================================        
#----------------Red Colour Control Methods-------------------------
    def update_redpercent(self,event):
        self.redvalue = int(self.redpercent.get())
        self.redscale.set(self.redvalue)

    def increase_redvalue(self): # Button increase
        self.redvalue = self.redvalue+5
        self.redscale.set(self.redvalue)
        
    def decrease_redvalue(self): # Button decrease
        self.redvalue = self.redvalue-5
        self.redscale.set(self.redvalue)
        
    def update_redscale(self, value):
        self.redvalue = int(value)
        self.redpercent.delete(0,END)
        self.redpercent.insert(10,self.redvalue)
        try:
            self.redpin.write(self.redvalue/100.0*self.intensityvalue*0.5/100)#multiplied by 0.75 of intensity so does not reach max
        except:
            print("Red pin (Arduino Pin 5) INACTIVE")
            pass
#-------Green Colour Control Methods-----------------------------
    def decrease_greenvalue(self):
        self.greenvalue = self.greenvalue-5
        self.greenscale.set(self.greenvalue)
        
    def increase_greenvalue(self):
        self.greenvalue = self.greenvalue+5
        self.greenscale.set(self.greenvalue)
        
    def update_greenpercent(self,event):
        self.greenvalue = int(self.greenpercent.get())
        self.greenscale.set(self.greenvalue)

    def update_greenscale(self, value):
        self.greenvalue = int(value)
        self.greenpercent.delete(0,END)
        self.greenpercent.insert(10,self.greenvalue)
        try:
            self.greenpin.write(self.greenvalue/100.0*self.intensityvalue*0.5/100.0) #multiplied by 0.75 of intensity so does not reach max
        except:
            print("Green pin (Arduino Pin 3) INACTIVE")
            pass
        
#-------Blue Colour Control Methods-----------------------------
    def decrease_bluevalue(self):
        self.bluevalue = self.bluevalue-5
        self.bluescale.set(self.bluevalue)

    def increase_bluevalue(self):
        self.bluevalue = self.bluevalue+5
        self.bluescale.set(self.bluevalue)

    def update_bluepercent(self,event):
        self.bluevalue = int(self.bluepercent.get())
        self.bluescale.set(self.bluevalue)        

    def update_bluescale(self, value):
        self.bluevalue = int(value)
        self.bluepercent.delete(0,END)
        self.bluepercent.insert(10,self.bluevalue)
        try:
            self.bluepin.write(self.bluevalue/100.0*self.intensityvalue*0.5/100)#multiplied by 0.75 of intensity so does not reach max
        except:
            print("Blue pin (Arduino Pin 6) INACTIVE")
            pass
        
#-------Intensity Control Methods-----------------------------
    def decrease_intensityvalue(self):
        self.intensityvalue = self.intensityvalue-5
        self.intensityscale.set(self.intensityvalue)

    def increase_intensityvalue(self):
        self.intensityvalue = self.intensityvalue+5
        self.intensityscale.set(self.intensityvalue)

    def update_intensitypercent(self,event):
        self.intensityvalue = int(self.intensitypercent.get())
        self.intensityscale.set(self.intensityvalue)  

    def update_intensityvalue(self, value):
        self.intensityvalue = int(value)
        self.intensitypercent.delete(0,END)
        self.intensitypercent.insert(10,self.intensityvalue)
        try:
            self.redpin.write(self.redvalue/100.0*self.intensityvalue*0.5/100.0) #multiplied by 0.75 of intensity so does not reach max
            self.bluepin.write(self.bluevalue/100.0*self.intensityvalue*0.5/100.0) #multiplied by 0.75 of intensity so does not reach max
            self.greenpin.write(self.greenvalue/100.0*self.intensityvalue*0.5/100.0) #multiplied by 0.75 of intensity so does not reach max
        except:
            pass
#-------Lighting Pre-set Control Methods-----------------------------
    def set_optimized_light(self):
        self.bluescale.set(90)
        self.redscale.set(15)
        self.greenscale.set(30)

    def save_light(self):
        self.saved_bluevalue = self.bluevalue
        self.saved_redvalue = self.redvalue
        self.saved_greenvalue = self.greenvalue
        self.saved_intensity = self.intensityvalue

    def restore_light(self):
        self.bluescale.set(self.saved_bluevalue)
        self.redscale.set(self.saved_redvalue)
        self.greenscale.set(self.saved_greenvalue)
        self.intensityscale.set(self.saved_intensity)

#-------GUI Exit Method-----------------------------    
    def _delete_window(self):
        try:
            self.redpin.write(0)
            self.bluepin.write(0)
            self.greenpin.write(0)
        except:
            pass
        print("Exiting GUI")
        self.cap.release()
        cv2.destroyAllWindows()        
        self.destroy()

#-------GUI Video Feed-----------------------------   
    def video_loop(self):
        ok, frame = self.cap.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            cv2image = cv2.flip(cv2image,1)
            #cv2image = cv2.GaussianBlur(cv2image, (7,7), 0)
            #cv2image = cv2.Canny(cv2image, 50, 130)
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.video_feed.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.video_feed.config(image=imgtk)  # show the image
            self.after(10, self.video_loop)  # call the same function after 30 milliseconds  
            
#-------Video Feed Snapshot-----------------------------  
    def take_snapshot(self):
        #ts = datetime.datetime.now() # grab the current timestamp
        #filename = "{}.png".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
        ftypes = [("png file","*.png")]
        filename = filedialog.asksaveasfile(initialdir = self.output_path,
                                                    title = "Save file as",
                                                    filetypes= ftypes)        
        p = os.path.join(self.output_path, filename.name)  # construct output path
        self.current_image.save(filename.name, "PNG")  # save image as png file
        print("[INFO] saved {}".format(filename))       

#---------------Main GUI Application---------------------------  

# Program execution starts here
app = lighting_GUI() # Create GUI instance
app.mainloop()
