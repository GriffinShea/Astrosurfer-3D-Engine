from config import *
from Core.Props.BaseProp import BaseProp

@attr.define
class Jet(BaseProp):
	direction: glm.vec3
	force: float
	