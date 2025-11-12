from config import *
from Level.Core.Prop import Prop

@attr.define
class Light(Prop):
	colour: glm.vec3
	intensity: float
	