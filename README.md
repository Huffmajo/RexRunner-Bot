# RexRunner-Bot
Auto-plays the chrome T-Rex runner game using computer vision template matching

## Goal
Create an AI that can successfully play the chrome dinosaur game on it's own.

## The Plan
My code will have to do the following to achieve my goal:
1. :white_check_mark: Open a browser and direct it to the chrome dino game
    * Python's webbrowser library can take care of this
1. :white_large_square: Screen capture the chrome dino game for analysis
    * Screen capture must give consistent framerate > 30FPS
    * Ideally OS agnostic
    * ~~PIL's ImageGrab?~~ Too slow :turtle:
    * mss? :thumbsup:
1. :white_check_mark: Use dinosaur position to crop screengrab to only gameplay area
1. :white_check_mark: Process the screengrabs to identify obstacles 
    * OpenCV's template matching
    * Draw rectangles around 
1. :white_check_mark: Send inputs based on identified obstacle positions to avoid obstacles
    * pyautogui can simulate keyboard inputs :keyboard::thumbsup:
    * Jump over cacti
    * Duck under pterodactyls
1. :white_large_square: Account for speedup over time
    * Speed variable that increases over time?
    * Track cacti speed basde on last position?
1. :white_check_mark: Auto restart game on failures
    * Template match restart symbol and press a key to restart


## Iterations
### MK-I
![MK-I](/gifs/mkI.gif)
> Top image is directly from the browser. Bottom image is the screen grabs after processing

My first effort worked but had some large shortcomings. The cacti were getting noticed (seen by the rectangles drawn around them on the lower screen)  and the dinosaur was properly jumping to avoid them, but framerates were dropping from 30 FPS to around 6 FPS once the cacti got within range. I think we're losing frames from trying to match multiple catci templates. I'll need to optimize some code to keep those frames steady.
