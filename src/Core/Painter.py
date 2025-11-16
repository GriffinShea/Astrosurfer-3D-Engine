from config import *
from Renderer import Renderer

from Core.Props.Transf import Transf
from Core.Props.Timer import Timer

from Core.Props.Graphics.Camera import Camera
from Core.Props.Graphics.Rend import Rend
from Core.Props.Graphics.Sprite import Sprite
from Core.Props.Graphics.Model import Model
from Core.Props.Graphics.ParticleEffect import ParticleEffect
from Core.Props.Graphics.Segment import Segment
from Core.Props.Graphics.KeySegment import KeySegment

from Core.Props.Graphics.Lights import Light
from Core.Props.Graphics.Lights import PointLight
from Core.Props.Graphics.Lights import DirLight
from Core.Props.Graphics.Lights import SpotLight

class Painter:
	@classmethod
	def paint(cls, index, canvas):
		cameraobj = index.get(index.getSing("camerakey"))
		lightingDict = cls.getLightingDict(index, canvas)
		cls.updateUniforms(index)
		
		#render each model to the shadow buffer
		if SHADOW_MAPPING:
			Renderer.bindAndClearShadowBuffer()
			cls.drawModelShadows(index, lightingDict)
		
		#render each model, particle, and segment to the gBuffer
		sceneDict = lightingDict | {
			"projMat": glmh.calcPerspectiveMat(glm.radians(cameraobj[Camera].fov)/2),
			"viewMat": glmh.calcViewMat(cameraobj[Transf].cpos, cameraobj[Transf].cori),
			"cameraPos": cameraobj[Transf].cpos,
			
			"fogDensity": canvas.fogRange.x,
			"fogGradient": canvas.fogRange.y,
		}
		Renderer.bindAndClearGBuffer(canvas.bgColour)
		cls.drawModels(index, sceneDict)
		cls.drawParticleEffects(index, sceneDict)
		cls.drawSegments(index, sceneDict)
		cls.drawSprites(index)
		
		#finally, use gBuffer to render the final scene frame
		sceneDict = lightingDict | {
			"viewMat": glmh.calcViewMat(cameraobj[Transf].cpos, cameraobj[Transf].cori),
			"fogColour": canvas.bgColour
		}
		
		canvas.drawUI(index)
		
		Renderer.renderGBuffer(sceneDict)
		
		return
	
	@staticmethod
	def getLightingDict(index, canvas):
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
		globalAmbience = canvas.baseAmbience + sum(ambiences)
		
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
					glmh.calcOrthographicMat(glm.vec2(lightTypeProp.shadowRange))
					* glmh.calcViewMat(p, glm.quatLookAt(glm.normalize(p), glmh.yUnit()))
				]
			
			elif isinstance(lightTypeProp, SpotLight):
				lightTypes += [3]
				shadowMats += [
					glmh.calcPerspectiveMat(glm.radians(lightTypeProp.cutoff.y)/2)
					* glmh.calcViewMat(
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
	
	@staticmethod
	def updateUniforms(index):
		for (timer, rend) in index.match(Timer, Rend):
			rend.uniformDict["time"] = timer.time
			
		for (rend, transf) in index.match(Rend, Transf):
			rend.uniformDict["worldMat"] = transf.calcMatrix()
		
		for (sprice, rend, transf) in index[Sprite, Rend, Transf]:
			rend.uniformDict["transfMat"] = glm.scale(
				glm.translate(glm.mat4(), transf.cpos),
				glm.vec3(transf.scale.x, transf.scale.y, 1)
			)
			rend.uniformDict["depth"] = transf.cpos.z
		
		return
	@staticmethod
	def drawModelShadows(index, sceneDict):
		for (model, rend) in index[Model, Rend]:
			if rend.visible and model.castShadow:
				Renderer.mapModelShadow(
					model.mesh,
					sceneDict | rend.uniformDict,
				)
		return
	@staticmethod
	def drawModels(index, sceneDict):
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
	@staticmethod
	def drawParticleEffects(index, sceneDict):
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
	@staticmethod
	def drawSegments(index, sceneDict):
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
	@staticmethod
	def drawSprites(index):
		for (sprite, rend) in index[Sprite, Rend]:
			if rend.visible:
				Renderer.drawSprite(
					rend.shader,
					rend.uniformDict
				)
		return
	