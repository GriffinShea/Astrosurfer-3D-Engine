from config import *

class ShaderHelper:
	@staticmethod
	def loadShaderFromGLSLH(glslhName):
		if DEBUG_PRINT_SHADERS:
			print("loading ", glslhName, ".glslh", sep="")
		
		with open("assets//shaders//headers//" + glslhName + ".glslh") as headerFile:
			shaderDict = json.load(headerFile)
			mask = ""
			if "mask" in shaderDict:
				mask = shaderDict["mask"]
				del shaderDict["mask"]
			
			return ShaderHelper.createShader(mask, shaderDict)
	
	@staticmethod
	def createShaderFromMask(mask):
		if DEBUG_PRINT_SHADERS:
			print("creating shader with mask:", mask)
		if mask[1] != "0":
			return ShaderHelper.createShader(mask, {
				"vert": "engine//tess.vert",
				"tesc": "masters//tess.tesc",
				"tese": "masters//vertex.glsl",
				"frag": "masters//master.frag"
			})
		else:
			return ShaderHelper.createShader(mask, {
				"vert": "masters//vertex.glsl",
				"frag": "masters//master.frag"
			})
	
	@staticmethod
	def createShader(mask, shaderDict):
		if DEBUG_PRINT_SHADERS:
			print(mask, shaderDict)
		shaderTypes = {
			"vert": gl.GL_VERTEX_SHADER,
			"geom": gl.GL_GEOMETRY_SHADER,
			"frag": gl.GL_FRAGMENT_SHADER,
			"tesc": gl.GL_TESS_CONTROL_SHADER,
			"tese": gl.GL_TESS_EVALUATION_SHADER
		}
		
		uniformDefs = {}
		shadersList = []
		for glslType in shaderDict.keys():
			if shaderDict[glslType].startswith("masters//"):
				shaderString = ShaderHelper.generateShader(mask, shaderDict[glslType])
			else:
				shaderString = open("assets//shaders//source//" + shaderDict[glslType]).read()
			uniformDefs = uniformDefs | ShaderHelper.parseUniformDefs(shaderString)
			shader = shaders.compileShader(shaderString, shaderTypes[glslType])
			shadersList.append(shader)
		
		program = shaders.compileProgram(*shadersList)
		return (program, uniformDefs)
	
	@staticmethod
	def parseUniformDefs(shaderString):
		uniformDefs = {}
		for line in shaderString.split("\n"):
			if line[:7] == "uniform":
				lineSplit = line[:-1].split(" ")
				lineSplit[2] = lineSplit[2].split("[")
				uniformDefs[lineSplit[2][0]] = lineSplit[1]
		return uniformDefs
	
	@staticmethod
	def generateShader(eMask, filename):
		#open and read the file ignoring irrelevant lines based on two char tags in the iMask
		iMask = ShaderHelper.convertMask(eMask)
		with open("assets//shaders//source//" + filename) as masterFile:
			shader = "//THIS SHADER GENERATED WITH MASK: " + eMask + "\n"
			while True:
				line = masterFile.readline()
				if not line:
					break
				
				if line[0] == "$":
					if line[1:3] in iMask:
						shader += line[3:]
				else:
					shader += line
		if DEBUG_PRINT_SHADERS:
			ShaderHelper.printShader(shader)
		return shader
	
	@staticmethod
	def convertMask(eMask):
		iMask = set()
		
		#lighting options:
		#	(P) Phong shading (fragment by fragment), (G) Gouraud shading (vertex by vertex),
		#		(F) flat shading (face by face), (0) no shading
		#	(P) Phong specularity, (B) Blinn-Phong specularity
		#	(M) shadow mapping, (0) no shadow mapping
		#	(F) fog, (0) no fog
		if GLOBAL_SHADER_SETTING[0] == "0":
			iMask.add("NL")
		else:
			iMask.add("LA")
			if GLOBAL_SHADER_SETTING[0] == "P":
				iMask.add("PA")
				iMask.add("P" + GLOBAL_SHADER_SETTING[1])
				if GLOBAL_SHADER_SETTING[2] == "S":
					iMask.add("SM")
			else:
				iMask.add("VA")
				iMask.add("V" + GLOBAL_SHADER_SETTING[1])
				iMask.add("V" + GLOBAL_SHADER_SETTING[0])
		if GLOBAL_SHADER_SETTING[3] == "F":
			iMask.add("FE")
		
		if eMask:
			#vertex effect option: (B) basic, (X) psx
			if eMask[0] == "B":
				iMask.add("BA")
			elif eMask[0] == "X":
				iMask.add("XA")
			else:
				print("WARNING: bad mask -->", eMask, "@ position 0.")
			
			#tesselator option: (T) triangle, (Q) quads
			if eMask[1] == "T" or eMask[1] == "Q":
				iMask.add("TE")
				iMask.add("T" + eMask[1])
			elif eMask[1] == "0":
				iMask.add("TD")
			else:
				print("WARNING: bad mask -->", eMask, "@ position 1.")
			
			#lighting option: (L) enable lighting, (0) do not enable
			if eMask[2] == "L":
				iMask.add("LE")
			elif eMask[2] == "0":
				iMask.add("LD")
			else:
				print("WARNING: bad mask -->", eMask, "@ position 2.")
			
			#colouring option: (T) texture, (U) uniform, (I) interpolated, (S) static
			validOptions = set([char for char in "TUISV"])
			if eMask[3] in validOptions:
				iMask.add("C" + eMask[3])
			else:
				print("WARNING: bad mask -->", eMask, "@ position 3.")
			
			#invert colour option: (I) enable invert colour, (0) do not enable
			if eMask[4] == "I":
				iMask.add("IE")
			elif eMask[4] == "0":
				pass
			else:
				print("WARNING: bad mask -->", eMask, "@ position 4.")
		
		if DEBUG_PRINT_SHADERS:
			print(GLOBAL_SHADER_SETTING, eMask, "-->", iMask)
		
		return iMask
	
	@staticmethod
	def printShader(shader):
		shaderLines = shader.split("\n")
		for i in range(len(shaderLines)):
			print(i, shaderLines[i])
		print()
		return
	