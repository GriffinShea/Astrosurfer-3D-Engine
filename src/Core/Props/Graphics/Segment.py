from config import *
from Core.Props.BaseProp import BaseProp

@attr.define
class Segment(BaseProp):
	destination: glm.vec3
	