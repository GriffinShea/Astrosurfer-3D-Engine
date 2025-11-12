#version 460

layout(location = 0) in vec3 posXYZ;

uniform mat4 worldMat;

void main()
{
	gl_Position = worldMat * vec4(posXYZ, 1.0);
	return;
}
