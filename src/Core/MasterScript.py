
from Core.Props.Timer import Timer
from Core.Props.Transf import Transf
from Core.Props.Coll import Coll
from Core.Props.Scripts import PreScript, InterScript, PostScript, DeleteScript

from Core.Systems.Physics.Integrator import Integrator
from Core.Systems.Collisions.Detector import Detector
from Core.Systems.Physics.Solver import Solver

class MasterScript:
	@classmethod
	def run(cls, index, dTime):
		#increment timers
		cls.updateTimers(index, dTime)
		
		#execute prescripts
		cls.runScripts(PreScript, index)
		
		#integrate timestep
		Integrator.run(index, dTime)
		
		#execute interscripts
		cls.runScripts(InterScript, index)
		
		#detect collisions, resolve physical collisions, and execute collision scripts
		collisions = Detector.detect(index)
		
		#execute precollide scripts
		for (keyA, keyB, contactA, contactB, sepvec) in collisions:
			collA = index.get(keyA)[Coll]
			collB = index.get(keyB)[Coll]
			if collA.precollide:
				collA.precollide(
					index,
					(
						keyA, keyB,
						contactA, contactB,
						sepvec
					)
				)
			if collB.precollide:
				collB.precollide(
					index,
					(
						keyB, keyA,
						contactB, contactA,
						sepvec
					)
				)
		
		Solver.run(index, collisions)
		
		#execute postcollide scripts
		for (keyA, keyB, contactA, contactB, sepvec) in collisions:
			collA = index.get(keyA)[Coll]
			collB = index.get(keyB)[Coll]
			if collA.postcollide:
				collA.postcollide(
					index,
					(
						keyA, keyB,
						contactA, contactB,
						sepvec
					)
				)
			if collB.postcollide:
				collB.postcollide(
					index,
					(
						keyB, keyA,
						contactB, contactA,
						sepvec
					)
				)
			
		#execute postscripts
		cls.runScripts(PostScript, index)
		
		#run delete scripts and remove deleted transfs from the index
		#cls.runScripts(DeleteScript, index)
		deletedKeys = [index.deleteObj(k) for (t, k) in index[Transf, "Key"] if t.delete]
		if deletedKeys:
			print("Deleted transfs: ", deletedKeys)
		
		return
	
	def updateTimers(index, dTime):
		#update timer (not parallel due to cycleFunc)
		for (timer, transf, key) in index[Timer, Transf, "Key"]:
			timer.click = False
			timer.time += dTime / timer.cycle
			if timer.time > 1:
				timer.click = True
				if timer.deleteOnCycle:
					transf.delete = True
				else:
					timer.time -= 1
		return
	
	@staticmethod
	def runScripts(ScriptType, index):
		for (script, key) in index[ScriptType, "Key"]:
			script.run(index.get(key), index)
		return