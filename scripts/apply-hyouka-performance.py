#!/usr/bin/env python3
from pathlib import Path

def replace_once(path: str, old: str, new: str):
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    if old not in s:
        if new in s:
            return
        raise SystemExit(f"Expected text not found in {path}: {old!r}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")

replace_once("Core/Config.cpp",
    'ConfigSetting("AndroidFramerateMode", SETTING(g_Config, iDisplayFramerateMode), 1, CfgFlag::DEFAULT)',
    'ConfigSetting("AndroidFramerateMode", SETTING(g_Config, iDisplayFramerateMode), 3, CfgFlag::DEFAULT)')
replace_once("Core/Config.cpp",
    'ConfigSetting("InflightFrames", SETTING(g_Config, iInflightFrames), 2, CfgFlag::DEFAULT)',
    'ConfigSetting("InflightFrames", SETTING(g_Config, iInflightFrames), 1, CfgFlag::DEFAULT)')
replace_once("Core/Config.cpp",
    'ConfigSetting("RenderDuplicateFrames", SETTING(g_Config, bRenderDuplicateFrames), false, CfgFlag::PER_GAME)',
    'ConfigSetting("RenderDuplicateFrames", SETTING(g_Config, bRenderDuplicateFrames), true, CfgFlag::PER_GAME)')
replace_once("Core/Config.cpp",
    'ConfigSetting("LowLatencyPresent", SETTING(g_Config, bLowLatencyPresent), false, CfgFlag::PER_GAME)',
    'ConfigSetting("LowLatencyPresent", SETTING(g_Config, bLowLatencyPresent), true, CfgFlag::PER_GAME)')
replace_once("android/build.gradle.kts",
    'applicationId = "org.ppsspp.ppsspp"',
    'applicationId = "com.hyouka.psp60"')
replace_once("android/res/values/strings.xml",
    '<string name="app_name">PPSSPP</string>',
    '<string name="app_name">Hyouka PSP 60</string>')
replace_once("android/res/values/strings.xml",
    '<string name="shortcut_name">PPSSPP game</string>',
    '<string name="shortcut_name">Hyouka PSP 60 game</string>')
print("Hyouka PSP 60 build configuration applied.")
