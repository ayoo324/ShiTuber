#version 450 core

uniform sampler2D Texture;
uniform bool use_texture;
uniform vec3 color;

in vec3 v_vertex;
in vec3 v_normal;
in vec2 v_uv;

layout (location = 0) out vec4 out_color;

void main() {
    out_color = vec4(color, 1.0);
    if (use_texture) {
        out_color *= texture(Texture, v_uv);
    }
}