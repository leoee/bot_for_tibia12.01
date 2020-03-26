from tkinter import *
import logging
from pynput.mouse import Listener as MouseListener
from pynput import mouse
from tkinter import ttk
import tkinter as tk
import threading
import pyscreenshot as ImageGrab
from PIL import Image
import pyautogui
import time
import sys
import os
import json

configIndex = 0
P1 = 0
P2 = 0
firstTime = False
shouldListener = False

def returnListPointsBar():
	file = open("config_screen.txt", "r")
	contents = file.read()
	list = []
	indexPrevious = 0
	indexNext = 0
	for i in range (16):
		value = ""
		indexPrevious = contents.index('"', indexNext + 1)
		indexNext = contents.index('"', indexPrevious + 1)
		for x in range(indexPrevious + 1, indexNext):
			value += contents[x]
		list.append(value)
	return list

def checkConfigScreen():
	im=pyautogui.screenshot()
	im = im.crop((int(P1[0]), int(P1[1]), int(P2[0]), int(P2[1])))
	im.show()
	popupmsg('Please, confirm if the following points are valids\n P1' + str(P1) + ', P2' + str(P2))

def on_move(x, y):
	global firstTime
	if (firstTime == False):
		return False

def on_click(x, y, button, pressed):
	global shouldListener
	if pressed:
		if (button == mouse.Button.right and shouldListener):
			shouldListener = False
			checkConfigScreen()
			return False
		else:
			global configIndex, P1, P2
			#file = open('config_screen.txt', 'a')
			if (configIndex == 0):
				#file.write('x:"' + str(x) + '" - y:"' + str(y) + '"\n')
				P1 = [x, y]
				configIndex = 1
			elif (configIndex == 1):
				#file.write('mx:"' + str(x) + '" - my:"' + str(y) + '"\n')
				P2 = [x, y]
				configIndex = 0
			#file.close()

with MouseListener(on_move=on_move, on_click=on_click) as listener:
	listener.join()

class Concur(threading.Thread):
	def __init__(self):
		super(Concur, self).__init__()
		self.iterations = 0
		self.master = None
		self.daemon = True  # Allow main to exit even if still running.
		self.paused = True  # Start out paused.
		self.state = threading.Condition()

	def setMaster(self, master):
		self.master = master

	def run(self):
		self.resume()
		while True:
			with self.state:
				if self.paused:
					self.state.wait()  # Block execution until notified.
			controller(self)
			time.sleep(.1)
			self.iterations += 1

	def resume(self):
		with self.state:
			self.paused = False
			self.state.notify()  # Unblock self if waiting.

	def pause(self):
		with self.state:
			self.paused = True  # Block self.


def changeGeneratorToList(vector_life, vector_mana):
	for i in range(0, 10):
		vector_life[i] = list(vector_life[i])
		vector_mana[i] = list(vector_mana[i])

def configHeal(master, currentLife, currentMana):
	valueTotalMana = concur.master["totalMana"].get()
	valueTotalLife = concur.master["totalLife"].get()
	keyLife90 = concur.master["keyPressCure90"].get().lower()
	keyLife70 = concur.master["keyPressCure70"].get().lower()
	keyLife50 = concur.master["keyPressCure50"].get().lower()
	manaPercentForHeal = concur.master["manaPercent"].get()
	keyPressMana = concur.master["keyPressCureMana"].get().lower()
	
	if (valueTotalLife.isdigit() == False or valueTotalMana.isdigit() == False):
		return

	currentLifePercent = (float(currentLife/int(valueTotalLife)) * 100)
	currentManaPercent = (float(currentMana/int(valueTotalMana)) * 100)
		
	if (currentLifePercent <= 50 and keyLife50 != " "):
		pyautogui.press(keyLife50)
	elif (currentLifePercent <= 70 and keyLife70 != " "):
		pyautogui.press(keyLife70)
	elif (currentLifePercent <= 90 and keyLife90 != " "):
		pyautogui.press(keyLife90)
	
	if (manaPercentForHeal.isdigit() == False):
		return

	if (currentManaPercent <= int(manaPercentForHeal) and keyPressMana != " "):
		pyautogui.press(keyPressMana)

def confirmIsTarget(image):
	left = pyautogui.locate('C:/Users/Leo/Desktop/heal_bot/images/left.png', image, grayscale=True, confidence=.75)
	right = pyautogui.locate('C:/Users/Leo/Desktop/heal_bot/images/right.png', image, grayscale=True, confidence=.75)
	top = pyautogui.locate('C:/Users/Leo/Desktop/heal_bot/images/top.png', image, grayscale=True, confidence=.75)
	bottom = pyautogui.locate('C:/Users/Leo/Desktop/heal_bot/images/bottom.png', image, grayscale=True, confidence=.75)
	
	if (left != None and right != None and top != None and bottom != None):
		return True

	return False

def identifyNumbers(imgLife, imgMana, vector_life, vector_mana):
	for x in range(0, 10):
		vector_life[x] =  pyautogui.locateAll('C:/Users/Leo/Desktop/heal_bot/images/' + str(x) + '.png', imgLife, grayscale=True, confidence=.95)
		vector_mana[x] =  pyautogui.locateAll('C:/Users/Leo/Desktop/heal_bot/images/' + str(x) + '.png', imgMana, grayscale=True, confidence=.95)

def convertNumbersToString(validIndex, vector, currentValue):
	while(validIndex):
		max = 2000
		indexRemoved = 0
		insideIndexRemove = 0
		for value in vector:
			if (vector[value] != None):
				for valueIntoItem in vector[value]:
					if (max > valueIntoItem[0]):
						indexRemoved = value
						insideIndexRemove = valueIntoItem
						max = valueIntoItem[0]
		if (insideIndexRemove != 0):
			vector[indexRemoved].remove(insideIndexRemove)
		currentValue += str(indexRemoved)
		validIndex -= 1
	return currentValue

def controller(concur):
	time.sleep(1)
	while (True):
		if (concur.paused == True):
			break
		time.sleep(0.2)
		im=pyautogui.screenshot()
		life = im
		mana = im
		food = im
		isTarget = im
		list = returnListPointsBar()
		#life = life.crop((1200, 135, 1350, 155))
		life = life.crop((int(list[0]), int(list[1]), int(list[2]), int(list[3])))
		mana = mana.crop((int(list[4]), int(list[5]), int(list[6]), int(list[7])))
		food = food.crop((int(list[8]), int(list[9]), int(list[10]), int(list[11])))
		isTarget = isTarget.crop((int(list[12]), int(list[13]), int(list[14]), int(list[15])))
		#mana = mana.crop((1200, 152, 1350, 174))
		#food = food.crop((1190, 310, 1310, 330))
		#isTarget = isTarget.crop((1170, 405, 1300, 482))
		
		screenBot = pyautogui.locate('C:/Users/Leo/Desktop/heal_bot/images/bot.png', im, grayscale=True, confidence=.75)
		
		if (screenBot != None):
			print('Skipping')
			continue
		
		vector_life = {}
		vector_mana = {}
		
		hasHungry = pyautogui.locate('C:/Users/Leo/Desktop/heal_bot/images/food.png', food, grayscale=True, confidence=.75)
		hasSpeed = pyautogui.locate('C:/Users/Leo/Desktop/heal_bot/images/speed.png', food, grayscale=True, confidence=.75)
		
		identifyNumbers(life, mana, vector_life, vector_mana)
		
		validIndexLife = 0
		validIndexMana = 0
		lifeValue = ""
		manaValue = ""
				
		changeGeneratorToList(vector_life, vector_mana)
		
		for i in range(0, 10):
			validIndexLife += (sum(x is not None for x in vector_life[i]))
			validIndexMana += (sum(x is not None for x in vector_mana[i]))
			
		if (validIndexLife == validIndexMana and validIndexMana == 0):
			continue;
		
		mustEatFood = concur.master["eatFood"].get()
		keyPressEatFood = concur.master["keyPressFood"].get().lower()
		mustUseHur = concur.master["autoRun"].get()
		spellHur = concur.master["spellHur"].get().lower()
		mustAtk = concur.master["autoSpellInTarget"].get()
		spellAtk = concur.master["keyAutoAtk"].get().lower()
				
		lifeValue = convertNumbersToString(validIndexLife, vector_life, lifeValue)
		manaValue = convertNumbersToString(validIndexMana, vector_mana, manaValue)
		
		print(lifeValue + ' ---- ' + manaValue)
		#print(e1)
			
		if (hasHungry != None and mustEatFood):
			pyautogui.press(keyPressEatFood)
		if (hasSpeed == None and mustUseHur and spellHur != " "):
			pyautogui.press(spellHur)
		if (mustAtk and spellAtk != " " and confirmIsTarget(isTarget)):
			pyautogui.press(spellAtk)
			
		configHeal(master, int(lifeValue), int(manaValue))

def increaseConfig(popup):
	configIndex += 1
	print(configIndex)

def popupmsg(msg):
	popup = tk.Tk()
	popup.wm_title("Warning")
	label = ttk.Label(popup, text=msg, font=("Verdana", 8))
	label.pack(side="top", fill="x", pady=10)
	B2 = ttk.Button(popup, text="Ok", command = popup.destroy)
	B2.pack()
	popup.mainloop()

def stopBot(concur, master):
	master.title('TibiaBot - Stopped')
	concur.pause()

def loadConfig(a, b):
	print(a.get())
	print(b.get())
	
def startBot(concur, master):
	valueTotalMana = concur.master["totalMana"].get()
	valueTotalLife = concur.master["totalLife"].get()
	
	if (valueTotalLife.isdigit() == False or valueTotalMana.isdigit() == False):
		popupmsg('Configure Total Life and Total Mana')
	else:
		concur.resume()
		master.title('TibiaBot - Running')

def configScreen(openConfigScreen):
	global shouldListener
	shouldListener = True
	listener.run()
		
if __name__ == '__main__':
	firstTime = True
	master = tk.Tk()
	master.geometry("510x150")
	master.resizable(False, False)
	master.title('TibiaBot - Stopped')
		
	fKeys = ('F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 
				'F9', 'F10', 'F11', 'F12', 'HOME', 'INSERT', 'DEL', 'NONE')
			
	tk.Label(master, 
			 text="Total Life").grid(row = 0)
	tk.Label(master, 
			 text="Total Mana").grid(row = 1)
	tk.Label(master, 
			 text="Spell").grid(row = 0, column = 4)

	totalLife = tk.Entry(master, width=7)
	totalMana = tk.Entry(master, width=7)
	
	totalLife.grid(row=0, column=1)
	totalMana.grid(row=1, column=1)

	keyPressHur = StringVar()
	keyPressRun = ttk.Combobox(master, width = 6, textvariable = keyPressHur)

	keyPressRun['values'] = fKeys
	  
	keyPressRun.grid(row = 0, column = 4) 
	keyPressRun.current()	

	eatFood = IntVar()
	Checkbutton(master, text="Eat Food", variable=eatFood).grid(row=1, column = 3, sticky=W)
	
	autoRun = IntVar()
	Checkbutton(master, text="Auto Run", variable=autoRun).grid(row=0, column = 3, sticky=W)
	
	autoTarget = IntVar()
	Checkbutton(master, text="Auto Target", variable=autoTarget).grid(row=0, column = 5, sticky=W)
	
	changeGold = IntVar()
	Checkbutton(master, text="Change Gold", variable=changeGold).grid(row=1, column = 5, sticky=W)
	
	keyAtk = StringVar()
	keyAutoAtk = ttk.Combobox(master, width = 4, textvariable = keyAtk)
	
	keyAutoAtk['values'] = fKeys 
	  
	keyAutoAtk.grid(row = 0, column = 5, sticky=W, padx = 95) 
	keyAutoAtk.current() 

	keyPressFood = StringVar()
	keyChoosen = ttk.Combobox(master, width = 4, textvariable = keyPressFood)
	
	keyChoosen['values'] = fKeys 
	  
	keyChoosen.grid(row = 1, column = 4, sticky=W) 
	keyChoosen.current(11) 	
					 
	tk.Label(master, 
			text="Life 90%").grid(row = 3)
			
	keyPressCure90 = StringVar()
	keyChoosenCure90 = ttk.Combobox(master, width = 6, textvariable = keyPressCure90)
	
	keyChoosenCure90['values'] = fKeys
	  
	keyChoosenCure90.grid(row = 3, column = 1, sticky=W) 
	keyChoosenCure90.current()
	
	tk.Label(master, 
			text="Life 70%").grid(row = 3, column = 3)
			
	keyPressCure70 = StringVar()
	keyChoosenCure70 = ttk.Combobox(master, width = 6, textvariable = keyPressCure70) 

	keyChoosenCure70['values'] = fKeys
	  
	keyChoosenCure70.grid(row = 3, column = 4, sticky=W) 
	keyChoosenCure70.current()

	tk.Label(master, 
			text="Life 50%").grid(row = 3, column = 5, sticky=W)
			
	keyPressCure50 = StringVar()
	keyChoosenCure50 = ttk.Combobox(master, width = 6, textvariable = keyPressCure50) 

	keyChoosenCure50['values'] =  fKeys
	  
	keyChoosenCure50.grid(row = 3, column = 5, sticky=W, padx = 60) 
	keyChoosenCure50.current()
	
	tk.Label(master, 
		text="When Mana <=").grid(row = 4, column = 0)
	
	manaPercent = tk.Entry(master, width=6)	
	manaPercent.grid(row=4, column=1)
	
	tk.Label(master, 
		text="% use").grid(row = 4, column = 2)	
	keyPressCureMana = StringVar()
	keyPressCureMana = ttk.Combobox(master, width = 6, textvariable = keyPressCureMana) 
	  
	# Adding combobox drop down list 
	keyPressCureMana['values'] =  fKeys
	  
	keyPressCureMana.grid(row = 4, column = 3) 
	keyPressCureMana.current()
			
	itemsFromScreen = {
		"keyPressCure90": keyChoosenCure90,
		"keyPressCure70": keyChoosenCure70,
		"keyPressCure50": keyChoosenCure50,
		"manaPercent": manaPercent,
		"keyPressCureMana": keyPressCureMana,
		"eatFood": eatFood,
		"keyPressFood": keyPressFood,
		"totalLife": totalLife,
		"totalMana": totalMana,
		"autoRun": autoRun,
		"spellHur": keyPressRun,
		"autoSpellInTarget": autoTarget,
		"keyAutoAtk": keyAutoAtk,
		"changeGold": changeGold
	}
	
	concur = Concur()
	concur.setMaster(itemsFromScreen)
	concur.start()
	concur.pause()

	openConfigScreen = tk.Button(master, 
			  text='Config Screen', 
			  bg='red',
			  activebackground='green',
			  command=lambda: configScreen(openConfigScreen)).grid(row=4, 
										column=5, 
										sticky=W, 
										pady=4)
	tk.Button(master, 
			  text='Check Config', 
			  command = lambda: checkConfigScreen()).grid(row=4, 
										column=4, 
										sticky=E, 
										pady=4,
										padx=4)

	tk.Button(master, 
			  text='Stop', command = lambda: stopBot(concur, master)).grid(row=5, 
														   column=4, 
														   sticky=tk.W, 
														   pady=4)

	tk.Button(master, 
			  text='Start', command = lambda: startBot(concur, master)).grid(row=5, 
														   column=3, 
														   sticky=tk.W, 
														   pady=4)

	tk.mainloop()
	