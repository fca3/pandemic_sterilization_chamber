from tkinter import *
from tkinter import font
import RPi.GPIO as GPIO
import configparser
import os
import time
import threading

#Read Settings
parser = configparser.ConfigParser()
parser.read('config.ini')

#Gloval Variables
pin = 21
appMode = 'IDLE'
cwd = os.getcwd()

armingTime = int(parser.get('Settings','ArmingSeconds'))
activeUVTime = int(parser.get('Settings','ActiveUVSeconds'))

armingSound = parser.get('Settings','ArmingSoundFile')
activeSound = parser.get('Settings','ActiveSoundFile')

TIME = 0

#Setting GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.HIGH)

def countDown():
	global globalTimer, TIME
		
	if TIME>0:
		mins, secs = divmod(TIME, 60)
		timer = '{:02d}:{:02d}'.format(mins, secs)
		timerLabel['text'] = timer
		TIME = TIME-1
		globalTimer = threading.Timer(1, countDown)
		globalTimer.start()
	else:
		if appMode == 'ARMED':
			activateUV()
		elif appMode == 'ACTIVE':
			disarmDevice()
		
	
def displayMode(modeText):
	global appMode
	appMode = modeText
	
	if modeText == 'IDLE':
		backColor = 'white'
		textColor = 'black'
		timerLabel['text'] = '00:00'
				
	elif modeText == 'ARMED':
		backColor = 'black'
		textColor = 'red'
		
	elif modeText == 'ACTIVE':
		backColor = 'light blue'
		textColor = 'purple'
	
	win['background'] = backColor 
	
	armButton['background'] = backColor
	armButton['highlightbackground'] = backColor
	
	resetButton['background'] = backColor
	resetButton['highlightbackground'] = backColor
	
	exitButton['background'] = backColor
	exitButton['highlightbackground'] = backColor
	exitButton['fg'] = textColor
	
	statusLabel['background'] = backColor
	statusLabel['fg'] = textColor
	statusLabel['text'] = modeText
	
	timerLabel['background'] = backColor
	timerLabel['fg'] = textColor
	

def activateUV():
	global globalTimer, TIME
	
	#Set timer
	TIME = activeUVTime
	globalTimer = threading.Timer(0, countDown)
	globalTimer.start()

	#Set display mode
	displayMode('ACTIVE')

	os.system('pkill omxplayer')
	command = 'omxplayer --loop -o local {0}/audios/{1} &'.format(cwd, activeSound)
	os.system(command)

	#Turn on Light
	GPIO.output(pin,GPIO.LOW)
	

def armDevice():
	global globalTimer, TIME

	if appMode == 'IDLE':
		#Set timer
		TIME = armingTime
		globalTimer = threading.Timer(0, countDown)
		globalTimer.start()
	
	#Set display mode
	displayMode('ARMED')
	command = 'omxplayer --loop --vol -1000 -o local {0}/audios/{1} &'.format(cwd, armingSound)
	os.system(command)
	
	
def disarmDevice():
	global globalTimer, TIME
	
	#Cancel Timer
	globalTimer.cancel()

	os.system('pkill omxplayer')
	
	#Turn off Light
	GPIO.output(pin,GPIO.HIGH)
	
	#Set display mode
	displayMode('IDLE')
	

def exitProgram():
	disarmDevice()
	
	GPIO.cleanup()
	win.quit()	

# Create and configure Window
win = Tk()
#win.geometry('480x320')
win.attributes("-fullscreen", True)

globalTimer = threading.Timer(0.01, countDown)

exitFont = font.Font(family = 'Helvetica', size = 16, weight = 'bold')
statusFont = font.Font(family = 'Helvetica', size = 30, weight = 'bold')
timerFont = font.Font(family = 'Helvetica', size = 50, weight = 'bold')

statusLabel  = Label(win, text = "Idle", font = statusFont, height =1 , width = 7) 
statusLabel.pack()
statusLabel.place(x=480-180,y=5)

timerLabel  = Label(win, text = "00:00", font = timerFont, height =1 , width = 5) 
timerLabel.pack()
timerLabel.place(x=480-200,y=60)

armImg = PhotoImage(file = 'arming_button.png')
armButton = Button(win, image=armImg, command=armDevice )
armButton.pack()
armButton.place(x=5,y=5)

resetImg = PhotoImage(file = 'reset_button.png')
resetButton = Button(win, image=resetImg, command=disarmDevice )
resetButton.pack()
resetButton.place(x=480-110,y=320-110)

exitButton  = Button(win, text = "Exit", font = exitFont, command = exitProgram, height =1 , width = 3) 
exitButton.pack()
exitButton.place(x=5,y=320-40)

displayMode('IDLE')
mainloop()
