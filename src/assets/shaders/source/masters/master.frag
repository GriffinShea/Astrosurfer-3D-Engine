#version 460

#define MAX_LIGHTS 16	//duplicated in config and other masters

layout(location = 0) out vec4 gPos;
layout(location = 1) out vec4 gNorm;
layout(location = 2) out vec4 gCol;
layout(location = 3) out vec4 gExtra;

$PA//(P) Phong shading
$PAin vec3 posInt;
$PAin vec3 normInt;
$VG//(VG) Gouraud shading
$VGin float diffuseCalcs[MAX_LIGHTS];
$VGin float specularCalcs[MAX_LIGHTS];
$VF//(VF) flat shading
$VFflat in float diffuseCalcs[MAX_LIGHTS];
$VFflat in float specularCalcs[MAX_LIGHTS];

$FE//(FE) fog
$FEin vec3 viewPosInt;
$FEuniform float fogDensity;
$FEuniform float fogGradient;

$BA//(BA) basic uses perspective correct uv
$BAin vec2 texInt;
$XA//(XA) PSX uses affine uv
$XAnoperspective in vec2 texInt;

$CI//(CI) interpolated colour
$CIin vec3 colourInt;
$CV//(CV) vertex noise colour
$CVin vec3 vertNoiseInt;
$CT//(CT) texture colour
$CTuniform sampler2D texture;
$CTuniform vec2 uvScale = vec2(1);
$CU//(CU) uniform colour
$CUuniform vec3 colour;

$CS//(CS) static colour
$CSfloat rngFloat(float last) {
$CS	//this generates a psuedo-random number depending on texInt
$CS	return fract(sin(dot(texInt, vec2(12.9898, 78.233)) ) * 43758.5453123);
$CS}

void main() {

$PA	//(PA) Phong shading (fragment by fragment shading)
$PA	gPos = vec4(posInt, 1);
$PA	gNorm = vec4(normInt, 1);
$VA	//(VA) Gouraud and flat shading already calculate diffuse and specular per vertex
$VA	gPos = vec4(diffuseCalcs[0], diffuseCalcs[1], diffuseCalcs[2], diffuseCalcs[3]);
$VA	gNorm = vec4(specularCalcs[0], specularCalcs[1], specularCalcs[2], specularCalcs[3]);

$FE	//(FE) view distance needed for fog calculation
$FE	gExtra.r = clamp(pow(length(viewPosInt) * fogDensity, fogGradient), 0, 1);

$LE	//(LE) enable lighting for this fragment
$LE	gCol.a = 1;
$LD	//(LD) do not enable lighting for this fragment
$LD	gCol.a = 0;

$CI	//(CI) interpolated colour from vertex
$CI	gCol.rgb = colourInt;
$CV	//(CV) vertex noise colour interpolated from vertex
$CV	gCol.rgb = vertNoiseInt;
$CT	//(CT) texture colour
$CT	gCol.rgb = texture2D(texture, uvScale * texInt).rgb;
$CU	//(CU) uniform colour
$CU	gCol.rgb = colour;
$CS	//(CS) static colour
$CS	gCol.r = rngFloat(0);
$CS	gCol.g = rngFloat(gCol.r);
$CS	gCol.b = rngFloat(gCol.g);

$IE	//(IE) invert colour
$IE	gCol.rgb = vec3(1) - gCol.rgb;

	return;
}
