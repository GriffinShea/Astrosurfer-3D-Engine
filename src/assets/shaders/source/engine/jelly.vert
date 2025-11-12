#version 460

layout(location = 0) in vec3 posXYZ;
layout(location = 1) in vec3 normXYZ;
layout(location = 2) in vec2 texUV;

uniform float RUN_TIME;
uniform mat4 worldMat;
uniform mat4 viewMat;
uniform mat4 projMat;

out vec2 texInt;

float rngFloat(float last) {
	//this generates a psuedo-random number depending on texUV
	return fract(sin(dot(vec2(last + texUV.s, last - texUV.t), vec2(12.9898, 78.233))) * 43758.5453123);
}

void main() {
	
	vec4 worldPos = worldMat * vec4(posXYZ, 1);
	
	//jellification calculation
	float lastRNG = rngFloat(0);
	float period = sin(radians(fract(asin(lastRNG) + RUN_TIME / 4000) * 360));
	worldPos.xyz += normXYZ * period / 10;
	
	//calculate position, texture coordinate
	gl_Position = projMat * viewMat * worldPos;
	texInt = texUV;
	
	return;
}
