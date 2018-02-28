#Test GUI

from Tkinter import *

import pyfirmata as f
import threading as th


import warnings
import serial
import serial.tools.list_ports as ports



from time import sleep

class Application(Frame):

    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid()
        self.redvalue = 50
        self.greenvalue = 50
        self.bluevalue = 50        
        self.intensityvalue = 0

        self.saved_bluevalue = self.bluevalue
        self.saved_redvalue = self.redvalue
        self.saved_greenvalue = self.greenvalue
        self.saved_intensity = self.intensityvalue
        
        self.tiltvalue = 90
        self.panvalue = 180
        self.no_pan_servo_val = 90
        self.pan_decrease = -15
        self.pan_increase = 15
        self.speedvalue = 0
        self.create_widgets()
        #create variables for red green and blue

##        arduino_ports = [
##            p.device
##            for p in serial.tools.list_ports.comports()
##            if 'Arduino' in p.description
##        ]
##        if not arduino_ports:
##            raise IOError("No Arduino found")
##        if len(arduino_ports) > 1:
##            warnings.warn('Multiple Arduinos found - using the first')

##        ser = serial.Serial(arduino_ports[0])
        
        
        #self.board = f.Arduino(str(ports.comports()[0].device))



       
        
        self.redpin = self.board.get_pin('d:5:p')
        self.greenpin = self.board.get_pin('d:3:p')
        self.bluepin = self.board.get_pin('d:6:p')

        self.panpin = self.board.get_pin('d:9:i')
        self.tiltpin = self.board.get_pin('d:10:s')
        self.tiltpin.write(90)

        self.lockobj = th.Lock()

        self.degpan_per_sec = 425.0  # set to degrees pan servo turns in one second
        self.set_pan_to_halfway()
        
    def set_pan_to_halfway(self):
        self.do_timed_pan(360/self.degpan_per_sec, self.no_pan_servo_val+self.pan_decrease)
        self.do_timed_pan(180/self.degpan_per_sec, self.no_pan_servo_val+self.pan_increase)
        self.panvalue = 180
        
        
    def decrease_redvalue(self):
        self.redvalue = self.redvalue-5
        self.redscale.set(self.redvalue)

    def increase_redvalue(self):
        self.redvalue = self.redvalue+5
        self.redscale.set(self.redvalue)

    def update_redpercent(self,event):
        self.redvalue = int(self.redpercent.get())
        self.redscale.set(self.redvalue)        

    def update_redscale(self, value):
        self.redvalue = int(value)
        self.redpercent.delete(0,END)
        self.redpercent.insert(10,self.redvalue)
        self.redpin.write(self.redvalue/100.0*self.intensityvalue*0.5/100)#multiplied by 0.75 of intensity so does not reach max

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
        self.greenpin.write(self.greenvalue/100.0*self.intensityvalue*0.5/100.0) #multiplied by 0.75 of intensity so does not reach max       
        

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
        self.bluepin.write(self.bluevalue/100.0*self.intensityvalue*0.5/100)#multiplied by 0.75 of intensity so does not reach max
        
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
        self.redpin.write(self.redvalue/100.0*self.intensityvalue*0.5/100.0) #multiplied by 0.75 of intensity so does not reach max
        self.bluepin.write(self.bluevalue/100.0*self.intensityvalue*0.5/100.0) #multiplied by 0.75 of intensity so does not reach max
        self.greenpin.write(self.greenvalue/100.0*self.intensityvalue*0.5/100.0) #multiplied by 0.75 of intensity so does not reach max

    def decrease_panvalue(self):
        if self.panvalue-5 >= 0:
            self.panvalue = self.panvalue-5
            self.panscale.set(self.panvalue)
            self.pan_warning()
        else:
            self.panlimitwarning.grid()
        t = th.Thread(target=self.do_timed_pan, args=(5/self.degpan_per_sec, self.no_pan_servo_val+self.pan_decrease) )
        t.start()
        self.panscale.set(self.panvalue)
        self.panvaluepercent.delete(0,END)
        self.panvaluepercent.insert(10,self.panvalue)


    def decrease_big_panvalue(self):
        if self.panvalue-10 >= 0:
            self.panvalue = self.panvalue-10
            self.panscale.set(self.panvalue)
            self.pan_warning()
        else:
            self.panlimitwarning.grid()
        t = th.Thread(target=self.do_timed_pan, args=(10/self.degpan_per_sec, self.no_pan_servo_val+self.pan_decrease) )
        t.start()
        self.panscale.set(self.panvalue)
        self.panvaluepercent.delete(0,END)
        self.panvaluepercent.insert(10,self.panvalue)

    def increase_panvalue(self):
        if self.panvalue+5 <= 350:
            self.panvalue = self.panvalue+5
            self.panscale.set(self.panvalue)
            self.pan_warning()
        else:
            self.panlimitwarning.grid() 
        t = th.Thread(target=self.do_timed_pan, args=(5/self.degpan_per_sec, self.no_pan_servo_val+self.pan_increase) )
        t.start()
        self.panscale.set(self.panvalue)
        self.panvaluepercent.delete(0,END)
        self.panvaluepercent.insert(10,self.panvalue)

    def pan_warning(self):
        if self.panvalue <= 0 or self.panvalue >= 350:
            self.panlimitwarning.grid()
        else:
            self.panlimitwarning.grid_remove()
    
    def increase_big_panvalue(self):
        if self.panvalue+10 <= 350:
            self.panvalue = self.panvalue+10
            self.panscale.set(self.panvalue)
            self.pan_warning()
        else:
            self.panlimitwarning.grid()
        t = th.Thread(target=self.do_timed_pan, args=(10/self.degpan_per_sec, self.no_pan_servo_val+self.pan_increase) )
        t.start()
        self.panscale.set(self.panvalue)
        self.panvaluepercent.delete(0,END)
        self.panvaluepercent.insert(10,self.panvalue)

    def update_panpercent(self,event):
        if (int(self.panvaluepercent.get()) >= 0 and int(self.panvaluepercent.get()) <= 350):
            diff = self.panvalue - int(self.panvaluepercent.get())
            if (diff > 0):
                val = self.pan_decrease
            else:
                val = self.pan_increase   
            t = th.Thread(target=self.do_timed_pan, args=(abs(diff)/self.degpan_per_sec, self.no_pan_servo_val+val) )
            t.start()
            
            self.panvalue = int(self.panvaluepercent.get())
            self.panscale.set(self.panvalue)
            self.pan_warning()
        

  #  def update_panscale(self, value):
  #      self.panvalue = int(value)
  #      self.panvalue.delete(0,END)
  #      self.panvalue.insert(10,self.panvalue)
        

    def update_panvalue(self, value):
        self.panvalue = int(value)
        self.panvaluepercent.delete(0,END)
        self.panvaluepercent.insert(10,self.panvalue)
        

    def do_timed_pan(self, time, val):
        with self.lockobj:        
            print("Doing pan {0}, {1}".format(time, val))
            self.panpin.mode = f.SERVO
            self.panpin.write(val)
            sleep(time)
            self.panpin.write(self.no_pan_servo_val)
            self.panpin.mode = f.INPUT
    
    def update_tiltvalue(self, value):
        self.tiltvalue = value
        self.tiltpin.write(value)
        self.tiltpercent.delete(0,END)
        self.tiltpercent.insert(10,self.tiltvalue)

    def update_tiltpercent(self,event):
        self.tiltvalue = int(self.tiltpercent.get())
        self.tiltscale.set(self.tiltvalue)    

    def decrease_tiltvalue(self):
        self.tiltvalue = int(self.tiltvalue)-1
        self.tiltscale.set(self.tiltvalue)
        
    def increase_tiltvalue(self):
        self.tiltvalue = int(self.tiltvalue)+1
        self.tiltscale.set(self.tiltvalue) 

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

    def create_widgets(self):
        #color label
        self.Color = Label(self, text = "Color              ", font=16)
        self.Color.grid()
        #red light
        self.red = Label(self, text = "     Red:")
        self.red.grid(sticky=W)
        self.redpercentlabel = Label(self, text = "Enter") 
        self.redpercentlabel.grid(row=2, column=9)
        self.redpercent = Entry(self, width=4)
        self.redpercent.grid(row=2, column=11)        
        self.redpercent.bind("<Return>", self.update_redpercent)        
        self.red.grid(row=2, column=0)
        self.reddecrease = Button(self, text = "-",command=self.decrease_redvalue)
        self.reddecrease.grid(row=2, column=2)
        self.redscale = Scale(self, from_=0, to=100, orient=HORIZONTAL, command=self.update_redscale, activebackground="red")
        self.redscale.set(self.redvalue)
        self.redscale.grid(row=2, column=3)
        self.redincrease = Button(self, text = "+", command=self.increase_redvalue)
        self.redincrease.grid(row=2, column=8)
        #green light
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
        #blue light
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
        #intensity 
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
        #camera label
        self.spacemaker = Label(self, text = " ", font=16)
        self.spacemaker.grid(row=9, column=0)
        self.Camera = Label(self, text = "Camera angle", font=16)
        self.Camera.grid(row=10, column=0)
        #pan 
        self.pan = Label(self, text = "     Pan:")
        self.pan.grid(sticky=W)
        self.panvaluelabel = Label(self, text = "Enter") 
        self.panvaluelabel.grid(row=11, column=9)
        self.panvaluepercent = Entry(self, width=4)
        self.panvaluepercent.grid(row=11, column=11)        
        self.panvaluepercent.bind("<Return>", self.update_panpercent)
        self.pan.grid(row=11, column=0)
        self.pandecrease = Button(self, text = "-", command=self.decrease_panvalue)
        self.pandecrease.grid(row=11, column=2)

        self.panlimitwarning = Label(self, text = "Close/at limit", fg="red")
        self.panlimitwarning.grid(row=11, column=12)
        self.panlimitwarning.grid_remove()
        

        self.pandecrease = Button(self, text = "--", command=self.decrease_big_panvalue)
        self.pandecrease.grid(row=11, column=1)
        #self.pandecreaseplus
        
        #self.panscale = Scale(self, from_=0, to=350, command=self.update_panvalue, orient=HORIZONTAL)
        self.panscale = StringVar()
        self.panscale.set(self.panvalue)
        self.panvaluepercent.delete(0,END)
        self.panvaluepercent.insert(10,self.panvalue)
        self.panscalelabel = Label(self, textvariable=self.panscale)
        self.panscalelabel.grid(row=11, column=3)
        self.panincrease = Button(self, text = "+", command=self.increase_panvalue)
        self.panincrease.grid(row=11, column=8)

        self.panincrease = Button(self, text = "++", command=self.increase_big_panvalue)
        self.panincrease.grid(row=11, column=9)
        
        #tilt
        self.tilt = Label(self, text = "     Tilt:")
        self.tilt.grid(row=12, sticky=W)
        self.tiltdecrease = Button(self, text = "-", command=self.decrease_tiltvalue)
        self.tiltdecrease.grid(row=12, column=2)
        self.tiltscale = Scale(self, from_=10, to=170, orient=HORIZONTAL, command=self.update_tiltvalue)
        self.tiltscale.set(90)   #POSSIBLY CHANGE TO 0
        self.tiltscale.grid(row=12, column=3)
        self.tiltincrease = Button(self, text = "+", command=self.increase_tiltvalue)
        self.tiltincrease.grid(row=12, column=8)
        self.tiltpercentlabel = Label(self, text = "Enter") 
        self.tiltpercentlabel.grid(row=12, column=9)
        self.tiltpercent = Entry(self, width=4)
        self.tiltpercent.grid(row=12, column=11)        
        self.tiltpercent.bind("<Return>", self.update_tiltpercent)

        #lighting pre-sets
      
        self.lightset1 = Button(self, text = "Aged Oil Optimized Light", command=self.set_optimized_light)
        self.lightset1.grid(row=6, column=2, columnspan =3, sticky=W)
        self.lightsave = Button(self, text = "Save Current Lighting", command=self.save_light)
        self.lightsave.grid(row=7, column =2, columnspan =3, sticky=W)
        self.lightrestore = Button(self, text = "Restore Saved Lighting", command=self.restore_light)
        self.lightrestore.grid(row=8, column = 2, columnspan =3, sticky=W)


def on_close():
    try:
        app.bluepin.write(0)
        app.redpin.write(0)
        app.greenpin.write(0)
        app.panpin.mode = f.INPUT
        app.tiltpin.mode = f.INPUT
    except:
        pass
    root.destroy()

root = Tk()

root.title("GUI")
root.geometry("425x400")
root.protocol("WM_DELETE_WINDOW", on_close)

app = Application(root)


root.mainloop()
