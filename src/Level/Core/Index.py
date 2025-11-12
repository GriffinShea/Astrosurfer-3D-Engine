from config import *
from Level.Props.Transf import Transf

class Obj:
	def __init__(self, key, propsDict):
		self.key = key
		self.propsDict = propsDict
		return
	
	def __contains__(self, label):
		return label in self.propsDict
	
	def __getitem__(self, propLabel):
		if propLabel in self.propsDict:
			return self.propsDict[propLabel]
		else:
			raise KeyError("Obj with key " + self.key + " has no " + str(propLabel))
	
	def propsToStr(self):
		#doesnt print Key
		return "".join([str(prop).split(".")[-1][:-2] + "\n" for prop in self.propsDict.keys()][1:])

class Index:
	def __init__(self):
		self.nextKey = 0
		self.objs = {}					#key --> (label --> prop)
		self.keysByLabel = {}			#label --> set(keys)
		self.keysByLabel["Key"] = set()
		self.sings = {}
		return
	
	def __contains__(self, key):
		return key in self.objs
	
	def objHasProp(self, key, label):
		return label in self.objs[key]
	
	def __getitem__(self, labels):
		#labels[0] is the primary key, all its objs must have the prop labels as dependencies
		if type(labels) == tuple and labels[0] in self.keysByLabel:
			keys = self.keysByLabel[labels[0]]
			try:
				return [tuple([self.objs[key][label] for label in labels]) for key in keys]
			except KeyError:
				raise KeyError(
					"Some "
					+ str(labels[0])
					+ " are missing other dependent properties: "
					+ str(labels[1:])
				)
		else:
			try:
				return [
					self.objs[key][labels]
					for key 
					in self.keysByLabel[labels]
				]
			except KeyError:
				return []
	
	def match(self, *labels):
		if self.prod([label in self.keysByLabel for label in labels]):
			return [
				tuple([self.objs[key][label] for label in labels])
				for key
				in self.keysByLabel[labels[0]].intersection(
					*[self.keysByLabel[label] for label in labels[1:]]
				)
			]
		else:
			return []
	
	def prod(self, args):
		if len(args) == 1:
			return args[0]
		if len(args) == 2:
			return args[0] * args[1]
		else:
			return args[0] * self.prod(args[1:])
	
	def makeObj(self, key):
		if key in self.objs:
			if not DEBUG_SUPPRESS_WARNINGS:
				print("WARNING (Index): objkey "+key+" already assigned.")
			newkey = key
			i = 0
			while newkey in self.objs:
				i -= 1
				newkey = key+str(i)
			key = newkey
			if not DEBUG_SUPPRESS_WARNINGS:
				print("............assigning "+newkey+" instead.")
		
		self.objs[key] = {"Key": key}
		self.keysByLabel["Key"].add(key)
		return key
	
	def createObj(self, key, props):
		objkey = self.makeObj(key)
		for prop in props:
			self.addProp(objkey, prop)
		return objkey
	
	def get(self, key):
		try:
			return Obj(key, self.objs[key])
		except KeyError:
			print("WARNING (Index): objkey ", key, " not assigned (or None). Returning None.")
			return None
	
	#REVISIT: very inefficient
	def findObjs(self, key):
		foundObjs = []
		for objkey in self.objs.keys():
			if key in objkey:
				foundObjs.append(Obj(objkey, self.objs[objkey]))
		return foundObjs
	
	def deleteObj(self, key):
		obj = self.objs[key]
		#REVISIT: do we need this?
		#if Transf in obj:
		#	for child in obj[Transf].children:
		#		self.deleteObj(child.key)
		for label in obj.keys():
			self.keysByLabel[label].discard(key)
		#print(key, "deleted from index.")
		del self.objs[key]
		return key
	
	def addProp(self, key, prop):
		obj = self.objs[key]
		
		if type(prop) in obj:
			raise ValueError(str(type(prop))+" property already in objkey "+key+".")
		
		if type(prop) not in self.keysByLabel:
			self.keysByLabel[type(prop)] = set()
		
		obj[type(prop)] = prop
		self.keysByLabel[type(prop)].add(key)
		type(prop).setup(self.get(key))
		return
	
	def deleteProp(self, key, label):
		self.keysByLabel[label].discard(key)
		del self.objs[key][label]
		return
	
	def getSing(self, name):
		if name not in self.sings:
			raise ValueError(name+" not in sings.")
		return self.sings[name]
	
	def setSing(self, name, sing):
		self.sings[name] = sing
		return
		