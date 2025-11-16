from config import *
from Renderer import Renderer
from Controller import Controller

from Session import Session
from assets.levels.Level1.Level1 import Level1

#game state constants
QUIT = 0
MENU = 1
GAME = 2

class Game:
	def __init__(self):
		self.state = MENU
		self.session = None
		#self.menu = self.createMainMenu()
		return

	def setState(self, state):
		stateStr = ["QUIT", "MENU", "GAME"]
		print("Game state: ", stateStr[self.state], " --> ", stateStr[state], ".", sep="")
		self.state = state
		return

	def update(self):
		#check for quitting events
		if Controller.handleClose() or Controller.handleKey(K_DELETE, DOWN):
			self.setState(QUIT)
		
		#do different things depending on game state
		elif self.state == MENU:
			#self.menu.update()
			#return --> start session
			if Controller.handleKey(K_RETURN, DOWN):
				self.session = Session(Level1)
				self.setState(GAME)
				#Controller.startFocus()
			#escape --> return to game if session else quit
			elif Controller.handleKey(K_ESCAPE, DOWN):
				if self.session:
					self.setState(GAME)
					#Controller.startFocus()
				else:
					self.setState(QUIT)
		
		elif self.state == GAME:
			self.session.update()
			#escape --> open menu
			if Controller.handleKey(K_ESCAPE, DOWN):
				self.setState(MENU)
				Controller.endFocus()
		
		return
	
	def draw(self):
		if self.session:
			self.session.draw()
	
		if self.state != GAME:
			Renderer.drawFrameEffect("normalizeColour", {})
			Renderer.drawFrameEffect("fullBlurFrame", {})
			pass#self.menu.draw()
		
		if HORI_BLUR:
			Renderer.drawFrameEffect("horiBlurFrame", {})
		
		return
	