from Core.Systems.Physics.resolveCollisions import resolveCollisions
from Core.Systems.Physics.resolveConstraints import resolveConstraints

class Solver:
	@staticmethod
	def run(index, collisions):
		#resolve physical collisions (parallel)
		resolveCollisions(index, collisions)
		#resolve constraints
		resolveConstraints(index)
		return