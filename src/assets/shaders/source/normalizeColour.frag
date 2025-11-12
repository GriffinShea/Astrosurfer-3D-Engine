#version 460

in vec2 texInt;

uniform sampler2D frame;

void main() 
{
	gl_FragColor = normalize(texture2D(frame, texInt));
	return;
}
