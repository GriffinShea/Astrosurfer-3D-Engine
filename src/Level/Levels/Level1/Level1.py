from config import *
from Level.Core.LevelDefinitionFile import LevelDefinitionFile

from Renderer import Renderer
from Controller import Controller

from Level.Core.Canvas import Canvas

from Level.Levels.Level1.RagdollFactory import RagdollFactory
from Level.Levels.Level1.SpawnerFactory import SpawnerFactory
from Level.Levels.Level1.ArrowFactory import ArrowFactory
from Level.Levels.Level1.GrappleGunFactory import GrappleGunFactory

from Level.Props.UpdateScripter import UpdateScripter
from Level.Props.Timer import Timer
from Level.Props.Transf import Transf
from Level.Props.PIDSteer import PIDSteer
from Level.Props.Attractor import Attractor
from Level.Props.Coll import Coll
from Level.Props.Rigidbody import Rigidbody
from Level.Props.PhysJoint import PhysJoint
from Level.Props.Jet import Jet

from Level.Props.Rendering.Rend import Rend
from Level.Props.Rendering.Model import Model
from Level.Props.Rendering.Segment import Segment
from Level.Props.Rendering.Camera import Camera
from Level.Props.Rendering.ParticleEffect import ParticleEffect

from Level.Props.Rendering.Lighting.Light import Light
from Level.Props.Rendering.Lighting.PointLight import PointLight
from Level.Props.Rendering.Lighting.SpotLight import SpotLight

from Level.Levels.Level2.Level2 import Level2

class Level1(LevelDefinitionFile):
	swapTimer = 0
	@classmethod
	def ldfUpdate(cls, level, index):
		#when rocket has attached count three seconds until level swap
		if index.getSing("handsOnRocket") == 2:
			cls.swapTimer += Renderer.dTime
			if cls.swapTimer > 3:
				cls.swapLevel(level, index)
		
		#ragdoll controls/update
		if index.getSing("handsOnRocket") < 2:
			ragdollTorso = index.get(index.getSing("ragdollkeys")["torso"])
			ragdollTorso[Transf].setRpos(glm.vec3(
				ragdollTorso[Transf].cpos.x
				+ Renderer.dTime * ((Controller.checkKey(K_d)>0)-(Controller.checkKey(K_a)>0)),
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
			print(obj, obj.key)
			index.deleteObj(obj.key)
		level.LDF = Level2
		level.LDF.buildLevel(level, level.index)
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
			"DISTANCE TO SPACE SHIP: "+str(distance)+"m\nSPEED: "+speed+"m/s",
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
		
		#congradulations
		if index.getSing("handsOnRocket") == 2:
			Renderer.drawText(
				"CONGRADULATIONS!!!",
				"basicText",
				"fancyFont",
				{
					"colour": WHITE, "alpha": 0.5, "depth": 1,
					"transfMat": glm.scale(
						glm.translate(glm.mat4(), glm.vec3(-0.5, 0, 0)),
						glm.vec3(2, 4, 2)
					)
				}
			)
		return
	
	@classmethod
	def buildLevel(cls, level, index):
		#specify the canvas
		level.canvas = Canvas(
			glm.vec3(0.55, 0.65, 0.75)/16,
			glm.vec3(0.1),
			glm.vec2(0, 1)
		)
		#background
		index.createObj(
			"background",
			[
				Transf(glm.vec3(0, 500, 16), glm.quat(), glm.vec3(1024, 2048, 1)),
				Rend(True, "unLitTexture", {"texture": "purpleSky", "uvScale": glm.vec2(17, 33)}),
				Model("plane", False)
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
		#index.addProp(ragdollkeys["leftarmbot"], Attractor(righthandlekey, 1000, 2, 100))
		#index.get(ragdollkeys["leftarmbot"])[Coll].postcollide = cls.attachRocketHandle
		index.addProp(ragdollkeys["rightarmbot"], Attractor(lefthandlekey, 1000, 2, 100))
		index.get(ragdollkeys["rightarmbot"])[Coll].postcollide = cls.attachRocketHandle
		index.setSing("ragdollkeys", ragdollkeys)
		
		#add a camera attached to the player
		camerakey = index.createObj(
			index.getSing("ragdollkeys")["torso"]+"_camera",
			[
				Transf(glm.vec3(0, 0, -32), glm.quat(), glm.vec3(0.1)),
				Camera(100),
				UpdateScripter(postupdate=cls.fixCameraPos),
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
				Transf(glm.vec3(0, 100, 0), glm.quat(), glm.vec3(2, 6, 2)),
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
						UpdateScripter(preupdate=cls.rocketSteererUpdate),
					]
				)
				index.addProp("rocket", PIDSteer("rocketSteerer", 0.6, 0, 0.125, 100))
				index.addProp("rocket", Timer(0.0625, cycleFunc=cls.makeEmission))
				
				
				for key in index.getSing("ragdollkeys").values():
					index.get(key)[Rigidbody].suffersGravity = False
				
				cls.swapTimer = 0
			
		return
	@staticmethod
	def makeEmission(obj, index):
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
	