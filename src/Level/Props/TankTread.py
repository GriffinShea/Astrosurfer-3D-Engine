from config import *
from Level.Core.Prop import Prop
from Level.Props.Coll import Coll

@attr.define
class TankTread(Prop):
	thrust: float
	moveSpeed: float
	turnSpeed: float
	
	#REVISIT: remove moveDirection just use associated Transf.foward() or whatever
	moveDirection: glm.vec3 = attr.field(init=False, default=attr.Factory(glm.vec3))
	turnDirection: int = attr.field(init=False, default=0)#between -1 and 1
	grounded: bool = attr.field(init=False, default=False)
	
	@classmethod
	def getGroundDetectorClosure(cls, tankkey):
		return lambda i, c: cls.groundDetectorClosure(i, c, tankkey)
	@staticmethod
	def groundDetectorClosure(index, collision, tankkey):
		(_, keyB, _, _, _) = collision
		if index.get(keyB)[Coll].isSolid():
			index.get(tankkey)[TankTread].grounded = True
		return
	