from config import *
from Level.Core.AABB import AABB

class Box:

	#transf.scale == side lengths

	@staticmethod
	def getDebugMeshName():
		return "cube"

	@staticmethod
	def calcAABB(transf):
		topRight = abs(transf.cori * (glm.vec3(1, 1, 1) * transf.scale))
		botRight = abs(transf.cori * (glm.vec3(1, -1, 1) * transf.scale))
		topLeft = abs(transf.cori * (glm.vec3(-1, 1, 1) * transf.scale))
		botLeft = abs(transf.cori * (glm.vec3(-1, -1, 1) * transf.scale))
		aabbShape = glm.vec3(
			max(topRight.x, botRight.x, topLeft.x, botLeft.x),
			max(topRight.y, botRight.y, topLeft.y, botLeft.y),
			max(topRight.z, botRight.z, topLeft.z, botLeft.z)
		)
		return AABB.createAABB(transf.cpos, aabbShape)

	@staticmethod
	def calcSupport(transf, direction):
		xBasis = glmh.xBasis(transf.cori)
		yBasis = glmh.yBasis(transf.cori)
		zBasis = glmh.zBasis(transf.cori)
		return (
			transf.cpos
			+ xBasis * transf.scale.x/2 * -glmh.sign(-glm.dot(direction, xBasis))
			+ yBasis * transf.scale.y/2 * -glmh.sign(-glm.dot(direction, yBasis))
			+ zBasis * transf.scale.z/2 * -glmh.sign(-glm.dot(direction, zBasis))
		)
	
	@staticmethod
	def castRay(transf, origin, direction):
		relOrigin = (origin - transf.cpos) * transf.cori
		relDir = direction * -transf.cori
		boundChecks = [(relOrigin[i] > transf.scale[i]) - (relOrigin[i] < -transf.scale[i]) for i in range(3)]
		
		if boundChecks[0] and glmh.sign(relDir.x) != boundChecks[0]:
			if relDir.x != 0:
				l = (boundChecks[0]*transf.scale.x - relOrigin.x) / relDir.x
				if l > 0:
					absRelIntersect = abs(relOrigin + l * relDir)
					if absRelIntersect.y <= transf.scale.y and absRelIntersect.z <= transf.scale.z:
						return origin + l * direction
		
		if boundChecks[1] and glmh.sign(relDir.y) != boundChecks[1]:
			if relDir.y != 0:
				l = (boundChecks[1]*transf.scale.y - relOrigin.y) / relDir.y
				if l > 0:
					absRelIntersect = abs(relOrigin + l * relDir)
					if absRelIntersect.x <= transf.scale.x and absRelIntersect.z <= transf.scale.z:
						return origin + l * direction
			
		
		if boundChecks[2] and glmh.sign(relDir.z) != boundChecks[2]:
			if relDir.z != 0:
				l = (boundChecks[2]*transf.scale.z - relOrigin.z) / relDir.z
				if l > 0:
					absRelIntersect = abs(relOrigin + l * relDir)
					if absRelIntersect.x <= transf.scale.x and absRelIntersect.y <= transf.scale.y:
						return origin + l * direction
		
		return False
