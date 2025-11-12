#version 460

layout(location = 0) in vec2 posXY;
layout(location = 1) in vec2 texUV;

uniform mat4 transfMat;
uniform float depth;
uniform vec2 charPos;

out vec2 texInt;

void main()
{
    gl_Position = transfMat * vec4(posXY.x + charPos.x * 2, posXY.y - charPos.y * 2, 0, 1.0);
	gl_Position.z = depth;
    texInt = texUV;
	return;
}
