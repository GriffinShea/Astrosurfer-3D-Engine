from config import *

from Core.Props.Transf import Transf
from Core.Props.OriSteer import OriSteer
from Core.Props.Scripts import PreScript

from Core.Props.Graphics.Rend import Rend
from Core.Props.Graphics.Model import Model

class ArrowFactory:
	@classmethod
	def create(cls, index, key, size, targetkey):
		shaftkey = index.createObj(
			key+"_arrow_shaft",
			[
				Transf(
					glm.vec3(), glm.quat(), size * glm.vec3(0.5, 2, 0.5),
					parent=index.get(index.getSing("camerakey"))[Transf]
				),
				OriSteer(
					targetkey, 10,
					True, relOri=glm.angleAxis(-glm.pi()/2, glmh.xUnit())
				),
				PreScript(cls.fixArrowPos),
				Rend(True, "unLitTexture", {"texture": "eyeball", "uvScale": glm.vec2(1)}),
				Model("cylinder", False)
			]
		)
		shaftTransf = index.get(shaftkey)[Transf]
		index.createObj(
			key+"_arrow_tip",
			[
				Transf(
					glm.vec3(0, shaftTransf.scale.y, 0),
					glm.quat(),
					glm.vec3(shaftTransf.scale.x, shaftTransf.scale.y / 2, shaftTransf.scale.z),
					parent=index.get(shaftkey)[Transf]
				),
				Rend(True, "unLitTexture", {"texture": "eyeball", "uvScale": glm.vec2(1)}),
				Model("pyr", False)
			]
		)
		return
	@classmethod
	def fixArrowPos(cls, obj, index):
		torsoTransf = index.get(index.getSing("ragdollkeys")["torso"])[Transf]
		targetTransf = index.get(obj[OriSteer].targetKey)[Transf]
		v = targetTransf.cpos - torsoTransf.cpos
		v = glm.normalize(v) * 8
		obj[Transf].setRpos(glm.vec3(
			v.x,
			v.y,
			16
		))
		return
