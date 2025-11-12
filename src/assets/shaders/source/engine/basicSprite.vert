#version 460

layout(location = 0) in vec2 posXY;
layout(location = 1) in vec2 texUV;

uniform mat4 transfMat;
uniform float depth;

out vec2 texInt;

void main()
{
    gl_Position = transfMat * vec4(posXY, 0, 1.0);
	gl_Position.z = depth;
    texInt = texUV;
	return;
}
