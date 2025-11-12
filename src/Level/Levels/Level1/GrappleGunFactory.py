from config import *

from Controller import Controller
from Renderer import Renderer

from Level.Core.Canvas import Canvas

from Level.Props.UpdateScripter import UpdateScripter
from Level.Props.Timer import Timer
from Level.Props.Transf import Transf
from Level.Props.Coll import Coll
from Level.Props.Rigidbody import Rigidbody
from Level.Props.Attractor import Attractor
from Level.Props.OriSteer import OriSteer
from Level.Props.PhysJoint import PhysJoint
from Level.Props.Jet import Jet

from Level.Props.Rendering.Rend import Rend
from Level.Props.Rendering.Sprite import Sprite
from Level.Props.Rendering.Model import Model
from Level.Props.Rendering.Segment import Segment
from Level.Props.Rendering.Camera import Camera

from Level.proc.rb import rb

from Level.Levels.Level1.ChainFactory import ChainFactory

class GrappleGunFactory:
	CHAINLENGTH = 50
	CHAINLINKS = 10

	@classmethod
	def create(cls, index):
		ragdollkeys = index.getSing("ragdollkeys")
		
		grapplekeys = {}
		
		cls.addCursorAndTarget(index, grapplekeys)
		cls.addGunLineAndHook(index, grapplekeys, ragdollkeys)
		cls.setupControls(index, grapplekeys, ragdollkeys)
		
		return grapplekeys
	
	@classmethod
	def addCursorAndTarget(cls, index, grapplekeys):
		grapplekeys["cursor"] = index.createObj(
			"cursor",
			[
				Transf(glm.vec3(), glm.quat(), glm.vec3(0.025, 0.025 * FRAME_RATIO, 1)),
				UpdateScripter(postupdate=cls.fixCursorPos),
				Rend(True, "basicSprite", {"sprite": "reticle", "alpha": 0.5}),
				Sprite(),
			]
		)
		grapplekeys["target"] = index.createObj(
			"target",
			[
				Transf(glm.vec3(), glm.quat(), glm.vec3(1)),
				UpdateScripter(postupdate=cls.fixTargetPos),
				Rend(True, "solidUnlitColour", {"colour": YELLOW}),
				Model("sphere", False),
			]
		)
		return
	@classmethod
	def fixCursorPos(cls, obj, index):
		mousePosRaw = Controller.getMousePos()
		obj[Transf].setRpos(glm.vec3(
			mousePosRaw[0],
			mousePosRaw[1],
			0
		))
		return
	@classmethod
	def fixTargetPos(cls, obj, index):
		cameraObj = index.get(index.getSing("camerakey"))
		mousePosRaw = Controller.getMousePos()#([-1,1], [-1,1])
		#REVISIT: Canvas should not be called here, must move these functions to glmh or proc
		mouseNearPos = glm.vec4(mousePosRaw[0], mousePosRaw[1], 0, 1) * glm.inverse(
			Canvas.calcViewMat(cameraObj[Transf].cpos, cameraObj[Transf].cori)
			* Canvas.calcPerspectiveMat(cameraObj[Camera].fov)
		)
		mouseOriginIntersect = mouseNearPos * -cameraObj[Transf].cpos.z
		n = glm.normalize(glm.vec2(mouseOriginIntersect.x, mouseOriginIntersect.y))
		
		torsoPos = cameraObj[Transf].cpos
		obj[Transf].setRpos(glm.vec3(
			torsoPos.x + n.x * 10,
			torsoPos.y + n.y * 10,
			0
		))
		return
	
	@classmethod
	def addGunLineAndHook(cls, index, grapplekeys, ragdollkeys):
		#create grapple gun
		grapplekeys["gun"] = index.createObj(
			"gun",
			[
				Transf(
					glm.vec3(0, -0.25, 0), glm.quat(), glm.vec3(1),
					parent=index.get(ragdollkeys["leftarmbot"])[Transf]
				),
				Rend(True, "solidUnlitColour", {"colour": PINK}),
				Model("pyr", True),
			]
		)
		
		#create grapple hook
		gunTransf = index.get(grapplekeys["gun"])[Transf]
		hookPos = gunTransf.cpos + gunTransf.cori * glm.vec3(0, -3, 0)
		grapplekeys["hook"] = index.createObj(
			"hook",
			[
				Transf(
					hookPos,
					glm.angleAxis(glm.pi(), glmh.zUnit()),
					gunTransf.scale * glm.vec3(0.25, 2, 0.25)
				),
				Coll(
					COLLCAPSULE, COLLGHOST,
					ignoreKeys=set([grapplekeys["gun"]]).union(ragdollkeys)
				),
				Rigidbody(100, 0, 0, 0, suffersGravity=False),
				UpdateScripter(preupdate=cls.hookUpdate),
				
				Rend(True, "solidUnlitColour", {"colour": YELLOW}),
				Model("cylinder", True),
			]
		)
		
		#create grapple line and attach one end to the hook
		grapplekeys["rope"] = ChainFactory.create(
			"rope", index,
			glm.vec3(20, 0, 0), cls.CHAINLENGTH, 0.2, cls.CHAINLINKS,
			ignoreKeys=set([ragdollkeys["leftarmbot"], grapplekeys["hook"]])
		)
		grapplekeys["rope_hook_joint"] = index.createObj(
			"rope_hook_joint",
			[PhysJoint(
				grapplekeys["hook"], grapplekeys["rope"][0][-1],
				glm.vec3(0, 0, 0), glm.vec3(0, 1.5, 0),
				glm.quat()
			)]
		)
		
		
		#this will be moved along the line to pull the player towards the hook
		grapplekeys["pulljoint"] = index.createObj(
			"pulljoint",
			[PhysJoint(
				ragdollkeys["leftarmbot"], grapplekeys["rope"][0][0],
				glm.vec3(0, 3, 0), glm.vec3(0, -2.5, 0),
				glm.quat()
			)]
		)
		#keeps hook in front of player when loaded
		grapplekeys["arm_hook_joint"] = index.createObj(
			"rope_hook_joint",
			[PhysJoint(
				ragdollkeys["torso"], grapplekeys["hook"],
				index.get(ragdollkeys["torso"])[Transf].cpos - hookPos, glm.vec3(0, 0, 0),
				glm.quat(), distance=600
			)]
		)
		cls.reloadHook(index, grapplekeys)
		
		return
	@classmethod
	def hookUpdate(cls, obj, index):
		transf = obj[Transf]
		transf.setRpos(glm.vec3(
			transf.cpos.x,
			transf.cpos.y,
			min(max(-3, transf.cpos.z), 3)
		))
		if PhysJoint in obj:
			if not obj[PhysJoint].key2 in index:
				cls.removeHook(index, obj)
		return
	
	@classmethod
	def setupControls(cls, index, grapplekeys, ragdollkeys):
		#add steers to left arm, head, torso to implement pointing to the target
		index.addProp(ragdollkeys["leftarmbot"], OriSteer(
			grapplekeys["target"], 0, True, 
			relOri=glm.angleAxis(glm.pi()/2, glmh.xUnit())
		))
		index.addProp(ragdollkeys["leftarmtop"], OriSteer(
			grapplekeys["target"], 0, True, 
			relOri=glm.angleAxis(glm.pi()/2, glmh.xUnit())
		))
		index.addProp(ragdollkeys["head"], OriSteer(
			grapplekeys["target"], 0, True
		))
		index.addProp(ragdollkeys["torso"], OriSteer(
			grapplekeys["target"], 0, True
		))
		
		#add an updater to implement grapple controls
		index.addProp(
			ragdollkeys["leftarmbot"],
			UpdateScripter(preupdate=cls.grappleControlsClosure(grapplekeys, ragdollkeys))
		)
		
		return
	@classmethod
	def grappleControlsClosure(cls, grapplekeys, ragdollkeys):
		return lambda o, i: cls.grappleControls(o, i, grapplekeys, ragdollkeys)
	@classmethod
	def grappleControls(cls, obj, index, grapplekeys, ragdollkeys):
		target = index.get(grapplekeys["target"])
		gun = index.get(grapplekeys["gun"])
		hook = index.get(grapplekeys["hook"])
		hand = index.get(ragdollkeys["leftarmbot"])
		torso = index.get(ragdollkeys["torso"])
		gunHookJoint = index.get(grapplekeys["arm_hook_joint"])[PhysJoint]
		
		#when hook is loaded
		if gunHookJoint.distance == 0:
			
			#when right mouse is held down, player points to target
			if Controller.checkMouse(M_RIGHT):
				index.get(ragdollkeys["leftarmbot"])[OriSteer].turnSpeed = 25
				index.get(ragdollkeys["leftarmtop"])[OriSteer].turnSpeed = 100
				index.get(ragdollkeys["head"])[OriSteer].turnSpeed = 5
				index.get(ragdollkeys["torso"])[OriSteer].turnSpeed = 2.5
			
			#when left mouse and right mouse:
			if Controller.checkMouse(M_RIGHT) and Controller.checkMouse(M_LEFT):
				#fire the hook by applying an impulse and releasing the joint
				gunHookJoint.distance = cls.CHAINLENGTH
				rb.applyImpulse(
					hook[Rigidbody],
					hook[Transf],
					5000 * glm.normalize(target[Transf].cpos - gun[Transf].cpos),
					hook[Transf].cpos - gun[Transf].cpos + hook[Transf].cpos
				)
				hook[Coll].postcollide = cls.attachHook
				index.setSing("rightMouseReleased", False)
			
			#when right mouse is released or hook is fired, player stops pointing, back to ragdoll
			if Controller.handleMouse(M_RIGHT, UP) or gunHookJoint.distance != 0:
				index.get(ragdollkeys["leftarmbot"])[OriSteer].turnSpeed = 0
				index.get(ragdollkeys["leftarmtop"])[OriSteer].turnSpeed = 0
				index.get(ragdollkeys["head"])[OriSteer].turnSpeed = 0
				index.get(ragdollkeys["torso"])[OriSteer].turnSpeed = 0
		
		#when hook has been released
		else:
			#wait for right mouse release
			if Controller.handleMouse(M_RIGHT, UP):
				index.setSing("rightMouseReleased", True)
				index.setSing("ta", 0)
			
			#after releasing right mouse, right mouse will reel in the line
			elif index.getSing("rightMouseReleased") and Controller.checkMouse(M_RIGHT):
				#move the pull joint along the line towards the hook
				pullJoint = index.get(grapplekeys["pulljoint"])
				index.setSing("ta", index.getSing("ta") + Renderer.dTime)
				ta = index.getSing("ta")
				if ta > 1:
					ta = 1
					#cls.reloadHook(index, grapplekeys)
				else:
					pullJoint[PhysJoint].key2 = grapplekeys["rope"][0][int(glm.floor(ta * cls.CHAINLINKS))]
					pullJoint[PhysJoint].offset2 = glm.vec3(
						0,
						(((ta * cls.CHAINLINKS) % 1) * 2 - 1) * (cls.CHAINLENGTH / cls.CHAINLINKS / 2),
						0
					)
					
					"""print()
					print(ta)
					print(int(glm.floor(ta * cls.CHAINLINKS)))
					print((ta * cls.CHAINLINKS) % 1)
					print((cls.CHAINLENGTH / cls.CHAINLINKS) / 2)#1
					print(grapplekeys["rope"][0][int(glm.floor(ta * cls.CHAINLINKS))])
					print(glm.vec3(
						0,
						(((ta * cls.CHAINLINKS) % 1) * 2 - 1) * (cls.CHAINLENGTH / cls.CHAINLINKS / 2),
						0
					))"""
		
		return
	@classmethod
	def attachHook(cls, index, collision):
		(hookkey, otherkey, contactA, contactB, sepvec) = collision
		if "grappleable" in index.get(otherkey)[Coll].tags:
			#anchor torso to grappleable
			#index.addProp(
			#	index.getSing("ragdollkeys")["torso"],
			#	PhysJoint(
			#		index.getSing("ragdollkeys")["torso"], otherkey,
			#		glm.vec3(),
			#		(contactA - index.get(otherkey)[Transf].cpos) * index.get(otherkey)[Transf].cori,
			#		glm.quat(), distance=cls.CHAINLENGTH
			#	)
			#)
			#index.addProp(
			#	index.getSing("ragdollkeys")["torso"],
			#	Attractor(otherkey, 0, 0)
			#)
			
			#attach hook to grappleable
			index.addProp(
				hookkey,
				PhysJoint(
					hookkey, otherkey,
					glm.vec3(),
					(contactA - index.get(otherkey)[Transf].cpos) * index.get(otherkey)[Transf].cori,
					glm.quat()
				)
			)
			index.get(hookkey)[Coll].postcollide = None
			index.get(hookkey)[Coll].ignoreKeys.add(otherkey)
		return
	
	@classmethod
	def removeHook(cls, index, hook):
		index.get(hook.key)[Coll].ignoreKeys.remove(hook[PhysJoint].key2)
		index.deleteProp(hook.key, PhysJoint)
		#index.deleteProp(index.getSing("ragdollkeys")["torso"], PhysJoint)
		#index.deleteProp(index.getSing("ragdollkeys")["torso"], Attractor)
		return
	
	@classmethod
	def reloadHook(cls, index, grapplekeys):
		hook = index.get(grapplekeys["hook"])
		gunHookJoint = index.get(grapplekeys["arm_hook_joint"])[PhysJoint]
		
		gunHookJoint.distance = 0
		hook[Coll].postcollide = None
		if PhysJoint in hook:
			cls.removeHook(index, hook)
		
		index.get(grapplekeys["pulljoint"])[PhysJoint].key2 = grapplekeys["rope"][0][0]
		index.get(grapplekeys["pulljoint"])[PhysJoint].offset2 = glm.vec3(0, -2.5, 0)
		
		return
	
	@classmethod
	def releaseHook(cls, index, hook):
		
		return
	