from config import *

from Level.Props.Transf import Transf
from Level.Props.Timer import Timer
from Level.Props.UpdateScripter import UpdateScripter

from Level.Levels.Level2.AsteroidFactory import AsteroidFactory

class SpawnerFactory:
	@classmethod
	def createSpawner(cls, index, key, pos):
		return index.createObj(key, [
			Transf(pos, glm.quat(), glm.vec3()),
			Timer(8, time=random.random(), cycleFunc=cls.spawnerCycle),
			UpdateScripter(preupdate=cls.fixSpawnerPosClosure(glm.vec2(pos.x, pos.y)))
		])
	@staticmethod
	def spawnerCycle(obj, index):
		transf = obj[Transf]
		AsteroidFactory.create(
			index,
			obj[Transf].cpos,
			transf.cori * glm.vec3(
				(random.random() - 0.5) / 2,
				-(1+random.random()*2)/2,
				(random.random() - 0.5)
			)
		)
		return
	@classmethod
	def fixSpawnerPosClosure(cls, offsetXY):
		return lambda o, i: cls.fixSpawnerPos(o, i, offsetXY)
	@staticmethod
	def fixSpawnerPos(obj, index, offsetXY):
		obj[Transf].setRpos(glm.vec3(
			index.get(index.getSing("ragdollkeys")["torso"])[Transf].cpos.x + offsetXY.x,
			index.get(index.getSing("ragdollkeys")["torso"])[Transf].cpos.y + offsetXY.y,
			0
		))
		return
	
	