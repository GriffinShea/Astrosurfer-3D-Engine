#version 460

in vec2 texInt;

uniform sampler2D sprite;
uniform float alpha;

void main() 
{
	gl_FragColor = texture2D(sprite, texInt);
	gl_FragColor.a = min(gl_FragColor.a, alpha);
	return;
}
