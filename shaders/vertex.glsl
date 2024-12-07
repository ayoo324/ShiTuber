#version 450 core

uniform mat4 camera;
uniform vec3 position;
uniform float scale;
uniform float audio_data;

layout (location = 0) in vec3 in_vertex;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec2 in_uv;

out vec3 v_vertex;
out vec3 v_normal;
out vec2 v_uv;

float threshold = 1200;
float max_audio = 150000;
float max_x = 1;
float max_y = 1;

void main() {
    v_vertex = position + in_vertex * scale;
    v_normal = in_normal;
    v_uv = in_uv;
    float resolved_audio = audio_data;
    if(resolved_audio > max_audio){
        resolved_audio = max_audio;
    }
    if(resolved_audio > threshold){
        float x_move = min((max_x),  ((resolved_audio - max_audio) / (max_audio - threshold)) + max_x);
        float y_move = min((max_y),  ((resolved_audio - max_audio) / (max_audio - threshold)) + max_y);
        v_vertex.x = v_vertex.x + x_move;
        v_vertex.y = v_vertex.y - y_move;
    }
    gl_Position = camera * vec4(v_vertex, 1.0);
}