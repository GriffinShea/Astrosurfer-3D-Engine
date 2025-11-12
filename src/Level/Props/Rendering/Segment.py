from config import *
from Level.Core.Prop import Prop

@attr.define
class Segment(Prop):
	destination: glm.vec3
	