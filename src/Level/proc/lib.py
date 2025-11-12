from Level.proc.collShapeSwitch.collShapeSwitch import collShapeSwitch as collShapeSwitchFunc
from Level.proc.checkCollision import checkCollision as checkCollisionFunc
from Level.proc.integrateTimestep import integrateTimestep as integrateTimestepFunc
from Level.proc.resolveCollisions import resolveCollisions as resolveCollisionsFunc
from Level.proc.resolveConstraints import resolveConstraints as resolveConstraintsFunc

class proc:
	@staticmethod
	def collShapeSwitch(*args):
		return collShapeSwitchFunc(*args)
	@staticmethod
	def checkCollision(*args):
		return checkCollisionFunc(*args)
	@staticmethod
	def integrateTimestep(*args):
		return integrateTimestepFunc(*args)
	@staticmethod
	def resolveCollisions(*args):
		return resolveCollisionsFunc(*args)
	@staticmethod
	def resolveConstraints(*args):
		return resolveConstraintsFunc(*args)
	