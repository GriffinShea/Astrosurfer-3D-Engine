from config import *

from Core.Props.BaseProp import BaseProp
from Core.Index import Index

#REVISIT: consider how to remove this from Coll (props shouldnt access to systems)
from Core.Systems.Collisions.AABB import AABB

@attr.define
class Coll(BaseProp):
	shape: int
	physType: int
	
	tags: set = attr.field(default=attr.Factory(set))
	ignoreKeys: set = attr.field(default=attr.Factory(set))#REVISIT: replace with ignoreTags?
	
	aabb: AABB = attr.field(default=AABB.createDummy())
	
	#REVISIT: these should be abstract functions? idk. actually. idk...
	precollide: collections.abc.Callable[[Index, tuple], None] = attr.field(default=None)
	postcollide: collections.abc.Callable[[Index, tuple], None] = attr.field(default=None)
	
	def isStatic(self):
		return self.physType == COLLFLAG or self.physType == COLLTERRAIN
	def isSolid(self):
		return not (self.physType == COLLFLAG or self.physType == COLLGHOST)
	
	@classmethod
	def setup(cls, obj):
		assert obj[Coll].shape in range(6)		#see constants.py
		assert obj[Coll].physType in range(5)	#see constants.py
		return
	