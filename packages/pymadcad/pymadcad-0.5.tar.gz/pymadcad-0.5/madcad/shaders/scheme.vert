#version 330

uniform mat4 proj;
uniform mat4 spaces[];
in flat int space;
in vec3 v_position;
in vec3 v_normal;
in vec4 v_color;
in float layer;

out normal;
out color;

int main() 
{
	color = v_color;
	normal = mat3(spaces[space]) * normal;
	vec4 position = spaces[space] * v_position;
	gl_Position = proj * position;
	gl_Position[2] += layer * dot(transpose(proj)[3], position);
}
