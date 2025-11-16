from config import *
from Core.Props.Transf import Transf

class MainScript:
	@staticmethod
	def run(level, index):
		#rocket update
		rocket = index.get(index.getSing("rocketkey"))
		rocket[Transf].setRpos(glm.vec3(
			rocket[Transf].cpos.x,
			rocket[Transf].cpos.y,
			min(max(-1, rocket[Transf].cpos.z), 1)
		))
		
		return