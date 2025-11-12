#version 460

layout (triangles) in;

layout (line_strip, max_vertices=2) out;

uniform mat4 viewMat;
uniform mat4 projMat;

uniform vec3 pos0;
uniform vec3 pos1;

void main()
{	
	gl_Position = projMat * viewMat * vec4(pos0, 1.0);
	EmitVertex();
	
	gl_Position = projMat * viewMat * vec4(pos1, 1.0);
	EmitVertex();

	EndPrimitive();
	return;
}
