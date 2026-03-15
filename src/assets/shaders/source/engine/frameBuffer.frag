#version 460

in vec2 texInt;

uniform sampler2D frame;

layout(location = 0) out vec4 gCol;

void main() 
{
	gCol = texture(frame, texInt);
	return;
}
