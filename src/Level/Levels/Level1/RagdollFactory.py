from config import *

from Controller import Controller

from Level.Props.Transf import Transf
from Level.Props.Coll import Coll
from Level.Props.Rigidbody import Rigidbody
from Level.Props.PhysJoint import PhysJoint

from Level.Props.Rendering.Rend import Rend
from Level.Props.Rendering.Model import Model

from Level.Props.Rendering.Lighting.Light import Light
from Level.Props.Rendering.Lighting.SpotLight import SpotLight
from Level.Props.Rendering.Lighting.PointLight import PointLight

class RagdollFactory:
	BASEMASS = 10
	PHI = glm.pi()/16
	MEW = 0.3
	
	@classmethod
	def createRagdoll(cls, index, key, pos, ori, scale, suffersGravity):
		keys = {}
		keys["torso"] = index.createObj(
			key+"_torso",
			[
				Transf(pos, ori, scale * glm.vec3(0.3, 0.24, 0.3)),
				Coll(COLLCAPSULE, COLLRIGIDBODY),
				Rigidbody(77 * scale * cls.BASEMASS, 0, cls.PHI, cls.MEW, suffersGravity=suffersGravity)
			]
		)
		_ = cls.makeModelSon(
			index, keys["torso"],
			glm.vec3(0, -0.85, 0),
			scale, "astronauta_torso"
		)
		
		keys["head"] = cls.makeAndJointPart(
			index, keys["torso"], key+"_head", scale, 12.6, COLLSPHERE, glm.vec3(0.25),
			glm.vec3(0, 0.275, 0), glm.vec3(0, -0.125, 0),
			glm.quat(), glm.vec3(70, 90, 30), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["head"],
			glm.vec3(0, -1.225, 0),
			scale, "astronauta_reloded_head"
		)
		index.get(keys["head"])[Coll].ignoreKeys.add(keys["torso"])
		lightkey = index.createObj(
			key+"_spotlight",
			[
				Transf(
					glm.vec3(0, 0, 5), glm.quat(), glm.vec3(0.25),
					parent=index.get(keys["head"])[Transf]
				),
				Light(glm.vec3(1, 1, 0.8), 1/2),
				#PointLight(),
				SpotLight(glmh.zUnit(), glm.vec2(30, 90)),
			]
		)
		
		#arms
		keys["leftarmtop"] = cls.makeAndJointPart(
			index, keys["torso"], key+"_leftarmtop", scale, 4.3, COLLCAPSULE, glm.vec3(0.1, 0.15, 0.1),
			glm.vec3(0.125, 0.2, -0.05), glm.vec3(0, 0.2, 0),
			glm.normalize(glm.angleAxis(glm.pi()/2, glmh.zUnit()) * glm.angleAxis(-glm.pi()/3, glmh.xUnit())),
			glm.vec3(90, 22.5, 90), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["leftarmtop"],
			glm.vec3(-1, -0.1, 0.05),
			scale, "astronauta_reloded_leftarmtop"
		)
		index.get(keys["leftarmtop"])[Coll].ignoreKeys.add(keys["torso"])
		
		keys["leftarmbot"] = cls.makeAndJointPart(
			index, keys["leftarmtop"], key+"_leftarmbot", scale, 3.4, COLLCAPSULE, glm.vec3(0.1, 0.15, 0.1),
			glm.vec3(0, -0.125, 0), glm.vec3(0, 0.125, 0),
			glm.angleAxis(-5*glm.pi()/12, glmh.xUnit()), glm.vec3(75, 0, 0), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["leftarmbot"],
			glm.vec3(-1, 0.15, 0.05),
			scale, "astronauta_reloded_leftarmbot"
		)
		index.get(keys["leftarmbot"])[Coll].ignoreKeys.add(keys["leftarmtop"])
		
		keys["rightarmtop"] = cls.makeAndJointPart(
			index, keys["torso"], key+"_rightarmtop", scale, 4.3, COLLCAPSULE, glm.vec3(0.1, 0.15, 0.1),
			glm.vec3(-0.125, 0.2, -0.05), glm.vec3(0, 0.2, 0),
			glm.normalize(glm.angleAxis(-glm.pi()/2, glmh.zUnit()) * glm.angleAxis(-glm.pi()/3, glmh.xUnit())),
			glm.vec3(90, 22.5, 90), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["rightarmtop"],
			glm.vec3(1, -0.1, 0.05),
			scale, "astronauta_reloded_rightarmtop"
		)
		index.get(keys["rightarmtop"])[Coll].ignoreKeys.add(keys["torso"])
		
		keys["rightarmbot"] = cls.makeAndJointPart(
			index, keys["rightarmtop"], key+"_rightarmbot", scale, 3.4, COLLCAPSULE, glm.vec3(0.1, 0.15, 0.1),
			glm.vec3(0, -0.125, 0), glm.vec3(0, 0.125, 0),
			glm.angleAxis(-5*glm.pi()/12, glmh.xUnit()), glm.vec3(75, 0, 0), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["rightarmbot"],
			glm.vec3(1, 0.15, 0.05),
			scale, "astronauta_reloded_rightarmbot"
		)
		index.get(keys["rightarmbot"])[Coll].ignoreKeys.add(keys["rightarmtop"])
		
		#legs
		keys["leftlegtop"] = cls.makeAndJointPart(
			index, keys["torso"], key+"_leftlegtop", scale, 15.5, COLLCAPSULE, glm.vec3(0.15, 0.125, 0.15),
			glm.vec3(0.08, -0.2, 0), glm.vec3(0, 0.2125, 0),
			glm.normalize(glm.angleAxis(-glm.pi()/6, glmh.xUnit()) * glm.angleAxis(glm.pi()/6, glmh.zUnit())),
			glm.vec3(90, 75, 45), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["leftlegtop"],
			glm.vec3(-0.1, -0.45, 0),
			scale, "astronauta_reloded_leftlegtop"
		)
		index.get(keys["leftlegtop"])[Coll].ignoreKeys.add(keys["torso"])
		keys["leftlegbot"] = cls.makeAndJointPart(
			index, keys["leftlegtop"], key+"_leftlegbot", scale, 9.4, COLLCAPSULE, glm.vec3(0.15, 0.15, 0.15),
			glm.vec3(0, -0.125, 0), glm.vec3(0, 0.15, 0),
			glm.angleAxis(4*glm.pi()/12, glmh.xUnit()), glm.vec3(60, 0, 0), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["leftlegbot"],
			glm.vec3(-0.1, -0.175, 0),
			scale, "astronauta_reloded_leftlegbot"
		)
		index.get(keys["leftlegbot"])[Coll].ignoreKeys.add(keys["leftlegtop"])
		
		keys["rightlegtop"] = cls.makeAndJointPart(
			index, keys["torso"], key+"_rightlegtop", scale, 15.5, COLLCAPSULE, glm.vec3(0.15, 0.125, 0.15),
			glm.vec3(-0.08, -0.2, 0), glm.vec3(0, 0.2125, 0),
			glm.normalize(glm.angleAxis(-glm.pi()/6, glmh.xUnit()) * glm.angleAxis(-glm.pi()/6, glmh.zUnit())),
			glm.vec3(90, 75, 60), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["rightlegtop"],
			glm.vec3(0.1, -0.45, 0),
			scale, "astronauta_reloded_rightlegtop"
		)
		index.get(keys["rightlegtop"])[Coll].ignoreKeys.add(keys["torso"])
		keys["rightlegbot"] = cls.makeAndJointPart(
			index, keys["rightlegtop"], key+"_rightlegbot", scale, 9.4, COLLCAPSULE, glm.vec3(0.15, 0.15, 0.15),
			glm.vec3(0, -0.125, 0), glm.vec3(0, 0.15, 0),
			glm.angleAxis(4*glm.pi()/12, glmh.xUnit()), glm.vec3(60, 0, 0), suffersGravity
		)
		_ = cls.makeModelSon(
			index, keys["rightlegbot"],
			glm.vec3(0.1, -0.175, 0),
			scale, "astronauta_reloded_rightlegbot"
		)
		index.get(keys["rightlegbot"])[Coll].ignoreKeys.add(keys["rightlegtop"])
		
		return keys
	
	@classmethod
	def makeAndJointPart(
		cls, index, dadkey, sonkey, scale, massMod, shape, size,
		dadOffset, sonOffset, jointOri, freedom, suffersGravity
	):
		dadTransf = index.get(dadkey)[Transf]
		jointPos = dadTransf.cpos + dadTransf.cori * dadOffset * scale
		sonkey = index.createObj(
			sonkey,
			[
				Transf(
					jointPos - glm.normalize(dadTransf.cori * jointOri) * sonOffset * scale,
					glm.normalize(dadTransf.cori * jointOri),
					scale * size
				),
				Coll(shape, COLLRIGIDBODY),
				Rigidbody(
					massMod * scale * cls.BASEMASS,
					0, cls.PHI, cls.MEW,
					suffersGravity=suffersGravity
				)
			]
		)
		_ = index.createObj(
			"joint_"+dadkey+"_"+sonkey,
			[PhysJoint(
				dadkey, sonkey,
				dadOffset * scale, sonOffset * scale,
				jointOri, freedom=freedom
			)]
		)
		return sonkey
	
	@classmethod
	def makeModelSon(cls, index, dadkey, pos, scale, mesh):
		sonkey = index.createObj(
			dadkey+"_model",
			[
				Transf(
					pos * scale, glm.quat(), glm.vec3(scale),
					parent=index.get(dadkey)[Transf]
				),
				Rend(True, "texture", {"texture": "multpaleta", "uvScale": glm.vec2(1)}),
				Model(mesh, False)
			]
		)
		return sonkey
		
	
	