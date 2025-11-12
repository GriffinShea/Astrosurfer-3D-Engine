from config import *

from Level.Props.Coll import Coll

def checkCollision(collA, transfA, keyA, collB, transfB, keyB):
	#find a simplex from the minkowski difference of the colliders that contains the origin if
	#	it exists in order to determine if there is an intersection between the objects
	simplex = checkGJKSMIntersect(collA, transfA, collB, transfB)
	
	if simplex:
		#expand the simplex to find the smallest distance by which to seperate the intersecting
		#	colliders (if no epaArtefact, colliders are kissing)
		epaArtefact = expandPolytope(collA, transfA, collB, transfB, simplex)
		if epaArtefact:
			(facePointsDirs, sepVec) = epaArtefact
			if not glmh.isZeroVec(sepVec):
			
				#find a contact point for each collider
				(contactA, contactB) = findContactPoints(
					collA, transfA,
					collB, transfB,
					facePointsDirs, sepVec
				)
				
				#if either contact point is a vertex, set both contacts to that point
				if glmh.vecEquals(
					contactA,
					Coll.calcSupport(collA, transfA, glm.normalize(contactA - transfA.cpos))
				):
					contactB = contactA
				elif glmh.vecEquals(
					contactB,
					Coll.calcSupport(collB, transfB, glm.normalize(contactB - transfB.cpos))
				):
					contactA = contactB
				
				return [keyA, keyB, contactA, contactB, sepVec]
	
	return None

def supportDiff(collA, transfA, collB, transfB, direction):
	return Coll.calcSupport(collA, transfA, direction) - Coll.calcSupport(collB, transfB, -direction)

def checkGJKSMIntersect(collA, transfA, collB, transfB):
	#source: https://www.youtube.com/watch?v=Qupqu1xe7Io
	nextDir = glm.normalize(transfA.cpos - transfB.cpos)
	nextPoint = supportDiff(collA, transfA, collB, transfB, nextDir)
	pointDirs = [(nextPoint, nextDir)]
	
	nextDir = glm.normalize(-nextPoint)
	for i in range(COLLISION_MAX_ITERATIONS):
		nextPoint = supportDiff(collA, transfA, collB, transfB, nextDir)
		if glm.dot(nextPoint, nextDir) < 0:
			return None
		
		pointDirs.insert(0, (nextPoint, nextDir))
		flag, pointDirs, nextDir = doSimplex(pointDirs)
		if flag:
			#if flag, nextDir actually contains the simplex that contains the origin, meaning there
			#	is an intersection
			return nextDir
	
	return None

def doSimplex(pointDirs):
	#source: https://www.youtube.com/watch?v=Qupqu1xe7Io
	if len(pointDirs) == 2:
		#if parallel, use an arbitrary norm (if this norm happens to give the same point again, on
		#	the second iteration it will give the negative norm)
		d = glmh.nndot(pointDirs[1][0], pointDirs[0][0])
		if glmh.floatEquals(abs(d), -1):
			if glmh.sign(d):
				return False, [pointDirs[0]], -glmh.FUNNY_NORM
			else:
				return False, [pointDirs[0]], glmh.FUNNY_NORM
		
		a = pointDirs[1][0] - pointDirs[0][0]
		
		if glmh.isZeroVec(a):
			return False, [pointDirs[0]], -glmh.FUNNY_NORM
			
		return False, pointDirs, glm.normalize(glmh.vecTripProd(a, -pointDirs[0][0], a))
	
	elif len(pointDirs) == 3:
		a = pointDirs[1][0] - pointDirs[0][0]
		b = pointDirs[2][0] - pointDirs[0][0]
		triSurfNorm = glm.cross(a, b)
			
		if glm.dot(-pointDirs[0][0], glm.cross(a, triSurfNorm)) >= 0:
			if glm.dot(-pointDirs[0][0], a) >= 0:
				return False, [pointDirs[0],pointDirs[1]], glm.normalize(glmh.vecTripProd(a,-pointDirs[0][0],a))
			elif glm.dot(-pointDirs[0][0], b) >= 0:
				return False, [pointDirs[0],pointDirs[2]], glm.normalize(glmh.vecTripProd(b,-pointDirs[0][0],b))
			else:
				return False, [pointDirs[0]], glm.normalize(-pointDirs[0][0])
		elif glm.dot(-pointDirs[0][0], glm.cross(triSurfNorm, b)) >= 0:
			if glm.dot(-pointDirs[0][0], b) >= 0:
				return False, [pointDirs[0],pointDirs[2]], glm.normalize(glmh.vecTripProd(b,-pointDirs[0][0],b))
			else:
				return False, [pointDirs[0]], glm.normalize(-pointDirs[0][0])
		elif glm.dot(-pointDirs[0][0], triSurfNorm) >= 0:
			return False, pointDirs, glm.normalize(triSurfNorm)
		else:
			return False, [pointDirs[0], pointDirs[2], pointDirs[1]], -glm.normalize(triSurfNorm)
	
	elif len(pointDirs) == 4:
		faces = [
			((pointDirs[0], pointDirs[1]), (pointDirs[1], pointDirs[2]), (pointDirs[2], pointDirs[0])),
			((pointDirs[0], pointDirs[3]), (pointDirs[3], pointDirs[1]), (pointDirs[1], pointDirs[0])),
			((pointDirs[0], pointDirs[2]), (pointDirs[2], pointDirs[3]), (pointDirs[3], pointDirs[0])),
			((pointDirs[1], pointDirs[3]), (pointDirs[3], pointDirs[2]), (pointDirs[2], pointDirs[1]))
		]
		faceNorms = [glmh.ncross(face[0][1][0]-face[0][0][0], face[2][0][0]-face[2][1][0]) for face in faces]
		faceDists = [glm.dot(faces[i][0][0][0], faceNorms[i]) for i in range(len(faceNorms))]
		minFaceDistIndex = glmh.argmin(faceDists)
		
		#if all the faces point away from the origin, there is a collision
		if faceDists[minFaceDistIndex] >= 0:
			return True, pointDirs, (faces, faceNorms, faceDists, minFaceDistIndex)
		
		#otherwise, repeat doSimplex with the closest face
		if minFaceDistIndex == 0:
			return doSimplex([pointDirs[0], pointDirs[1], pointDirs[2]])
		if minFaceDistIndex == 1:
			return doSimplex([pointDirs[0], pointDirs[3], pointDirs[1]])
		if minFaceDistIndex == 2:
			return doSimplex([pointDirs[0], pointDirs[2], pointDirs[3]])
		if minFaceDistIndex == 3:
			return doSimplex([pointDirs[1], pointDirs[2], pointDirs[3]])

def expandPolytope(collA, transfA, collB, transfB, simplex):
	#source: https://www.youtube.com/watch?v=6rgiPrzqt9w
	(faces, faceNorms, faceDists, minFaceDistIndex) = simplex
	bestFit = None
	
	for i in range(COLLISION_MAX_ITERATIONS):
		#calculate distance of point furthest in the direction of the closest face's norm
		norm = faceNorms[minFaceDistIndex]
		normPoint = supportDiff(collA, transfA, collB, transfB, norm)
		normPointDist = glm.dot(normPoint, faceNorms[minFaceDistIndex])
		
		difference = abs(normPointDist - faceDists[minFaceDistIndex])
		if not bestFit or bestFit[0] > difference:
			bestFit = [
				difference,
				faces[minFaceDistIndex],
				faceNorms[minFaceDistIndex],
				faceDists[minFaceDistIndex]
			]
			
			#if difference is 0, found the correct collision vector
			if glmh.floatEquals(difference, 0):
				#best fit can be negative sometimes due to curved surfaces
				if bestFit[3] < 0:
					if not DEBUG_SUPPRESS_WARNINGS:
						print("WARNING: bestFit[3] < 0 in Collider.expandPolytope()")
					bestFit[2] *= -1
					bestFit[3] *= -1
				break
		
		#remove faces whos norms point in the same direction of the new point but save the remaining
		#	edges
		savedEdges = []
		for i in range(len(faces)-1, -1, -1):
			if glm.dot(normPoint, faceNorms[i]) >= 0:
				faceEdges = list(faces[i])
				for edgeA in faceEdges:
					if (edgeA[1], edgeA[0]) in savedEdges:
						#REVISIT: you sure about that? (index())
						del savedEdges[savedEdges.index((edgeA[1], edgeA[0]))]
					else:
						savedEdges.append(edgeA)
				del faces[i]
				del faceNorms[i]
				del faceDists[i]
		
		#add new faces made with the saved edges and the new point
		for edge in savedEdges:
			faces.append((edge, (edge[1], (normPoint, norm)), ((normPoint, norm), edge[0])))
			faceNorms.append(glmh.ncross(
				faces[-1][1][0][0]-faces[-1][0][0][0],
				faces[-1][2][0][0]-faces[-1][0][0][0]
			))
			faceDists.append(glm.dot(faces[-1][0][0][0], faceNorms[-1]))
			
			#i dont know why but sometimes a backword facing norm is generated and this fixes it
			if faceDists[-1] < 0:
				faceDists[-1] *= -1
				faceNorms[-1] *= -1
		
		minFaceDistIndex = glmh.argmin(faceDists)
		
		if len(faceDists) == 0:
			if not DEBUG_SUPPRESS_WARNINGS:
				print("WARNING: len(faceDists) == 0 in Collider.expandPolytope()")
			break
	
	return ((bestFit[1][0][0], bestFit[1][0][1], bestFit[1][1][1]), bestFit[3] * bestFit[2])

def findContactPoints(collA, transfA, collB, transfB, facePointsDirs, sepVec):
	#calculate contact point using projection of origin onto face (the collision vector) and using
	#	barycentric coordinate coefficients to linearly combine associated support points for each
	#	collider (source: https://allenchou.net/2013/12/game-physics-contact-generation-epa/)
	
	#the points of the triangle in 3D space
	p0 = facePointsDirs[0][0]
	p1 = facePointsDirs[1][0]
	p2 = facePointsDirs[2][0]
	
	#calculation of barycentric coordinates for the contact points
	r0 = p1 - p0
	r1 = p2 - p0
	r2 = sepVec - p0
	d00 = glm.dot(r0, r0)
	d01 = glm.dot(r0, r1)
	d11 = glm.dot(r1, r1)
	d20 = glm.dot(r2, r0)
	d21 = glm.dot(r2, r1)
	s = d00 * d11 - d01 * d01
	if glmh.floatEquals(s, 0):
		if not DEBUG_SUPPRESS_WARNINGS:
			print("WARNING: barycentric coordinate calculation failed in findContactPoints().")
		s = 1
	
	coeffs = glm.vec3()
	coeffs.x = (d11*d20-d01*d21) / s
	coeffs.y = (d00*d21-d01*d20) / s
	coeffs.z = 1 - coeffs.x - coeffs.y
	
	#finally, use these barycentric coordinates as coefficients to calculate contact points
	contactA = (
		coeffs.x * Coll.calcSupport(collA, transfA, facePointsDirs[0][1])
		+ coeffs.y * Coll.calcSupport(collA, transfA, facePointsDirs[1][1])
		+ coeffs.z * Coll.calcSupport(collA, transfA, facePointsDirs[2][1])
	)
	contactB = (
		coeffs.x * Coll.calcSupport(collB, transfB, -facePointsDirs[0][1])
		+ coeffs.y * Coll.calcSupport(collB, transfB, -facePointsDirs[1][1])
		+ coeffs.z * Coll.calcSupport(collB, transfB, -facePointsDirs[2][1])
	)
	
	return (contactA, contactB)