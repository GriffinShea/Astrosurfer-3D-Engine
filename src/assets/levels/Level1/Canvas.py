from config import *

from Renderer import Renderer

from Core.Systems.Physics.rb import rb

from Core.Props.Transf import Transf
from Core.Props.Physics.Rigidbody import Rigidbody

class Canvas:
	bgColour = glm.vec3(0.55, 0.65, 0.75)/16
	baseAmbience = glm.vec3(0.1)
	fogRange = glm.vec2(0, 1)
	
	
	@classmethod
	def drawUI(cls, index):
		#player progress
		distance = round(glm.distance(
			index.get(index.getSing("ragdollkeys")["torso"])[Transf].cpos,
			index.get(index.getSing("rocketkey"))[Transf].cpos
		))
		vel = glm.length(rb.calcVel(
			index.get(index.getSing("ragdollkeys")["torso"])[Rigidbody],
			index.get(index.getSing("ragdollkeys")["torso"])[Transf]
		))
		vel = 0 if glm.isnan(vel) else vel
		speed = str(round(vel))
		Renderer.drawText(
			"DISTANCE TO SPACE SHIP: "+str(distance)+"m\nSPEED: "+speed+"m/s",
			"basicText",
			"fancyFont",
			{
				"colour": WHITE, "alpha": 0.5, "depth": -1,
				"transfMat": glm.scale(
					glm.translate(glm.mat4(), glm.vec3(-1, -0.75, 0)),
					glm.vec3(1, 1, 1)
				)
			}
		)
		
		#congradulations
		if index.getSing("handsOnRocket") == 2:
			Renderer.drawText(
				"CONGRADULATIONS!!!",
				"basicText",
				"fancyFont",
				{
					"colour": WHITE, "alpha": 0.5, "depth": -1,
					"transfMat": glm.scale(
						glm.translate(glm.mat4(), glm.vec3(-0.5, 0, 0)),
						glm.vec3(2, 4, 2)
					)
				}
			)
			
		#REVISIT:
		#	$the depth was 1 before the numpy update but now it must be -1 for text to show
		#	$the blending function appears to be off, setting alpha to 1 and 0 are both illegible
		Renderer.drawText(
			"FPS: " + str(Renderer.getAverageFrameRate()),
			"basicText",
			"fancyFont",
			{
				"colour": RED, "alpha": 0.5, "depth": -1,
				"transfMat": glm.scale(glm.translate(glm.mat4(), glm.vec3(0.75, 1, 0)), glm.vec3(1))
			}
		)
		return