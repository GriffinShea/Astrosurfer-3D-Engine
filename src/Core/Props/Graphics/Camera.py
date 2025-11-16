from config import *
from Core.Props.BaseProp import BaseProp

@attr.define
class Camera(BaseProp):
	fov: float
	