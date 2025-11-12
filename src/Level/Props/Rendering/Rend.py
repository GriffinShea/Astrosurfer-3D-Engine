from config import *
from Level.Core.Prop import Prop

@attr.define
class Rend(Prop):
	visible: bool
	shader: str
	uniformDict: dict
	