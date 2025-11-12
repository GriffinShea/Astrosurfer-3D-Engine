from config import *
from Level.Core.Prop import Prop

@attr.define
class PIDSteer(Prop):
	targetkey: str
	pGain: float
	iGain: float
	dGain: float
	turnSpeed: float
	i: glm.vec3 = attr.field(init=False, default=attr.Factory(glm.vec3))
	