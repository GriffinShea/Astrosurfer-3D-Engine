#version 460

#define MAX_SINGLE_SHADOW_MAPS 8			//duplicated in config and other masters

layout (triangles) in;

uniform mat4 shadowMats[MAX_SINGLE_SHADOW_MAPS];

layout (triangle_strip, max_vertices=3*MAX_SINGLE_SHADOW_MAPS) out;

void main()
{
	for (int i = 0; i < MAX_SINGLE_SHADOW_MAPS; i++) {
		gl_Layer = i;
		gl_Position = shadowMats[i] * gl_in[0].gl_Position;
		EmitVertex();
		
		gl_Layer = i;
		gl_Position = shadowMats[i] * gl_in[1].gl_Position;
		EmitVertex();
		
		gl_Layer = i;
		gl_Position = shadowMats[i] * gl_in[2].gl_Position;
		EmitVertex();
		
		EndPrimitive();
	}
	return;
}
