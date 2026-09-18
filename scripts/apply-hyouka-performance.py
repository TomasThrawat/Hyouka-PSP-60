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

# Performance defaults.
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

# Play-only / no-debug defaults.
replacements = [
    ('ConfigSetting("Enable Logging", SETTING(g_Config, bEnableLogging), true, CfgFlag::PER_GAME)',
     'ConfigSetting("Enable Logging", SETTING(g_Config, bEnableLogging), false, CfgFlag::PER_GAME)'),
    ('ConfigSetting("FileLogging", SETTING(g_Config, bEnableFileLogging), false, CfgFlag::PER_GAME)',
     'ConfigSetting("FileLogging", SETTING(g_Config, bEnableFileLogging), false, CfgFlag::PER_GAME)'),
    ('ConfigSetting("ShowDebuggerOnLoad", SETTING(g_Config, bShowDebuggerOnLoad), false, CfgFlag::DEFAULT)',
     'ConfigSetting("ShowDebuggerOnLoad", SETTING(g_Config, bShowDebuggerOnLoad), false, CfgFlag::DEFAULT)'),
    ('ConfigSetting("ShowImDebugger", SETTING(g_Config, bShowImDebugger), false, CfgFlag::DONT_SAVE)',
     'ConfigSetting("ShowImDebugger", SETTING(g_Config, bShowImDebugger), false, CfgFlag::DONT_SAVE)'),
    ('ConfigSetting("CheckForNewVersion", SETTING(g_Config, bCheckForNewVersion), true, CfgFlag::DEFAULT)',
     'ConfigSetting("CheckForNewVersion", SETTING(g_Config, bCheckForNewVersion), false, CfgFlag::DEFAULT)'),
    ('ConfigSetting("DiscordRichPresence", SETTING(g_Config, bDiscordRichPresence), false, CfgFlag::DEFAULT)',
     'ConfigSetting("DiscordRichPresence", SETTING(g_Config, bDiscordRichPresence), false, CfgFlag::DEFAULT)'),
    ('ConfigSetting("DebugOverlay", SETTING(g_Config, iDebugOverlay), 0, CfgFlag::DONT_SAVE)',
     'ConfigSetting("DebugOverlay", SETTING(g_Config, iDebugOverlay), 0, CfgFlag::DONT_SAVE)'),
    ('ConfigSetting("RemoteDebuggerOnStartup", SETTING(g_Config, bRemoteDebuggerOnStartup), false, CfgFlag::DEFAULT)',
     'ConfigSetting("RemoteDebuggerOnStartup", SETTING(g_Config, bRemoteDebuggerOnStartup), false, CfgFlag::DEFAULT)'),
    ('ConfigSetting("RemoteDebuggerLocal", SETTING(g_Config, bRemoteDebuggerLocal), false, CfgFlag::DEFAULT)',
     'ConfigSetting("RemoteDebuggerLocal", SETTING(g_Config, bRemoteDebuggerLocal), false, CfgFlag::DEFAULT)'),
    ('ConfigSetting("GfxDebugOutput", SETTING(g_Config, bGfxDebugOutput), false, CfgFlag::DONT_SAVE)',
     'ConfigSetting("GfxDebugOutput", SETTING(g_Config, bGfxDebugOutput), false, CfgFlag::DONT_SAVE)'),
    ('ConfigSetting("LogFrameDrops", SETTING(g_Config, bLogFrameDrops), false, CfgFlag::DEFAULT)',
     'ConfigSetting("LogFrameDrops", SETTING(g_Config, bLogFrameDrops), false, CfgFlag::DEFAULT)'),
    ('ConfigSetting("GpuLogProfiler", SETTING(g_Config, bGpuLogProfiler), false, CfgFlag::DEFAULT)',
     'ConfigSetting("GpuLogProfiler", SETTING(g_Config, bGpuLogProfiler), false, CfgFlag::DEFAULT)'),
    ('ConfigSetting("ShowDeveloperMenu", SETTING(g_Config, bShowDeveloperMenu), false, CfgFlag::DEFAULT)',
     'ConfigSetting("ShowDeveloperMenu", SETTING(g_Config, bShowDeveloperMenu), false, CfgFlag::DEFAULT)'),
]
for old, new in replacements:
    replace_once("Core/Config.cpp", old, new)

replace_once("android/build.gradle.kts",
    'isJniDebuggable = true',
    'isJniDebuggable = false')

replace_once("android/build.gradle.kts",
    'create("optimized") {\n\t\t\tisMinifyEnabled = false',
    'create("optimized") {\n\t\t\tisDebuggable = false\n\t\t\tisMinifyEnabled = false')

replace_once("android/build.gradle.kts",
    'create("optimized") {\n\t\t\tisDebuggable = false\n\t\t\tisMinifyEnabled = false\n\t\t\tisJniDebuggable = false',
    'create("optimized") {\n\t\t\tisDebuggable = false\n\t\t\tisMinifyEnabled = false\n\t\t\tisJniDebuggable = false')

print("Hyouka PSP 60 Minimal Play-Only profile applied: performance defaults, logging/debug disabled, optimized Android build non-debuggable.")
