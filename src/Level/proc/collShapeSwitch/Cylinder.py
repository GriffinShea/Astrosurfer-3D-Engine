from config import *
from Level.Core.AABB import AABB

class Cylinder:

	@staticmethod
	def diameter(transf):
		return transf.scale.x
	@staticmethod
	def radius(transf):
		return transf.scale.x / 2
	@staticmethod
	def height(transf):
		return transf.scale.y
	
	
	
	@staticmethod
	def getDebugMeshName():
		return "cylinder"

	@classmethod
	def calcAABB(cls, transf):
		surfaceNorm = glmh.yBasis(transf.cori)
		aabbShape = cls.height(transf)*abs(surfaceNorm)
		
		#the below was simplified from these three:
		#abs(glm.cross(surfaceNorm, glm.normalize(glm.vec3(0, -surfaceNorm.z, surfaceNorm.y))).x)
		#abs(glm.cross(surfaceNorm, glm.normalize(glm.vec3(-surfaceNorm.z, 0, surfaceNorm.x))).y)
		#abs(glm.cross(surfaceNorm, glm.normalize(glm.vec3(-surfaceNorm.y, surfaceNorm.x, 0))).z)
		#the idea is find the cross product between the norm and a perpendicular vector in the two dimensions you dont want
		#also what the hell man is there no better way to do this?
		if surfaceNorm.y != 0 or surfaceNorm.z != 0:
			aabbShape.x += cls.diameter(transf)*(surfaceNorm.y**2 + surfaceNorm.z**2) / glm.length(glm.vec2(surfaceNorm.y, surfaceNorm.z))
		if surfaceNorm.x != 0 or surfaceNorm.z != 0:
			#REVISIT: got division by zero here one time
			aabbShape.y += cls.diameter(transf)*(surfaceNorm.x**2 + surfaceNorm.z**2) / glm.length(glm.vec2(surfaceNorm.x, surfaceNorm.z))
		if surfaceNorm.x != 0 or surfaceNorm.y != 0:
			aabbShape.z += cls.diameter(transf)*(surfaceNorm.y**2 + surfaceNorm.x**2) / glm.length(glm.vec2(surfaceNorm.x, surfaceNorm.y))
		
		
		return AABB.createAABB(transf.cpos, aabbShape)

	@classmethod
	def calcSupport(cls, transf, direction):
		yBasis = glmh.yBasis(transf.cori)
		return (
			transf.cpos
			+ yBasis * cls.height(transf)/2 * -glmh.sign(-glm.dot(direction, yBasis))
			+ cls.diameter(transf)/2 * glmh.ncross(glm.cross(yBasis, direction), yBasis)
		)
	
	@classmethod
	def castRay(cls, transf, origin, direction):
		relOrigin = (origin - transf.cpos) * transf.cori
		relOriginXZ = glm.vec2(relOrigin.x, relOrigin.z)
		relDir = direction * -transf.cori
		relDirXZ = glm.vec2(relDir.x, relDir.z)
		
		#parallel case
		if abs(relDir.y) == 1:
			if (
				abs(relOrigin.y) > cls.height(transf)/2 and
				glmh.sign(relDir.y) != glmh.sign(relOrigin.y) and
				glm.length(relOriginXZ) < cls.radius(transf)
			):
				return origin + (abs(relOrigin.y) - cls.height(transf)/2) * direction
		else:
			#calculate intersect on infinite cylinder by looking for line-circle intersect on infinite cylinder
			relDirUnitXZ = glm.normalize(relDirXZ)
			tXZ = glm.dot(-relOriginXZ, relDirUnitXZ)
			yXZ = glm.length(relOriginXZ + tXZ * relDirUnitXZ)
			
			#check that ray doesnt miss cylinder
			if yXZ < cls.radius(transf):
				xXZ = glm.sqrt(cls.radius(transf) ** 2 - yXZ ** 2)
				dXZ = tXZ - xXZ
				
				#dXZ is the 2D distance along relDirUnitXZ to the cylinder, dXZ gets scaled into d, the 3d distance along relDir
				d = dXZ / glm.length(relDirXZ)
				iCyl = relOrigin + d * relDir
				
				#if on curved surface (origin outside and intersect within height)
				if tXZ > xXZ and abs(iCyl.y) <= cls.height(transf)/2:
					return origin + d * direction
				
				#if dir points down and intersect and origin both outside height, have to check flat surface
				if (
					relDir.y != 0 and
					glmh.sign(iCyl.y) != glmh.sign(relDir.y) and
					abs(iCyl.y + relOrigin.y) > cls.height(transf)
				):
					l = (glmh.sign(iCyl.y > 0)*cls.height(transf)/2 - relOrigin.y) / relDir.y
					if l > 0:
						if glm.length(relOriginXZ + l * relDirXZ) <= cls.radius(transf):
							return origin + l * direction
		
		return False
