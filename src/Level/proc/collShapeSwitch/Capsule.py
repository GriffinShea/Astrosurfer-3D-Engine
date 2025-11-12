from config import *
from Level.Core.AABB import AABB

class Capsule:

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
		return "capsule"
	
	@classmethod
	def calcAABB(cls, transf):
		aabbShape = abs(cls.height(transf)*glmh.yBasis(transf.cori)) + cls.diameter(transf)
		return AABB.createAABB(transf.cpos, aabbShape)

	@classmethod
	def calcSupport(cls, transf, direction):
		yBasis = glmh.yBasis(transf.cori)
		return (
			transf.cpos
			+ yBasis * cls.height(transf) / 2 * -glmh.sign(-glm.dot(direction, yBasis))
			+ cls.radius(transf) * direction
		)
	
	@classmethod
	def castRay(cls, transf, origin, direction):
		relOrigin = (origin - transf.cpos) * transf.cori
		relOriginXZ = glm.vec2(relOrigin.x, relOrigin.z)
		
		relDir = direction * -transf.cori
		relDirXZ = glm.vec2(relDir.x, relDir.z)
		
		#parallel case
		if abs(relDir.y) == 1:
			if glmh.sign(relDir.y) != glmh.sign(relOrigin.y):
				x2D = glm.length(relOriginXZ)
				if x2D < cls.radius(transf):
					iY = cls.height(transf)/2 + glm.sqrt(cls.radius(transf) ** 2 - x2D ** 2)
					if abs(relOrigin.y) > iY:
						return origin + (abs(relOrigin.y) - iY) * direction
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
				
				#if intersect outside of height, have to check corrosponding sphere cap
				if abs(iCyl.y) > cls.height(transf) / 2:
					capPos = glm.vec3(0, glmh.sign(iCyl.y > 0) * cls.height(transf)/2, 0)
					t = glm.dot((capPos - relOrigin), relDir)
					y = glm.distance(capPos, relOrigin + t * relDir)
					if y < cls.radius(transf):
						x = glm.sqrt(cls.radius(transf) ** 2 - y ** 2)
						if t > x:
							return origin + (t - x) * direction
		
		return False
