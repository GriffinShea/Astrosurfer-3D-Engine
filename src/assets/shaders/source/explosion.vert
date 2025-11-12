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
		vec2(12.9898,78.233)
	)) * 43758.5453123);
}

void main()
{
	float lastRng = 1;
	
	//create random floats for position
	lastRng = rngFloat(lastRng);
	float rngX = lastRng;
	lastRng = rngFloat(lastRng);
	float rngY = lastRng;
	lastRng = rngFloat(lastRng);
	float rngZ = lastRng;
	lastRng = rngFloat(lastRng);
	float rngD = lastRng;

	//set position
	vec3 randomPosition = -normalize(vec3((rngX*2-1), (rngY*2-1), (rngZ*2-1))) * rngD;
	gl_Position = vec4(randomPosition * 3 * (1 - 1 / pow(2, 3 * time)), 1.0);
    gl_Position = projMat * viewMat * worldMat * gl_Position;
	
	//calculate colour
	//colourInt = vec4(1, 1-time/6, 0, (1-time/6)*rngD);
	colourInt = vec3(0.25+rngX*0.75, 0.25+rngY*0.75, 0.25+rngZ*0.75);
	
	return;
}
