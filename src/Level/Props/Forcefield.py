from config import *
from Level.Core.Prop import Prop

@attr.define
class Forcefield(Prop):
	#force = power * (1 - pow(distance / radius, 2))
	power: float
	