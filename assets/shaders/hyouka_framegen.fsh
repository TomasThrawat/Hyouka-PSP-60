#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

uniform sampler2D sampler0;
uniform sampler2D sampler2;
uniform vec4 u_setting;
uniform vec4 u_time;
uniform vec4 u_timeDelta;
uniform vec2 u_texelDelta;
varying vec2 v_texcoord0;

float Luma(vec3 c) {
    return dot(c, vec3(0.299, 0.587, 0.114));
}

vec3 SampleCurrent(vec2 uv) {
    return texture2D(sampler0, clamp(uv, 0.0, 1.0)).rgb;
}

vec3 SamplePrevious(vec2 uv) {
    return texture2D(sampler2, clamp(uv, 0.0, 1.0)).rgb;
}

float ColorError(vec3 a, vec3 b) {
    vec3 d = a - b;
    return dot(d, d) + abs(Luma(a) - Luma(b)) * 0.20;
}

void main() {
    vec2 uv = v_texcoord0.xy;
    vec2 texel = u_texelDelta;

    vec3 current = SampleCurrent(uv);
    float strength = clamp(u_setting.x, 0.0, 1.0);

    // Estimate a small local motion vector by matching the current pixel
    // against the previous frame. This is intentionally lightweight for
    // mobile Adreno GPUs and avoids a full-resolution motion-vector buffer.
    float bestError = 1000000.0;
    vec2 bestMotion = vec2(0.0);

    for (int y = -1; y <= 1; ++y) {
        for (int x = -1; x <= 1; ++x) {
            vec2 offset = vec2(float(x), float(y)) * texel;
            vec3 previous = SamplePrevious(uv + offset);

            float error = ColorError(current, previous);

            // Prefer coherent motion over arbitrary equal-color matches.
            vec3 previousX = SamplePrevious(uv + offset + vec2(texel.x, 0.0));
            vec3 previousY = SamplePrevious(uv + offset + vec2(0.0, texel.y));
            error += length(previousX - previous) * 0.05;
            error += length(previousY - previous) * 0.05;

            if (error < bestError) {
                bestError = error;
                bestMotion = offset;
            }
        }
    }

    // Reproject the previous image toward the current position.
    vec2 motion = bestMotion * strength;
    vec3 history = SamplePrevious(uv + motion * 0.5);

    // Local history clamp reduces the ghost trails that the previous
    // implementation produced around moving edges.
    vec3 minCurrent = current;
    vec3 maxCurrent = current;

    for (int y = -1; y <= 1; ++y) {
        for (int x = -1; x <= 1; ++x) {
            vec3 c = SampleCurrent(uv + vec2(float(x), float(y)) * texel);
            minCurrent = min(minCurrent, c);
            maxCurrent = max(maxCurrent, c);
        }
    }

    vec3 range = max(maxCurrent - minCurrent, vec3(0.002));
    vec3 historyClamped = clamp(history, minCurrent - range * 0.25, maxCurrent + range * 0.25);

    float matchConfidence = clamp(1.0 - bestError * 5.0, 0.0, 1.0);
    float motionConfidence = clamp(length(bestMotion) / max(length(texel), 0.00001), 0.0, 1.0);

    // Reject history on cuts, disocclusions, and poor matches.
    float difference = length(current - historyClamped);
    float rejection = smoothstep(0.10, 0.35, difference);

    // u_timeDelta.x is wall-clock delta. Keep interpolation conservative
    // when timing is unstable, which helps avoid large temporal jumps.
    float timing = clamp(u_timeDelta.x * 60.0, 0.5, 2.0);
    float temporalWeight = mix(0.18, 0.42, matchConfidence);
    temporalWeight *= mix(0.85, 1.0, motionConfidence);
    temporalWeight *= strength;
    temporalWeight /= timing;
    temporalWeight *= (1.0 - rejection);

    vec3 generated = mix(current, historyClamped, clamp(temporalWeight, 0.0, 0.5));

    gl_FragColor = vec4(generated, 1.0);
}
