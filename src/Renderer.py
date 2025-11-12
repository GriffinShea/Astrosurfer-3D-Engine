from config import *
from ResourceManager import ResourceManager

class Renderer:
	currentShader = None
	boundTextures = 0
	
	clock = None
	lTime = 0
	dTime = 0
	
	suppressWarnings = False
	triangleCounter = 0
	pointCounter = 0
	patchCounter = 0
	
	getSpecialUniforms = {
		"RESOLUTION": lambda cls: FRAME_BUFFER_DIMS,
		"JIGGLE_FACTOR": lambda cls: JIGGLE_FACTOR,
		"CAM_TO_TEX_MAT": lambda cls: glmh.CAM_TO_TEX_MAT,
		"ATTENTUATION_RANGE": lambda cls: ATTENTUATION_RANGE,
		"RUN_TIME": lambda cls: cls.lTime
	}
	buffers = {}
	textures = {}
	
	@classmethod
	def init(cls):
		print("Initializing Renderer...")
	
		#setup pygame window and create clock
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(600, 32)
		pygame.init()
		if FULLSCREEN:
			pygame.display.set_mode(WINDOW_DIMS, pygame.FULLSCREEN|DOUBLEBUF|OPENGL)
		else:
			pygame.display.set_mode(WINDOW_DIMS, DOUBLEBUF|OPENGL)
		print("\tPygame window opened with OpenGL version:\n\t\t", gl.glGetString(gl.GL_VERSION))
	
		#OPENGL SETTINGS
		#set background colour and clear
		gl.glClearColor(0, 0, 0, 0)
		#setup z-buffer function
		gl.glEnable(gl.GL_DEPTH_TEST)
		gl.glDepthFunc(gl.GL_LEQUAL)
		#setup blend function
		gl.glDisable(gl.GL_BLEND)
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
		gl.glBlendEquation(gl.GL_FUNC_ADD)
		#size for GL_LINE, and GL_POINT
		gl.glPointSize(POINT_SIZE)
		gl.glLineWidth(LINE_SIZE)
		#sets front faces to CCW and removes backword faces
		gl.glFrontFace(gl.GL_CCW)
		gl.glEnable(gl.GL_CULL_FACE)
		gl.glCullFace(gl.GL_BACK)
		#set provoking vertex mode
		gl.glProvokingVertex(gl.GL_FIRST_VERTEX_CONVENTION)
		
		#create main frame buffer and texture
		(
			cls.buffers["frame"],
			cls.textures["frame"]
		) = cls.createMainFrameBuffer()
		
		#create gBuffer and textures for the deferred rendering pipeline
		(
			cls.buffers["gBuffer"],
			cls.textures["gBuffer"]
		) = cls.createGBuffer()
		
		#create shadow map buffers and textures
		(
			cls.buffers["shadowMaps"],
			cls.textures["shadowMaps"]
		) = cls.createShadowMapBuffer()
		
		#load meshes, shaders, and textures
		ResourceManager.init()
		
		#get current time and create clock
		cls.clock = pygame.time.Clock()
		cls.lTime = pygame.time.get_ticks()
		
		#start tracemalloc to track memory usage
		if DEBUG_TRACEMALLOC or DEBUG_TRACEMALLOC_KiB_STATS:
			tracemalloc.start()
		
		print("Done.")
		return
	
	@classmethod
	def createMainFrameBuffer(cls):
		#create a frame buffer object
		buffer = gl.glGenFramebuffers(1)
		gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, buffer)
		
		#attach a texture to use as a colour buffer
		texture = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
		colourFormat = [gl.GL_RGBA8, gl.GL_RGBA4, gl.GL_RGBA2, gl.GL_R3_G3_B2][COLOUR_MODE]
		gl.glTexImage2D(
			gl.GL_TEXTURE_2D,
			0,
			colourFormat,
			FRAME_BUFFER_DIMS[0],
			FRAME_BUFFER_DIMS[1],
			0,
			gl.GL_RGB,
			gl.GL_UNSIGNED_BYTE,
			None
		)
		filterOption = gl.GL_LINEAR if FILTER_FRAME else gl.GL_NEAREST
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, filterOption)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, filterOption)
		gl.glFramebufferTexture(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, texture, 0)
		
		#attach a combination depth and stencil buffer
		renderBuffer = gl.glGenRenderbuffers(1)
		gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, renderBuffer)
		gl.glRenderbufferStorage(
			gl.GL_RENDERBUFFER,
			gl.GL_DEPTH24_STENCIL8,
			FRAME_BUFFER_DIMS[0],
			FRAME_BUFFER_DIMS[1]
		)
		gl.glFramebufferRenderbuffer(
			gl.GL_FRAMEBUFFER,
			gl.GL_DEPTH_STENCIL_ATTACHMENT,
			gl.GL_RENDERBUFFER,
			renderBuffer
		)
		
		return (buffer, texture)
	
	@classmethod
	def createGBuffer(cls):
		#create a frame buffer object
		buffer = gl.glGenFramebuffers(1)
		gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, buffer)
		
		#setup the texture array with four (4) colour attachments
		textureArray = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, textureArray)
		gl.glTexImage3D(
			gl.GL_TEXTURE_2D_ARRAY,
			0,
			gl.GL_RGBA16F,
			FRAME_BUFFER_DIMS[0],
			FRAME_BUFFER_DIMS[1],
			4,
			0,
			gl.GL_RGBA,
			gl.GL_FLOAT,
			None
		)
		gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
		gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
		gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
		gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
		drawBuffers = []
		for i in range(4):
			gl.glFramebufferTextureLayer(
				gl.GL_DRAW_FRAMEBUFFER,
				gl.GL_COLOR_ATTACHMENT0 + i,
				textureArray,
				0,
				i
			)
			drawBuffers.append(gl.GL_COLOR_ATTACHMENT0 + i)
		gl.glDrawBuffers(len(drawBuffers), numpy.array(drawBuffers))
		
		#attach a depth render buffer
		renderBuffer = gl.glGenRenderbuffers(1)
		gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, renderBuffer)
		gl.glRenderbufferStorage(
			gl.GL_RENDERBUFFER,
			gl.GL_DEPTH24_STENCIL8,
			FRAME_BUFFER_DIMS[0],
			FRAME_BUFFER_DIMS[1]
		)
		gl.glFramebufferRenderbuffer(
			gl.GL_FRAMEBUFFER,
			gl.GL_DEPTH_STENCIL_ATTACHMENT,
			gl.GL_RENDERBUFFER,
			renderBuffer
		)
		
		return (buffer, textureArray)
	
	@classmethod
	def createShadowMapBuffer(cls):
		#create a frame buffer object
		buffer = gl.glGenFramebuffers(1)
		gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, buffer)
		
		#attach a depth texture array for the shadow map
		textureArray = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, textureArray)
		gl.glTexImage3D(
			gl.GL_TEXTURE_2D_ARRAY,
			0,
			gl.GL_DEPTH_COMPONENT32,
			FRAME_BUFFER_DIMS[0],
			FRAME_BUFFER_DIMS[1],
			MAX_SINGLE_SHADOW_MAPS,
			0,
			gl.GL_DEPTH_COMPONENT,
			gl.GL_FLOAT,
			None
		)
		gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_BORDER)
		gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_BORDER)
		gl.glTexParameterfv(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_BORDER_COLOR, numpy.array([1, 1, 1, 1]))
		gl.glFramebufferTexture(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, textureArray, 0)
		gl.glDrawBuffer(gl.GL_NONE)
		
		return (buffer, textureArray)
	
	
	
	@classmethod
	def getAverageFrameRate(cls):
		return int(cls.clock.get_fps() * 100) / 100
	
	
	
	@classmethod
	def flipDisplay(cls):
		#prepare openGL to draw to window
		if GAMMA_CORRECTION:
			gl.glEnable(gl.GL_FRAMEBUFFER_SRGB)
		gl.glDisable(gl.GL_DEPTH_TEST)
		gl.glViewport(0, 0, WINDOW_DIMS[0], WINDOW_DIMS[1])
		gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
		
		#draw the framebuffer texture to the window, then flip buffer
		cls.drawFrameEffect("frameBuffer", {})
		pygame.display.flip()
		
		#prepare openGL to draw to the framebuffer, and clear the framebuffer
		if GAMMA_CORRECTION:
			gl.glDisable(gl.GL_FRAMEBUFFER_SRGB)
		gl.glEnable(gl.GL_DEPTH_TEST)
		gl.glViewport(0, 0, FRAME_BUFFER_DIMS[0], FRAME_BUFFER_DIMS[1])
		gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, cls.buffers["frame"])
		gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT|gl.GL_STENCIL_BUFFER_BIT)
		
		#increment frame, calculate dTime, and tick clock
		cTime = pygame.time.get_ticks()
		cls.dTime = (cTime - cls.lTime) / 1000
		cls.lTime = cTime
		
		if LIMIT_FRAME_RATE:
			cls.clock.tick(FRAME_RATE)
		else:
			cls.clock.tick()
		
		#print number of triangles, points, and patches drawn
		if DEBUG_RENDERER_OUTPUT:
			print(
				"FPS:", cls.getAverageFrameRate(),
				"\tTriangles:", cls.triangleCounter,
				"\tPoints:", cls.pointCounter,
				"\tPatches:", cls.patchCounter,
				"\tErrors:", gl.glGetError()
			)
		cls.triangleCounter = 0
		cls.pointCounter = 0
		cls.patchCounter = 0
		
		#print memory usage
		if DEBUG_TRACEMALLOC:
			tracemalloc.take_snapshot()
			currPeak = tracemalloc.get_traced_memory()
			print(
				"Current memory:", currPeak[0],
				"\tPeak memory:", currPeak[1],
				"\tUnreachable items:", gc.collect()
			)
		
		if DEBUG_TRACEMALLOC_KiB_STATS:
			stats = tracemalloc.take_snapshot().statistics("lineno")
			for stat in stats:
				if str(stat).find("KiB") > 0:
					print(stat)
			print()
		
		return
	
	@classmethod
	def bindAndClearShadowBuffer(cls):
		gl.glCullFace(gl.GL_FRONT)
		gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, cls.buffers["shadowMaps"])
		gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
		return
	
	@classmethod
	def bindAndClearGBuffer(cls, gBufferClearColour):
		gl.glCullFace(gl.GL_BACK)
		gl.glPolygonMode(gl.GL_FRONT, [gl.GL_FILL, gl.GL_LINE, gl.GL_POINT][POLYGON_MODE])
		gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, cls.buffers["gBuffer"])
		gl.glClearColor(gBufferClearColour.x, gBufferClearColour.y, gBufferClearColour.z, 0)
		gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT|gl.GL_STENCIL_BUFFER_BIT)
		gl.glClearColor(0, 0, 0, 0)
		return
	
	@classmethod
	def renderGBuffer(cls, uniformDict):
		gl.glPolygonMode(gl.GL_FRONT, gl.GL_FILL)
		gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, cls.buffers["frame"])
		gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT|gl.GL_STENCIL_BUFFER_BIT)
		cls.drawFrameEffect("gBuffer", uniformDict)
		return
	
	
	
	@classmethod
	def setupMesh(cls, mesh):
		#bind the VBO, EBO then tell the GPU how to read the verticies
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, mesh[0])
		gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, mesh[3])
		stride = 0
		for i in range(len(mesh[2])):
			gl.glEnableVertexAttribArray(i)
			gl.glVertexAttribPointer(
				i,
				mesh[2][i][0],
				mesh[2][i][1],
				gl.GL_FALSE,
				mesh[1]*4,
				gl.ctypes.c_void_p(stride*4)
			)
			stride += mesh[2][i][0]
		return
	
	@classmethod
	def setupShaderUniforms(cls, shaderName, values):
		(program, defs) = ResourceManager.getShader(shaderName)
		
		cls.currentShader = program
		gl.glUseProgram(cls.currentShader)
		
		uniforms = set(defs.keys())
		
		#remove phantom uniforms which are set manually in the draw functions
		if "charPos" in uniforms:
			uniforms.remove("charPos")
		if "character" in uniforms:
			uniforms.remove("character")
		
		#fill each uniform with a texture or value from the values dict or the Renderer
		cls.boundTextures = 0
		for uniform in uniforms:
			if uniform in values:
				if defs[uniform] in cls.textureTypeSwitch:
					cls.bindTexture(
						uniform,
						defs[uniform],
						ResourceManager.getTexture(values[uniform])
					)
				else:
					cls.bindUniform(uniform, defs[uniform], values[uniform])
			elif uniform in cls.textures:
				cls.bindTexture(uniform, defs[uniform], cls.textures[uniform])
			elif uniform in cls.getSpecialUniforms:
				cls.bindUniform(uniform, defs[uniform], cls.getSpecialUniforms[uniform](cls))
			else:
				cls.writeWarning(
					uniform + " value missing from uniformDict or Renderer (shaderName="
					+ shaderName + ")."
				)
		return
	
	textureTypeSwitch = {
		"sampler2D": gl.GL_TEXTURE_2D,
		"sampler2DArray": gl.GL_TEXTURE_2D_ARRAY
	}
	
	@classmethod
	def bindTexture(cls, uniformName, uniformType, location):
		gl.glUniform1i(
			gl.glGetUniformLocation(cls.currentShader, uniformName),
			cls.boundTextures
		)
		gl.glActiveTexture(gl.GL_TEXTURE0 + cls.boundTextures)
		gl.glBindTexture(cls.textureTypeSwitch[uniformType], location)
		cls.boundTextures += 1
		return
	
	uniformFunctionSwitch = {
		"float":	gl.glUniform1fv,
		"vec2":		gl.glUniform2fv,
		"vec3":		gl.glUniform3fv,
		"vec4":		gl.glUniform4fv,
		
		"int":		gl.glUniform1iv,
		"ivec2":	gl.glUniform2iv,
		"ivec3":	gl.glUniform3iv,
		"ivec4":	gl.glUniform4iv,
		
		"uint":		gl.glUniform1uiv,
		"uvec2":	gl.glUniform2uiv,
		"uvec3":	gl.glUniform3uiv,
		"uvec4":	gl.glUniform4uiv,
		
		"mat2":		gl.glUniformMatrix2fv,
		"mat2x3":	gl.glUniformMatrix2x3fv,
		"mat2x4":	gl.glUniformMatrix2x4fv,
		
		"mat3x2":	gl.glUniformMatrix3x2fv,
		"mat3":		gl.glUniformMatrix3fv,
		"mat3x4":	gl.glUniformMatrix3x4fv,
		
		"mat4x2":	gl.glUniformMatrix4x2fv,
		"mat4x3":	gl.glUniformMatrix4x3fv,
		"mat4":		gl.glUniformMatrix4fv
	}
	
	uniformArgumentSwitch = {
		"f": lambda value: [numpy.array(value, dtype=numpy.float32)],
		"v": lambda value: [numpy.array(value, dtype=numpy.float32)],
		"i": lambda value: [numpy.array(value, dtype=numpy.int32)],
		"u": lambda value: [numpy.array(value, dtype=numpy.uint32)],
		"m": lambda value: [gl.GL_FALSE, numpy.array(value, dtype=numpy.float32)],
	}
	
	@classmethod
	def bindUniform(cls, uniformName, uniformType, value):
		if uniformType in cls.uniformFunctionSwitch:
			if type(value) == list and uniformType[0] == "m":
				value = [numpy.array(v, dtype=numpy.float32) for v in value]
			
			cls.uniformFunctionSwitch[uniformType](
				gl.glGetUniformLocation(cls.currentShader, uniformName),
				len(value) if type(value) == list else 1,
				*cls.uniformArgumentSwitch[uniformType[0]](value)
			)
		else:
			cls.writeWarning(
				"unhandled uniform type ("
				+ defs[uniform]
				+ ") in following shader definition:\n\t"
				+ defs
			)
		return
	
	@classmethod
	def drawTriangles(cls, count):
		gl.glDrawElements(gl.GL_TRIANGLES, count * 3, gl.GL_UNSIGNED_INT, None)
		cls.triangleCounter += count
		return

	#REVISIT: quads is depreciated!
	@classmethod
	def drawQuads(cls, count):
		gl.glDrawElements(gl.GL_QUADS, count * 4, gl.GL_UNSIGNED_INT, None)
		cls.triangleCounter += count * 2
		return
	
	@classmethod
	def writeWarning(cls, message):
		if not cls.suppressWarnings:
			print("WARNING:", message)
		return
	
	
	
	@classmethod
	def drawFrameEffect(cls, shaderName, uniformDict):
		#drawing a frame effect is exactly like drawing a sprite but with depth test disabled
		gl.glDisable(gl.GL_DEPTH_TEST)
		cls.drawSprite(shaderName, uniformDict)
		gl.glEnable(gl.GL_DEPTH_TEST)
		return
	
	@classmethod
	def drawSprite(cls, shaderName, uniformDict):
		#get mesh and shader and setup to draw
		mesh = ResourceManager.getMesh("frame")
		cls.setupMesh(mesh)
		cls.setupShaderUniforms(shaderName, uniformDict)
		
		#draw with blending enabled
		gl.glEnable(gl.GL_BLEND)
		cls.drawTriangles(mesh[4])
		gl.glDisable(gl.GL_BLEND)
		
		return
	
	@classmethod
	def drawText(cls, string, shaderName, fontName, uniformDict):
		#get the mesh and bind it
		mesh = ResourceManager.getMesh("frame")
		cls.setupMesh(mesh)
		
		#add font to uniforms, activate shader and load up uniforms
		font = ResourceManager.getFont(fontName)
		uniformDict["bitmap"] = font[0]
		uniformDict["bitmapDims"] = font[1]
		uniformDict["transfMat"] = glm.scale(
			uniformDict["transfMat"],
			glm.vec3(font[2][0] * PIXEL_DIMS[0], font[2][1] * PIXEL_DIMS[1], 1)
		)
		cls.setupShaderUniforms(shaderName, uniformDict)
		
		#draw string character by character incrementing position with blending enabled
		gl.glEnable(gl.GL_BLEND)
		charPos = glm.vec2(0.5, 0.5)
		for i in range(len(string)):
			if string[i] == '\n':
				charPos.y += 1
				charPos.x = 0.5
			elif string[i] == '\t':
				charPos.x = ((charPos.x // 4) + 1) * 4 + 0.5
			else:
				cls.bindUniform("character", "int", ord(string[i]) - 32)
				cls.bindUniform("charPos", "vec2", charPos)
				cls.drawTriangles(mesh[4])
				charPos.x += 1
		gl.glDisable(gl.GL_BLEND)
		
		return

	@classmethod
	def drawTextureParticles(cls, shaderName, uniformDict, count):
		#get mesh and shader and setup to draw
		mesh = ResourceManager.getMesh("square")
		cls.setupMesh(mesh)
		cls.setupShaderUniforms(shaderName, uniformDict)
		
		#draw count instances of the particle with cull face disabled to save two triangles
		gl.glDisable(gl.GL_CULL_FACE)
		gl.glDrawElementsInstanced(
			gl.GL_TRIANGLES,
			mesh[4]*3,
			gl.GL_UNSIGNED_INT,
			gl.ctypes.c_void_p(0),
			count
		)
		gl.glEnable(gl.GL_CULL_FACE)
		cls.triangleCounter += mesh[4] * count
		
		return

	@classmethod
	def drawPointParticles(cls, shaderName, uniformDict, count, pointSize):
		#get mesh and shader and setup to draw
		mesh = ResourceManager.getMesh("nullElement")
		cls.setupMesh(mesh)
		cls.setupShaderUniforms(shaderName, uniformDict)
		
		#draw count instances of the particle
		gl.glPointSize(pointSize)
		gl.glDrawElementsInstanced(
			gl.GL_POINTS,
			1,
			gl.GL_UNSIGNED_INT,
			gl.ctypes.c_void_p(0),
			count
		)
		cls.pointCounter += count
		
		return
	
	@classmethod
	def mapModelShadow(cls, meshName, uniformDict):
		#get mesh and shader and setup to draw
		mesh = ResourceManager.getMesh(meshName)
		cls.setupMesh(mesh)
		cls.setupShaderUniforms("mapModelShadow", uniformDict)
		
		#draw model
		if mesh[5] == 3:
			cls.drawTriangles(mesh[4])
		elif mesh[5] == 4:
			cls.drawQuads(mesh[4])
		
		return
	
	@classmethod
	def drawModel(cls, meshName, shaderName, uniformDict):
		#get mesh and shader and setup to draw
		mesh = ResourceManager.getMesh(meshName)
		cls.setupMesh(mesh)
		cls.setupShaderUniforms(shaderName, uniformDict)
		
		#draw model
		if mesh[5] == 3:
			cls.drawTriangles(mesh[4])
		elif mesh[5] == 4:
			cls.drawQuads(mesh[4])
		
		if DEBUG_NORMALS:
			cls.drawNormals(mesh, uniformDict)
			
		return

	@classmethod
	def drawTesselatedModel(cls, meshName, shaderName, uniformDict):
		#get mesh and shader and setup to draw
		mesh = ResourceManager.getMesh(meshName)
		cls.setupMesh(mesh)
		cls.setupShaderUniforms(shaderName, uniformDict)
		
		#draw model
		gl.glPatchParameteri(gl.GL_PATCH_VERTICES, mesh[5])
		gl.glDrawElements(gl.GL_PATCHES, mesh[4]*mesh[5], gl.GL_UNSIGNED_INT, gl.ctypes.c_void_p(0))
		cls.patchCounter += mesh[4]
		
		if DEBUG_NORMALS:
			cls.drawNormals(mesh, uniformDict)
		
		return
	
	@classmethod
	def drawNormals(cls, mesh, uniformDict):
		if (
			mesh[2] == ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)) and
			mesh[5] == 3
		):
			cls.suppressWarnings = True
			cls.setupShaderUniforms("normals", uniformDict)
			gl.glDrawElements(
				gl.GL_TRIANGLES,
				mesh[4]*mesh[5],
				gl.GL_UNSIGNED_INT,
				gl.ctypes.c_void_p(0)
			)
			cls.suppressWarnings = False
		return
