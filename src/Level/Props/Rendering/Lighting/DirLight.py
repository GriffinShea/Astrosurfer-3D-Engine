from config import *
from Level.Core.Prop import Prop

@attr.define
class DirLight(Prop):
	shadowRange: float
	distance: float
	