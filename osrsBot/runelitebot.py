import pyautogui as pg
import numpy as np
import cv2
from matplotlib import pyplot as plt
from time import time
import keyboard

# \\mac\Home\Documents\Code\Python\osrsBot\opencv\build\x64\vc15\bin\opencv_annotation.exe --annotations=pos.txt --images=positive/    
# \\mac\Home\Documents\Code\Python\osrsBot\opencv\build\x64\vc15\bin\opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 600 -vec pos.vec  
# \\mac\Home\Documents\Code\Python\osrsBot\opencv\build\x64\vc15\bin\opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -w 50 -h 50 -precalcValBufSize 3000 -precalcIdxBufSize 3000 -numPos 70 -numNeg 1000 -maxFalseAlarmRate 0.4 -minHitRate 0.999 -numStages 12 

# Trained Model
model = cv2.CascadeClassifier("treeDetector50x50s8.xml")

# top-left coordinates
top_left_x = 758   
top_left_y = 625

# bottom-right coordinates
bottom_right_x = 1520
bottom_right_y = 1095

# width and height of the RuneLite window
window_width = bottom_right_x - top_left_x  
window_height = bottom_right_y - top_left_y  

previous_frame_time = 0

while True:
    loop_time = time()
    # Get screenshot
    screenshot = pg.screenshot(region=(top_left_x, top_left_y, window_width, window_height))
    # Convert the image into a numpy array and then to BGR
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Do Object Detection
    rectangles = model.detectMultiScale(screenshot)

    # Draw rectangles
    for (x, y, w, h) in rectangles:
        cv2.rectangle(screenshot, (x, y), (x+w, y+h), (0, 255, 0), 2) # change the color and thickness as you prefer

    # Display image
    cv2.imshow("RuneLite Bot", screenshot)
    
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
