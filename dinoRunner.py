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
    # find dino's position in screengrab
    result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)

    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result)

    if maxVal < threshold:
        print("Template not confidently located. Confidence: {}".format(maxVal))
        sys.exit()

    tempX, tempY = maxLoc
    return tempX, tempY, maxVal

def Main():
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
    templateDino = cv.imread("images/dino.png", 0)      # needle
    cropX, cropY, confidence = GetTemplatePosition(fullScreen, templateDino, 0.8)
    cropH = 150
    cropW = 600

    while True:
        lastTime = time.time()

        # grab gameplay frame
        img = GrabScreen(int(cropY - cropH/2 - 20), cropX, cropW, cropH)

        # FPS counter
        fps = "FPS: {}".format(int(1/(time.time() - lastTime)))
        cv.putText(img, fps, (int(cropW/2), 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        # show cropped image
        cv.imshow("Cropped Image", img)

        if cv.waitKey(1) == ord("q"):
            break

    cv.destroyAllWindows()
Main()
