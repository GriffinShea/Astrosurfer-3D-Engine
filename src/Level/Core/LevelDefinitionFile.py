from config import *

class LevelDefinitionFile:
	@staticmethod
	def ldfUpdate(index):
		if not DEBUG_SUPPRESS_WARNINGS:
			print("WARNING: abstract method ldfUpdate() of LDF subclass not defined.")
		return
	
	@staticmethod
	def ldfDraw(index):
		if not DEBUG_SUPPRESS_WARNINGS:
			print("WARNING: abstract method ldfDraw() of LDF subclass not defined.")
		return
		
	@staticmethod
	def buildLevel(level):
		if not DEBUG_SUPPRESS_WARNINGS:
			print("WARNING: abstract method buildLevel() of LDF subclass not defined.")
		return