from config import *
from Level.Core.AABB import AABB

class Ray:

	#transf.cpos == origin
	#glmh.zBasis(transf.cori) == dir
	#transf.scale.x == range

	@staticmethod
	def dir(transf):
		return glmh.zBasis(transf.cori)
	@staticmethod
	def range(transf):
		return transf.scale.x
	@staticmethod
	def ray(transf):
		return Ray.dir(transf) * Ray.range(transf)

	@staticmethod
	def getDebugMeshName():
		return "ray"

	@staticmethod
	def calcAABB(transf):
		ray = Ray.ray(transf)
		return AABB.createAABB(transf.cpos + ray / 2, abs(ray))

	@staticmethod
	def calcSupport(transf, direction):
		ray = Ray.ray(transf)
		return transf.cpos + ray * (1 - glmh.sign(-glm.dot(direction, ray))) / 2
		#zBasis = glmh.zBasis(transf.cori)
		#return transf.rpos + zBasis * transf.scale.x * (-glmh.sign(-glm.dot(direction, zBasis)) + 1) / 2
	
	@staticmethod
	def castRay(transf, origin, direction):
		return False	#rays dont cross
