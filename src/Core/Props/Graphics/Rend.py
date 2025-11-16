from config import *
from Core.Props.BaseProp import BaseProp

@attr.define
class Rend(BaseProp):
	visible: bool
	shader: str
	uniformDict: dict
	