#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            return
        raise SystemExit(f"Expected text not found in {path}: {old!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")

# Hyouka PSP 60 A73 profile:
# Target: OPPO A73 CPH2095 / Snapdragon 662 / Adreno 610 / 60 Hz.
# The APK is intentionally built as this device-specific profile.
replacements = [
    (
        "Core/Config.cpp",
        'ConfigSetting("AndroidFramerateMode", SETTING(g_Config, iDisplayFramerateMode), 1, CfgFlag::DEFAULT)',
        'ConfigSetting("AndroidFramerateMode", SETTING(g_Config, iDisplayFramerateMode), 3, CfgFlag::DEFAULT)',
    ),
    (
        "Core/Config.cpp",
        'ConfigSetting("InflightFrames", SETTING(g_Config, iInflightFrames), 2, CfgFlag::DEFAULT)',
        'ConfigSetting("InflightFrames", SETTING(g_Config, iInflightFrames), 1, CfgFlag::DEFAULT)',
    ),
    (
        "Core/Config.cpp",
        'ConfigSetting("RenderDuplicateFrames", SETTING(g_Config, bRenderDuplicateFrames), false, CfgFlag::PER_GAME)',
        'ConfigSetting("RenderDuplicateFrames", SETTING(g_Config, bRenderDuplicateFrames), true, CfgFlag::PER_GAME)',
    ),
    (
        "Core/Config.cpp",
        'ConfigSetting("LowLatencyPresent", SETTING(g_Config, bLowLatencyPresent), false, CfgFlag::PER_GAME)',
        'ConfigSetting("LowLatencyPresent", SETTING(g_Config, bLowLatencyPresent), true, CfgFlag::PER_GAME)',
    ),
]

for item in replacements:
    replace_once(*item)

# Keep this build non-debuggable on Android.
replace_once(
    "android/build.gradle.kts",
    'isJniDebuggable = true',
    'isJniDebuggable = false',
)
replace_once(
    "android/build.gradle.kts",
    'isDebuggable = true',
    'isDebuggable = false',
)

profile = ROOT / "android/hyouka-a73-profile.txt"
profile.write_text(
    "Hyouka PSP 60\n"
    "Target device: OPPO A73 CPH2095\n"
    "SoC: Qualcomm Snapdragon 662\n"
    "GPU: Qualcomm Adreno 610\n"
    "Display: 60 Hz, 1080x2400\n"
    "Profile: Vulkan-first, low-latency, 1 inflight frame, duplicate frames enabled\n",
    encoding="utf-8",
)

print("Hyouka PSP 60 OPPO A73 CPH2095 profile applied.")
