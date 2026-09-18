# Hyouka PSP 60

Android-focused PPSSPP build with a performance-oriented default profile.

## Included

- Upstream PPSSPP emulator core.
- Vulkan remains the Android default on supported 64-bit Android 8.1+ devices.
- Existing Android 12/API 31 frame-rate APIs are used by the PPSSPP renderer.
- Strongest existing PPSSPP 60 Hz mode enabled by default.
- Frame skipping disabled by default.
- Low-latency presentation enabled by default.
- One in-flight graphics frame by default.
- Duplicate-frame presentation enabled for games that internally render below 60 FPS.
- Separate Android application ID: com.hyouka.psp60.

A 60 Hz display request does not turn a 30 FPS game into a true 60 FPS game. Game-specific 60 FPS patches are not enabled globally.

Use only game files you are legally entitled to use.

Build from the "Hyouka PSP 60 APK" GitHub Actions workflow with "NormalOptimized".
