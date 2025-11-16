from config import *

from Core.Props.Transf import Transf
from Core.Props.Timer import Timer
from Core.Props.Scripts import PreScript

from assets.levels.Level1.AsteroidFactory import AsteroidFactory

class SpawnerFactory:
	@classmethod
	def createSpawner(cls, index, key, pos):
		return index.createObj(key, [
			Transf(pos, glm.quat(), glm.vec3()),
			Timer(4, time=random.random()),
			PreScript(cls.spawnerPreScriptClosure(glm.vec2(pos.x, pos.y)))
		])
	@staticmethod
	def spawnerCycle(obj, index):
		transf = obj[Transf]
		AsteroidFactory.create(
			index,
			obj[Transf].cpos,
			transf.cori * glm.vec3(
				(random.random() - 0.5) / 2,
				(8+random.random()*16)/8,
				(random.random() - 0.5)
			)
		)
		return
	@classmethod
	def spawnerPreScriptClosure(cls, offsetXY):
		return lambda o, i: cls.spawnerPreScript(o, i, offsetXY)
	@staticmethod
	def spawnerPreScript(obj, index, offsetXY):
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
					(8+random.random()*16)/8,
					(random.random() - 0.5)
				)
			)
		return
	
	