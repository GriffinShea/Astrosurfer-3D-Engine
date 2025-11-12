from config import *
from Level.Core.Prop import Prop

@attr.define
class DomJoint(Prop):
	dom: str
	sub: str
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
	