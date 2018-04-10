# Capstone
Contains code used for Transformer Inspection Robot Capstone project for Altalink. It is intended to be run with an Arduino Uno, and USB camera connected to two USB ports on a Windows laptop or desktop machine.

The executable is only supported on Windows; however, the GUI can still be run through Python on Linux and MacOS.

## Running the GUI
**Load StandardFirmata sketch to Arduino**

1. Upload the StandardFirmata sketch to the Arduino. If you are new to Arduino, download the Arduino IDE [here](https://www.arduino.cc/en/Main/Software).
2. Once downloaded, navigate to File -> Examples -> Firmata -> StandardFirmata, and upload this sketch to the Arduino.
3. Ensure that the red, green, and blue LEDs are connected to PWM pins 5, 3, and 6, respectively.

**Run the executable**
1. Navigate to the /GUI/Executable/ folder in this repository, download the lighting_gui.exe file. 
2. Double-click on the executable to run.

## Making Changes
1. Check out GUI/lighting_gui.py
2. Ensure all dependencies are installed. In an administrative command window (or using sudo command if Unix-based OS):

```
    pip install pyfirmata
    pip install opencv-python
    pip install pillow
```
    
If any dependencies are missing, an error message will be shown when attempting to run the GUI. Simply install any missing dependencies and you should be good to go. Happy coding!
