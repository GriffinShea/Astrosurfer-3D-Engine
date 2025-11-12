from config import *

from Level.proc.lib import proc

from Level.Core.KDimTree import KDimTree
from Level.Core.AABB import AABB

from Level.Props.Transf import Transf
from Level.Props.Coll import Coll
from Level.Props.Field import Field

class CollTree:
	def __init__(self):
		self.staticTreeRoot = None
		return
	
	def calibrate(self, index):
		#generate a KDimTree for the static colliders
		self.staticTreeRoot = KDimTree.makeTree([
			(coll, transf, key)
			for (coll, transf, key)
			in index[Coll, Transf, "Key"]
			if coll.isStatic()
		])
		return
	
	def detectCollisions(self, index):
		#generate a KDimTree for the dynamic colliders
		dynamicColls = [
			(coll, transf, key)
			for (coll, transf, key)
			in index[Coll, Transf, "Key"]
			if not coll.isStatic()
		]
		dynamicTreeRoot = KDimTree.makeTree(dynamicColls)
		
		#sift through KDimTree to detect AABB intersections
		aabbCollisions = []
		for (coll, transf, key) in dynamicColls:
			if self.staticTreeRoot:
				aabbCollisions.extend(CollTree.sift(coll, transf, key, self.staticTreeRoot))
			if dynamicTreeRoot:
				aabbCollisions.extend(CollTree.sift(coll, transf, key, dynamicTreeRoot))
		
		#REVISIT: i think fields should go at collision resolution?
		#clear all fields
		for field in index[Field]:
			field.keys = set()
		
		#detect true collisions, dont check same pair twice
		collisions = []
		checkedSet = set()
		for (collA, transfA, keyA, collB, transfB, keyB) in aabbCollisions:
			if (
				keyA != keyB
				and keyA not in collB.ignoreKeys
				and keyB not in collA.ignoreKeys
				and keyB + keyA not in checkedSet
			):
				checkedSet.add(keyA + keyB)
				
				artefact = proc.checkCollision(
					collA, transfA, keyA,
					collB, transfB, keyB
				)
				if artefact:
					#REVISIT: wrong because many reasons, no index.get allowed here, this code just
					#	feels retarded, it belongs somewhere else
					if Field in index.get(keyA):
						index.get(keyA)[Field].keys.add(keyB)
					if Field in index.get(keyB):
						index.get(keyB)[Field].keys.add(keyA)
					
					collisions.append(artefact)
		
		return collisions
	
	@staticmethod
	def sift(coll, transf, key, node):
		#sift through tree to find AABB intersections
		if AABB.checkIntersection(coll.aabb, node.volume):
			if isinstance(node, KDimTree):
				#sift through children, combine into one list
				l = [CollTree.sift(coll, transf, key, child) for child in node.children]
				l = sum(l, [])
				return l
			else:
				#return [(collA, transfA, keyA, collB, transfB, keyB)]
				return [(coll, transf, key, node.coll, node.transf, node.key)]
		else:
			return []
		