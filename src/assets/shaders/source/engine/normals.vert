#version 460

layout(location = 0) in vec3 posXYZ;
layout(location = 1) in vec3 normXYZ;
layout(location = 2) in vec2 texUV;

uniform mat4 worldMat;
uniform mat4 viewMat;
uniform mat4 projMat;

out vec4 normInts;
out vec2 texInts;

void main()
{
	gl_Position = projMat * viewMat * worldMat * vec4(posXYZ, 1);
	normInts = projMat * vec4(mat3(transpose(inverse(viewMat * worldMat))) * normXYZ, 0);
	texInts = texUV;
	return;
}
