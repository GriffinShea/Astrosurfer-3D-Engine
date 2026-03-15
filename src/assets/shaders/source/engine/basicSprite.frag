#version 460

in vec2 texInt;

uniform sampler2D sprite;
uniform float alpha;

layout(location = 0) out vec4 gCol;

void main() 
{
	gCol = texture(sprite, texInt);
	gCol.a = min(gCol.a, alpha);
	return;
}
