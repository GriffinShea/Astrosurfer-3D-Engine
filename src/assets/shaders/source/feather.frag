#version 460

in vec2 texInt;

uniform sampler2D texture;

void main()
{

	gl_FragColor = texture2D(texture, texInt);
	if (gl_FragColor.r < 0.25) { discard; }
	gl_FragColor.a = 0;

	return;
}
