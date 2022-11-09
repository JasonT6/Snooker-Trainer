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

cam.set(3, width)
cam.set(4, height)

fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter('output.avi', fourcc, 20, (width, height),0)


framesWanted = 120
frameCount = 0

start = False


while (True):
    success, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if (success):
        out.write(gray)

    cv2.imshow('video', cv2.flip(gray, 1))

    gray = cv2.flip(gray,-1)


    if keyboard.is_pressed("s") and start == False:
        start = True
        time.sleep(3)


    if start == True and (frameCount < framesWanted):

        frameCount += 1
        brightspot = (cv2.minMaxLoc(gray))[3]

        brightestArrayX.append(brightspot[0])
        brightestArrayY.append(brightspot[1])


    if frameCount == framesWanted:

        plt.plot(brightestArrayX, brightestArrayY, color = 'red', linestyle = 'solid', linewidth = 1, marker = 'o', markersize = 2, markerfacecolor = 'blue', markeredgecolor = 'blue')
        
        averageX = np.mean(brightestArrayX)
        averageY = np.mean(brightestArrayY)

        standardDeviationX = np.std(brightestArrayX)
        standardDeviationY = np.std(brightestArrayY)

        print("standard deviation is:", standardDeviationX)

        plt.xlim(np.amin(brightestArrayX) - standardDeviationX, np.amax(brightestArrayX) + standardDeviationX)
        plt.ylim(np.amin(brightestArrayY) - standardDeviationY, np.amax(brightestArrayY) + standardDeviationY)

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
