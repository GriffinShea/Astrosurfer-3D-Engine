from config import *

class AABB:
	@classmethod
	def createAABB(cls, pos, shape):
		bounds = (
			(pos.x - shape.x/2, pos.x + shape.x/2),
			(pos.y - shape.y/2, pos.y + shape.y/2),
			(pos.z - shape.z/2, pos.z + shape.z/2)
		)
		return cls(bounds)
	
	@classmethod
	def createDummy(cls):
		bounds = (
			(0, 0),
			(0, 0),
			(0, 0)
		)
		return cls(bounds)
	
	def __init__(self, bounds):
		self.bounds = bounds
		return
	
	def getPosShape(self):
		shape = glm.vec3(
			self.bounds[0][1] - self.bounds[0][0],
			self.bounds[1][1] - self.bounds[1][0],
			self.bounds[2][1] - self.bounds[2][0]
		)
		pos = glm.vec3(
			self.bounds[0][0] + shape.x/2,
			self.bounds[1][0] + shape.y/2,
			self.bounds[2][0] + shape.z/2
		)
		return pos, shape
	
	@staticmethod
	def checkIntersection(a, b):
		return not (
			a.bounds[0][1] < b.bounds[0][0] or
			a.bounds[0][0] > b.bounds[0][1] or
			a.bounds[1][1] < b.bounds[1][0] or
			a.bounds[1][0] > b.bounds[1][1] or
			a.bounds[2][1] < b.bounds[2][0] or
			a.bounds[2][0] > b.bounds[2][1]
		)
		
	@classmethod
	def union(cls, a, b):
		bounds = [
			[
				min(a.bounds[0][0], b.bounds[0][0]),
				max(a.bounds[0][1], b.bounds[0][1])
			],
			[
				min(a.bounds[1][0], b.bounds[1][0]),
				max(a.bounds[1][1], b.bounds[1][1])
			],
			[
				min(a.bounds[2][0], b.bounds[2][0]),
				max(a.bounds[2][1], b.bounds[2][1])
			]
		]
		return cls(bounds)
