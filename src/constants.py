import glm

#colours
WHITE = glm.vec3(1, 1, 1)
GREY = glm.vec3(0.5, 0.5, 0.5)
BLACK = glm.vec3(0, 0, 0)
RED = glm.vec3(1, 0, 0)
YELLOW = glm.vec3(1, 1, 0)
GREEN = glm.vec3(0, 1, 0)
CYAN = glm.vec3(0, 1, 1)
BLUE = glm.vec3(0, 0, 1)
MAGENTA = glm.vec3(1, 0, 1)

LBLUE = glm.vec3(0.5, 0.5, 1)
PINK = glm.vec3(1, 0.5, 0.5)

#Coll shapes
COLLSPHERE = 0
COLLCAPSULE = 1
COLLCYLINDER = 2
COLLBOX = 3
COLLPLANE = 4
COLLRAY = 5

#Coll physTypes
COLLFLAG = 0		#static, nonsolid
COLLTERRAIN = 1		#static, solid
COLLGHOST = 2		#nonstatic, nonsolid
COLLSOLID = 3		#nonstatic, solid
COLLRIGIDBODY = 4	#for Rigidbodys (nonstatic, solid)

#input constants
M_LEFT = 0
M_MIDDLE = 1
M_RIGHT = 2
M_SCROLLUP = 3
M_SCROLLDOWN = 4
M_4 = 5
M_5 = 6

OFF = 0
DOWN = 2
ON = 1
UP = 3
