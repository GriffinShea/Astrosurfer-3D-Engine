from config import *
from Core.Props.BaseProp import BaseProp
from Core.Index import Index
from Core.Index import Obj

@attr.define
class Timer(BaseProp):
	cycle: float
	
	time: float = attr.field(default=0)#between 0 and 1
	click: bool = attr.field(default=False)
	deleteOnCycle: bool = attr.field(default=False)
