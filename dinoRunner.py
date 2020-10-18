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
        color: if true, returns a color screengrab
               otherwise returns a gray screengrab

Return  image of screenshot at provided
"""
def GrabScreen(top, left, width, height, color = False):
    sct = mss.mss()
    crop = {"top": top, "left": left, "width": width, "height": height}
    img = np.asarray(sct.grab(crop))
    if color is False:
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return img

"""
Returns position of needle in haystack
"""
def GetTemplatePosition(haystack, needle):
    result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)
    _, maxVal, _, maxLoc = cv.minMaxLoc(result)
    tempX, tempY = maxLoc
    return tempX, tempY, maxVal

"""
Returns array of positions of needles in haystack
"""
def GetTemplatePositions(haystack, needle, threshold):
    result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    return locations

"""
GetCenterPoint
Returns x and y position coordinates of given image's center
"""
def GetCenterPoint(img, topLeftX, topLeftY):
    w, h = img.shape[::-1]
    # h = img.shape[1]
    # w = img.shape[0]
    centerX = topLeftX + int(w/2)
    centerY = topLeftY + int(h/2)
    return (centerX, centerY)

"""
GetLowerRightPoint
Returns x and y position coordinates of given image's lower right
"""
def GetLowerRightPoint(img, topLeftX, topLeftY):
    x = topLeftX + img.shape[1]
    y = topLeftY + img.shape[0]
    return (x, y)

def OpenWebPage(url):
    try:
        wb.open(url, 1, True)
        time.sleep(2)    # give page time to load
    except wb.Error as e:
        print("Unable to open {} : {}".format(url, e))
        sys.exit()

def Jump():
    pyautogui.press("up")
    status = "jumping"
    return status

def Duck(duration):
    status = "ducking"
    pyautogui.keyDown("down")
    time.sleep(duration)
    pyautogui.keyUp("down")
    return status

def StopDucking():
    pyautogui.keyUp("down")
    status = ""
    return status

def Main():
    # load obstacle templates
    templateCacti = []
    templatePtero = []
    templateDino = cv.imread("images/dino.png", 0)
    templateRestart = cv.imread("images/restart.png", 0)
    for i in range(1, 7):
        templateCacti.append(cv.imread("images/cacti_{}.png".format(i), 0))
    for i in range(1, 3):
        templatePtero.append(cv.imread("images/pterodactyl_{}.png".format(i), 0))

    threshold = 0.95
    grounded = True
    status = ""

    # open game webpage
    OpenWebPage("https://chromedino.com/")
    # OpenWebPage("http://www.trex-game.skipser.com/")

    monitorW, monitorH = pyautogui.size()
    fullScreen = GrabScreen(0, 0, monitorW, monitorH)   # haystack
    cropX, cropY , _ = GetTemplatePosition(fullScreen, templateDino) # dino's position in fullscreen
    dinoWidth = templateDino.shape[1]
    dinoHeight = templateDino.shape[0]
    cropH = 150
    cropW = 600

    dinoCrop = GrabScreen(int(cropY - cropH/2 - 20), cropX, cropW, cropH)
    dinoX, startingDinoY , _ = GetTemplatePosition(dinoCrop, templateDino) # dino's position in crop
    dinoCenterX, _ = GetCenterPoint(templateDino, dinoX, startingDinoY)

    runOffset = 12
    dinoX += runOffset
    dinoCenterX += runOffset

    speedOffset = baseSpeed = 122
    jumpCheck = dinoX + dinoWidth + speedOffset
    duckCheck = dinoX + dinoWidth + 55
    pteroCheck = startingDinoY + 10

    startTime = time.time()
    onlyOnce = True

    while True:
        lastTime = time.time()
        elapsedTime = time.time() - startTime

        speedModifier = elapsedTime * 0.24
        speedOffset = baseSpeed + speedModifier
        jumpCheck = dinoX + dinoWidth + int(speedOffset)

        # grab gameplay frame
        imgColor = GrabScreen(int(cropY - cropH/2 - 20), cropX, cropW, cropH, color=True)
        img = cv.cvtColor(imgColor, cv.COLOR_BGR2GRAY)

        # draw horizontal and vertical limit lines
        lineJump = cv.line(imgColor, (jumpCheck, 0), (jumpCheck, cropH), (255, 0, 0), 1)
        cv.putText(lineJump, str(jumpCheck), (jumpCheck, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        lineDuck = cv.line(imgColor, (duckCheck, 0), (duckCheck, cropH), (255, 0, 0), 1)
        cv.putText(lineDuck, str(duckCheck), (duckCheck, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        linePtero = cv.line(imgColor, (0, pteroCheck), (860, pteroCheck), (255, 0, 0), 1)
        cv.putText(linePtero, str(pteroCheck), (jumpCheck, pteroCheck - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        lineDino = cv.line(imgColor, (dinoCenterX, 0), (dinoCenterX, cropH), (0, 255, 0), 1)
        cv.putText(lineDino, "Dino", (dinoCenterX, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # find dino
        dinoX, dinoY, confidence = GetTemplatePosition(img, templateDino)
        dinoCenterX, _ = GetCenterPoint(templateDino, dinoX, dinoY)
        if confidence >= threshold:
            rect = cv.rectangle(imgColor, (dinoX, dinoY), (dinoX + dinoWidth, dinoY + dinoHeight), (155, 255, 155), 1)
        grounded = dinoY >= startingDinoY

        # check for cacti
        for cactus in templateCacti:
            w, h = cactus.shape[::-1]
            positions = GetTemplatePositions(img, cactus, threshold)

            for pos in zip(*positions[::-1]):
                centerX, _ = GetCenterPoint(cactus, pos[0], pos[1])
                lrX, _ = GetLowerRightPoint(cactus, pos[0], pos[1])
                rect = cv.rectangle(imgColor, pos, (pos[0] + w, pos[1] + h), (0, 0, 255), 1)
                cv.putText(rect, str(centerX), pos, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                if centerX <= dinoCenterX and not grounded:
                    status = Duck(0.01)
                if centerX <= jumpCheck and grounded:
                    status = Jump()

        # check for pterodactyl
        for ptero in templatePtero:
            w, h = ptero.shape[::-1]
            positions = GetTemplatePositions(img, ptero, threshold)

            for pos in zip(*positions[::-1]):
                centerX, centerY = GetCenterPoint(ptero, pos[0], pos[1])
                rect = cv.rectangle(imgColor, pos, (pos[0] + w, pos[1] + h), (255, 255, 0), 1)
                cv.putText(rect, str(centerY), pos, cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                if centerY >= pteroCheck:
                    if centerX <= dinoCenterX and not grounded:
                        status = Duck(0.01)
                    elif centerX <= jumpCheck:
                        if grounded:
                            status = Jump()
                elif centerX <= duckCheck:
                    status = Duck(0.2)

        # auto restart on failure
        _, _, confidence = GetTemplatePosition(img, templateRestart)
        if confidence >= threshold:
            pyautogui.press("up")
            # print("ElapsedTime: {}".format(elapsedTime))
            # print("jumpCheck: {}".format(jumpCheck))
            startTime = time.time()
            status = ""

        # FPS counter
        fps = "FPS: {}".format(int(1/(time.time() - lastTime)))
        cv.putText(imgColor, fps, (int(cropW/2) - 40, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

        # Dino action status
        cv.putText(imgColor, status, (int(cropW/2) + 80, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

        # show cropped image
        cv.imshow("Cropped Image", imgColor)

        if onlyOnce:
            onlyOnce = False
            pyautogui.hotkey("alt", "tab")  # focus browser window for game control
            time.sleep(0.5)
            pyautogui.press("up")           # start the game

        if cv.waitKey(1) == ord("q"):
            break

    cv.destroyAllWindows()
Main()
