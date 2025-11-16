from config import *
from Core.Props.BaseProp import BaseProp
from Core.Index import Index
from Core.Index import Obj

@attr.define
class Script(BaseProp):
	#run: collections.abc.Callable[[Obj, Index], None] = attr.field(default=None)
	run: collections.abc.Callable[[Obj, Index], None]

@attr.define
class PreScript(Script):
	pass
	
@attr.define
class InterScript(Script):
	pass
	
@attr.define
class PostScript(Script):
	pass
	
@attr.define
class DeleteScript(Script):
	pass
	