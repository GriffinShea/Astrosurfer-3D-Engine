#version 460

#define MAX_LIGHTS 16						//duplicated in config and other masters
#define MAX_SINGLE_SHADOW_MAPS 8			//duplicated in config and other masters
#define PHONG_EXPONENT 64					//duplicated in gBufferMaster.frag
#define BLINNPHONG_EXPONENT 192	//64 * 3	//duplicated in gBufferMaster.frag

in vec2 texInt;

uniform sampler2DArray gBuffer;

//(LA) three term lighting model
$LAuniform vec3 globalAmbience;
$LAuniform int lightCount;
$LAuniform int lightTypes[MAX_LIGHTS];
$LAuniform float lightIntensities[MAX_LIGHTS];
$LAuniform vec3 lightColours[MAX_LIGHTS];
$LAfloat diffuseCalcs[MAX_LIGHTS];
$LAfloat specularCalcs[MAX_LIGHTS];

//(PA) Phong shading
$PAuniform mat4 viewMat;
$PAuniform vec3 lightPositions[MAX_LIGHTS];
$PAuniform vec2 spotLightCutoffs[MAX_LIGHTS];
$PAuniform vec3 spotLightDirections[MAX_LIGHTS];
$PAuniform float ATTENTUATION_RANGE;

//(SM) shadow mapping
$SMuniform mat4 CAM_TO_TEX_MAT;
$SMuniform mat4 shadowMats[MAX_SINGLE_SHADOW_MAPS];
$SMuniform sampler2DArray shadowMaps;

//(FE) fog
$FEuniform vec3 fogColour;

//

$SMbool outsideDirLightShadow(int i, int mapNum, vec3 worldPos) {
$SM	//(SM) remove lighting if inside the directional light's shadow
$SM	vec4 shadowCoordinate = CAM_TO_TEX_MAT * shadowMats[mapNum] * vec4(worldPos, 1);
$SM	vec2 shadowCoord = shadowCoordinate.xy/shadowCoordinate.w;
$SM	float closestDepth = texture(shadowMaps, vec3(shadowCoord, mapNum)).r;
$SM	if (diffuseCalcs[i] <= 0 || closestDepth < shadowCoordinate.z) return false;
$SM	return true;
$SM}

$SMbool outsideSpotLightShadow(int i, int mapNum, vec3 worldPos) {
$SM	//(SM) remove lighting if inside the spotlight's shadow
$SM	vec4 shadowCoordinate = CAM_TO_TEX_MAT * shadowMats[mapNum] * vec4(worldPos, 1);
$SM	vec2 shadowCoord = shadowCoordinate.xy/shadowCoordinate.w;
$SM	float closestDepth = texture(shadowMaps, vec3(shadowCoord, mapNum)).r;
$SM	if (diffuseCalcs[i] <= 0 || closestDepth < shadowCoordinate.z/shadowCoordinate.w) return false;
$SM	return true;
$SM}

void main() {

	vec4 pos = texture(gBuffer, vec3(texInt, 0));
	vec4 norm = texture(gBuffer, vec3(texInt, 1));
	vec4 col = texture(gBuffer, vec3(texInt, 2));
	vec4 extra = texture(gBuffer, vec3(texInt, 3));

$PA	//(PA) Phong shading (fragment by fragment shading)
$PA	vec3 worldPos = pos.rgb;
$PA	vec3 viewPos = (viewMat * vec4(worldPos, 1)).xyz;
$PA	vec3 lightViewPos;
$PA	vec3 N = normalize(norm.rgb);
$PA	vec3 V = normalize(-viewPos);
$PA	vec3 L;
$PP	vec3 R;
$PB	vec3 H;
$PA	float atten;
$PA	int p = 0, s = 0;
$PA	for (int i = 0; i < lightCount; i++) {
$PA		lightViewPos = (viewMat * vec4(lightPositions[i], 1)).xyz;//REVISIT: this is calculated the same for all fragments
$PA		L = normalize(lightViewPos - viewPos);
$PA		//calculate light attentuation factor for point lights
$PA		atten = 1;
$PA		//pointlight
$PA		if (lightTypes[i] == 1)
$PA			atten = ATTENTUATION_RANGE * lightIntensities[i] / length(worldPos - lightPositions[i]);
$PA		//spotlight
$PA		if (lightTypes[i] == 3) {
$PA			atten = dot(normalize(worldPos - lightPositions[i]), spotLightDirections[s]);
$PA			atten -= spotLightCutoffs[s].y;
$PA			atten /= spotLightCutoffs[s].x - spotLightCutoffs[s].y;
$PA			atten = clamp(atten, 0, 1);
$PA			s++;
$PA			//REVISIT: This line fixes the spotlight, but the above calculation has broken
$PA			//With this formulation, the spotlight has a solid barrier instead of fading out
$PA			atten = ATTENTUATION_RANGE * lightIntensities[i] / length(worldPos - lightPositions[i]);
$PA		}
$PA		//calculate diffuse component
$PA		diffuseCalcs[i] = atten * max(dot(N, L), 0);
$PP		//calculate specular component using (PP) Phong calculation for specular component
$PP		R = reflect(-L, N);
$PP		specularCalcs[i] = atten * pow(max(dot(V, R), 0), PHONG_EXPONENT);
$PB		//calculate specular component using (PB) Blinn-Phong calculation for specular component
$PB		H = normalize(V + L);
$PB		specularCalcs[i] = atten * pow(max(dot(N, H), 0), BLINNPHONG_EXPONENT);
$PA	}

$VA	//(VA) diffuse and specular values are calculated in vertex shader (max of 4)
$VA	diffuseCalcs[0] = pos.x;
$VA	diffuseCalcs[1] = pos.y;
$VA	diffuseCalcs[2] = pos.z;
$VA	diffuseCalcs[3] = pos.w;
$VA	specularCalcs[0] = norm.x;
$VA	specularCalcs[1] = norm.y;
$VA	specularCalcs[2] = norm.z;
$VA	specularCalcs[3] = norm.w;

//

$LA	//(LA)
$LA	vec3 diffuseMat = vec3(1);
$LA	vec3 specularMat = vec3(1);
$LA	vec3 albedo = col.rgb;
$LA
$LA	//if col.a is 1 apply the lighting model, otherwise set frag colour to albedo
$LA	if (col.a == 1) {
$LA		//apply ambient lighting
$LA		gl_FragColor.rgb = globalAmbience * albedo;
$LA		vec3 reflectionColour;
$SM		int mapNum = 0;
$PA		for (int i = 0; i < lightCount; i++) {
$VA		for (int i = 0; i < min(lightCount, 4); i++) {
$SM			if (
$SM				lightTypes[i] == 1
$SM				|| lightTypes[i] == 2 && outsideDirLightShadow(i, mapNum++, worldPos)
$SM				|| lightTypes[i] == 3 && outsideSpotLightShadow(i, mapNum++, worldPos)
$SM	//			|| lightTypes[i] == 4 && outsideOmniLightShadow(i, mapNum++, worldPos)
$SM			) {
$LA				reflectionColour = lightIntensities[i] * lightColours[i] * albedo;
$LA				gl_FragColor.rgb += diffuseCalcs[i] * diffuseMat * reflectionColour;
$LA				gl_FragColor.rgb += specularCalcs[i] * specularMat * reflectionColour;
$SM			}
$LA		}
$LA	} else {
$LA		gl_FragColor.rgb = albedo;
$LA	}
$LA	gl_FragColor.a = 1;
	
$NL	//(NL) no lighting
$NL	gl_FragColor.rgba = vec4(col.rgb, 1);
	
$FE	//(FE) mix in fog colour
$FE	gl_FragColor.rgb = mix(gl_FragColor.rgb, fogColour, extra.r);
	
	return;
}
