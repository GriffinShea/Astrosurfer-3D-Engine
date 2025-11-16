from config import *
from Renderer import Renderer
from Core.Props.Physics.Rigidbody import Rigidbody

class rb:
	@staticmethod
	def warpTo(body, transf, pos):
		delta = pos - transf.cpos
		transf.translateRpos(delta)
		body.lpos = body.lpos + delta
		return
	@staticmethod
	def zeroVel(body, transf):
		body.lpos = transf.cpos
		return
	@staticmethod
	def spinTo(body, transf, ori):
		delta = glmh.quatDiff(ori, transf.cori)
		transf.rotateRori(delta)
		body.lori = glm.normalize(body.lori * delta)
		return
	@staticmethod
	def zeroWel(body, transf):
		body.lori = transf.cori
		return
	@staticmethod
	def matchInertia(body1, transf1, body2, transf2):
		dp = transf1.cpos - body1.lpos
		do = glmh.quatDiff(transf1.cori, body1.lori)
		body2.lpos = transf2.cpos - dp
		body2.lori = glmh.quatDiff(transf2.cori, do)
		return
	
	@classmethod
	def applyImpulse(cls, body, transf, impulse, contact):
		if not body.lockOri:
			rot = cls.calcWel(body, transf) + cls.momentify(body, transf, glm.cross(contact - transf.cpos, impulse))
			body.lori = glmh.quatAddRotVec(transf.cori, -rot * Renderer.dTime)
		body.lpos = transf.cpos - (cls.calcVel(body, transf) + impulse / body.mass) * Renderer.dTime
		return
	@staticmethod
	def calcVel(body, transf):
		return (transf.cpos - body.lpos) / Renderer.dTime
	@staticmethod
	def calcWel(body, transf):
		logDiff = glmh.quatLog(glmh.quatDiff(transf.cori, body.lori))
		return 2 * glm.vec3(logDiff.x, logDiff.y, logDiff.z) / Renderer.dTime
	@staticmethod
	def momentify(body, transf, vector):
		return transf.cori * ((vector * transf.cori) * body.invInertiaMat)