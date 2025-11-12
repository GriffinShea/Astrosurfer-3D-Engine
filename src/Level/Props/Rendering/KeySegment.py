from config import *
from Level.Core.Prop import Prop

@attr.define
class KeySegment(Prop):
	start: str
	end: str
	