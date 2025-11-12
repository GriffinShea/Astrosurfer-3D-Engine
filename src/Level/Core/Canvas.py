from config import *
from Renderer import Renderer

from Level.Props.Transf import Transf

from Level.Props.Rendering.Camera import Camera
from Level.Props.Rendering.Rend import Rend
from Level.Props.Rendering.Sprite import Sprite
from Level.Props.Rendering.Model import Model
from Level.Props.Rendering.ParticleEffect import ParticleEffect
from Level.Props.Rendering.Segment import Segment
from Level.Props.Rendering.KeySegment import KeySegment

from Level.Props.Rendering.Lighting.Light import Light
from Level.Props.Rendering.Lighting.PointLight import PointLight
from Level.Props.Rendering.Lighting.DirLight import DirLight
from Level.Props.Rendering.Lighting.SpotLight import SpotLight

class Canvas:
	def __init__(self, bgColour, baseAmbience, fogRange):
		self.bgColour = bgColour
		self.baseAmbience = baseAmbience
		self.fogRange = fogRange
		return
	
	def drawFromIndex(self, index):
		cameraobj = index.get(index.getSing("camerakey"))
		lightingDict = self.getLightingDict(index)
		
		#render each model to the shadow buffer
		if SHADOW_MAPPING:
			Renderer.bindAndClearShadowBuffer()
			self.drawModelShadows(index, lightingDict)
		
		#render each model, particle, and segment to the gBuffer
		sceneDict = lightingDict | {
			"projMat": Canvas.calcPerspectiveMat(glm.radians(cameraobj[Camera].fov)/2),
			"viewMat": Canvas.calcViewMat(cameraobj[Transf].cpos, cameraobj[Transf].cori),
			"cameraPos": cameraobj[Transf].cpos,
			
			"fogDensity": self.fogRange.x,
			"fogGradient": self.fogRange.y,
		}
		Renderer.bindAndClearGBuffer(self.bgColour)
		self.drawModels(index, sceneDict)
		self.drawParticleEffects(index, sceneDict)
		self.drawSegments(index, sceneDict)
		self.drawSprites(index)
		
		#finally, use gBuffer to render the final scene frame
		sceneDict = lightingDict | {
			"viewMat": Canvas.calcViewMat(cameraobj[Transf].cpos, cameraobj[Transf].cori),
			"fogColour": self.bgColour
		}
		Renderer.renderGBuffer(sceneDict)
		
		return
	
	def getLightingDict(self, index):
		lights = index[Light]
		
		pointLights = index[PointLight, Light, Transf]
		dirLights = index[DirLight, Light, Transf]
		spotLights = index[SpotLight, Light, Transf]
		
		lights = pointLights + dirLights + spotLights
		
		ambiences = [
			light.intensity * light.colour * LIGHT_AMBIENCE_FACTOR
			for (_, light, _)
			in lights
		]
		globalAmbience = self.baseAmbience + sum(ambiences)
		
		lightTypes = []
		shadowMats = []
		spotLights = []
		for (lightTypeProp, light, transf) in lights:
			if isinstance(lightTypeProp, PointLight):
				lightTypes += [1]
			
			elif isinstance(lightTypeProp, DirLight):
				lightTypes += [2]
				#REVISIT: this crap (literally doesnt even work) (no shadows anyway
				p = transf.cori * glmh.yUnit() * lightTypeProp.distance
				shadowMats += [
					Canvas.calcOrthographicMat(glm.vec2(lightTypeProp.shadowRange))
					* Canvas.calcViewMat(p, glm.quatLookAt(glm.normalize(p), glmh.yUnit()))
				]
			
			elif isinstance(lightTypeProp, SpotLight):
				lightTypes += [3]
				shadowMats += [
					Canvas.calcPerspectiveMat(glm.radians(lightTypeProp.cutoff.y)/2)
					* Canvas.calcViewMat(
						transf.cpos,
						glm.quatLookAt(
							transf.cori * -lightTypeProp.direction,
							glmh.yUnit()
						)
					)
				]
		
		lightingDict = {
			"globalAmbience": globalAmbience,
			"lightCount": len(lightTypes),
			"lightTypes": lightTypes,
			"lightIntensities": [
				light.intensity
				for (_, light, _)
				in lights
			],
			"lightColours": [
				light.colour
				for (_, light, _)
				in lights
			],
			"lightPositions": [
				transf.cori * glmh.yUnit() * dirLight.distance
				if isinstance(dirLight, DirLight)
				else transf.cpos
				for (dirLight, light, transf)
				in lights
			],
			"spotLightCutoffs": [
				glm.cos(glm.radians(spotLight.cutoff))
				for (spotLight, _, _)
				in spotLights
			],
			"spotLightDirections": [
				transf.cori * spotLight.direction
				for (spotLight, _, transf)
				in spotLights
			],
			"shadowMats": shadowMats
		}
		return lightingDict
	
	def drawModelShadows(self, index, sceneDict):
		for (model, rend) in index[Model, Rend]:
			if rend.visible and model.castShadow:
				Renderer.mapModelShadow(
					model.mesh,
					sceneDict | rend.uniformDict,
				)
		return
	
	def drawModels(self, index, sceneDict):
		for (model, rend) in index[Model, Rend]:
			if rend.visible:
				if model.tesselated:
					Renderer.drawTesselatedModel(
						model.mesh,
						rend.shader,
						sceneDict | rend.uniformDict,
					)
				else:
					Renderer.drawModel(
						model.mesh,
						rend.shader,
						sceneDict | rend.uniformDict,
					)
		return
	
	def drawParticleEffects(self, index, sceneDict):
		for (particleEffect, rend) in index[ParticleEffect, Rend]:
			if rend.visible:
				if particleEffect.pointSize == 0:
					Renderer.drawTextureParticles(
						rend.shader,
						sceneDict | rend.uniformDict,
						particleEffect.count
					)
				else:
					Renderer.drawPointParticles(
						rend.shader,
						sceneDict | rend.uniformDict,
						particleEffect.count,
						particleEffect.pointSize
					)
		return
	
	def drawSegments(self, index, sceneDict):
		for (segment, rend, transf) in index[Segment, Rend, Transf]:
			if rend.visible:
				Renderer.drawModel(
					"nullElement",
					rend.shader,
					sceneDict | rend.uniformDict | {
						"pos0": transf.cpos,
						"pos1": transf.cpos + segment.destination
					}
				)
		for (keysegment, rend) in index[KeySegment, Rend]:
			if rend.visible:
				Renderer.drawModel(
					"nullElement",
					rend.shader,
					sceneDict | rend.uniformDict | {
						"pos0": index.get(keysegment.start)[Transf].cpos,
						"pos1": index.get(keysegment.end)[Transf].cpos
					}
				)
		return
	
	def drawSprites(self, index):
		for (sprite, rend) in index[Sprite, Rend]:
			if rend.visible:
				Renderer.drawSprite(
					rend.shader,
					rend.uniformDict
				)
		return
	
	@staticmethod
	def calcViewMat(pos, ori):
		#this is a mathematically well founded incantation
		#https://learnopengl.com/Getting-started/Camera
		currLeft = ori * glmh.xUnit()
		currUp = ori * glmh.yUnit()
		currBack = ori * -glmh.zUnit()
		
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
	
	@staticmethod
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
	
	@staticmethod
	def calcOrthographicMat(dims):
		return glm.ortho(
			-dims.x, dims.x,
			-dims.y, dims.y,
			NEAR_CLIPPING_PLANE, FAR_CLIPPING_PLANE
		)
	