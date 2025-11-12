#version 460

$TTlayout (vertices = 3) out;
$TQlayout (vertices = 4) out;

in vec3 posControl[];
in vec3 normControl[];
in vec2 texControl[];

uniform float tessPeterDist;
uniform float baseTessLevel;

uniform mat4 worldMat;
uniform mat4 viewMat;

out vec3 posEval[];
out vec3 normEval[];
out vec2 texEval[];

void main() {
	posEval[gl_InvocationID] = posControl[gl_InvocationID];
	normEval[gl_InvocationID] = normControl[gl_InvocationID];
	texEval[gl_InvocationID] = texControl[gl_InvocationID];
	
	if (gl_InvocationID == 0) {
		//use the distance from camera as a factor to reduce baseTessLevel based on tessPeterDist
		float distTessFact = length(viewMat * worldMat * vec4(
$TT			(posControl[0] + posControl[1] + posControl[2]) / 3,
$TQ			(posControl[0] + posControl[1] + posControl[2] + posControl[3]) / 4,
			1
		));
		distTessFact = max(0, min(1, (1 / tessPeterDist) * (-distTessFact + 2 * tessPeterDist)));
		distTessFact = max(2, baseTessLevel * distTessFact);
		
		gl_TessLevelInner[0] = distTessFact;
$TQ		gl_TessLevelInner[1] = distTessFact;
		gl_TessLevelOuter[0] = distTessFact;
		gl_TessLevelOuter[1] = distTessFact;
		gl_TessLevelOuter[2] = distTessFact;
$TQ		gl_TessLevelOuter[3] = distTessFact;
	}
	
	return;
}
