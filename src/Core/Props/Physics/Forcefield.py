from config import *
from Core.Props.BaseProp import BaseProp

@attr.define
class Forcefield(BaseProp):
	#force = power * (1 - pow(distance / radius, 2))
	power: float
	