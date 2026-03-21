from config import *

from Renderer import Renderer
from Controller import Controller
from Core.Props.Transf import Transf

from assets.levels.Level2.Level2 import Level2

class MainScript:
	@classmethod
	def run(cls, level, index):
		#when rocket has attached count three seconds until level swap
		if index.getSing("handsOnRocket") == 2:
			index.setSing("swapTimer", index.getSing("swapTimer") + Renderer.dTime)
			if index.getSing("swapTimer") > 3:
				cls.swapLevel(level, index)
		
		#ragdoll controls/update
		if index.getSing("handsOnRocket") < 2:
			ragdollTorso = index.get(index.getSing("ragdollkeys")["torso"])
			index.setSing("sinceLastColl", index.getSing("sinceLastColl") + Renderer.dTime)
			ragdollTorso[Transf].setRpos(glm.vec3(
				ragdollTorso[Transf].cpos.x
				+ Renderer.dTime * ((Controller.checkKey("DIR_E")>0)-(Controller.checkKey("DIR_W")>0)),
				ragdollTorso[Transf].cpos.y,
				min(max(-1, ragdollTorso[Transf].cpos.z), 1)
			))
		
		#rocket update
		rocket = index.get(index.getSing("rocketkey"))
		rocket[Transf].setRpos(glm.vec3(
			rocket[Transf].cpos.x,
			rocket[Transf].cpos.y,
			min(max(-1, rocket[Transf].cpos.z), 1)
		))
		
		return
	
	@classmethod
	def swapLevel(cls, level, index):
		objsToDelete = index.findObjs("spawner") + index.findObjs("arrow")
		for obj in objsToDelete:
			print("Level swap! Deleting: ", obj, obj.key)
			index.deleteObj(obj.key)
		
		level.builder = Level2.builder
		level.builder.build(index)
		level.mainScript = Level2.mainScript
		
		return
	