from config import *
from Core.Props.BaseProp import BaseProp

@attr.define
class Attractor(BaseProp):
	#force = power / pow(distance, taper) if distance < range else 0
	targetkey: str
	power: float
	taper: float
	range: float = attr.field(default=glmh.INF)
	