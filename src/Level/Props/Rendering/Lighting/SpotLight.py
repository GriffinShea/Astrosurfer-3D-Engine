from config import *
from Level.Core.Prop import Prop

@attr.define
class SpotLight(Prop):
	direction: glm.vec3
	cutoff: glm.vec2
	