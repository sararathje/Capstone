# First test run at trying to import directly from camera
import cv2
import numpy as np

# Use 0 for device capture
cap = cv2.VideoCapture(0);

# Test if the capture can be opened
if (cap.isOpened() == False):
    print("Sad times :(")
else:
    print("Happy times :)")

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.imshow('Frame',frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

cap.release()
    
