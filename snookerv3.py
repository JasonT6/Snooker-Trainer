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


while (True):
    success, frame = cam.read()
    flipped = cv2.flip(frame, -1)


    qrcode = cv2.QRCodeDetector()
    data, coordinates, data2 = qrcode.detectAndDecode(flipped)

    if data != '':
        cv2.circle(frame, (int(coordinates[0, 0, 0]), int(coordinates[0, 0, 1])), 5, (255,255,0), -1)
        cv2.circle(frame, (int(coordinates[0, 1, 0]), int(coordinates[0, 1, 1])), 5, (255,255,0), -1)
        cv2.circle(frame, (int(coordinates[0, 2, 0]), int(coordinates[0, 2, 1])), 5, (255,255,0), -1)
        cv2.circle(frame, (int(coordinates[0, 3, 0]), int(coordinates[0, 3, 1])), 5, (255,255,0), -1)


    if (success):
        out.write(frame)

    cv2.imshow('SnookerV2', cv2.flip(frame, 1))

    frame = cv2.flip(frame, -1)

    if keyboard.is_pressed("s") and start == False:
        start = True
        time.sleep(3)


    if start == True and (frameCount < framesWanted):


        if data != '':
            centerX = int((coordinates[0, 0, 0] + coordinates[0, 1, 0] + coordinates[0, 2, 0] + coordinates[0, 3, 0])/4)
            centerY = int((coordinates[0, 0, 1] + coordinates[0, 1, 1] + coordinates[0, 2, 1] + coordinates[0, 3, 1])/4)
            brightestArrayX.append(centerX)
            brightestArrayY.append(centerY)
        frameCount += 1



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