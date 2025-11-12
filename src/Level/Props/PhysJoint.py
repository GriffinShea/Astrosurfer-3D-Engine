from config import *
from Level.Core.Prop import Prop

@attr.define
class PhysJoint(Prop):
	key1: str
	key2: str
	offset1: glm.vec3
	offset2: glm.vec3
	ori: glm.quat
	
	distance: float = attr.field(default=0)
	stiffness: float = attr.field(default=1)
	freedom: glm.vec3 = attr.field(default=attr.Factory(glm.vec3))
	
	@staticmethod
	def setup(obj):
		obj[PhysJoint].freedom = glm.radians(obj[PhysJoint].freedom)
		return
	
	#REVISIT this and setup in OriSteer and Attractor:
	#def setup(obj, index):
		#obj[PhysJoint].freedom = glm.radians(obj[PhysJoint].freedom)
		#assert key1 in index
		#assert Rigidbody in index.get(key1)
		#assert key2 in index
		#assert Rigidbody in index.get(key2)
		#return