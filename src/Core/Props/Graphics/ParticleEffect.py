from config import *
from Core.Props.BaseProp import BaseProp

from Core.Props.Transf import Transf
from Core.Props.Timer import Timer
from Core.Props.Graphics.Rend import Rend

@attr.define
class ParticleEffect(BaseProp):
	count: int
	seed: float = attr.field(default=attr.Factory(random.random))
	pointSize: int = attr.field(default=0)	#0 --> textured particles
	
	@staticmethod
	def setup(obj):
		obj[Rend].uniformDict["seed"] = obj[ParticleEffect].seed
		return
	