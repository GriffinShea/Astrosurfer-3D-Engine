#version 460

layout(location = 0) in vec3 posXYZ;
layout(location = 1) in vec3 normXYZ;
layout(location = 2) in vec2 texUV;

out vec3 posControl;
out vec3 normControl;
out vec2 texControl;

void main() {
	posControl = posXYZ;
	normControl = normXYZ;
	texControl = texUV;
	return;
}
