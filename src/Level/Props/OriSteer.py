from config import *
from Level.Core.Prop import Prop
from Level.Props.Transf import Transf

@attr.define
class OriSteer(Prop):
	targetKey: str
	turnSpeed: float
	allowRoll: bool
	
	relOri: glm.quat = attr.field(default=attr.Factory(glm.quat))
	
	@classmethod
	def setup(cls, obj):
		obj[Transf].noParentOri = True
		return
	