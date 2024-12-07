#version 450 core

uniform mat4 camera;
uniform vec3 position;
uniform float scale;

layout (location = 0) in vec3 in_vertex;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec2 in_uv;

out vec3 v_vertex;
out vec3 v_normal;
out vec2 v_uv;

void main() {
    v_vertex = position + in_vertex * scale;
    v_normal = in_normal;
    v_uv = in_uv;

    gl_Position = camera * vec4(v_vertex, 1.0);
}