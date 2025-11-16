from config import *
from Core.Props.BaseProp import BaseProp

@attr.define
class Field(BaseProp):
	keys: set = attr.field(default=attr.Factory(set))
	
	#setup: assert Coll ?