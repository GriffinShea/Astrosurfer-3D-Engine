from config import *

class Controller:
	inputDict = {}
	inputDict["CLOSE"] = False
	inputDict["MOUSE_BUTTONS"] = [OFF]*7
	inputDict["MOUSE_POS"] = (0, 0)
	inputDict["MOUSE_MOVE"] = (0, 0)
	inputDict["MOUSE_POS"] = (0, 0)
	focus = False
	firstFrameFocus = False
	
	@classmethod
	def pollInput(cls):
		
		#get mouse position from pygame and translate it
		cls.inputDict["MOUSE_POS"] = pygame.mouse.get_pos()
		cls.inputDict["MOUSE_POS"] = (
			cls.inputDict["MOUSE_POS"][0]*2/WINDOW_DIMS[0] - 1,
			-(cls.inputDict["MOUSE_POS"][1]*2/WINDOW_DIMS[1] - 1)
		)
		
		if cls.focus:
			#...set mouse movement to mouse pos, set pos to center of screen
			if cls.firstFrameFocus:
				cls.inputDict["MOUSE_MOVE"] = (0, 0)
				cls.firstFrameFocus = False
			else:
				cls.inputDict["MOUSE_MOVE"] = cls.inputDict["MOUSE_POS"]
			pygame.mouse.set_pos((WINDOW_DIMS[0]/2, WINDOW_DIMS[1]/2))
		else:
			#...get mouse movement from pygame
			cls.inputDict["MOUSE_MOVE"] = pygame.mouse.get_rel()
			cls.inputDict["MOUSE_MOVE"] = (
				cls.inputDict["MOUSE_MOVE"][0]*2/WINDOW_DIMS[0],
				-cls.inputDict["MOUSE_MOVE"][1]*2/WINDOW_DIMS[1]
			)
		
		#get basic input from pygame
		cls.inputDict["CLOSE"] = False
		cls.inputDict["MOUSE_BUTTONS"] = [
			*list(pygame.mouse.get_pressed()),
			OFF,
			OFF,
			ON * (cls.inputDict["MOUSE_BUTTONS"][M_4] == DOWN
				or cls.inputDict["MOUSE_BUTTONS"][M_4] == ON),
			ON * (cls.inputDict["MOUSE_BUTTONS"][M_5] == DOWN
				or cls.inputDict["MOUSE_BUTTONS"][M_5] == ON)
		]
		cls.inputDict["KEYBOARD"] = list(pygame.key.get_pressed())

		#get input events from pygame
		for event in pygame.event.get():
			if event.type == QUIT:
				cls.inputDict["CLOSE"] = True

			elif event.type == pygame.MOUSEBUTTONUP:
				cls.inputDict["MOUSE_BUTTONS"][event.button-1] = UP
			elif event.type == pygame.MOUSEBUTTONDOWN:
				cls.inputDict["MOUSE_BUTTONS"][event.button-1] = DOWN

			elif event.type == pygame.KEYDOWN:
				cls.inputDict["KEYBOARD"][event.key] = DOWN
			elif event.type == pygame.KEYUP:
				cls.inputDict["KEYBOARD"][event.key] = UP
			
		return
	
	@classmethod
	def startFocus(cls):
		pygame.mouse.set_visible(False)
		pygame.event.set_grab(True)
		cls.focus = True
		cls.firstFrameFocus = True
		return
	
	@classmethod
	def endFocus(cls):
		pygame.mouse.set_visible(True)
		pygame.event.set_grab(False)
		cls.focus = False
		return
	
	@classmethod
	def getMouseMove(cls):
		return cls.inputDict["MOUSE_MOVE"]
	
	@classmethod
	def getMouseMoveX(cls):
		return cls.inputDict["MOUSE_MOVE"][0]
	
	@classmethod
	def getMouseMoveY(cls):
		return cls.inputDict["MOUSE_MOVE"][1]
	
	@classmethod
	def getMousePos(cls):
		return cls.inputDict["MOUSE_POS"]

	@classmethod
	def handleClose(cls):
		if cls.inputDict["CLOSE"]:
			cls.inputDict["CLOSE"] = False
			return True
		else:
			return False

	@classmethod
	def checkKey(cls, key):
		return cls.inputDict["KEYBOARD"][key]

	@classmethod
	def handleKey(cls, key, state):
		if state == ON or state == OFF:
			raise ValueError("handleKeyEvent() may only take DOWN or UP for state.")
		
		if cls.inputDict["KEYBOARD"][key] == state:
			if state == DOWN:
				cls.inputDict["KEYBOARD"][key] = ON
			else:
				cls.inputDict["KEYBOARD"][key] = OFF
			return True
		else:
			return False

	@classmethod
	def checkMouse(cls, button):
		return cls.inputDict["MOUSE_BUTTONS"][button]

	@classmethod
	def handleMouse(cls, button, state):
		if state == ON or state == OFF:
			raise ValueError("handleMouseEvent() may only take DOWN or UP for state.")
		
		if cls.inputDict["MOUSE_BUTTONS"][button] == state:
			if state == DOWN:
				cls.inputDict["MOUSE_BUTTONS"][button] = ON
			else:
				cls.inputDict["MOUSE_BUTTONS"][button] = OFF
			return True
		else:
			return False
