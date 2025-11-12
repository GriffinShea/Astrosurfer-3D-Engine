from config import *
from Level.Core.Prop import Prop

@attr.define
class Model(Prop):
	mesh: str
	castShadow: bool
	tesselated: bool = attr.field(default=False)
	