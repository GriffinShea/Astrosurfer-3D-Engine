from config import *
from Renderer import Renderer
from Level.Props.Rigidbody import Rigidbody

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
	
	@staticmethod
	def applyImpulse(body, transf, impulse, contact):
		if not body.lockOri:
			rot = Rigidbody.calcWel(body, transf) + Rigidbody.momentify(body, transf, glm.cross(contact - transf.cpos, impulse))
			body.lori = glmh.quatAddRotVec(transf.cori, -rot * Renderer.dTime)
		body.lpos = transf.cpos - (Rigidbody.calcVel(body, transf) + impulse / body.mass) * Renderer.dTime
		return
	