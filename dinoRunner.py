"""
Control chromeDino web game through computer vision template matching
"""

import sys
import webbrowser as wb
from time import sleep
import cv2 as cv
import numpy as np
from PIL import ImageGrab

# get templates
templateDino = cv.imread("dino.png")

# open game webpage
url = "https://chromedino.com/"
try:
    wb.open(url, 1, True)
    sleep(3)    # give page time to load
except wb.Error as e:
    print("Unable to open {} : {}".format(url, e))
    sys.exit()

# screenshot open webpage
ssFull = ImageGrab.grab()
ssFullNp = np.array(ssFull)
ssFullFrame = cv.cvtColor(ssFullNp, cv.COLOR_BGR2GRAY)

# check what screenshot looks like
cv.imshow("screenshot", ssFullFrame)
cv.waitKey(0)
cv.destroyAllWindows()

# find dino's position in screengrab
