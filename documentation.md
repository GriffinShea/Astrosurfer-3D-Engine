#ASTROSURFER – v3.01
###By Griffin Shea

##INTRODUCTION AND PROJECT HISTORY

Astrosurfer began as an honours project I worked on in University in 2022 but did not complete. I dropped the course and decided to pursue other 4000-level classes in its place. The original, incomplete report for that project is available as-is in this GitHub repository titled incomplete_report.pdf.

I continued to develop the project afterwords in my spare time and I intend to make a few more improvements in the near future. This document is intended as a guide to the codebase and an introduction to its architectural design. It will be a work in progress so expect incompleteness. I feel that it may provide a good reference for novice programmers interested in learning to write code for real-time 3D games. If you’re interested in this project, feel free to contact me at griffin.shea@danjo.ca with any questions or suggestions you may have.

##DEPENDENCIES

This project makes use of six external libraries. They are:
-	PyGame – opens the game window and collects user input (https://www.pygame.org/)
-	PyOpenGL – 3D rendering using the GPU (https://mcfletch.github.io/pyopengl/documentation/index.html)
-	PyGLM – for vector, matrix, and quaternion mathematical operations (https://pypi.org/project/pyglm/)
-	Numpy – used in Renderer and ResourceManager classes to load data into OpenGL (https://pypi.org/project/numpy/)
-	Attr – enables simpler definitions for game data properties (see Props below) (https://www.attrs.org/en/stable/)
-	TraceMalloc – to track memory and other debugging purposes (https://docs.python.org/3/library/tracemalloc.html)

##MAIN – GAME LOOP, CONTROLLER, RENDERER, AND GAME

```
	from config import *
	from Renderer import Renderer
	from Controller import Controller
	from Game import Game

	#===================================================================================================
	#
	#	v3.01
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
```
 
A game loop is implemented following the pattern: input-update-draw-render. The input and render steps are handled by the static classes Controller and Renderer, while the update and draw steps are handled by an instance of Game which contains logic for a simple menu as well as level data.

Controller is a static class with two main responsibilities: capture user input and store it in an accessible place. Controller.pollInput() records keypresses and mouse movements using the pygame library and processes them into a series of dictionaries to be accessed later using “getter” functions in Game.update(). 

Renderer is a static class that handles the game window, clock, and drawing functions used in Game.draw(). It must be initialized by Renderer.init() which uses pygame to open a window and then sets up an OpenGL frame buffer. It also starts a clock and loads resources using another static class called ResourceManager. Renderer’s drawing functions write to the frame buffer between frames and then the frame buffer is drawn to the pygame window by Renderer.flipDisplay(), which also limits the frame rate.

Game is responsible for wrapping an instance of Level and implementing a menu. It has two main functions.
-	Game.update() controls the menu in response to user input (via Controller) and calls Level.update(), which itself manages level data in response time between frames (Renderer.dTime) as well as user input. 
-	Game.draw() draws the menu and calls Level.draw() to draw level data to the frame buffer (using Renderer’s draw functions).

