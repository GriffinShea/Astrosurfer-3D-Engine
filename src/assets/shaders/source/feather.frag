#version 460

in vec2 texInt;

uniform sampler2D tex;

layout(location = 0) out vec4 gCol;

void main()
{

	gCol = texture(tex, texInt);
	if (gCol.r < 0.25) { discard; }
	gCol.a = 0;

	return;
}
