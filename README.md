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
    * Draw rectangles around obstacles
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
> Top feed is from the browser. Bottom feed is the screen grabs with debug processing added

My first effort worked but had some large shortcomings. The cacti were getting noticed (seen by the rectangles drawn around them on the lower screen)  and the dinosaur was properly jumping to avoid them, but framerates were dropping from 30 FPS to around 6 FPS once the cacti got within range. I think we're losing frames from trying to match multiple catci templates. I'll need to optimize some code to keep those frames steady.

### MK-II
![MK-II](/gifs/mkII.gif)
> Top feed is from the browser. Bottom feed is the screen grabs with debug processing added

I've added more debug information to the processed feed. The vertical line shows how close an obstacle will get before the dino will jump. I'll probably have to have this gradually move to the right as the game speeds up over time. The horizontal line shows how the dinosaur handles pterodactyls once they're past the vertical line. If they're above the horizontal line, the dino will duck. If they're below the line, the dino will jump. I also refactored some code for performance and clarity. I'm still looking into how to keep framerate consistent while remaining OS agnostic.

### MK-III
![MK-III](/gifs/mkIII.gif)
> Top feed is from the browser. Bottom feed is the screen grabs with debug processing added

I resolved some of the framerate drop issues by only issuing jump commands when the dino is on the ground. This also meant I had to track the dinos y-position to determine this. I Tweaked the horizontal jump-check line to gradually move to the right to account for gamespeed increasing over time. I also adjusted the vertical duck-check line so the dino more accurately jumps or ducks past the pterodactyls. Next I'll fine-tune the starting jump-check position and how it will increase over time (linearly? exponetially? logrithmicly?).