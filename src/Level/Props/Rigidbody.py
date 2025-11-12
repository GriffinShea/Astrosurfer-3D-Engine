from config import *
from Renderer import Renderer
from Level.Core.Prop import Prop
from Level.Props.Transf import Transf
from Level.Props.Coll import Coll

@attr.define
class Rigidbody(Prop):
	mass: float			#positive number
	coeffRest: float	#between 0 and 1
	phi: float			#between 0 and glm.pi()/2
	mew: float			#between 0 and atan(phi)
	
	lockOri: bool = attr.field(default=False)
	suffersGravity: bool = attr.field(default=True)
	
	lpos: glm.vec3 = attr.field(alias="iniVel", default=attr.Factory(glm.vec3))
	lori: glm.quat = attr.field(alias="iniWel", default=attr.Factory(glm.quat))
	
	forces: glm.vec3 = attr.field(init=False, default=attr.Factory(glm.vec3))
	torques: glm.vec3 = attr.field(init=False, default=attr.Factory(glm.vec3))
	invInertiaMat: glm.mat3 = attr.field(init=False, default=attr.Factory(glm.mat3))
	
	@classmethod
	def setup(cls, obj):
		obj[Rigidbody].lpos = -obj[Rigidbody].lpos
		obj[Rigidbody].lpos += obj[Transf].cpos	#+= because iniVel may be loaded
		obj[Rigidbody].lori = glm.normalize(obj[Transf].cori * obj[Rigidbody].lori)
		
		obj[Rigidbody].invInertiaMat = Rigidbody.calcInvInertiaMat(obj)
		obj[Rigidbody].forces = glm.vec3()
		obj[Rigidbody].torques = glm.vec3()
		
		assert not obj[Transf].parent
		#assert obj[Coll].physType == COLLRIGIDBODY
		
		return
	
	@staticmethod
	def calcInvInertiaMat(obj):
		mat = glm.mat3()
		if obj[Coll].shape == COLLSPHERE:
			mat = glm.mat3(2 / 5 * (obj[Transf].scale.x/2) ** 2)
		if obj[Coll].shape == COLLCAPSULE:
			#source: https://www.gamedev.net/tutorials/programming/math-and-physics/capsule-inertia-tensor-r3856/
			mat = glm.mat3()
			
			r = obj[Transf].scale.x / 2
			h = obj[Transf].scale.y / 2
			
			r2 = r ** 2
			h2 = h ** 2
			
			mcy = h * r2 * glm.pi()
			mhs = 2 * r ** 3 * glm.pi() / 3
			
			mat[0][0] = mcy * (h2 / 12 + r2 / 4) + mhs * 2 * (2 * r2 / 5 + h2 / 2 + 3 * h * r / 8)
			mat[1][1] = mcy * (r2 / 2) + mhs * 2 * (2 * r2 / 5)
			mat[2][2] = mcy * (h2 / 12 + r2 / 4) + mhs * 2 * (2 * r2 / 5 + h2 / 2 + 3 * h * r / 8)
			
			m = 1 / (mcy + 2 * mhs)
			mat[0][0] *= m
			mat[1][1] *= m
			mat[2][2] *= m
		elif obj[Coll].shape == COLLCYLINDER:
			mat = glm.mat3(1 / 12)
			mat[0][0] *= 3 * obj[Transf].scale.x ** 2 + obj[Transf].scale.y ** 2
			mat[1][1] *= 6 * obj[Transf].scale.x ** 2
			mat[2][2] *= 3 * obj[Transf].scale.x ** 2 + obj[Transf].scale.y ** 2
		elif obj[Coll].shape == COLLBOX:
			mat = glm.mat3(1 / 12)
			halfScale = obj[Transf].scale
			mat[0][0] *= halfScale.y ** 2 + halfScale.z ** 2
			mat[1][1] *= halfScale.x ** 2 + halfScale.z ** 2
			mat[2][2] *= halfScale.x ** 2 + halfScale.y ** 2
		return glm.inverse(obj[Rigidbody].mass * mat)
	
	#REVISIT: move to proc.physics
	@staticmethod
	def calcVel(body, transf):
		return (transf.cpos - body.lpos) / Renderer.dTime
	@staticmethod
	def calcWel(body, transf):
		logDiff = glmh.quatLog(glmh.quatDiff(transf.cori, body.lori))
		return 2 * glm.vec3(logDiff.x, logDiff.y, logDiff.z) / Renderer.dTime
	@staticmethod
	def momentify(body, transf, vector):
		return transf.cori * ((vector * transf.cori) * body.invInertiaMat)
	
