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

replacements = [
    ("Core/Config.cpp", 'ConfigSetting("AndroidFramerateMode", SETTING(g_Config, iDisplayFramerateMode), 1, CfgFlag::DEFAULT)', 'ConfigSetting("AndroidFramerateMode", SETTING(g_Config, iDisplayFramerateMode), 3, CfgFlag::DEFAULT)'),
    ("Core/Config.cpp", 'ConfigSetting("InflightFrames", SETTING(g_Config, iInflightFrames), 2, CfgFlag::DEFAULT)', 'ConfigSetting("InflightFrames", SETTING(g_Config, iInflightFrames), 1, CfgFlag::DEFAULT)'),
    ("Core/Config.cpp", 'ConfigSetting("RenderDuplicateFrames", SETTING(g_Config, bRenderDuplicateFrames), false, CfgFlag::PER_GAME)', 'ConfigSetting("RenderDuplicateFrames", SETTING(g_Config, bRenderDuplicateFrames), true, CfgFlag::PER_GAME)'),
    ("Core/Config.cpp", 'ConfigSetting("LowLatencyPresent", SETTING(g_Config, bLowLatencyPresent), false, CfgFlag::PER_GAME)', 'ConfigSetting("LowLatencyPresent", SETTING(g_Config, bLowLatencyPresent), true, CfgFlag::PER_GAME)'),
    ("Core/Config.cpp", 'ConfigSetting("Enable Logging", SETTING(g_Config, bEnableLogging), true, CfgFlag::PER_GAME)', 'ConfigSetting("Enable Logging", SETTING(g_Config, bEnableLogging), false, CfgFlag::PER_GAME)'),
    ("Core/Config.cpp", 'ConfigSetting("CheckForNewVersion", SETTING(g_Config, bCheckForNewVersion), true, CfgFlag::DEFAULT)', 'ConfigSetting("CheckForNewVersion", SETTING(g_Config, bCheckForNewVersion), false, CfgFlag::DEFAULT)'),
    ("android/build.gradle.kts", 'isJniDebuggable = true', 'isJniDebuggable = false'),
    ("android/build.gradle.kts", 'create("optimized") {
			isMinifyEnabled = false', 'create("optimized") {
			isDebuggable = false
			isMinifyEnabled = false'),
    ("android/AndroidManifest.xml", '<profileable android:shell="true" android:enabled="true" />', '<profileable android:shell="false" android:enabled="false" />'),
]
for item in replacements:
    replace_once(*item)

# Use a separate application ID for the Hyouka normal flavor.
replace_once(
    "android/build.gradle.kts",
    'applicationId = "org.ppsspp.ppsspp"
			dimension = "variant"',
    'applicationId = "com.hyouka.psp60"
			dimension = "variant"',
)

profile = ROOT / "android/hyouka-a73-profile.txt"
profile.write_text(
    "Hyouka PSP 60
"
    "Target device: OPPO A73 CPH2095
"
    "SoC: Qualcomm Snapdragon 662
"
    "GPU: Qualcomm Adreno 610
"
    "Display: 60 Hz, 1080x2400
"
    "Profile: Vulkan-first, low-latency, 1 inflight frame, duplicate frames enabled
"
    "Logging/debug defaults: disabled
"
    "Android optimized build: non-debuggable, non-profileable
",
    encoding="utf-8",
)
print("Hyouka PSP 60 OPPO A73 CPH2095 profile applied.")
