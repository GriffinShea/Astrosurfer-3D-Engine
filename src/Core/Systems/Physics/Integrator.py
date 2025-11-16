from config import *

from Core.Systems.Physics.rb import rb

from Core.Props.Timer import Timer
from Core.Props.Transf import Transf
from Core.Props.Field import Field
from Core.Props.OriSteer import OriSteer

from Core.Props.Physics.Rigidbody import Rigidbody
from Core.Props.Physics.TankTread import TankTread
from Core.Props.Physics.PIDSteer import PIDSteer
from Core.Props.Physics.Attractor import Attractor
from Core.Props.Physics.Forcefield import Forcefield
from Core.Props.Physics.Jet import Jet

class Integrator:
	@staticmethod
	def run(index, dTime):
		
		#nonphysical dynamics
		oriSteerUpdate(index, dTime)
		#rigidbody dynamics (applies forces)
		pidSteerUpdate(index, dTime)
		tankTreadUpdate(index, dTime)
		attractorUpdate(index)
		forcefieldUpdate(index)
		jetUpdate(index)
		
		rigidbodyUpdate(index, dTime)
		return

def oriSteerUpdate(index, dTime):
	#update OriSteer (parallel) (pull out targetKey)
	for (steer, transf) in index[OriSteer, Transf]:
		toObj = glm.normalize(index.get(steer.targetKey)[Transf].cpos - transf.cpos)
		
		if not steer.allowRoll and steer.turnSpeed:
			#REVISIT: doesnt incorporate steer.turnSpeed
			#REVISIT: doesnt incorporate steer.relOri
			transf.setRori(glm.quatLookAt(-toObj, glmh.yUnit()))
		else:
			relToObj = toObj * -transf.cori * steer.relOri

			yaw = relToObj.x * steer.turnSpeed * dTime
			yawRot = glm.angleAxis(yaw, glmh.yUnit())
			pitch = relToObj.y * steer.turnSpeed * dTime
			pitchRot = glm.angleAxis(pitch, -glmh.xUnit())
			
			newOri = transf.cori * yawRot * pitchRot
			#newOri.z = 0
			if not glmh.isNanVec(newOri):
				transf.setRori(glm.normalize(newOri))
	return

def pidSteerUpdate(index, dTime):
	#update PIDSteer (parallel) (pull out targetKey)
	for (steer, transf, body) in index[PIDSteer, Transf, Rigidbody]:
		toDest = glm.normalize(index.get(steer.targetkey)[Transf].cpos - transf.cpos)
		rocketDir = glmh.yBasis(transf.cori)
		
		error = (glm.dot(toDest, rocketDir) - 1) / -2
		errorVec = error * glm.cross(rocketDir, toDest)
		if glm.any(glm.isnan(toDest)):
			errorVec = -rb.calcWel(body, transf)
		
		p = steer.pGain * errorVec
		
		steer.i += steer.iGain * errorVec * dTime
		
		d = steer.dGain * -rb.calcWel(body, transf)
		
		body.torques += (p + steer.i + d) * body.mass * steer.turnSpeed
	
	return

def tankTreadUpdate(index, dTime):
	#update tank controllers (parallel)
	for (tank, transf, body) in index[TankTread, Transf, Rigidbody]:
		if tank.grounded:
			#add force in tank moveDirection
			forceMagnitude = tank.thrust * body.mass
			absoluteDirection = transf.cori * tank.moveDirection
			body.forces += forceMagnitude * absoluteDirection
			
			#slow to moveSpeed if speed exceeds
			vel = rb.calcVel(body, transf)
			speed = glm.length(vel)
			if (speed > 0 and glmh.isZeroVec(absoluteDirection)) or speed > tank.moveSpeed:
				scaledSpeed = speed * body.mass / dTime
				resistance = min(forceMagnitude, scaledSpeed) * glm.normalize(-vel)
				body.forces += resistance
			
			#turn (not using torque) (meaning it induces a torque actually?)
			#REVISIT: why not using torque?
			rot = glm.angleAxis(tank.turnDirection * tank.turnSpeed * dTime, glmh.yUnit())
			transf.rotateRori(rot)
			body.lori = glm.normalize(body.lori * rot)
		
		tank.grounded = False
		
	return

def attractorUpdate(index):
	for (attractor, body, transf) in index[Attractor, Rigidbody, Transf]:
		if attractor.targetkey:
			targetPos = index.get(attractor.targetkey)[Transf].cpos
			delta = targetPos - transf.cpos
			distance = glm.length(delta)
			if distance > 0:
				force = attractor.power / pow(distance, attractor.taper) if distance < attractor.range else 0
				body.forces += force * delta * body.mass
	
	return

def forcefieldUpdate(index):
	for (forcefield, field, transf) in index[Forcefield, Field, Transf]:
		for key in field.keys:
			if Rigidbody in index.get(key):
				body = index.get(key)[Rigidbody]
				targetPos = index.get(key)[Transf].cpos
				delta = targetPos - transf.cpos
				distance = glm.length(delta)
				norm = glm.normalize(delta)
				radius = transf.scale.x / 2	#i.e. sphere radius
				force = forcefield.power * (1 - pow(distance / radius, 2))
				body.forces += force * norm
	
	return

def jetUpdate(index):
	for (jet, body, transf) in index[Jet, Rigidbody, Transf]:
		body.forces += transf.cori * jet.direction * jet.force
	return

def rigidbodyUpdate(index, dTime):
	fluidFriction = 1 - dTime * FLUID_FRICTION
	dTime2 = dTime ** 2
	
	#update rigidbodies (parallel)
	for (body, transf) in index[Rigidbody, Transf]:
		#add force of gravity, if necesssary
		body.forces += body.suffersGravity * GRAVITY * -glmh.yUnit() * body.mass
		
		#integrate forces, linear momentum, apply to position
		accel = body.forces / body.mass
		posDelta = (transf.cpos - body.lpos) * fluidFriction
		posDelta += accel * dTime2
		body.lpos = transf.cpos
		transf.translateRpos(posDelta)
		body.forces = glm.vec3()
		
		#if orientation not locked, integrate torques, angular velocity, apply to orientation
		if not body.lockOri:
			alpha = rb.momentify(body, transf, body.torques)
			logDiff = glmh.quatLog(glmh.quatDiff(transf.cori, body.lori))
			oriDelta = 2 * glm.vec3(logDiff.x, logDiff.y, logDiff.z) * fluidFriction
			oriDelta += alpha * dTime2
			body.lori = transf.cori
			#REVISIT: doesnt rotate root which infertilates Rigidbody
			transf.setRori(glmh.quatAddRotVec(transf.cori, oriDelta))
			body.torques = glm.vec3()
	return
	