#version 460

layout(location = 0) in vec2 posXY;
layout(location = 1) in vec2 texUV;

out vec2 texInt;

void main()
{
    gl_Position = vec4(posXY, 0, 1.0);
    texInt = texUV;
	return;
}
