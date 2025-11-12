from config import *
from Controller import Controller
from Renderer import Renderer

from Level.proc.lib import proc

from Level.Core.Index import Index
from Level.Core.CollTree import CollTree

from Level.Props.Transf import Transf
from Level.Props.Coll import Coll
from Level.Props.Timer import Timer
from Level.Props.UpdateScripter import UpdateScripter

from Level.Props.Rendering.Rend import Rend
from Level.Props.Rendering.Sprite import Sprite
from Level.Props.Rendering.Segment import Segment

class Level:
	def __init__(self, LDF):
		self.LDF = LDF
		
		self.index = None
		self.canvas = None
		self.collTree = None
		
		self.freeze = False
		self.buildLevel()
		
		return
	
	def buildLevel(self):
		print("Building level:")
		self.index = Index()
		self.canvas = None
		print("\tPopulating index... ")
		self.collTree = CollTree()
		self.LDF.buildLevel(self, self.index)
		print("done.\n\tCalibrating collTree... ", end="")
		self.collTree.calibrate(self.index)
		self.index.setSing("CollTree", self.collTree)#REVISIT: needed for editor... what to do...
		print("done.")
		print("Finished.\n")
		return
	
	def update(self):
		#restart and freeze buttons
		if Controller.handleKey(K_f, DOWN):
			self.freeze = not self.freeze
		
		#do not continue if frozen
		if self.freeze and not Controller.handleKey(K_l, DOWN):
			return
		
		#execute preupdate scripts, and level definition update
		for (script, key) in self.index[UpdateScripter, "Key"]:
			if script.preupdate:
				script.preupdate(self.index.get(key), self.index)
		self.LDF.ldfUpdate(self, self.index)
		
		#integrate timestep
		proc.integrateTimestep(self.index)
		
		#execute interupdate scripts
		for (script, key) in self.index[UpdateScripter, "Key"]:
			if script.interupdate:
				script.interupdate(self.index.get(key), self.index)
		
		#detect collisions, resolve physical collisions, and execute collision scripts
		collisions = self.collTree.detectCollisions(self.index)
		
		#print()
		#execute precollide scripts
		for (keyA, keyB, contactA, contactB, sepvec) in collisions:
			#print(keyA, "      &      ", keyB)
			collA = self.index.get(keyA)[Coll]
			collB = self.index.get(keyB)[Coll]
			if collA.precollide:
				collA.precollide(
					self.index,
					(
						keyA, keyB,
						contactA, contactB,
						sepvec
					)
				)
			if collB.precollide:
				collB.precollide(
					self.index,
					(
						keyB, keyA,
						contactB, contactA,
						sepvec
					)
				)
		
		#resolve physical collisions (parallel)
		proc.resolveCollisions(self.index, collisions)
		#resolve constraints
		proc.resolveConstraints(self.index)
		
		#execute postcollide scripts
		for (keyA, keyB, contactA, contactB, sepvec) in collisions:
			collA = self.index.get(keyA)[Coll]
			collB = self.index.get(keyB)[Coll]
			if collA.postcollide:
				collA.postcollide(
					self.index,
					(
						keyA, keyB,
						contactA, contactB,
						sepvec
					)
				)
			if collB.postcollide:
				collB.postcollide(
					self.index,
					(
						keyB, keyA,
						contactB, contactA,
						sepvec
					)
				)
			
		#REVISIT: consider this being prerender instead of postupdate?
		#execute postupdate scripts
		for (script, key) in self.index[UpdateScripter, "Key"]:
			if script.postupdate:
				script.postupdate(self.index.get(key), self.index)
		
		#remove deleted transfs from the index
		deletedKeys = [self.index.deleteObj(k) for (t, k) in self.index[Transf, "Key"] if t.delete]
		if deletedKeys:
			print("Deleted transfs: ", deletedKeys)
		
		return
	
	def draw(self):
		#draw renderables
		self.postupdate()
		self.canvas.drawFromIndex(self.index)
		self.LDF.ldfDraw(self.index)
		Renderer.drawText(
			"FPS: " + str(Renderer.getAverageFrameRate()),
			"basicText",
			"fancyFont",
			{
				"colour": RED, "alpha": 0.5, "depth": 1,
				"transfMat": glm.scale(glm.translate(glm.mat4(), glm.vec3(0.75, 1, 0)), glm.vec3(1))
			}
		)
		return
	
	def postupdate(self):
		#REVISIT: consider move these to inside canvas?
		for (timer, rend) in self.index.match(Timer, Rend):
			rend.uniformDict["time"] = timer.time
			
		for (rend, transf) in self.index.match(Rend, Transf):
			rend.uniformDict["worldMat"] = transf.calcMatrix()
		
		for (sprice, rend, transf) in self.index[Sprite, Rend, Transf]:
			rend.uniformDict["transfMat"] = glm.scale(
				glm.translate(glm.mat4(), transf.cpos),
				glm.vec3(transf.scale.x, transf.scale.y, 1)
			)
			rend.uniformDict["depth"] = transf.cpos.z
		
		return
