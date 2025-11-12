from config import *
from Level.Core.Prop import Prop

@attr.define
class Camera(Prop):
	fov: float
	