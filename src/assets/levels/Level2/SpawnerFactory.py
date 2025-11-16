from config import *

from Core.Props.Transf import Transf
from Core.Props.Timer import Timer
from Core.Props.Scripts import PreScript

from assets.levels.Level2.AsteroidFactory import AsteroidFactory

class SpawnerFactory:
	@classmethod
	def createSpawner(cls, index, key, pos):
		return index.createObj(key, [
			Transf(pos, glm.quat(), glm.vec3()),
			Timer(8, time=random.random()),
			PreScript(cls.fixSpawnerPosClosure(glm.vec2(pos.x, pos.y)))
		])
	@staticmethod
	def spawnerCycle(obj, index):
		if obj[Timer].click:
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
		if obj[Timer].click:
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
	
	