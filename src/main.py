from config import *
from Renderer import Renderer
from Controller import Controller
from Game import Game

#===================================================================================================
#
#	v3.01
#
#	@commented out grappling hook from Level1.py
#	@discovered a problem in gBufferMaster.frag and bandaged it (see spotlight)
#
#	========================================================================================
#
#	REVISIT:
#	
#	$"glmh.zUnit() * self[Transf].scale.x" --> "glmh.vecZ(self[Transf].scale.x)"
#
#	$need to split Renderer into Renderer and System
#
#	$optimize Transf ?
#	$need to check BoxCollider.castRay's (use of scale)
#
#	$spotlight implementation must be double-checked
#
#	$cylinders with locked orientation do not like inclines
#	$rigidbody physics needs some work basically i would like collision manifolds instead of just
#		points and/or repeat collision detection and resolution until objects settle, maybe use
#		parallelism and increment timesteps???
#		(continuous detection would also be a nice addition)
#
#===================================================================================================

def main():
	random.seed(1250)#random.seed(time.time())
	Renderer.init()
	game = Game()
	print("\nStarting game loop...")
	print("================================================================\n")
	while game.state != 0:		#game.state != QUIT
		Controller.pollInput()
		game.update()
		game.draw()
		Renderer.flipDisplay()
	print("\n================================================================")
	print("Game loop exit.")
	return

if __name__ == "__main__":
	main()

exit()
