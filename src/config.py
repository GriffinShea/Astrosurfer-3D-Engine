#import libraries
import collections
import sys
import os
import time
import random
import gc
import json

import numpy
import attr
import tracemalloc

print("Python version:", sys.version)

print("Importing pygame:")
import pygame
from pygame.locals import *
print()

import OpenGL.GL as gl
from OpenGL.GL import shaders

import glm
import glmh

from constants import *

#game settings
MOUSE_SENSITIVITY = glm.vec2(60, 30)
INVERT_Y = False

#game engine constants
COLLISION_MAX_ITERATIONS = 8
RESOLVE_CONSTRAINTS_ITERATIONS = 8
GRAVITY = 9.807
DEFAULT_COEFF_REST = 0
DEFAULT_MEW_STATIC = 1
DEFAULT_MEW_DYNAMIC = 0.5
FLUID_FRICTION = 0.25

#display settings
LIMIT_FRAME_RATE = False
FRAME_RATE = 60
FRAME_TIME = 1000 / FRAME_RATE
FULLSCREEN = False
if FULLSCREEN:
	WINDOW_DIMS = (1920, 1080)
else:
	WINDOW_DIMS = (1280, 960)
FRAME_BUFFER_DIMS = (320, 240)
FRAME_BUFFER_DIMS = (640, 480)
FRAME_BUFFER_DIMS = (1280, 960)
#FRAME_BUFFER_DIMS = (1920, 1080)
FRAME_RATIO = FRAME_BUFFER_DIMS[0] / FRAME_BUFFER_DIMS[1]
PIXEL_DIMS = glm.vec2(1/FRAME_BUFFER_DIMS[0], 1/FRAME_BUFFER_DIMS[1])
NEAR_CLIPPING_PLANE = 0.1
FAR_CLIPPING_PLANE = 250

#graphics and shader settings
POINT_SIZE = 4
LINE_SIZE = 2

MIN_FILTER_LEVEL = 0
MAG_FILER = False
FILTER_FRAME = True
COLOUR_MODE = 0	#[gl.GL_RGBA8, gl.GL_RGBA4, gl.GL_RGBA2, gl.GL_R3_G3_B2][COLOUR_MODE]

HORI_BLUR = False
JIGGLE_FACTOR = 4
GAMMA_CORRECTION = False

MAX_LIGHTS = 16	#duplicated in master shader files
MAX_SINGLE_SHADOW_MAPS = 8
ATTENTUATION_RANGE = 32
LIGHT_AMBIENCE_FACTOR = 1 / 32
SHADOW_BUFFER_DIMS = (2048, 2048)
#SHADER SETTINGS REFERENCE:
#	0 1 2 3
#	0   0 0
#	P B S F
#	G P
#	F
#
#	1: (P)hong, (G)ouraud, (F)lat, or no shading (0)
#	2: (B)linn-Phong or (P)hong specularity calculation
#	3: enable (S)hadow mapping or not (0) (only supported for phong shading)
#	3: enable (F)og or not (0)
#
GLOBAL_SHADER_SETTING = "PBSF"
SHADOW_MAPPING = GLOBAL_SHADER_SETTING[2] == "S"

#debug modes
DEBUG_SUPPRESS_WARNINGS = True
DEBUG_PRINT_SHADERS = False
DEBUG_RENDERER_OUTPUT = False
DEBUG_TRACEMALLOC = False
DEBUG_TRACEMALLOC_KiB_STATS = False

POLYGON_MODE = 0	#[gl.GL_FILL, gl.GL_LINE, gl.GL_POINT]
DEBUG_NORMALS = False			#NOTE: this mode only works for triangles because there is no
								#geometry shader support for quads
