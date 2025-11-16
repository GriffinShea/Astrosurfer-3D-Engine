from config import *
from Core.Props.BaseProp import BaseProp

@attr.define
class PIDSteer(BaseProp):
	targetkey: str
	pGain: float
	iGain: float
	dGain: float
	turnSpeed: float
	i: glm.vec3 = attr.field(init=False, default=attr.Factory(glm.vec3))
	