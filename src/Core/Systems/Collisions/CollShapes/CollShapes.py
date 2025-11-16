from config import *

from Core.Systems.Collisions.CollShapes.Sphere import Sphere
from Core.Systems.Collisions.CollShapes.Capsule import Capsule
from Core.Systems.Collisions.CollShapes.Cylinder import Cylinder
from Core.Systems.Collisions.CollShapes.Box import Box
from Core.Systems.Collisions.CollShapes.Ray import Ray

class CollShapes:
	COLLSHAPESWITCH = {
		COLLSPHERE: Sphere,
		COLLCAPSULE: Capsule,
		COLLCYLINDER: Cylinder,
		COLLBOX: Box,
		COLLRAY: Ray
	}
	
	@classmethod
	def calcSupport(cls, coll, transf, direction):
		return cls.COLLSHAPESWITCH[coll.shape].calcSupport(transf, direction)
	
	@classmethod
	def calcAABB(cls, coll, transf):
		return cls.COLLSHAPESWITCH[coll.shape].calcAABB(transf)
	