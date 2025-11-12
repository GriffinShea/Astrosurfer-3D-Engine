from config import *
from Level.Core.Prop import Prop

from Level.Props.Transf import Transf
from Level.Props.Timer import Timer
from Level.Props.Rendering.Rend import Rend

@attr.define
class ParticleEffect(Prop):
	count: int
	seed: float = attr.field(default=attr.Factory(random.random))
	pointSize: int = attr.field(default=0)	#0 --> textured particles
	
	@staticmethod
	def setup(obj):
		obj[Rend].uniformDict["seed"] = obj[ParticleEffect].seed
		return
	