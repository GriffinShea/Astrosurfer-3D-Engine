#version 460

in vec2 texInt;

uniform sampler2D frame;

float blurWeight[5] = float[] (0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);

layout(location = 0) out vec4 gCol;

void main() 
{
	vec2 pixelSize = 1.0 / textureSize(frame, 0);
	vec3 colour = texture(frame, texInt).rgb * blurWeight[0];
    
	//add colour horizontally
	for(int i = 1; i < 5; ++i) {
		colour += texture(frame, texInt + vec2(pixelSize.x * i, 0.0)).rgb * blurWeight[i];
		colour += texture(frame, texInt - vec2(pixelSize.x * i, 0.0)).rgb * blurWeight[i];
	}
    
	gCol = vec4(colour, 1.0);
	return;
}
