from config import *
from ShaderHelper import ShaderHelper

class ResourceManager:
	meshes = {}
	unloadedMeshes = set()
	shaders = {}
	unloadedShaders = set()
	textures = {}
	unloadedTextures = set()
	fonts = {}
	unloadedFonts = set()
	
	@classmethod
	def init(cls):
		print("\tInitializing ResourceManager...")
		#===========================================================================================
		
		print("\t\tGenerating and loading meshes...")
		
		#these meshes are all CCW wrapped and square like triangle meshes
		#i.e., the first vertex is the same on both triangles for each quad
		
		cls.meshes["nullElement"] = createNullElement()
		cls.meshes["frame"] = createFrame()
		cls.meshes["square"] = createSquare()
		cls.meshes["quadSquare"] = createQuadSquare()
		cls.meshes["plane"] = createPlane()				#a plane is a double sided square
		cls.meshes["cylinder"] = createCylinder(20)
		cls.meshes["cube"] = createCube()
		cls.meshes["room"] = createRoom()				#room is a cube with inverted faces
		cls.meshes["dieCube"] = createDieCube()
		
		#REVISIT: sphere here because loading astronauta corrupted dolphin's data somehow
		cls.loadMeshTris("pyr")
		cls.loadMeshTris("dolphin")
		cls.meshes["sphere"] = createSphere(10, 10)
		
		cls.loadMeshTris("astronauta")
		cls.loadMeshTris("astronauta_nobackpack")
		cls.loadMeshTris("astronauta_torso")
		cls.loadMeshTris("astronauta_torso_backpack")
		cls.loadMeshTris("astronauta_reloded_head")
		cls.loadMeshTris("astronauta_reloded_leftlegtop")
		cls.loadMeshTris("astronauta_reloded_rightlegtop")
		cls.loadMeshTris("astronauta_reloded_leftarmtop")
		cls.loadMeshTris("astronauta_reloded_rightarmtop")
		cls.loadMeshTris("astronauta_reloded_leftlegbot")
		cls.loadMeshTris("astronauta_reloded_rightlegbot")
		cls.loadMeshTris("astronauta_reloded_leftarmbot")
		cls.loadMeshTris("astronauta_reloded_rightarmbot")
		
		cls.loadMeshTris("asteroids//AST_1", "asteroid1")
		cls.loadMeshTris("asteroids//AST_2", "asteroid2")
		cls.loadMeshTris("asteroids//AST_3", "asteroid3")
		cls.loadMeshTris("asteroids//AST_4", "asteroid4")
		cls.loadMeshTris("asteroids//AST_5", "asteroid5")
		
		
		#===========================================================================================
		
		print("\t\tCompiling shader programs...")
		
		#debug shaders
		cls.shaders["colouredSegment"] = ShaderHelper.loadShaderFromGLSLH("debug//colouredSegment")
		#cls.shaders["colouredWireframe"] = ShaderHelper.loadShaderFromGLSLH("debug//colouredWireframe")
		#cls.shaders["normals"] = ShaderHelper.loadShaderFromGLSLH("debug//normals")
		#cls.shaders["orthographicDepthMap"] = ShaderHelper.loadShaderFromGLSLH("debug//orthographicDepthMap")
		#cls.shaders["perspectiveDepthMap"] = ShaderHelper.loadShaderFromGLSLH("debug//perspectiveDepthMap")
		#cls.shaders["gPos"] = ShaderHelper.loadShaderFromGLSLH("debug//gPos")
		#cls.shaders["gNorm"] = ShaderHelper.loadShaderFromGLSLH("debug//gNorm")
		#cls.shaders["gCol"] = ShaderHelper.loadShaderFromGLSLH("debug//gCol")
		#cls.shaders["frame"] = ShaderHelper.loadShaderFromGLSLH("debug//frame")
		
		#used by the game engine
		cls.shaders["frameBuffer"] = ShaderHelper.loadShaderFromGLSLH("engine//frameBuffer")
		cls.shaders["basicText"] = ShaderHelper.loadShaderFromGLSLH("engine//basicText")
		cls.shaders["basicSprite"] = ShaderHelper.loadShaderFromGLSLH("engine//basicSprite")
		cls.shaders["mapModelShadow"] = ShaderHelper.loadShaderFromGLSLH("engine//mapModelShadow")
		cls.shaders["gBuffer"] = ShaderHelper.loadShaderFromGLSLH("engine//gBuffer")
		cls.shaders["jelly"] = ShaderHelper.loadShaderFromGLSLH("engine//jelly")
		
		#frame effects
		cls.shaders["fullBlurFrame"] = ShaderHelper.loadShaderFromGLSLH("frameEffects//fullBlurFrame")
		cls.shaders["horiBlurFrame"] = ShaderHelper.loadShaderFromGLSLH("frameEffects//horiBlurFrame")
		cls.shaders["normalizeColour"] = ShaderHelper.loadShaderFromGLSLH("frameEffects//normalizeColour")
		
		#particle effects
		cls.shaders["explosion"] = ShaderHelper.loadShaderFromGLSLH("particleEffects//explosion")
		cls.shaders["rocketEmission"] = ShaderHelper.loadShaderFromGLSLH("particleEffects//rocketEmission")
		cls.shaders["spinningFeathers"] = ShaderHelper.loadShaderFromGLSLH("particleEffects//spinningFeathers")
		cls.shaders["fallingFeathers"] = ShaderHelper.loadShaderFromGLSLH("particleEffects//fallingFeathers")
		
		#SHADER MASK REFERENCE:
		#	0 1 2 3 4
		#	  0 0   0
		#	B T L T I
		#	X Q   U
		#	      I
		#         S
		#
		#	0: (B)asic or ps(X) shader
		#	1: (T)riangle or (Q)uad or no tesselation (0)
		#	2: apply (L)ighting or not (0)
		#	3: (T)exture, (U)niform, (I)nterpolated, or (S)tatic colour
		#	4: enable (I)nvert colour or not (0)
		#
		
		#template shaders
		cls.shaders["texture"] = ShaderHelper.createShaderFromMask("B0LT0")
		cls.shaders["unLitTexture"] = ShaderHelper.createShaderFromMask("B00T0")
		cls.shaders["invertedTexture"] = ShaderHelper.createShaderFromMask("B0LTI")
		cls.shaders["solidUnlitColour"] = ShaderHelper.createShaderFromMask("B00U0")
		cls.shaders["solidLitColour"] = ShaderHelper.createShaderFromMask("B0LU0")
		cls.shaders["triTess"] = ShaderHelper.createShaderFromMask("BTLT0")
		cls.shaders["quadTess"] = ShaderHelper.createShaderFromMask("BQLT0")
		
		#===========================================================================================
		
		print("\t\tLoading textures...")
		cls.textures["die"] = cls.loadTexture("misc//die.png")
		cls.textures["eyeball"] = cls.loadTexture("misc//eyeball.png")
		cls.textures["tesseract"] = cls.loadTexture("misc//tesseract.png")
		cls.textures["dolphinWireframe"] = cls.loadTexture("misc//dolphinWireframe.png")
		cls.textures["play4keeps"] = cls.loadTexture("misc//play4keeps128.png")
		cls.textures["swimcity"] = cls.loadTexture("misc//SWIMCITY128.png")
		cls.textures["multpaleta"] = cls.loadTexture("misc//multpaleta.png")
		#cls.textures["dolphin"] = cls.loadTexture("misc//dolphin.png")
		
		cls.textures["purpleWall"] = cls.loadTexture("walls//purpleWall.png")
		cls.textures["stoneWall"] = cls.loadTexture("walls//stoneWall.png")
		
		#REVISIT: need to catch this user error (nonexistant file)
		cls.textures["purpleSky"] = cls.loadTexture("misc//purple_sky.png")
		
		cls.textures["featherParticle"] = cls.loadTexture("particles//featherParticle.png")
		
		cls.textures["reticle"] = cls.loadTexture("gui//reticle.png", (255, 255, 255))
		
		#===========================================================================================
		
		print("\t\tLoading fonts...")
		cls.fonts["basicFont"] = cls.loadFont("basicFont.font")
		cls.fonts["fancyFont"] = cls.loadFont("fancyFont.font")
		
		#===========================================================================================
		print("\tDone.")
		return
	
	@classmethod
	def getFont(cls, name):
		if name in cls.fonts:
			return cls.fonts[name]
		if not name in cls.unloadedFonts:
			cls.unloadedFonts.add(name)
			print("WARNING: unloaded font:", name)
		return cls.fonts["basicFont"]
	
	@classmethod
	def getTexture(cls, name):
		if name in cls.textures:
			return cls.textures[name]
		if not name in cls.unloadedTextures:
			cls.unloadedTextures.add(name)
			print("WARNING: unloaded texture:", name)
		return cls.textures["die"]
	
	@classmethod
	def getMesh(cls, name):
		if name in cls.meshes:
			return cls.meshes[name]
		if not name in cls.unloadedMeshes:
			cls.unloadedMeshes.add(name)
			print("WARNING: unloaded mesh:", name)
		return cls.meshes["dieCube"]
	
	@classmethod
	def getShader(cls, name):
		if name in cls.shaders:
			return cls.shaders[name]
		if not name in cls.unloadedShaders:
			cls.unloadedShaders.add(name)
			print("WARNING: unloaded shader:", name)
		return cls.shaders["jelly"]
	
	@classmethod
	def loadFont(cls, fontName):
		with open("assets//fonts//" + fontName) as fontFile:
			font = json.load(fontFile)
			cls.textures[font["bitmap"]] = cls.loadTexture("bitmaps//" + font["bitmap"] + ".bmp")
			return (font["bitmap"], glm.vec2(font["bitmapDims"]), glm.vec2(font["glyphDims"]))
	
	@classmethod
	def loadTexture(cls, fileName, transparentColour=None):
		try:
			#load image as pygame surface
			surface = pygame.image.load("assets//textures//" + fileName).convert()
			surfaceString = pygame.image.tostring(surface, "RGBA", 1)
			
			#zero out alpha value of pixels with transparentColour
			if transparentColour:
				bytesList = []
				channelCounter = 0
				channelValues = [0, 0, 0, 0]
				for i in range(len(surfaceString)):
					if channelCounter == 3:
						if (
							channelValues[0] == transparentColour[0] and
							channelValues[1] == transparentColour[1] and
							channelValues[2] == transparentColour[2]
						):
							channelValues[channelCounter] = 0x00
						else:
							channelValues[channelCounter] = 0xff
						channelCounter = 0
						bytesList += channelValues
					else:
						channelValues[channelCounter] = surfaceString[i]
						channelCounter += 1
				surfaceString = bytes(bytesList)
			
			#get and bind a texture location
			location = gl.glGenTextures(1)
			gl.glBindTexture(gl.GL_TEXTURE_2D, location)
			
			#load surface data into texture
			gl.glTexImage2D(
				gl.GL_TEXTURE_2D,
				0,
				gl.GL_RGBA,
				surface.get_width(),
				surface.get_height(),
				0,
				gl.GL_RGBA,
				gl.GL_UNSIGNED_BYTE,
				surfaceString
			)
			
			#setup texture drawing rules and mipmap (if applicable)
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
				
			filterLevel = [
				gl.GL_NEAREST_MIPMAP_NEAREST,
				gl.GL_LINEAR_MIPMAP_NEAREST,
				gl.GL_NEAREST_MIPMAP_LINEAR,
				gl.GL_LINEAR_MIPMAP_LINEAR
			][MIN_FILTER_LEVEL]
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, filterLevel)
			
			gl.glTexParameteri(
				gl.GL_TEXTURE_2D,
				gl.GL_TEXTURE_MAG_FILTER,
				gl.GL_LINEAR if MAG_FILER else gl.GL_NEAREST
			)
			
			gl.glGenerateTextureMipmap(location)
			return location
			
		except pygame.error as message:
			print("Pygame error:", message)
			return 2
	
	@classmethod
	def loadMeshTris(cls, name, newName=None):
		newName = newName if newName else name
		with open("assets//meshes//" + name + ".obj") as file:
			positions = []
			texCoords = []
			normals = []
			
			verticiesDict = {}
			verticies = []
			triangles = []
			
			while True:
				line = file.readline().strip()
				if not line:
					break
				
				line = line.split(" ")
				if line[0] == "v":
					positions.append(glm.vec3(float(line[1]), float(line[2]), float(line[3])))
				elif line[0] == "vt":
					texCoords.append(glm.vec2(float(line[1]), float(line[2])))
				elif line[0] == "vn":
					normals.append(glm.vec3(float(line[1]), float(line[2]), float(line[3])))
				elif line[0] == "f":
					line[1:] = [line[3], line[2], line[1]]
					for vertexString in line[1:]:
						if not vertexString in verticiesDict:
							verticiesDict[vertexString] = len(verticies) / 8
							vertex = vertexString.split("/")
							verticies.append(positions[int(vertex[0])-1].x)
							verticies.append(positions[int(vertex[0])-1].y)
							verticies.append(positions[int(vertex[0])-1].z)
							verticies.append(normals[int(vertex[2])-1].x)
							verticies.append(normals[int(vertex[2])-1].y)
							verticies.append(normals[int(vertex[2])-1].z)
							if texCoords:
								verticies.append(texCoords[int(vertex[1])-1].x)
								verticies.append(texCoords[int(vertex[1])-1].y)
							else:
								verticies.append(0)
								verticies.append(0)
						triangles.append(verticiesDict[vertexString])
		
		verticies = numpy.array(verticies, dtype=numpy.float32)
		triangles = numpy.array(triangles, dtype=numpy.uint32)
		
		vbo = gl.glGenBuffers(1)
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
		gl.glBufferData(gl.GL_ARRAY_BUFFER, verticies.nbytes, verticies, gl.GL_STATIC_DRAW)
		
		ebo = gl.glGenBuffers(1)
		gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
		gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, triangles.nbytes, triangles, gl.GL_STATIC_DRAW)
		
		cls.meshes[newName] = (
			vbo,
			8,
			((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)),
			ebo,
			len(triangles),
			3
		)
		return
	
def createNullElement():
	verticies = (
		0
	)
	verticies = numpy.array(verticies, dtype=numpy.float32)
	
	vbo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
	gl.glBufferData(gl.GL_ARRAY_BUFFER, verticies.nbytes, verticies, gl.GL_STATIC_DRAW)
	
	triangles = (
		0, 0, 0
	)
	triangles = numpy.array(triangles, dtype=numpy.uint32)
	
	ebo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
	gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, triangles.nbytes, triangles, gl.GL_STATIC_DRAW)
	
	return (vbo, 1, [(1, gl.GL_FLOAT)], ebo, 1, 3)

def createFrame():
	verticies = (
		-1, -1, 0, 0,
		1, -1, 1, 0,
		-1, 1, 0, 1,
		1, 1, 1, 1
	)
	verticies = numpy.array(verticies, dtype=numpy.float32)
	
	vbo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
	gl.glBufferData(gl.GL_ARRAY_BUFFER, verticies.nbytes, verticies, gl.GL_STATIC_DRAW)
	
	triangles = (
		1, 2, 0,
		1, 3, 2
	)
	triangles = numpy.array(triangles, dtype=numpy.uint32)
	
	ebo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
	gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, triangles.nbytes, triangles, gl.GL_STATIC_DRAW)
	
	return (vbo, 4, ((2, gl.GL_FLOAT), (2, gl.GL_FLOAT)), ebo, 2, 3)

def createSquare():
	verticies = (
		-0.5, -0.5, 0, 0, 0, -1, 0, 0,
		0.5, -0.5, 0, 0, 0, -1, 1, 0,
		-0.5, 0.5, 0, 0, 0, -1, 0, 1,
		0.5, 0.5, 0, 0, 0, -1, 1, 1
	)
	verticies = numpy.array(verticies, dtype=numpy.float32)
	
	vbo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
	gl.glBufferData(gl.GL_ARRAY_BUFFER, verticies.nbytes, verticies, gl.GL_STATIC_DRAW)
	
	triangles = (
		1, 2, 0,
		1, 3, 2
	)
	triangles = numpy.array(triangles, dtype=numpy.uint32)
	
	ebo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
	gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, triangles.nbytes, triangles, gl.GL_STATIC_DRAW)
	
	return (vbo, 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), ebo, 2, 3)

def createQuadSquare():
	verticies = (
		-0.5, -0.5, 0, 0, 0, -1, 0, 0,
		0.5, -0.5, 0, 0, 0, -1, 1, 0,
		0.5, 0.5, 0, 0, 0, -1, 1, 1,
		-0.5, 0.5, 0, 0, 0, -1, 0, 1
	)
	verticies = numpy.array(verticies, dtype=numpy.float32)
	
	vbo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
	gl.glBufferData(gl.GL_ARRAY_BUFFER, verticies.nbytes, verticies, gl.GL_STATIC_DRAW)
	
	quads = (
		0, 1, 2, 3
	)
	quads = numpy.array(quads, dtype=numpy.uint32)
	
	ebo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
	gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, quads.nbytes, quads, gl.GL_STATIC_DRAW)
	
	return (vbo, 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), ebo, 1, 4)

def createPlane():
	verticies = (
		-0.5, -0.5, 0, 0, 0, -1, 0, 0,
		0.5, -0.5, 0, 0, 0, -1, 1, 0,
		-0.5, 0.5, 0, 0, 0, -1, 0, 1,
		0.5, 0.5, 0, 0, 0, 1, 1, 1,
		-0.5, -0.5, 0, 0, 0, 1, 0, 0,
		0.5, -0.5, 0, 0, 0, 1, 1, 0,
		-0.5, 0.5, 0, 0, 0, 1, 0, 1,
		0.5, 0.5, 0, 0, 0, 1, 1, 1
	)
	verticies = numpy.array(verticies, dtype=numpy.float32)
	
	vbo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
	gl.glBufferData(gl.GL_ARRAY_BUFFER, verticies.nbytes, verticies, gl.GL_STATIC_DRAW)
	
	triangles = (
		1, 2, 0,
		1, 3, 2,
		6, 5, 4,
		6, 7, 5
	)
	triangles = numpy.array(triangles, dtype=numpy.uint32)
	
	ebo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
	gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, triangles.nbytes, triangles, gl.GL_STATIC_DRAW)
	
	return (vbo, 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), ebo, 4, 3)

def createSphere(h, v):	#h = horizontal slices, v = vertical slices
	verticies = []
	for i in range(v):
		verticies = verticies + [0, 0.5, 0, 0, 1, 0, i/v+1/(2*v), 1]
	for i in range(h):
		phi = (i+1)*glm.pi()/(h+1)
		sliceRadius = glm.sin(phi)/2
		sliceY = glm.cos(phi)/2
		for j in range(v+1):
			theta = j*glm.pi()/(v/2)
			position = (
				glm.angleAxis(glm.pi()/2, glmh.yUnit())
				* glm.vec3(sliceRadius*glm.cos(theta), sliceY, sliceRadius*glm.sin(theta))
			)
			normal = glm.normalize(position)
			verticies = verticies + [position.x, position.y, position.z]
			verticies = verticies + [normal.x, normal.y, normal.z]
			verticies = verticies + [abs(theta/(glm.pi()) - 1), sliceY+0.5]
	for i in range(v):
		verticies = verticies + [0, -0.5, 0, 0, -1, 0, i/v+1/(2*v), 0]
	verticies = numpy.array(verticies, dtype=numpy.float32)
	
	vbo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
	gl.glBufferData(gl.GL_ARRAY_BUFFER, verticies.nbytes, verticies, gl.GL_STATIC_DRAW)
	
	triangles = []
	for i in range(v):
		triangles = triangles + [i, v+i, v+i+1]
	for i in range(h-1):
		for j in range(v):
			triangles = triangles + [(v+1)*i+j+v+1, (v+1)*i+j+v, (v+1)*(i+1)+j+v]
			triangles = triangles + [(v+1)*i+j+v+1, (v+1)*(i+1)+j+v, (v+1)*(i+1)+j+v+1]
	for i in range(v):
		triangles = triangles + [h*(v+1)+i, h*(v+1)+i-1, (h+1)*(v+1)+i-1]
	triangles = numpy.array(triangles, dtype=numpy.uint32)
	
	ebo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
	gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, triangles.nbytes, triangles, gl.GL_STATIC_DRAW)
	
	return (vbo, 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), ebo, 2*h*v, 3)

def createCylinder(v):	#v = vertical slices
	verticies = []
	for i in range(v):
		verticies = verticies + [0, 0.5, 0, 0, 1, 0, i/v+1/(2*v), 1]
	for i in range(v+1):
		verticies = verticies + [glm.cos(i*glm.pi()/v*2)/2, 0.5, glm.sin(i*glm.pi()/v*2)/2, 0, 1, 0, i/v, 0]
	for i in range(v+1):
		position = glm.vec3(glm.cos(i*glm.pi()/v*2)/2, 0.5, glm.sin(i*glm.pi()/v*2)/2)
		normal = glm.normalize(glm.vec3(position.x, 0, position.z))
		verticies = verticies + [position.x, position.y, position.z, normal.x, normal.y, normal.z, i/v, 1]
	for i in range(v+1):
		position = glm.vec3(glm.cos(i*glm.pi()/v*2)/2, -0.5, glm.sin(i*glm.pi()/v*2)/2)
		normal = glm.normalize(glm.vec3(position.x, 0, position.z))
		verticies = verticies + [position.x, position.y, position.z, normal.x, normal.y, normal.z, i/v, 0]
	for i in range(v+1):
		verticies = verticies + [glm.cos(i*glm.pi()/v*2)/2, -0.5, glm.sin(i*glm.pi()/v*2)/2, 0, -1, 0, i/v, 0]
	for i in range(v):
		verticies = verticies + [0, -0.5, 0, 0, -1, 0, i/v+1/(2*v), 1]
	verticies = numpy.array(verticies, dtype=numpy.float32)
	
	vbo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
	gl.glBufferData(gl.GL_ARRAY_BUFFER, verticies.nbytes, verticies, gl.GL_STATIC_DRAW)
	
	triangles = []
	for i in range(v):
		triangles = triangles + [i, v+i, v+i+1]
	for i in range(v):
		triangles = triangles + [3*(v+1)+i-1, 2*(v+1)+i, 2*(v+1)+i-1]
		triangles = triangles + [3*(v+1)+i-1, 3*(v+1)+i, 2*(v+1)+i]
	for i in range(v):
		triangles = triangles + [5*(v+1)+i-1, 4*(v+1)+i, 4*(v+1)+i-1]
	triangles = numpy.array(triangles, dtype=numpy.uint32)
	
	ebo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
	gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, triangles.nbytes, triangles, gl.GL_STATIC_DRAW)
	
	return (vbo, 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), ebo, 4*v, 3)

def createCube():
	positions = (
		glm.vec3(-0.5, -0.5, -0.5),
		glm.vec3(-0.5, -0.5, 0.5),
		glm.vec3(-0.5, 0.5, -0.5),
		glm.vec3(-0.5, 0.5, 0.5),
		glm.vec3(0.5, -0.5, -0.5),
		glm.vec3(0.5, -0.5, 0.5),
		glm.vec3(0.5, 0.5, -0.5),
		glm.vec3(0.5, 0.5, 0.5)
	)
	
	normals = (
		glmh.yUnit(),
		glm.vec3(0, 0, -1),
		glmh.zUnit(),
		glmh.xUnit(),
		glm.vec3(-1, 0, 0),
		glm.vec3(0, -1, 0),
	)
	
	texCoords = (
		glm.vec2(0, 1),
		glm.vec2(0, 0),
		glm.vec2(1, 1),
		glm.vec2(1, 0)
	)
	
	faces = (
		2, 6, 3, 7,
		2, 0, 6, 4,
		7, 5, 3, 1,
		6, 4, 7, 5,
		3, 1, 2, 0,
		4, 0, 5, 1
	)
	
	verticies = []
	for i in range(len(faces)):
		verticies = verticies + [positions[faces[i]].x, positions[faces[i]].y, positions[faces[i]].z]
		verticies = verticies + [normals[int(i/4)].x, normals[int(i/4)].y, normals[int(i/4)].z]
		verticies = verticies + [texCoords[i%4].x, texCoords[i%4].y]
	verticies = numpy.array(verticies, dtype=numpy.float32)
	
	vbo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
	gl.glBufferData(gl.GL_ARRAY_BUFFER, verticies.nbytes, verticies, gl.GL_STATIC_DRAW)
	
	triangles = []
	for i in range(6):
		triangles = triangles + [
			4*i+1, 4*i+2, 4*i,
			4*i+1, 4*i+3, 4*i+2
		]
	triangles = numpy.array(triangles, dtype=numpy.uint32)
	
	ebo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
	gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, triangles.nbytes, triangles, gl.GL_STATIC_DRAW)
	
	return (vbo, 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), ebo, 12, 3)

def createRoom():
	positions = (
		glm.vec3(-0.5, -0.5, -0.5),
		glm.vec3(-0.5, -0.5, 0.5),
		glm.vec3(-0.5, 0.5, -0.5),
		glm.vec3(-0.5, 0.5, 0.5),
		glm.vec3(0.5, -0.5, -0.5),
		glm.vec3(0.5, -0.5, 0.5),
		glm.vec3(0.5, 0.5, -0.5),
		glm.vec3(0.5, 0.5, 0.5)
	)
	
	normals = (
		glmh.yUnit(),
		glm.vec3(0, 0, -1),
		glmh.zUnit(),
		glmh.xUnit(),
		glm.vec3(-1, 0, 0),
		glm.vec3(0, -1, 0),
	)
	
	texCoords = (
		glm.vec2(0, 1),
		glm.vec2(0, 0),
		glm.vec2(1, 1),
		glm.vec2(1, 0)
	)
	
	faces = (
		2, 6, 3, 7,
		2, 0, 6, 4,
		7, 5, 3, 1,
		6, 4, 7, 5,
		3, 1, 2, 0,
		4, 0, 5, 1
	)
	
	verticies = []
	for i in range(len(faces)):
		verticies = verticies + [positions[faces[i]].x, positions[faces[i]].y, positions[faces[i]].z]
		verticies = verticies + [normals[int(i/4)].x, normals[int(i/4)].y, normals[int(i/4)].z]
		verticies = verticies + [texCoords[i%4].x, texCoords[i%4].y]
	verticies = numpy.array(verticies, dtype=numpy.float32)
	
	vbo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
	gl.glBufferData(gl.GL_ARRAY_BUFFER, verticies.nbytes, verticies, gl.GL_STATIC_DRAW)
	
	triangles = []
	for i in range(6):
		triangles = triangles + [
			4*i+2, 4*i+1, 4*i,
			4*i+2, 4*i+3, 4*i+1
		]
	triangles = numpy.array(triangles, dtype=numpy.uint32)
	
	ebo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
	gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, triangles.nbytes, triangles, gl.GL_STATIC_DRAW)
	
	return (vbo, 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), ebo, 12, 3)

def createDieCube():
	positions = (
		glm.vec3(-0.5, -0.5, -0.5),
		glm.vec3(-0.5, -0.5, 0.5),
		glm.vec3(-0.5, 0.5, -0.5),
		glm.vec3(-0.5, 0.5, 0.5),
		glm.vec3(0.5, -0.5, -0.5),
		glm.vec3(0.5, -0.5, 0.5),
		glm.vec3(0.5, 0.5, -0.5),
		glm.vec3(0.5, 0.5, 0.5)
	)
	
	normals = (
		glmh.yUnit(),
		glm.vec3(0, 0, -1),
		glmh.zUnit(),
		glmh.xUnit(),
		glm.vec3(-1, 0, 0),
		glm.vec3(0, -1, 0),
	)
	
	texCoords = (
		glm.vec2(0, 0),
		glm.vec2(0, 1/2),
		glm.vec2(0, 1),
		glm.vec2(1/3, 0),
		glm.vec2(1/3, 1/2),
		glm.vec2(1/3, 1),
		glm.vec2(2/3, 0),
		glm.vec2(2/3, 1/2),
		glm.vec2(2/3, 1),
		glm.vec2(1, 0),
		glm.vec2(1, 1/2),
		glm.vec2(1, 1)
	)
	
	posCoordIndicies = (
		(2, 2), (6, 1), (3, 5), (7, 4),
		(2, 1), (0, 0), (6, 4), (4, 3),
		(7, 5), (5, 4), (3, 8), (1, 7),
		(6, 4), (4, 3), (7, 7), (5, 6),
		(3, 8), (1, 7), (2, 11), (0, 10),
		(4, 7), (0, 6), (5, 10), (1, 9)
	)
	
	verticies = []
	for i in range(len(posCoordIndicies)):
		verticies = verticies + [
			positions[posCoordIndicies[i][0]].x,
			positions[posCoordIndicies[i][0]].y,
			positions[posCoordIndicies[i][0]].z
		]
		verticies = verticies + [normals[int(i/4)].x, normals[int(i/4)].y, normals[int(i/4)].z]
		verticies = verticies + [texCoords[posCoordIndicies[i][1]].x, texCoords[posCoordIndicies[i][1]].y]
	verticies = numpy.array(verticies, dtype=numpy.float32)
	
	vbo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
	gl.glBufferData(gl.GL_ARRAY_BUFFER, verticies.nbytes, verticies, gl.GL_STATIC_DRAW)
	
	triangles = []
	for i in range(6):
		triangles = triangles + [
			4*i+1, 4*i+2, 4*i,
			4*i+1, 4*i+3, 4*i+2
		]
	triangles = numpy.array(triangles, dtype=numpy.uint32)
	
	ebo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
	gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, triangles.nbytes, triangles, gl.GL_STATIC_DRAW)
	
	return (vbo, 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), ebo, 12, 3)
