from config import *
from Level.Core.Prop import Prop

@attr.define
class Jet(Prop):
	direction: glm.vec3
	force: float
	