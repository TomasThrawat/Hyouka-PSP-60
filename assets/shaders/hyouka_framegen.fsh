#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

uniform sampler2D sampler0;
uniform sampler2D sampler2;
uniform vec4 u_setting;
uniform vec2 u_texelDelta;
varying vec2 v_texcoord0;

float Luma(vec3 c) {
    return dot(c, vec3(0.299, 0.587, 0.114));
}

vec3 SamplePrevious(vec2 uv) {
    return texture2D(sampler2, clamp(uv, 0.0, 1.0)).rgb;
}

void main() {
    vec2 uv = v_texcoord0.xy;
    vec2 texel = u_texelDelta;
    vec3 current = texture2D(sampler0, uv).rgb;

    float bestError = 1000000.0;
    vec2 bestOffset = vec2(0.0);
    float currentLuma = Luma(current);

    // 3x3 local search for a cheap screen-space motion estimate.
    for (int y = -1; y <= 1; ++y) {
        for (int x = -1; x <= 1; ++x) {
            vec2 offset = vec2(float(x), float(y)) * texel;
            vec3 previous = SamplePrevious(uv + offset);
            float error = abs(Luma(previous) - currentLuma);
            error += length(previous - current) * 0.35;
            if (error < bestError) {
                bestError = error;
                bestOffset = offset;
            }
        }
    }

    vec3 previousWarped = SamplePrevious(uv + bestOffset * 0.5);
    float confidence = clamp(1.0 - bestError * 4.0, 0.0, 1.0);
    float strength = clamp(u_setting.x, 0.0, 1.0);
    float temporalWeight = mix(0.5, 0.65, confidence) * strength;
    vec3 generated = mix(current, previousWarped, temporalWeight);

    // Hard cuts and unrelated pixels stay close to the current frame.
    float difference = length(current - previousWarped);
    float cutWeight = smoothstep(0.20, 0.45, difference);
    generated = mix(generated, current, cutWeight);

    gl_FragColor = vec4(generated, 1.0);
}
