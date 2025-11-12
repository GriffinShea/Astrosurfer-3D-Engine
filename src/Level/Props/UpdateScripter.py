from config import *
from Level.Core.Prop import Prop
from Level.Core.Index import Index
from Level.Core.Index import Obj

@attr.define
class UpdateScripter(Prop):
	preupdate: collections.abc.Callable[[Obj, Index], None] = attr.field(default=None)
	interupdate: collections.abc.Callable[[Obj, Index], None] = attr.field(default=None)
	postupdate: collections.abc.Callable[[Obj, Index], None] = attr.field(default=None)
	