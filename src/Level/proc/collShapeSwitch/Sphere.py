from config import *
from Level.Core.AABB import AABB

class Sphere:

	#transf.scale.x == diameter

	@staticmethod
	def getDebugMeshName():
		return "sphere"
	
	@staticmethod
	def calcAABB(transf):
		return AABB.createAABB(transf.cpos, glm.vec3(transf.scale.x))
	
	@staticmethod
	def calcSupport(transf, direction):
		return transf.cpos + 0.5 * transf.scale.x * direction
	
	@staticmethod
	def castRay(transf, origin, direction):
		t = glm.dot((transf.cpos - origin), direction)
		y = glm.distance(transf.cpos, origin + t * direction)
		if y < 0.5 * transf.scale.x:
			x = glm.sqrt((0.5 * transf.scale.x) ** 2 - y ** 2)
			if t > x:
				return origin + (t - x) * direction
		return False
	