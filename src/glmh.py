import glm
import random

#important program globals
LOW_FLOAT_CONSTANT = 0.00001
ZERO_VEC = glm.vec4()
NAN_VEC = glm.normalize(ZERO_VEC)
FUNNY_NORM = glm.normalize(glm.vec3(3.14159, 2.71828, 1.41421))
INF = 1000000	#REVISIT: can we use infinity?????

#transforms from camera space to texture space ( [-1,1] --> [0,1] )
CAM_TO_TEX_MAT = glm.scale(glm.translate(glm.mat4(), glm.vec3(0.5)), glm.vec3(0.5))


def copy(v):
	return glm.vec3(v.x, v.y, v.z)


#returns unit vectors and rotated basis vectors
def xUnit(l=1):
	return glm.vec3(l, 0, 0)
def yUnit(l=1):
	return glm.vec3(0, l, 0)
def zUnit(l=1):
	return glm.vec3(0, 0, l)
def xBasis(quat):
	return glm.normalize(quat * glm.vec3(1, 0, 0))
def yBasis(quat):
	return glm.normalize(quat * glm.vec3(0, 1, 0))
def zBasis(quat):
	return glm.normalize(quat * glm.vec3(0, 0, 1))



def floatEquals(a, b):
	return abs(a - b) < LOW_FLOAT_CONSTANT

def floatLessThanOrEqual(a, b):
	return (a - b) <= LOW_FLOAT_CONSTANT

def vecEquals(a, b):
	if len(a) == len(b):
		for i in range(len(a)):
			if not floatEquals(a[i], b[i]):
				return False
		return True
	else:
		return False

def mean(*args):
	return sum(args) / len(args)

def vecTripProd(a, b, c):
	return glm.cross(a, glm.cross(b, c))
	
def isZeroVec(vec):
	for i in range(len(vec)):
		if vec[i] != 0:
			return False
	return True
	
def isNanVec(vec):
	return glm.any(glm.isnan(vec))

def randVec3():
	return glm.normalize(glm.vec3(random.random(), random.random(), random.random()))
	
	
#safe cheatcodes
def robustNorm(v):
	u = glm.normalize(v)
	return glm.vec3() if glm.isnan(u) else u

def safeDot(a, b):
	c = glm.dot(a, b)
	if glm.isnan(c):
		print(a, "dot", b, "= NaN")
		raise ValueError
	return c

def safeCross(a, b):
	c = glm.cross(a, b)
	if glm.any(glm.isnan(c)):
		print(a, "cross", b, "= NaN")
		raise ValueError
	return c
	

#matricies

#REVISIT: these declarations must be moved
FRAME_BUFFER_DIMS = (1280, 960)
NEAR_CLIPPING_PLANE = 0.1
FAR_CLIPPING_PLANE = 250

def calcPerspectiveMat(fov):
	top = glm.tan(fov) * NEAR_CLIPPING_PLANE
	right = top * FRAME_BUFFER_DIMS[0] / FRAME_BUFFER_DIMS[1]
	return glm.frustum(
		-right,
		right,
		-top,
		top,
		NEAR_CLIPPING_PLANE,
		FAR_CLIPPING_PLANE
	)
def calcOrthographicMat(dims):
	return glm.ortho(
		-dims.x, dims.x,
		-dims.y, dims.y,
		NEAR_CLIPPING_PLANE, FAR_CLIPPING_PLANE
	)
def calcViewMat(pos, ori):
	#this is a mathematically well founded incantation
	#https://learnopengl.com/Getting-started/Camera
	currLeft = ori * xUnit()
	currUp = ori * yUnit()
	currBack = ori * -zUnit()
	
	viewMat = glm.mat4()
	viewMat[0][0] = currLeft[0]
	viewMat[1][0] = currLeft[1]
	viewMat[2][0] = currLeft[2]
	viewMat[0][1] = currUp[0]
	viewMat[1][1] = currUp[1]
	viewMat[2][1] = currUp[2]
	viewMat[0][2] = currBack[0]
	viewMat[1][2] = currBack[1]
	viewMat[2][2] = currBack[2]
	viewMat = glm.translate(viewMat, -pos)
	
	return viewMat
	
	
	

	
#normalized cheatcodes
def ncross(a, b):
	return glm.normalize(glm.cross(a, b))

def nndot(a, b):
	return glm.dot(glm.normalize(a), glm.normalize(b))

def ndot(a, b):
	return glm.dot(a, glm.normalize(b))

def absdot(a, b):
	return abs(glm.dot(a, b))

def nabsdot(a, b):
	return abs(glm.dot(a, glm.normalize(b)))

def nnabsdot(a, b):
	return abs(glm.dot(glm.normalize(a), glm.normalize(b)))


#quaternions
def rotVecToQuat(v):
	theta = glm.length(v)
	halfTheta = theta / 2
	n = v / theta
	s = glm.sin(halfTheta)
	return glm.quat(glm.cos(halfTheta), s * n)

def quatAddRotVec(q, v):
	#the following are equivalent
	#if glm.length(v) == 0:
	#	return q
	#return glm.normalize(rotVecToQuat(v) * q)
	return glm.normalize(q + glm.quat(0, v / 2) * q)

def quatLog(q):
	alpha = glm.acos(q.w)
	if alpha == 0:
		return glm.quat()
	else:
		return glm.quat(0, alpha / glm.sin(alpha) * glm.vec3(q.x, q.y, q.z))
	
def quatDiff(p, q):
	return glm.normalize(p * glm.inverse(q))

def transfMat(p, o, s):
	return (
		glm.translate(glm.mat4(), p)
		* glm.mat4_cast(o)
		* glm.scale(glm.mat4(), s)
	)


#for booleans: True = 1, False = -1
def sign(n):
	return n/abs(n) if n else -1

def argmax(l):
	i = 0
	for j in range(1, len(l)):
		if l[j] > l[i]:
			i = j
	return i

def argmin(l):
	i = 0
	for j in range(1, len(l)):
		if l[j] < l[i]:
			i = j
	return i
