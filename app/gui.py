from tkinter import *
from tkinter import font
import RPi.GPIO as GPIO
import configparser
import os

#Read Settings
parser = configparser.ConfigParser()
parser.read('config.ini')

#Gloval Variables
pin = 21
appMode = 'IDLE'

armingTime = int(parser.get('Settings','ArmingSeconds'))
activeUVTime = int(parser.get('Settings','ActiveUVSeconds'))

cwd = os.getcwd()
print(cwd)
armingSound = parser.get('Settings','ArmingSoundFile')
activeSound = parser.get('Settings','ActiveSoundFile')

#Setting GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.HIGH)

def displayMode(modeText):
	global appMode
	appMode = modeText
	
	if modeText == 'IDLE':
		backColor = 'white'
		textColor = 'black'
		timerLabel['text'] = '00:00'
				
	elif modeText == 'ARMED':
		backColor = 'white'
		textColor = 'black'
		
	elif modeText == 'ACTIVE':
		backColor = 'black'
		textColor = 'black'
	
	win['background'] = backColor 
	armButton['background'] = backColor
	resetButton['background'] = backColor
	exitButton['background'] = backColor
	
	armButton['highlightcolor'] = backColor
	resetButton['highlightcolor'] = backColor
	exitButton['highlightcolor'] = backColor
	
	statusLabel['text'] = modeText
	statusLabel['fg'] = textColor
	statusLabel['background'] = backColor
	
	timerLabel['fg'] = textColor
	timerLabel['background'] = backColor
	

		
def startTimer():
	GPIO.cleanup()
	win.quit()	

def activateUV():
	if GPIO.input(pin) :
		GPIO.output(pin,GPIO.LOW)
		armButton['text'] = 'LED ON'
		
	else:
		GPIO.output(pin,GPIO.HIGH)
		armButton['text'] = 'LED OFF'

def armDevice():
	GPIO.cleanup()
	win.quit()	

def disarmDevice():
	GPIO.cleanup()
	win.quit()	

def exitProgram():
	GPIO.cleanup()
	win.quit()	

# Create and configure Window
win = Tk()
win.geometry('480x320')

exitFont = font.Font(family = 'Helvetica', size = 16, weight = 'bold')
statusFont = font.Font(family = 'Helvetica', size = 30, weight = 'bold')
timerFont = font.Font(family = 'Helvetica', size = 50, weight = 'bold')

armImg = PhotoImage(file = 'arming_button.png')
armButton = Button(win, image=armImg, command=activateUV )
armButton.pack()
armButton.place(x=5,y=5)

resetImg = PhotoImage(file = 'reset_button.png')
resetButton = Button(win, image=resetImg )
resetButton.pack()
resetButton.place(x=480-110,y=320-110)

exitButton  = Button(win, text = "Exit", font = exitFont, command = exitProgram, height =1 , width = 3) 
exitButton.pack()
exitButton.place(x=5,y=320-40)

statusLabel  = Label(win, text = "Idle", font = statusFont, height =1 , width = 6) 
statusLabel.pack()
statusLabel.place(x=480-180,y=5)

timerLabel  = Label(win, text = "00:00", font = timerFont, height =1 , width = 5) 
timerLabel.pack()
timerLabel.place(x=480-200,y=60)

displayMode('IDLE')
mainloop()
