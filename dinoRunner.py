"""
Control chromeDino web game through computer vision template matching
"""

import sys
import webbrowser as wb
import time
import cv2 as cv
import numpy as np
import mss
import pyautogui

"""
Returns grayscale image of screen at provided points

Params  top: Y-position of top left corner of screenshot
        left: X-position of top left corner of screenshot
        width: Width of screenshot right from left
        height: Height of screenshot down from top

Return  Grayscale image of screenshot at provided
"""
def GrabScreen(top, left, width, height):
    sct = mss.mss()
    crop = {"top": top, "left": left, "width": width, "height": height}
    img = np.asarray(sct.grab(crop))
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return imgGray

"""
Returns position of needle in haystack
"""
def GetTemplatePosition(haystack, needle, threshold):
    result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result)

    # if maxVal < threshold:
    #     print("Template not confidently located. Confidence: {}".format(maxVal))
    #     sys.exit()

    tempX, tempY = maxLoc
    return tempX, tempY, maxVal

def Main():
    # load obstacle templates
    templateDino = cv.imread("images/dino.png", 0)  
    templateCactus1 = cv.imread("images/cactus_1.png", 0)  
    templateCactus2 = cv.imread("images/cactus_2.png", 0)  
    templateCacti1 = cv.imread("images/cacti_1.png", 0)  
    templateCacti2 = cv.imread("images/cacti_2.png", 0)  
    templateCacti3 = cv.imread("images/cacti_3.png", 0)  
    templatePtero1 = cv.imread("images/pterodactyl_1.png", 0)  
    templatePtero2 = cv.imread("images/pterodactyl_2.png", 0)  
    templateRestart = cv.imread("images/restart.png", 0)  

    threshold = 0.8
    

    # open game webpage
    url = "https://chromedino.com/"
    try:
        wb.open(url, 1, True)
        time.sleep(3)    # give page time to load
    except wb.Error as e:
        print("Unable to open {} : {}".format(url, e))
        sys.exit()

    monitorW, monitorH = pyautogui.size()
    fullScreen = GrabScreen(0, 0, monitorW, monitorH)   # haystack
    cropX, cropY , _ = GetTemplatePosition(fullScreen, templateDino, threshold)
    cropH = 150
    cropW = 600

    speedOffset = 0
    horizontalCheck = int(cropX + speedOffset)

    while True:
        lastTime = time.time()

        # grab gameplay frame
        img = GrabScreen(int(cropY - cropH/2 - 20), cropX, cropW, cropH)

        # check for cactus and draw rectangle if it exists
        obstacleX, obstacleY, confidence = GetTemplatePosition(img, templateCactus1, threshold)
        if confidence >= threshold:
            lowerRight = (obstacleX + templateCactus1.shape[1], obstacleY + templateCactus1.shape[0])
            cv.rectangle(img, (obstacleX, obstacleY), lowerRight, (0, 255, 0), 1)
            if obstacleX <= horizontalCheck:
                pyautogui.press("up")

        # cactus_2
        obstacleX, obstacleY, confidence = GetTemplatePosition(img, templateCactus2, threshold)
        if confidence >= threshold:
            lowerRight = (obstacleX + templateCactus2.shape[1], obstacleY + templateCactus2.shape[0])
            cv.rectangle(img, (obstacleX, obstacleY), lowerRight, (0, 255, 0), 1)
            if obstacleX <= horizontalCheck:
                pyautogui.press("up")
        # cacti_1
        obstacleX, obstacleY, confidence = GetTemplatePosition(img, templateCacti1, threshold)
        if confidence >= threshold:
            lowerRight = (obstacleX + templateCacti1.shape[1], obstacleY + templateCacti1.shape[0])
            cv.rectangle(img, (obstacleX, obstacleY), lowerRight, (0, 255, 0), 1)
            if obstacleX <= horizontalCheck:
                pyautogui.press("up")
        # cacti_2
        obstacleX, obstacleY, confidence = GetTemplatePosition(img, templateCacti2, threshold)
        if confidence >= threshold:
            lowerRight = (obstacleX + templateCacti2.shape[1], obstacleY + templateCacti2.shape[0])
            cv.rectangle(img, (obstacleX, obstacleY), lowerRight, (0, 255, 0), 1)
            if obstacleX <= horizontalCheck:
                pyautogui.press("up")
        # pterodactyl
        obstacleX, obstacleY, confidence = GetTemplatePosition(img, templatePtero1, threshold)
        if confidence >= threshold:
            lowerRight = (obstacleX + templatePtero1.shape[1], obstacleY + templatePtero1.shape[0])
            cv.rectangle(img, (obstacleX, obstacleY), lowerRight, (0, 255, 0), 1)
            if obstacleX <= horizontalCheck:
                pyautogui.press("up")
        # pterodacty2
        obstacleX, obstacleY, confidence = GetTemplatePosition(img, templatePtero2, threshold)
        if confidence >= threshold:
            lowerRight = (obstacleX + templatePtero2.shape[1], obstacleY + templatePtero2.shape[0])
            cv.rectangle(img, (obstacleX, obstacleY), lowerRight, (0, 255, 0), 1)
            if obstacleX <= horizontalCheck:
                pyautogui.press("up")
        # restart
        obstacleX, obstacleY, confidence = GetTemplatePosition(img, templateRestart, threshold)
        if confidence >= threshold:
            lowerRight = (obstacleX + templateRestart.shape[1], obstacleY + templateRestart.shape[0])
            cv.rectangle(img, (obstacleX, obstacleY), lowerRight, (0, 255, 0), 1)
            pyautogui.press("up")

        # FPS counter
        fps = "FPS: {}".format(int(1/(time.time() - lastTime)))
        cv.putText(img, fps, (int(cropW/2), 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        # show cropped image
        cv.imshow("Cropped Image", img)

        if cv.waitKey(1) == ord("q"):
            break

    cv.destroyAllWindows()
Main()
