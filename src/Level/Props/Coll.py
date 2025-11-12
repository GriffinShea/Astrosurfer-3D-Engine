from config import *

from Level.Core.Prop import Prop
from Level.Core.AABB import AABB
from Level.Core.Index import Index
from Level.Props.Transf import Transf
from Level.proc.collShapeSwitch.collShapeSwitch import collShapeSwitch

@attr.define
class Coll(Prop):
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
	
	#REVISIT: move these
	@staticmethod
	def calcAABB(coll, transf):
		return collShapeSwitch(coll.shape).calcAABB(transf)
	@staticmethod
	def calcSupport(coll, transf, direction):
		return collShapeSwitch(coll.shape).calcSupport(transf, direction)
	
	"""
	def getDebugMeshName(self):
		return collShapeSwitch(self.shape).getDebugMeshName()
	
	def editorDescribe(self):
		shapeStr = ["sphere", "capsule", "cylinder", "box", "plane", "ray"][self.shape]
		physTypeStr = ["flag", "terrain", "ghost", "rigidbody"][self.physType]
		
		string = "\tColl:"
		string += "\n\t\tshape:\t\t\t"+shapeStr
		string += "\n\t\tphysType:\t\t"+physTypeStr
		string += "\n\t\tprecollide?:\t"+str(bool(self.precollide))
		string += "\n\t\tpostcollide?:\t"+str(bool(self.postcollide))
		string += "\n"
		
		return string
	"""
	