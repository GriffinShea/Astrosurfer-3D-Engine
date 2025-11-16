from config import *

from Core.Props.Transf import Transf
from Core.Props.Coll import Coll
from Core.Props.Physics.Rigidbody import Rigidbody
from Core.Props.Physics.PhysJoint import PhysJoint
from Core.Props.Scripts import PostScript

from Core.Props.Graphics.Rend import Rend
from Core.Props.Graphics.Model import Model
from Core.Props.Graphics.KeySegment import KeySegment

class ChainFactory:
	@classmethod
	def create(cls, singkey, index, pos, length, width, links, ignoreKeys=set()):
		linkkeys = []
		jointkeys = []
		
		index.setSing(singkey, [linkkeys, jointkeys])
		
		linkLength = length / links / 2
		incVec = glm.vec3(0, linkLength, 0)
		linksize = glm.vec3(width*4, length / links, width*4)
		p = pos + incVec
		linkkeys.append(index.createObj(
			singkey+"_link_0",
			[
				Transf(pos, glm.quat(), linksize),
				Coll(COLLCAPSULE, COLLRIGIDBODY, ignoreKeys=ignoreKeys),
				Rigidbody(10, 0.5, 0, 0),
				
				#Rend(True, "solidUnlitColour", {"colour": GREEN}),
				#Model("cylinder", False)
			]
		))
		
		for i in range(1, links):
			p = p + incVec * 2
			linkkeys.append(index.createObj(
				singkey+"_link_"+str(i),
				[
					Transf(pos, glm.quat(), linksize),
					Coll(
						COLLCAPSULE, COLLRIGIDBODY,
						tags=set(["chain"]), ignoreKeys=set(linkkeys).union(ignoreKeys)
					),
					Rigidbody(10, 0.5, 0, 0),
				
					#Rend(True, "solidUnlitColour", {"colour": GREEN}),
					# Model("cylinder", False)
				]
			))
			
			jointkeys.append(index.createObj(
				singkey+"_joint_"+str(i-1),
				[
					Transf(pos, glm.quat(), glm.vec3(width)),
					PostScript(cls.jointUpdate),
					PhysJoint(
						linkkeys[-2], linkkeys[-1],
						incVec, -incVec,
						glm.quat(), stiffness=0.75
					),
				
					Rend(True, "solidUnlitColour", {"colour": YELLOW}),
					Model("cylinder", False)
				]
			))
		
		return [linkkeys, jointkeys]
	
	@classmethod
	def jointUpdate(cls, obj, index):
		end1 = index.get(obj[PhysJoint].key1)
		end2 = index.get(obj[PhysJoint].key2)
		delta = end2[Transf].cpos - end1[Transf].cpos
		
		obj[Transf].scale.y = glm.length(delta)
		obj[Transf].setRpos(end1[Transf].cpos + delta / 2)
		obj[Transf].setRori(
			glm.normalize(
				glm.quatLookAt(
					glm.normalize(-delta),
					glmh.zUnit()
				) * glm.angleAxis(glm.pi()/2, glmh.xUnit())
			)
		)
		
		return