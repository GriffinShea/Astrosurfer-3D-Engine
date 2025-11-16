from config import *
from Controller import Controller

from assets.levels.Level1.RagdollFactory import RagdollFactory
from assets.levels.Level1.SpawnerFactory import SpawnerFactory
from assets.levels.Level1.ArrowFactory import ArrowFactory
from assets.levels.Level1.GrappleGunFactory import GrappleGunFactory

from Core.Props.Timer import Timer
from Core.Props.Transf import Transf
from Core.Props.Coll import Coll

from Core.Props.Scripts import PreScript, PostScript

from Core.Props.Physics.Rigidbody import Rigidbody
from Core.Props.Physics.PhysJoint import PhysJoint
from Core.Props.Physics.Jet import Jet
from Core.Props.Physics.PIDSteer import PIDSteer
from Core.Props.Physics.Attractor import Attractor

from Core.Props.Graphics.Rend import Rend
from Core.Props.Graphics.Model import Model
from Core.Props.Graphics.Segment import Segment
from Core.Props.Graphics.Camera import Camera
from Core.Props.Graphics.ParticleEffect import ParticleEffect

from Core.Props.Graphics.Lights import Light
from Core.Props.Graphics.Lights import PointLight
from Core.Props.Graphics.Lights import SpotLight


class Builder:
	@classmethod
	def build(cls, index):
		#background
		index.createObj(
			"background",
			[
				Transf(glm.vec3(0, 500, 16), glm.quat(), glm.vec3(1024, 2048, 1)),
				Rend(True, "unLitTexture", {"texture": "purpleSky", "uvScale": glm.vec2(17, 33)}),
				Model("plane", False)
			]
		)
		#platform (static)
		index.createObj(
			"platform",
			[
				Transf(glm.vec3(0, -10, 0), glm.quat(), glm.vec3(10)),
				Coll(COLLBOX, COLLTERRAIN),
				Rend(True, "texture", {"texture": "play4keeps", "uvScale": glm.vec2(1)}),
				Model("cube", True)
			]
		)
		
		#set this counter
		index.setSing("handsOnRocket", 0)
		
		#create the rocket
		(rocketkey, righthandlekey, lefthandlekey) = cls.createRocket(index)
		index.setSing("rocketkey", rocketkey)
		
		#create a ragdoll and give keys to index
		ragdollkeys = RagdollFactory.createRagdoll(
			index, "ragdoll",
			glm.vec3(0, 0, 0), glm.angleAxis(glm.pi(), glmh.yUnit()), 4,
			True
		)
		index.addProp(ragdollkeys["leftarmbot"], Attractor(righthandlekey, 1000, 2, 100))
		index.get(ragdollkeys["leftarmbot"])[Coll].postcollide = cls.attachRocketHandle
		index.addProp(ragdollkeys["rightarmbot"], Attractor(lefthandlekey, 1000, 2, 100))
		index.get(ragdollkeys["rightarmbot"])[Coll].postcollide = cls.attachRocketHandle
		index.setSing("ragdollkeys", ragdollkeys)
		
		#add a camera attached to the player
		camerakey = index.createObj(
			index.getSing("ragdollkeys")["torso"]+"_camera",
			[
				Transf(glm.vec3(0, 0, -32), glm.quat(), glm.vec3(0.1)),
				Camera(100),
				PostScript(cls.fixCameraPos),
				Light(glm.vec3(1, 1, 0.8), 1/3),
				PointLight(),
			]
		)
		index.setSing("camerakey", camerakey)
		
		
		
		#create and setup grapple gun and setup associated controls
		#grapplekeys = GrappleGunFactory.create(index)
		
		
		
		#arrow to guide the player
		ArrowFactory.create(index, "guide", 1, index.getSing("rocketkey"))
		
		#create asteroid spawners
		for i in range(-4, 5, 1):
			SpawnerFactory.createSpawner(index, "spawner", glm.vec3(i*16, -128, 0))
		
		return
	
	@classmethod
	def fixCameraPos(cls, obj, index):
		obj[Transf].setRpos(glm.vec3(
			index.get(index.getSing("ragdollkeys")["torso"])[Transf].cpos.x,
			index.get(index.getSing("ragdollkeys")["torso"])[Transf].cpos.y,
			-32
		))
		return
	
	@staticmethod
	def createRocket(index):
		rocketkey = index.createObj(
			"rocket",
			[
				Transf(glm.vec3(0, -1, 0), glm.quat(), glm.vec3(2, 6, 2)),
				Coll(COLLCYLINDER, COLLRIGIDBODY),
				Rigidbody(60000, 0, glm.pi()/16, 0.3, suffersGravity=False),
				Jet(glm.vec3(0, 1, 0), 0),
				
				Rend(True, "texture", {"texture": "play4keeps", "uvScale": glm.vec2(8)}),
				Model("cylinder", True),
			]
		)
		rightkey = index.createObj(
			"rocket_right_handle",
			[
				Transf(
					glm.vec3(1, 0, -1),
					glm.normalize(
						glm.angleAxis(glm.pi()/4, glmh.yUnit())
						* glm.angleAxis(glm.pi()/2, glmh.zUnit())
					),
					glm.vec3(0.25, 1, 0.25),
					parent=index.get(rocketkey)[Transf]
				),
				Coll(COLLCYLINDER, COLLGHOST),
				
				Rend(True, "texture", {"texture": "tesseract", "uvScale": glm.vec2(1)}),
				Model("cylinder", True)
			]
		)
		leftkey = index.createObj(
			"rocket_left_handle",
			[
				Transf(
					glm.vec3(-1, 0, -1),
					glm.normalize(
						glm.angleAxis(-glm.pi()/4, glmh.yUnit())
						* glm.angleAxis(-glm.pi()/2, glmh.zUnit())
					),
					glm.vec3(0.25, 1, 0.25),
					parent=index.get(rocketkey)[Transf]
				),
				Coll(COLLCYLINDER, COLLGHOST),
				
				Rend(True, "texture", {"texture": "tesseract", "uvScale": glm.vec2(1)}),
				Model("cylinder", True)
			]
		)
		index.createObj(
			"rocket_tip",
			[
				Transf(
					glm.vec3(0, 4, 0), glm.quat(), glm.vec3(1, 1, 1),
					parent=index.get(rocketkey)[Transf]
				),
				
				Rend(True, "unLitTexture", {"texture": "eyeball", "uvScale": glm.vec2(1)}),
				Model("pyr", False)
			]
		)
		
		return (rocketkey, rightkey, leftkey)
	@classmethod
	def attachRocketHandle(cls, index, collision):
		hand = index.get(collision[0])
		if collision[1] == hand[Attractor].targetkey:
			#attach the hand to the rocket with a PhysJoint
			handleTransf = index.get(collision[1])[Transf]
			_ = index.createObj(
				"joint_" +collision[0]+"rocket",
				[PhysJoint(
					collision[0], "rocket",
					glm.vec3(0, -hand[Transf].scale.y / 2, 0), handleTransf.rpos,
					glm.angleAxis(glm.pi()*7/8, glmh.xUnit()), freedom=glm.vec3(30)
				)]
			)
			
			#turn off this collision function and increment counter
			hand[Attractor].power = 0
			hand[Coll].postcollide = None
			index.setSing("handsOnRocket", index.getSing("handsOnRocket") + 1)
			
			#turn off rocket gravity and turn on rocket
			if index.getSing("handsOnRocket") == 2:
				print("attach rocket!")
				rocket = index.get("rocket")
				rocket[Jet].force = index.get("rocket")[Rigidbody].mass * 20
				index.createObj(
					"rocketSteerer",
					[
						Transf(glm.vec3(), glm.quat(), glm.vec3(1/4)),
						Rend(True, "solidUnlitColour", {"colour": glm.vec3(1, 0, 0)}),
						Model("sphere", False),
						PreScript(cls.rocketSteererUpdate),
					]
				)
				index.addProp("rocket", PIDSteer("rocketSteerer", 0.6, 0, 0.125, 100))
				index.addProp("rocket", Timer(0.0625))
				index.addProp("rocket", PreScript(cls.makeEmission))
				
				
				for key in index.getSing("ragdollkeys").values():
					index.get(key)[Rigidbody].suffersGravity = False
				
				index.setSing("swapTimer", 0)
			
		return
	@staticmethod
	def makeEmission(obj, index):
		if obj[Timer].click:
			transf = obj[Transf]
			index.createObj(
				"rocketEmission",
				[
					Transf(transf.cpos + -glmh.yBasis(transf.cori) * 3, transf.cori, glm.vec3(1)),
					Timer(2, deleteOnCycle=True),
					Rend(True, "rocketEmission", {"time": None}),
					ParticleEffect(8, pointSize=4)
				]
			)
		return
	@staticmethod
	def rocketSteererUpdate(obj, index):
		rocketTransf = index.get("rocket")[Transf]
		obj[Transf].setRpos(glm.vec3(
			rocketTransf.cpos.x + 32 * ((Controller.checkKey(K_d)>0)-(Controller.checkKey(K_a)>0)),
			rocketTransf.cpos.y + 32 * ((Controller.checkKey(K_w)>0)-(Controller.checkKey(K_s)>0)),
			rocketTransf.cpos.z
		))
		
		return
	