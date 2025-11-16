from config import *
from Core.Props.BaseProp import BaseProp

@attr.define
class Model(BaseProp):
	mesh: str
	castShadow: bool
	tesselated: bool = attr.field(default=False)
	