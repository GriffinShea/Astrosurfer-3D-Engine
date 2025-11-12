from config import *
from Level.Core.Prop import Prop

@attr.define
class Transf(Prop):
	rpos: glm.vec3
	rori: glm.quat
	scale: glm.vec3
	
	parent: str = attr.field(default=None)
	children: list = attr.field(default=attr.Factory(list))
	noParentOri: bool = attr.field(default=False)
	
	cpos: glm.vec3 = attr.field(init=False, default=attr.Factory(glm.vec3))
	cori: glm.quat = attr.field(init=False, default=attr.Factory(glm.quat))
	delete: bool = attr.field(init=False, default=False)
	
	@staticmethod
	def setup(obj):
		if obj[Transf].parent:
			obj[Transf].getParent().children.append(obj[Transf])
		
		obj[Transf].recalculateDescend()
		
		return
	
	def getParent(self):
		if not self.parent:
			print("WARNING: Transf "+"SOME_NAME"+" has no parent.")
		return self.parent
	
	#calculates cpos, cori and call on children
	def recalculateDescend(self):
		if self.parent:
			parentTransf = self.getParent()
			if self.noParentOri:
				self.cori = self.rori
			else:
				self.cori = glm.normalize(parentTransf.cori * self.rori)
			self.cpos = parentTransf.cpos + parentTransf.cori * self.rpos
			
		else:
			self.cori = self.rori
			self.cpos = self.rpos
		
		if glmh.isNanVec(self.cpos):
			raise ValueError("Transf cpos changed to NaN!")
		
		for child in self.children:
			child.recalculateDescend()
		return
	
	#set rpos and descend to children
	def setRpos(self, newPos):
		self.rpos = newPos
		self.recalculateDescend()
		return
	#translate rpos
	def translateRpos(self, translation):
		self.setRpos(translation + self.rpos)
		return
	
	#set rori and descend to children
	def setRori(self, newOri):
		self.rori = newOri
		self.recalculateDescend()
		return
	#set rori and descend to children
	def rotateRori(self, rotation):
		self.setRori(glm.normalize(self.rori * rotation))
		return
		
	def setScale(self, newScale):
		self.scale = newScale
		return
		
	def calcMatrix(self):
		return glmh.transfMat(self.cpos, self.cori, self.scale)
	
	def editorDescribe(self):
		string = "\tTransf:"
		
		string += f"\n\t\trpos:\t\t({self.rpos.x:+8.2f} , {self.rpos.y:+8.2f} , {self.rpos.z:+8.2f})"
		string += f"\n\t\tcpos:\t\t({self.cpos.x:+8.2f} , {self.cpos.y:+8.2f} , {self.cpos.z:+8.2f})"
		
		string += f"\n\n\t\trori:\t({self.rori.x:+.4f} , {self.rori.y:+.4f} , {self.rori.z:+.4f} , {self.rori.w:+.4f})"
		string += f"\n\t\tcori:\t({self.cori.x:+.4f} , {self.cori.y:+.4f} , {self.cori.z:+.4f} , {self.cori.w:+.4f})"
		
		string += f"\n\n\t\tscale:\t\t({self.scale.x:+8.2f} , {self.scale.y:+8.2f} , {self.scale.z:+8.2f})"
		
		string += "\n"
		string += "\n\t\thas parent?:\t\t"+("YES" if self.parent else "NO")
		string += "\n\t\tnoParentOri:\t"+str(self.noParentOri)
		string += "\n\t\tchildren count:\t"+str(len([child for child in self.children]))
		string += "\n\t\tdelete:\t\t\t"+str(self.delete)
		string += "\n"
		
		return string
	