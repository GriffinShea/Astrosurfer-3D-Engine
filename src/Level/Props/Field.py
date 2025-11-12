from config import *
from Level.Core.Prop import Prop

@attr.define
class Field(Prop):
	keys: set = attr.field(default=attr.Factory(set))
	
	#setup: assert Coll ?