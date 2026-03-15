#version 460

in vec2 texInt;

uniform sampler2D bitmap;
uniform ivec2 bitmapDims;
uniform int character;
uniform vec3 colour;
uniform float alpha;

layout(location = 0) out vec4 gCol;

void main() 
{
	gCol = texture(
		bitmap, vec2(
			(texInt.x + mod(character, bitmapDims.x)) / bitmapDims.x,
			1 + (texInt.y - 1 - floor(character / bitmapDims.x)) / bitmapDims.y
		)
	);
	
	if (gCol.xyz != vec3(0, 0, 0)) {
		gCol = vec4(colour, alpha);
	} else {
		discard;
	}
	
	return;
}
