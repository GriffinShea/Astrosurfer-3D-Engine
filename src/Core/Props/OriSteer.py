from config import *
from Core.Props.BaseProp import BaseProp
from Core.Props.Transf import Transf

@attr.define
class OriSteer(BaseProp):
	targetKey: str
	turnSpeed: float
	allowRoll: bool
	
	relOri: glm.quat = attr.field(default=attr.Factory(glm.quat))
	
	@classmethod
	def setup(cls, obj):
		obj[Transf].noParentOri = True
		return
	