import pyautogui as pg
import numpy as np
import cv2
from matplotlib import pyplot as plt
from time import time
import keyboard

# \\mac\Home\Documents\Code\Python\osrsBot\opencv\build\x64\vc15\bin\opencv_annotation.exe --annotations=pos.txt --images=positive/    
# \\mac\Home\Documents\Code\Python\osrsBot\opencv\build\x64\vc15\bin\opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 600 -vec pos.vec  
# \\mac\Home\Documents\Code\Python\osrsBot\opencv\build\x64\vc15\bin\opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -w 24 -h 24 -numPos 52 -numNeg 200 -numStages 12

# Trained Model
#model = cv2.CascadeClassifier("cascade/cascade.xml")

# top-left coordinates
top_left_x = 756   
top_left_y = 593  

# bottom-right coordinates
bottom_right_x = 1520
bottom_right_y = 1095

# width and height of the RuneLite window
window_width = bottom_right_x - top_left_x  
window_height = bottom_right_y - top_left_y  

previous_frame_time = 0

# Masking Pink
#light = np.array([5,50,50])
#dark = np.array([15,255,255])

while True:
    loop_time = time()
    # Get screenshot
    screenshot = pg.screenshot(region=(top_left_x, top_left_y, window_width, window_height))
    # Convert the image into a numpy array and then to BGR
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    #mask = cv2.inRange(screenshot, light, dark)

    # Get mouse position and draw a circle at it only when the mouse is within the RuneLite window
    #mouse_x, mouse_y = pg.position()
    #if top_left_x <= mouse_x < top_left_x + window_width and top_left_y <= mouse_y < top_left_y + window_height:
    #    cv2.circle(screenshot, (int(mouse_x) - top_left_x, int(mouse_y) - top_left_y), 5, (0, 0, 255), -1)
    
    # Do Object Detection
    #rectangles = model.detectMultiScale(screenshot)

    # Draw rectangles
    #for (x, y, w, h) in rectangles:
        #cv2.rectangle(screenshot, (x, y), (x+w, y+h), (0, 255, 0), 2) # change the color and thickness as you prefer

    # Display image
    cv2.imshow("RuneLite Bot", screenshot)
    #cv2.imshow('RuneLite Bot Mask', screenshot)
    
    # Print FPS live
    fps = 1/(loop_time - previous_frame_time)
    previous_frame_time = loop_time

    fps = int(fps)
    print(f"Current FPS: {fps}")

    # Check if 'q' is pressed
    key = cv2.waitKey(1)
    if key == ord('q') or key == ord('Q'):
        # Close the specific 'screenshot' window
        cv2.destroyAllWindows()
        break
    elif key == ord('p'):
        cv2.imwrite(f"positive/{loop_time}.jpg", screenshot)
    elif key == ord('n'):
        cv2.imwrite(f"negative/{loop_time}.jpg", screenshot)

print("Done")
