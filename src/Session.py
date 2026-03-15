from config import *
from Controller import Controller
from Renderer import Renderer

from Core.MasterScript import MasterScript
from Core.Index import Index
from Core.Painter import Painter

class Session:
	def __init__(self, LevelFile):
		print("Building level:")
		self.builder = LevelFile.builder
		self.mainScript = LevelFile.mainScript
		self.canvas = LevelFile.canvas
		
		print("\tPopulating index... ")
		self.index = Index()
		self.builder.build(self.index)
		print("Finished.\n")
		
		self.clicker = False
		
		return
	
	def update(self):
		#F to stop time, L to run one frame
		if Controller.handleKey("FREEZE", DOWN):
			self.clicker = not self.clicker
		if self.clicker and not Controller.handleKey("STEP_FRAME", DOWN):
			return
		
		self.mainScript.run(self, self.index)
		MasterScript.run(self.index, Renderer.dTime)
		
		return
	
	
	def draw(self):
		Painter.paint(self.index, self.canvas)
		return
