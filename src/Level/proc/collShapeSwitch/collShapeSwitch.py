from config import *

from Level.proc.collShapeSwitch.Sphere import Sphere
from Level.proc.collShapeSwitch.Capsule import Capsule
from Level.proc.collShapeSwitch.Cylinder import Cylinder
from Level.proc.collShapeSwitch.Box import Box
from Level.proc.collShapeSwitch.Ray import Ray

COLLSHAPESWITCH = {
	COLLSPHERE: Sphere,
	COLLCAPSULE: Capsule,
	COLLCYLINDER: Cylinder,
	COLLBOX: Box,
	COLLRAY: Ray
}

def collShapeSwitch(shape):
	return COLLSHAPESWITCH[shape]
