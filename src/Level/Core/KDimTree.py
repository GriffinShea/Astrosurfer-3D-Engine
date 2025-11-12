from config import *
from Level.Core.AABB import AABB
from Level.Props.Coll import Coll

class KDimLeaf:
	def __init__(self, coll, transf, key):
		self.key = key
		self.coll = coll
		self.transf = transf
		self.volume = self.coll.aabb
		return

class KDimTree:
	@staticmethod
	def makeTree(collData):
		if not collData:
			return None
		
		#calculate AABBs
		for (coll, transf, key) in collData:
			coll.aabb = Coll.calcAABB(coll, transf)
		
		#turn data into leafs
		leafs = [KDimLeaf(coll, transf, key) for (coll, transf, key) in collData]
		
		return KDimTree(leafs, 0)
	
	def __init__(self, leafs, height):
		#if only one, leaf node
		if len(leafs) == 1:
			children = leafs
			volume = AABB(children[0].volume.bounds)
		
		#if more than one leaf, split into two trees at median position in alternating dimension,
		#nodes' volume is the union of its childrens'
		else:
			sortedLeafs = KDimTree.sortLeafs(leafs, height % 3)
			medianIndex = len(sortedLeafs) // 2
			children = (
				KDimTree(sortedLeafs[:medianIndex], height + 1),
				KDimTree(sortedLeafs[medianIndex:], height + 1)
			)
			volume = AABB.union(children[0].volume, children[1].volume)
			
		self.children = children
		self.volume = volume
		return
	
	@staticmethod
	def sortLeafs(leafs, dim):
		#returns list of leafs sorted by position in dimension dim
		sort = []
		for leaf in leafs:
			index = 0
			for i in range(len(sort)):
				if leaf.transf.cpos[dim] < sort[i].transf.cpos[dim]:
					index = i
			sort.insert(index, leaf)
		return sort
	