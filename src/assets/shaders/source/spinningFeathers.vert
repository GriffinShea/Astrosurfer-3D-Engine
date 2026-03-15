#version 460

layout(location = 0) in vec3 posXYZ;
layout(location = 1) in vec3 normXYZ;
layout(location = 2) in vec2 texUV;

uniform mat4 worldMat;
uniform mat4 viewMat;
uniform mat4 projMat;

uniform float time;
uniform float seed;

out vec3 posInt;
out vec3 normInt;
out vec3 viewPosInt;

out vec2 texInt;


//this generates a psuedo-random number depending on instance id and emission birth seed
float rngFloat(float last) {
	return fract(sin(dot(
		vec2(gl_InstanceID*seed*13.55860231, last*1358.00045),
		vec2(12.9898,78.233))
	) * 43758.5453123);
}

mat4 yAxisRotation(float angle) {
	return mat4(
		cos(angle),		0,		sin(angle),		0,
		0,				1,		0,				0,
		-sin(angle),	0,		cos(angle),		0,
		0,				0,		0,				1
	);
}

void main()
{
	float lastRng = 1;
	
	//height is randomized and modified by time
	lastRng = rngFloat(lastRng);
	float height = lastRng;
	height = height - mod(time, 0.25) * 4;
	if (height < 0) {
		height = height + 1;
	}

	//position is randomized in a disk shape
	lastRng = rngFloat(1.0);
	float theta = lastRng * 3.14159 * 2;
	lastRng = rngFloat(lastRng);
	float radius = (lastRng * 16) + 0.5;
	vec3 randomPosition = vec3(
		sin(theta) * radius,
		height * 8,
		cos(theta) * radius
	);
	
	//rotates around the center of the particle effect
	float circleStart = lastRng - 0.5;
	lastRng = rngFloat(lastRng);
	float circleDir = lastRng - 0.5;
	mat4 rot1 = yAxisRotation((circleStart + sign(circleDir) * time) * 3.14159 * 2);
    
	//rotates the feather around its own axis
	lastRng = rngFloat(lastRng);
	float spinStart = lastRng - 0.5;
	lastRng = rngFloat(lastRng);
	float spinDir = lastRng - 0.5;
	lastRng = rngFloat(lastRng);
	mat4 rot2 = yAxisRotation((spinStart + sign(spinDir) * time) * 3.14159 * 2);
	
	vec4 partPos = rot2 * vec4(posXYZ, 1) + rot1 * vec4(randomPosition * 3, 1.0);
    
	//determine final position
	gl_Position = projMat * viewMat * worldMat * partPos;
	
	vec4 worldPos = worldMat * partPos;
	posInt = worldPos.xyz;
	normInt = mat3(transpose(inverse(viewMat * worldMat))) * (rot1 * rot2 * vec4(normXYZ, 1)).xyz;
	viewPosInt = (viewMat * worldPos).xyz;
	
	//determine which feather texture to use on the atlas
	int featherNum = int(floor(rngFloat(lastRng) * 9));
    texInt = vec2(
		(texUV.x + mod(featherNum, 3)) / 3,
		(texUV.y - floor(featherNum / 3)) / 3
	);
	
	return;
}
