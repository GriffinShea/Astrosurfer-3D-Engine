#version 460

layout(location = 0) in vec3 posXYZ;
layout(location = 1) in vec3 normXYZ;
layout(location = 2) in vec2 texUV;

uniform mat4 worldMat;
uniform mat4 viewMat;
uniform mat4 projMat;

uniform vec3 cameraPos;
uniform float time;
uniform float seed;

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
	
	//starting position is random but fixed to a repeating grid moved by camera position
	vec2 gridDims = vec2(64, 64);
	lastRng = rngFloat(lastRng);
	float xPos = (lastRng - 0.5) * gridDims.x * 2;
	lastRng = rngFloat(lastRng);
	float yPos = (lastRng - 0.5) * gridDims.y * 2;
	
	vec2 startPos = vec2(xPos, yPos);
	vec3 cameraRelPos = (worldMat * vec4(cameraPos, 1)).xyz;
	startPos.x += ceil((cameraRelPos.x - startPos.x) / gridDims.x) * gridDims.x - gridDims.x/2;
	startPos.y += ceil((cameraRelPos.z - startPos.y) / gridDims.y) * gridDims.y - gridDims.y/2;
	
	//end position is random point in circle around startPos
	lastRng = rngFloat(1.0);
	float theta = lastRng * 3.14159 * 2;
	lastRng = rngFloat(lastRng);
	float radius = (lastRng * 8) + 4;
	vec2 endPos = vec2(sin(theta) * radius, cos(theta) * radius);
	
	//height is randomized and modified by time
	lastRng = rngFloat(lastRng);
	float height = lastRng;
	height = height - mod(time, 0.25) * 4;
	if (height < 0) {
		height = height + 1;
	}
	
	//position is interpolated by height 
	gl_Position = viewMat * vec4(
		startPos.x + endPos.x * height,
		height * 32,
		startPos.y + endPos.y * height,
		1
	);
    
	//rotates the feather around its own axis
	lastRng = rngFloat(lastRng);
	float spinStart = lastRng - 0.5;
	lastRng = rngFloat(lastRng);
	float spinDir = lastRng - 0.5;
	lastRng = rngFloat(lastRng);
	gl_Position = viewMat * yAxisRotation((spinStart + sign(spinDir) * time) * 3.14159 * 2) * vec4(posXYZ, 1) + gl_Position;
    
	//determine final position
	gl_Position = projMat * gl_Position;
	
	//determine which feather texture to use on the atlas
	int featherNum = int(floor(rngFloat(lastRng) * 9));
    texInt = vec2(
		(texUV.x + mod(featherNum, 3)) / 3,
		(texUV.y - floor(featherNum / 3)) / 3
	);
	
	return;
}
