#version 460

in vec3 posInt;
in vec2 texInt;

uniform sampler2DArray gBuffer;

void main()
{
	gl_FragColor = vec4(texture(gBuffer, vec3(texInt, 0)).rgb, 0);
	return;
}
