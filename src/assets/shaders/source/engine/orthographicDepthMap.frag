#version 460

in vec3 posInt;
in vec2 texInt;

uniform sampler2DArray shadowMaps;

void main()
{
	//this will show the depth map for a directional light
	float d = texture(shadowMaps, vec3(texInt, 0)).r;
	gl_FragColor = vec4(vec3(d), 0);

	return;
}
