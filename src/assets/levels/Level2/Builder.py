from config import *
from assets.levels.Level2.SpawnerFactory import SpawnerFactory

class Builder:
	@classmethod
	def build(cls, index):
		print(index.getSing("ragdollkeys"))
		for i in range(-4, 5, 1):
			SpawnerFactory.createSpawner(index, "spawner", glm.vec3(i*20, 200, 0))
		return