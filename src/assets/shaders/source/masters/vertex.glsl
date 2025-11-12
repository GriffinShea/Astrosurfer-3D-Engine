#version 460

#define MAX_LIGHTS 16						//duplicated in config and other masters
#define PHONG_EXPONENT 64					//duplicated in gBufferMaster.frag
#define BLINNPHONG_EXPONENT 192	//64 * 3	//duplicated in gBufferMaster.frag

$TTlayout (triangles, fractional_even_spacing, ccw) in;
$TQlayout (quads, fractional_even_spacing, ccw) in;

$TEin vec3 posEval[];
$TEin vec3 normEval[];
$TEin vec2 texEval[];

$TDlayout(location = 0) in vec3 posXYZ;
$TDlayout(location = 1) in vec3 normXYZ;
$TDlayout(location = 2) in vec2 texUV;

uniform mat4 worldMat;
uniform mat4 viewMat;
uniform mat4 projMat;

$PA//(PA) Phong shading (vertex shader)
$PAout vec3 posInt;
$PAout vec3 normInt;
$VA//(VA) vertex shading
$VAuniform float ATTENTUATION_RANGE;
$VAuniform int lightCount;
$VAuniform int lightTypes[MAX_LIGHTS];
$VAuniform vec3 lightPositions[MAX_LIGHTS];
$VAuniform float lightIntensities[MAX_LIGHTS];
$VG//(VG) Gouraud shading
$VGout float diffuseCalcs[MAX_LIGHTS];
$VGout float specularCalcs[MAX_LIGHTS];
$VF//(VF) flat shading
$VFflat out float diffuseCalcs[MAX_LIGHTS];
$VFflat out float specularCalcs[MAX_LIGHTS];

$FE//(FE) fog
$FEout vec3 viewPosInt;

$BA//(BA) basic setting uses perspective corrected texture mapping
$BAout vec2 texInt;
$XA//(XA) psx shader settings (pixel "jiggle" and affine texture mapping)
$XAuniform ivec2 RESOLUTION;
$XAuniform int JIGGLE_FACTOR;
$XAnoperspective out vec2 texInt;

$CV//(CV) vertex noise colour
$CVout vec3 vertNoiseInt;
$CVfloat rngFloat(float last, vec2 uv) {
$CV	//this generates a psuedo-random number depending on uv
$CV	return fract(sin(dot(vec2(last + uv.s, last - uv.t), vec2(12.9898, 78.233))) * 43758.5453123);
$CV}

void main() {

$TE	//calculate posXYZ from posEval, normXYZ from normEval, texUV from texEval
$TT	vec3 p0 = gl_TessCoord.x * posEval[0];
$TT	vec3 p1 = gl_TessCoord.y * posEval[1];
$TT	vec3 p2 = gl_TessCoord.z * posEval[2];
$TT	vec3 posXYZ = (p0 + p1 + p2);
$TQ	vec3 p0 = mix(posEval[1], posEval[2], gl_TessCoord.x);
$TQ	vec3 p1 = mix(posEval[0], posEval[3], gl_TessCoord.x);
$TQ	vec3 posXYZ = mix(p0, p1, gl_TessCoord.y);

$TT	vec3 n0 = gl_TessCoord.x * normEval[0];
$TT	vec3 n1 = gl_TessCoord.y * normEval[1];
$TT	vec3 n2 = gl_TessCoord.z * normEval[2];
$TT	vec3 normXYZ = (n0 + n1 + n2);
$TQ	vec3 n0 = mix(normEval[1], normEval[2], gl_TessCoord.x);
$TQ	vec3 n1 = mix(normEval[0], normEval[3], gl_TessCoord.x);
$TQ	vec3 normXYZ = mix(n0, n1, gl_TessCoord.y);

$TT	vec2 t0 = gl_TessCoord.x * texEval[0];
$TT	vec2 t1 = gl_TessCoord.y * texEval[1];
$TT	vec2 t2 = gl_TessCoord.z * texEval[2];
$TT	vec2 texUV = (t0 + t1 + t2);
$TQ	vec2 t0 = mix(texEval[1], texEval[2], gl_TessCoord.x);
$TQ	vec2 t1 = mix(texEval[0], texEval[3], gl_TessCoord.x);
$TQ	vec2 texUV = mix(t0, t1, gl_TessCoord.y);

	//calculate position, texture coordinate
	vec3 worldPos = (worldMat * vec4(posXYZ, 1)).xyz;
	vec3 viewPos = (viewMat * vec4(worldPos, 1)).xyz;
	gl_Position = projMat * vec4(viewPos, 1);
	texInt = texUV;
	
$PA	//(PA) Phong shading (vertex shader) sends these values to the interpolator
$PA	posInt = worldPos;
$PA	normInt = mat3(transpose(inverse(viewMat * worldMat))) * normXYZ;
$VA	//(VA) vertex shading
$VA	vec3 norm = mat3(transpose(inverse(viewMat * worldMat))) * normXYZ;
$VA	vec3 N = normalize(norm);
$VA	vec3 V = normalize(-viewPos);
$VA	vec3 L;
$VA	float atten;
$VP	vec3 R;
$VB	vec3 H;
$VA	for (int i = 0; i < lightCount; i++) {
$VA		//calculate light attentuation factor for point lights
$VA		atten = 1;
$VA		if (lightTypes[i] == 1)
$VA			atten = ATTENTUATION_RANGE * lightIntensities[i] / length(worldPos - lightPositions[i]);
$VA		//calculate diffuse coefficient
$VA		L = normalize((viewMat * vec4(lightPositions[i], 1)).xyz - viewPos);
$VA		diffuseCalcs[i] = atten * max(dot(N, L), 0);
$VP		//(VP) calculate specular coefficient using Phong calculation for the interpolator
$VP		R = reflect(-L, N);
$VP		specularCalcs[i] = atten * pow(max(dot(V, R), 0), PHONG_EXPONENT);
$VB		//(VB) calculate specular coefficient using Blinn-Phong calculation for the interpolator
$VB		H = normalize(V + L);
$VB		specularCalcs[i] = atten * pow(max(dot(N, H), 0), BLINNPHONG_EXPONENT);
$VA	}

$FE	//(FE) calculate distance from camera for fog calculation
$FE	viewPosInt = viewPos;

$XA	//(XA) emulate the psx pixel "jiggle"
$XA	gl_Position.xyz /= gl_Position.w;
$XA	gl_Position.xy = floor(RESOLUTION/JIGGLE_FACTOR*gl_Position.xy) / RESOLUTION*JIGGLE_FACTOR;
$XA	gl_Position.xyz *= gl_Position.w;

$CV	//(CV) vertex noise colour
$CV	vertNoiseInt.r = rngFloat(0, texUV);
$CV	vertNoiseInt.g = rngFloat(vertNoiseInt.r, texUV);
$CV	vertNoiseInt.b = rngFloat(vertNoiseInt.g, texUV);

	return;
}
