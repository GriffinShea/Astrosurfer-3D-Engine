from config import *
from Level.proc.rb import rb

from Level.Props.Transf import Transf
from Level.Props.Coll import Coll
from Level.Props.Rigidbody import Rigidbody

def resolveCollisions(index, collisions):
	for collision in collisions:
		(keyA, keyB, contactA, contactB, sepvec) = collision
		
		collA = index.get(keyA)[Coll]
		collB = index.get(keyB)[Coll]
		
		#swap A and B if physType wrong to reduce number of cases
		if collA.physType > collB.physType:
			tempKey, tempContact = keyA, contactA
			keyA, contactA = keyB, contactB
			keyB, contactB = tempKey, tempContact
			sepvec = -sepvec
			collA = index.get(keyA)[Coll]
			collB = index.get(keyB)[Coll]
		
		#terrain-rigidbody collision
		if collA.physType == COLLTERRAIN or collA.physType == COLLSOLID:
			if collB.physType == COLLRIGIDBODY:
				collideRigidbodyTerrain(
					index.get(keyB)[Rigidbody], index.get(keyB)[Transf],
					sepvec, contactB
				)
		#rigidbody-rigidbody collision
		elif collA.physType == COLLRIGIDBODY:
			if collB.physType == COLLRIGIDBODY:
				collideRigidbodyRigidbody(
					index.get(keyA)[Rigidbody], index.get(keyB)[Rigidbody],
					index.get(keyA)[Transf], index.get(keyB)[Transf],
					contactA, contactB, sepvec
				)
	
	return

def collideRigidbodyTerrain(body, transf, sep, contact):
	#move rigidbody away from static terrain
	transf.translateRpos(sep)
	body.lpos = body.lpos + sep
	
	#calculate velocity
	r = contact - transf.cpos
	vel = Rigidbody.calcVel(body, transf) + glm.cross(Rigidbody.calcWel(body, transf), r)
	
	#calculate collision normal impulse
	norm = glm.normalize(sep)
	imp = -glm.dot(vel, norm) * (1 + body.coeffRest)
	imp /= sum([
		1 / body.mass,
		glm.dot(norm, glm.cross(Rigidbody.momentify(body, transf, glm.cross(r, norm)), r)),
	])
	normalImpulse = norm * imp
	
	#calculate friction impulse
	frictionImpulse = calcFrictionImpulse(vel, norm, imp, body)
	
	#REVISIT: cheeky convergence condition, replace with manifolds?
	convMod = glm.min(1, glm.length(normalImpulse + frictionImpulse) / body.mass)
	
	#apply both impulses to the rigidbody
	rb.applyImpulse(body, transf, normalImpulse + frictionImpulse, transf.cpos + r * convMod)
	
	return

def collideRigidbodyRigidbody(bodyA, bodyB, transfA, transfB, contactA, contactB, sep):
	#move rigidbodies away from eachother
	sA = bodyB.mass / (bodyA.mass + bodyB.mass)
	offsetA = sep * sA
	transfA.translateRpos(-offsetA)
	bodyA.lpos = bodyA.lpos - offsetA
	sB = bodyA.mass / (bodyA.mass + bodyB.mass)
	offsetB = sep * sB
	transfB.translateRpos(offsetB)
	bodyB.lpos = bodyB.lpos + offsetB
	
	#calculate relative velocity
	rA = contactA - transfA.cpos
	velA = Rigidbody.calcVel(bodyA, transfA) + glm.cross(Rigidbody.calcWel(bodyA, transfA), rA)
	rB = contactB - transfB.cpos
	velB = Rigidbody.calcVel(bodyB, transfB) + glm.cross(Rigidbody.calcWel(bodyB, transfB), rB)
	vel = velA - velB
	
	#calculate collision normal impulse for each rigidbody
	norm = glm.normalize(sep)
	epsilon = glmh.mean(bodyA.coeffRest, bodyB.coeffRest)
	imp = -glm.dot(vel, norm) * (1 + epsilon)
	imp /= sum([
		1 / bodyA.mass,
		glm.dot(norm, glm.cross(Rigidbody.momentify(bodyA, transfA, glm.cross(rA, norm)), rA)),
		1 / bodyB.mass,
		glm.dot(norm, glm.cross(Rigidbody.momentify(bodyB, transfB, glm.cross(rB, norm)), rB)),
	])
	normalImpulse = norm * imp
	
	#calculate friction impulse for each rigidbody
	frictionImpulseA = calcFrictionImpulse(vel, norm, imp, bodyA)
	frictionImpulseB = calcFrictionImpulse(-vel, -norm, -imp, bodyB)
	
	#calculate the total impulse for each rigidbody
	impulseA = (normalImpulse + frictionImpulseA) * sA
	impulseB = -(normalImpulse - frictionImpulseB) * sB
	
	#REVISIT: cheeky convergence condition, replace with manifolds?
	convMod = glm.min(1,glm.min(glm.length(impulseA),glm.length(impulseB))/(bodyA.mass+bodyB.mass))
	
	#apply impulses to each rigidbody
	rb.applyImpulse(bodyA, transfA, impulseA, transfA.cpos + rA * convMod)
	rb.applyImpulse(bodyB, transfB, impulseB, transfB.cpos + rB * convMod)
	return

def calcFrictionImpulse(vel, norm, imp, body):
	#calculate friction impulse
	#source: https://en.wikipedia.org/wiki/Collision_response#Impulse-based_friction_model
	#except, I use (phi, mew) = (atan(mewS), mewK)
	
	tangent = glm.normalize(vel - glm.dot(vel, norm) * norm)
	tangent = glm.vec3() if glmh.isNanVec(tangent) else tangent
	tangentMomentum = body.mass * glm.dot(vel, tangent)
	if (
		abs(imp) > 0 and
		glm.atan(tangentMomentum / imp) <= body.phi
	):
		frictionImpulse = -tangentMomentum * tangent
	else:
		frictionImpulse = -body.mew * imp * tangent
	
	return frictionImpulse
	