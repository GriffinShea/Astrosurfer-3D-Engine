from config import *
from Core.Props.BaseProp import BaseProp

#REVISIT: should these inherit? works for Scripts

@attr.define
class Light(BaseProp):
	colour: glm.vec3
	intensity: float
	
@attr.define
class PointLight(BaseProp):
	pass
	
@attr.define
class DirLight(BaseProp):
	shadowRange: float
	distance: float
	
@attr.define
class SpotLight(BaseProp):
	direction: glm.vec3
	cutoff: glm.vec2
	