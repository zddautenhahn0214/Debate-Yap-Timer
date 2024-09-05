# Debate Yap Timer

Track how long a person is talking for. 
Currently based on the green border in Discord calls

## Description

Idea is to create a program that will track how long a person is 
speaking based on a screen capture of the discord call. 
This will be based on how long the green border around a speaker 
is active. I want to track how long each person is talking for in 
some debates I've watched on Youtube. Only works on windows.

Make sure to get the full border of their profile in Discord 
when drawing the rectangles or it wont be able to tell they are talking.
Also a similar color to the discord border is present you may need to 
up the min pixel requirement. That would be the minPixels variable in discord_yap_track() in DebateYapTimer.py
Finnally in the same function change maxTime to increase how long it will count for, currently its at 10 seconds for testing purposes

## Getting Started

### Dependencies

* Windows 10
* Developed it in Python 3.9.13
* Python reqs are in requirement.txt
* You need to have the video or discord call on your screen for the app to take screenshots of

### Installing

* Should be good to just download the zip
* Install reqruiemetns, then run main()

### Executing program

* Install Reqs, probably in a virtual enviroment
* Run main()
	```
	python .\main.py
	```
	This will bring up the main menu GUI:
* Once here there are 5 buttons
	* Select Theme: Which lets you change how the GUI looks
	* Select File: Which in theory will let you choose an mp4 to track
	* Select Screen: This runs the code for selecting a screen to track directly and lets you see how it will work
	* Ext: Closes app obv
	* Run: This runs the actual program
* After clicking "Run" it will open a new window for you to choose from. Choose the window that has the video or discord itself you want to track
* That window will be brought to the front, a screenshot taken, and borders auto detected for your speakers. Take a look and decide if they fully cover all the speakers.
	* Close this screen shot by pressing 'q' or any other key when you are ready.
* If those borders do not work click no and a new screenshot will be taken and allow you to manually draw the borders.
	* Right click while drawing to cancel and start over. No way to undo a border after its been drawn for now, so restart if you mess it up. Clsoe this screen the same way as the last.
* After you draw the borders it will ask you if you want to start. Make sure the window you selected is still front and center and press yes.
* After it runs its course the results will be printed to the big box in the GUI main screen
	* The data is not saved anywhere, just printed, so save it someone if you want to keep it before closing the app.

## Future Enhancement Ideas

test.py has a better method for capturing windos than using Pillow to take screenshots. 
Can get the images directly from windows so every single application doesn't have to be brought to fore lol.

I also need to make the GUI still responive while the tracker is running and possibly provide some occasional updates to console or to the GUI. Need to add an exit button for the tracker to know when to end instead of a pretdetermined time amount.

Better autodetection that could dynamicaly track and move the speakers if more joined or left

Another useful feature would be to feed that timer data to some kind of overlay on the video that shows the total speaking time counting up as it is tracked.

Allow for circles instead of just rectangles.
Make work for twitter spaces and add button to choose which.
Add a way to upload a mp4 file and perform all the same functions within the GUI itself