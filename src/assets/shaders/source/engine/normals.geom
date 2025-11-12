#version 460

layout (triangles) in;

in vec4 normInts[];
in vec2 texInts[];

layout (line_strip, max_vertices=2) out;

out vec2 texInt;

void main()
{
	vec4 avgPos = (gl_in[0].gl_Position + gl_in[1].gl_Position + gl_in[2].gl_Position) / 3;
	vec4 avgNorm = normalize(normInts[0] + normInts[1] + normInts[2]) / 3;
	vec2 texInt = (texInts[0] + texInts[1] + texInts[2]) / 3;
	
	gl_Position = avgPos;
	EmitVertex();
	
	gl_Position = avgPos + avgNorm;
	EmitVertex();

	EndPrimitive();
	return;
}
