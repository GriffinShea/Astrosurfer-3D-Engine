from config import *
from Core.Props.BaseProp import BaseProp

@attr.define
class KeySegment(BaseProp):
	start: str
	end: str
	