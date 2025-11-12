from config import *

from Level.Props.Transf import Transf
from Level.Props.Rigidbody import Rigidbody
from Level.Props.PhysJoint import PhysJoint

def resolveConstraints(index):
	#for i in range(1):
	for i in range(RESOLVE_CONSTRAINTS_ITERATIONS):
		n = len(index[PhysJoint])
		indicies = [i for i in range(n)]
		random.shuffle(indicies)
		for i in indicies:
			joint = index[PhysJoint][i]
			body1 = index.get(joint.key1)[Rigidbody]
			transf1 = index.get(joint.key1)[Transf]
			body2 = index.get(joint.key2)[Rigidbody]
			transf2 = index.get(joint.key2)[Transf]
			
			solvePinConstraint(joint, body1, transf1, body2, transf2)
			solveAngleConstraint(joint, body1, transf1, body2, transf2)
	
	return
	
def solvePinConstraint(joint, body1, transf1, body2, transf2):
	#calculate the distance that needs to be fixed (if zero, just return)
	r1 = transf1.cori * joint.offset1
	r2 = transf2.cori * joint.offset2
	posDelta = transf1.cpos + r1 - transf2.cpos - r2
	realDist = glm.length(posDelta)
	if realDist <= joint.distance:		#if already pinned, no need to continue
		return
	norm = glm.normalize(posDelta)
	fixDelta = norm * (realDist - joint.distance)
	
	#calculate an impulse to correct the position
	impulse = -1 / (
		1 / body1.mass
		+ 1 / body2.mass
		+ glm.dot(norm, glmh.safeCross(Rigidbody.momentify(body1, transf1, glmh.safeCross(r1, norm)), r1))
		+ glm.dot(norm, glmh.safeCross(Rigidbody.momentify(body2, transf2, glmh.safeCross(r2, norm)), r2))
	) * joint.stiffness
	
	#apply impulse to each body's orientation
	oriDist1 = Rigidbody.momentify(body1, transf1, glmh.safeCross(r1, impulse * fixDelta))
	transf1.setRori(glmh.quatAddRotVec(transf1.cori, oriDist1))
	oriDist2 = Rigidbody.momentify(body2, transf2, glmh.safeCross(r2, -impulse * fixDelta))
	transf2.setRori(glmh.quatAddRotVec(transf2.cori, oriDist2))
	
	#apply impulse to each body's position
	transf1.translateRpos(impulse * fixDelta / body1.mass)
	transf2.translateRpos(-impulse * fixDelta / body2.mass)
	
	return

def solveAngleConstraint(joint, body1, transf1, body2, transf2):
	
	#REVISIT: strange behaviour when freedom is >= 180
	
	#aquire the euler angles between the ideal orientation and the current orientation
	relOri = glm.normalize(
		transf1.cori
		* glmh.quatDiff(joint.ori, transf2.cori)
	)
	angleDiff = glm.vec3(
		2 * glm.asin(relOri.x),
		2 * glm.asin(relOri.y),
		2 * glm.asin(relOri.z)
	) * transf1.cori
	
	#calculate the difference between the current euler angles and their respective limits
	correction = transf1.cori * glm.vec3(
		glmh.sign(angleDiff.x) * max(abs(angleDiff.x) - joint.freedom.x, 0),
		glmh.sign(angleDiff.y) * max(abs(angleDiff.y) - joint.freedom.y, 0),
		glmh.sign(angleDiff.z) * max(abs(angleDiff.z) - joint.freedom.z, 0)
	)
	
	#create a quaternion to rotate the current orientation back within the limits
	rx = glm.angleAxis(correction.x, -glmh.xUnit())
	ry = glm.angleAxis(correction.y, -glmh.yUnit())
	rz = glm.angleAxis(correction.z, -glmh.zUnit())
	rot = glm.normalize(rx * ry * rz)
	rotVec = glm.vec3(rot.x, rot.y, rot.z) * rot.w * 4#REVISIT: 4 == strength???
	
	#apply the rotation to each body's orientation
	oriDist1 = Rigidbody.momentify(body1, transf1, rotVec)
	transf1.setRori(glmh.quatAddRotVec(transf1.cori, oriDist1))
	oriDist2 = Rigidbody.momentify(body2, transf2, -rotVec)
	transf2.setRori(glmh.quatAddRotVec(transf2.cori, oriDist2))
	
	return
	