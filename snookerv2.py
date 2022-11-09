from turtle import color
import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
import keyboard

width = 1280
height = 720

brightestArrayX = []
brightestArrayY = []

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
cam.set(cv2.CAP_PROP_EXPOSURE, 0.01)

cam.set(3, width)
cam.set(4, height)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20, (width, height),0)

framesWanted = 120
frameCount = 0

start = False

calibrationDone = False
calibrationKey = False
startCalibration = False
calibrationColor = []
calibrationLowerRange = []
calibrationUpperRange = []


while (calibrationDone == False):
    
    success, frame = cam.read()
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.circle(frame, (640, 360), 20, (255, 255, 255), thickness = 3)
    frame = cv2.flip(frame, 1)
    cv2.putText(frame, "Put cue tip in circle and press 'c' to callibrate.", (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2, cv2.LINE_AA)
    cv2.imshow('SnookerV2 Calibration Window', frame)

    
    if keyboard.is_pressed("c") and calibrationDone == False:
        startCalibration = True

    
    if startCalibration == True:
        time.sleep(3)
        calibrationColor = hsvFrame[int(height/2)][int(width/2)]

        calibrationLowerRange = np.array([int(calibrationColor[0] - 8), int(calibrationColor[1] - 15), int(calibrationColor[2] - 15)])
        calibrationUpperRange = np.array([int(calibrationColor[0] + 8), int(calibrationColor[1] + 15), int(calibrationColor[2] + 15)])

        calibrationDone = True
        
    key = cv2.waitKey(1)
    if key == 27:
        break

while (calibrationDone == True):
    success, frame = cam.read()
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    filteredFrame = cv2.inRange(hsvFrame, calibrationLowerRange, calibrationUpperRange)
    
    M = cv2.moments(filteredFrame)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0

    cv2.circle(filteredFrame, (cX, cY), 5, (255,0,0), -1)


    if (success):
        out.write(filteredFrame)

    cv2.imshow('SnookerV2', cv2.flip(filteredFrame, 1))

    filteredFrame = cv2.flip(filteredFrame, -1)



    if keyboard.is_pressed("s") and start == False:
        start = True
        time.sleep(3)


    if start == True and (frameCount < framesWanted):

        frameCount += 1

        moment = cv2.moments(filteredFrame)

        centerX = int(moment["m10"]/ moment["m00"])
        centerY = int(moment["m01"]/ moment["m00"])

        brightestArrayX.append(centerX)
        brightestArrayY.append(centerY)


    if frameCount == framesWanted:

        plt.plot(brightestArrayX, brightestArrayY, color = 'red', linestyle = 'solid', linewidth = 1, marker = 'o', markersize = 2, markerfacecolor = 'blue', markeredgecolor = 'blue')
        
        averageX = np.mean(brightestArrayX)
        averageY = np.mean(brightestArrayY)

        standardDeviationX = np.std(brightestArrayX)
        standardDeviationY = np.std(brightestArrayY)

        print("standard deviation is:", standardDeviationX)


        plt.xlim(0,1280)
        plt.ylim(0,720)

        plt.grid()
        plt.show()

        frameCount = 0
        start = False
        brightestArrayX.clear()
        brightestArrayY.clear()


    key = cv2.waitKey(1)
    if key == 27:
        break


cam.release()
out.release()
cv2.destroyAllWindows()