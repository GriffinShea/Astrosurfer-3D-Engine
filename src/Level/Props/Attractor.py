from config import *
from Level.Core.Prop import Prop

@attr.define
class Attractor(Prop):
	#force = power / pow(distance, taper) if distance < range else 0
	targetkey: str
	power: float
	taper: float
	range: float = attr.field(default=glmh.INF)
	