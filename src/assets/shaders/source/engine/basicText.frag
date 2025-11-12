#version 460

in vec2 texInt;

uniform sampler2D bitmap;
uniform ivec2 bitmapDims;
uniform int character;
uniform vec3 colour;
uniform float alpha;

void main() 
{
	gl_FragColor = texture2D(
		bitmap, vec2(
			(texInt.x + mod(character, bitmapDims.x)) / bitmapDims.x,
			1 + (texInt.y - 1 - floor(character / bitmapDims.x)) / bitmapDims.y
		)
	);
	
	if (gl_FragColor.xyz != vec3(0, 0, 0)) {
		gl_FragColor = vec4(colour, alpha);
	} else {
		discard;
	}
	
	return;
}
