# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for Invisible Drum Kit.

Usage:
    pyinstaller build.spec --noconfirm

Produces:  dist/InvisibleDrumKit/InvisibleDrumKit.exe  (one-folder bundle)
"""

from PyInstaller.utils.hooks import collect_data_files, collect_all

# ── MediaPipe ships .tflite models + protobuf data that must be bundled ──
mp_datas, mp_binaries, mp_hiddenimports = collect_all('mediapipe')

# ── OpenCV native binaries ──
cv2_datas, cv2_binaries, cv2_hiddenimports = collect_all('cv2')

# ── Pygame DLLs ──
pg_datas, pg_binaries, pg_hiddenimports = collect_all('pygame')

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=mp_binaries + cv2_binaries + pg_binaries,
    datas=[
        ('config.py', '.'),
    ] + mp_datas + cv2_datas + pg_datas,
    hiddenimports=mp_hiddenimports + cv2_hiddenimports + pg_hiddenimports + [
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='InvisibleDrumKit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,          # keep console so users see status messages
    icon=None,             # add an .ico path here if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='InvisibleDrumKit',
)
