from config import *
from Level.Core.LevelDefinitionFile import LevelDefinitionFile

from Renderer import Renderer
from Controller import Controller

from Level.Props.Transf import Transf
from Level.Props.Rigidbody import Rigidbody

from Level.Levels.Level2.SpawnerFactory import SpawnerFactory

class Level2(LevelDefinitionFile):
	time = 0
	
	@classmethod
	def ldfUpdate(cls, level, index):
		#rocket update
		rocket = index.get(index.getSing("rocketkey"))
		rocket[Transf].setRpos(glm.vec3(
			rocket[Transf].cpos.x,
			rocket[Transf].cpos.y,
			min(max(-1, rocket[Transf].cpos.z), 1)
		))
		
		return
	
	@classmethod
	def ldfDraw(cls, index):
		#player progress
		distance = round(glm.distance(
			index.get(index.getSing("ragdollkeys")["torso"])[Transf].cpos,
			index.get(index.getSing("rocketkey"))[Transf].cpos
		))
		vel = glm.length(Rigidbody.calcVel(
			index.get(index.getSing("ragdollkeys")["torso"])[Rigidbody],
			index.get(index.getSing("ragdollkeys")["torso"])[Transf]
		))
		vel = 0 if glm.isnan(vel) else vel
		speed = str(round(vel))
		Renderer.drawText(
			"\nSPEED: "+speed+"m/s",
			"basicText",
			"fancyFont",
			{
				"colour": WHITE, "alpha": 0.5, "depth": 1,
				"transfMat": glm.scale(
					glm.translate(glm.mat4(), glm.vec3(-1, -0.75, 0)),
					glm.vec3(1, 1, 1)
				)
			}
		)
		
		return
	
	@classmethod
	def buildLevel(cls, level, index):
		for i in range(-4, 5, 1):
			SpawnerFactory.createSpawner(index, "spawner", glm.vec3(i*20, 200, 0))
		return
	