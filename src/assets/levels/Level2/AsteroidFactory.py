from config import *

from Core.Props.Transf import Transf
from Core.Props.Coll import Coll
from Core.Props.Field import Field
from Core.Props.Physics.Forcefield import Forcefield
from Core.Props.Physics.Rigidbody import Rigidbody
from Core.Props.Timer import Timer
from Core.Props.Scripts import PreScript, PostScript

from Core.Props.Graphics.Rend import Rend
from Core.Props.Graphics.Model import Model
from Core.Props.Graphics.ParticleEffect import ParticleEffect

from Core.Systems.Physics.rb import rb

class AsteroidFactory:
	@classmethod
	def create(cls, index, pos, iniVel):
		texture = [
			"die",
			"eyeball",
			"tesseract",
			"dolphinWireframe",
			"play4keeps",
			"swimcity",
			"purpleWall",
			"stoneWall"
		][random.randint(0, 7)]
		shape = [COLLSPHERE, COLLSPHERE, COLLCYLINDER][random.randint(0, 2)]
		size = 16+random.random()*16
		mesh = [
			"asteroid1", "asteroid2", "asteroid3", "asteroid4", "asteroid5"
		][random.randint(0, 4)]
		mass = size*3000
		
		index.createObj(
			"asteroid",
			[
				Transf(pos, glm.quat(), glm.vec3(size)),
				Coll(shape, COLLRIGIDBODY),
				Rigidbody(
					mass, 0.5, 3*glm.pi()/8, 0.8,
					iniVel=iniVel,
					iniWel=glmh.rotVecToQuat(glmh.randVec3()/16),
					suffersGravity=False
				),
				PreScript(cls.fixZPos),
				Timer(8, deleteOnCycle=True),
				
				Rend(True, "texture", {"tex": texture, "uvScale": glm.vec2(1)}),
				Model(#mesh, True),
					{
						COLLSPHERE: "sphere",
						COLLBOX: "cube",
						COLLCYLINDER: "cylinder",
					}[shape],
					True
				),
			]
		)
		return
	@classmethod
	def fixZPos(cls, obj, index):
		transf = obj[Transf]
		transf.setRpos(glm.vec3(
			transf.cpos.x,
			transf.cpos.y,
			min(max(-3, transf.cpos.z), 3)
		))
		if obj[Timer].click:
			transf = obj[Transf]
			index.createObj(
				"explosion",
				[
					Transf(transf.cpos, transf.cori, 4 * transf.scale),
					Coll(COLLSPHERE, COLLGHOST),
					Field(),
					PostScript(cls.explosionEventClosure(obj[Rigidbody].mass)),
					
					Timer(2, deleteOnCycle=True),
					Rend(True, "explosion", {"time": None}),
					ParticleEffect(int(obj[Rigidbody].mass / 500), pointSize=2),
				]
			)
		return
	@classmethod
	def makeExplosion(cls, obj, index):
		if obj[Timer].click:
			transf = obj[Transf]
			index.createObj(
				"explosion",
				[
					Transf(transf.cpos, transf.cori, 4 * transf.scale),
					Coll(COLLSPHERE, COLLGHOST),
					Field(),
					PostScript(cls.explosionEventClosure(obj[Rigidbody].mass)),
					
					Timer(2, deleteOnCycle=True),
					Rend(True, "explosion", {"time": None}),
					ParticleEffect(int(obj[Rigidbody].mass / 500), pointSize=2),
				]
			)
		return
	@classmethod
	def explosionEventClosure(cls, p):
		return lambda o, i: cls.explosionEvent(o, i, p)
	@staticmethod
	def explosionEvent(obj, index, power):
		for key in obj[Field].keys:
			other = index.get(key)
			if (
				Rigidbody in other and
				"chain" not in other[Coll].tags
			):
				other = index.get(key)
				body = other[Rigidbody]
				delta = other[Transf].cpos - obj[Transf].cpos
				distance = glm.length(delta)
				norm = glm.normalize(delta)
				radius = obj[Transf].scale.x * 2	#i.e. sphere radius
				force = power * (1 - pow(distance / radius, 2))
				impulse = force * norm
				rb.applyImpulse(body, other[Transf], impulse, other[Transf].cpos)
		
		index.deleteProp(obj.key, PostScript)
		
		return
	