#version 450 core

uniform mat4 camera;
uniform vec3 position;
uniform float scale;
uniform float audio_data;
// uniform float previous_audio;
// uniform int time_since_last_frame;

layout (location = 0) in vec3 in_vertex;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec2 in_uv;

out vec3 v_vertex;
out vec3 v_normal;
out vec2 v_uv;

float threshold = 1200;
float max_audio = 100000;
float max_x = 1;
float max_y = 2;

void main() {
    v_vertex = position + in_vertex * scale;
    v_normal = in_normal;
    v_uv = in_uv;
    // float ratio = time_since_last_frame / 16.67;
    float resolved_audio = audio_data;
    if(resolved_audio > max_audio){
        resolved_audio = max_audio;
    }
    float x_move = (max_x) / ((max_audio - threshold) * (resolved_audio - max_audio) + max_x);
    float y_move = (max_y) / ((max_audio - threshold) * (resolved_audio - max_audio) + max_y);
    if(resolved_audio > threshold){
        v_vertex.x = v_vertex.x + x_move;
        v_vertex.y = v_vertex.y + y_move;
        // if(resolved_audio > previous_audio){
        //     v_vertex.x = v_vertex.x - (x_move * ratio);
        //     v_vertex.y = v_vertex.y + (y_move * ratio);
        // }else{
        //     v_vertex.x = v_vertex.x + (x_move * ratio);
        //     v_vertex.y = v_vertex.y - (y_move * ratio);
        // }
    }
    gl_Position = camera * vec4(v_vertex, 1.0);
}