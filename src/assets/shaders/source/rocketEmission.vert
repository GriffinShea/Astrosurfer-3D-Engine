#version 460

layout(location = 0) in vec3 posXYZ;
layout(location = 1) in vec3 normXYZ;
layout(location = 2) in vec2 texUV;

uniform mat4 worldMat;
uniform mat4 viewMat;
uniform mat4 projMat;

uniform float time;
uniform float seed;

out vec3 colourInt;

//this generates a psuedo-random number depending on instance id and emission birth seed
float rngFloat(float last) {
	return fract(sin(dot(
		vec2(gl_InstanceID*seed*13.55860231, last*1358.00045),
		vec2(12.9898,78.233))
	) * 43758.5453123);
}

void main()
{
	float lastRng = seed;
	
	/*REVISIT: superfluous but kept here for future reference
	//deconstruct worldMat and remove rotation
	vec3 scaleXYZ = vec3(
		length(worldMat[0]),
		length(worldMat[1]),
		length(worldMat[2])
	);
	mat4 newWorldMat = worldMat;
	newWorldMat[0] = vec4(scaleXYZ.x, 0, 0, 0);
	newWorldMat[1] = vec4(0, scaleXYZ.y, 0, 0);
	newWorldMat[2] = vec4(0, 0, scaleXYZ.z, 0);
	*/
	
	//create random floats for positioning
	lastRng = rngFloat(lastRng);
	float rngX = (lastRng * 2) - 1;
	lastRng = rngFloat(lastRng);
	float rngY = lastRng;
	lastRng = rngFloat(lastRng);
	float rngZ = (lastRng * 2) - 1;
	lastRng = rngFloat(lastRng);
	float rngD = lastRng * 4;
	
	//set position
	vec3 randomPosition = posXYZ + -normalize(vec3(rngX, rngY, rngZ)) * rngD;
	gl_Position = vec4(randomPosition * 4 * (1.05 - 1 / pow(2, 4 * time)), 1.0);
	gl_Position = projMat * viewMat * worldMat * gl_Position;

	//set colour to go from white to yellow to red to black
	colourInt = vec3(1 - time, 0.75 - time, 0.375 - time);
	
	return;
}
