from config import *
from Level.Core.Prop import Prop
from Level.Core.Index import Index
from Level.Core.Index import Obj

@attr.define
class Timer(Prop):
	cycle: float
	
	time: float = attr.field(default=0)#between 0 and 1
	deleteOnCycle: bool = attr.field(default=False)
	cycleFunc: collections.abc.Callable[[Obj, Index], None] = attr.field(default=None)
