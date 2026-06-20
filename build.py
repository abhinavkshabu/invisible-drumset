"""
Convenience build script for Invisible Drum Kit.

Usage:
    python build.py

This will:
  1. Install pyinstaller if it's missing.
  2. Run pyinstaller with build.spec.
  3. Print the output path.
"""

import subprocess
import sys
import shutil
from pathlib import Path


def ensure_pyinstaller():
    """Install PyInstaller if it isn't already available."""
    try:
        import PyInstaller  # noqa: F401
        print("[OK] PyInstaller is already installed.")
    except ImportError:
        print("[INFO] Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=6.0"])
        print("[OK] PyInstaller installed.")


def build():
    spec_file = Path(__file__).parent / "build.spec"
    if not spec_file.exists():
        print(f"[ERROR] Cannot find {spec_file}")
        sys.exit(1)

    print(f"[INFO] Building with spec: {spec_file}")
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", str(spec_file), "--noconfirm"],
        cwd=str(spec_file.parent),
    )

    if result.returncode != 0:
        print("[ERROR] Build failed. Check the output above for details.")
        sys.exit(result.returncode)

    output_dir = spec_file.parent / "dist" / "InvisibleDrumKit"
    exe_path = output_dir / "InvisibleDrumKit.exe"

    if exe_path.exists():
        print()
        print("=" * 60)
        print("  BUILD SUCCESSFUL")
        print(f"  Executable: {exe_path}")
        print(f"  Folder:     {output_dir}")
        print()
        print("  To distribute, zip the entire InvisibleDrumKit folder.")
        print("=" * 60)
    else:
        print(f"[WARNING] Build finished but {exe_path} not found.")
        print(f"          Check {output_dir} for output.")


if __name__ == "__main__":
    ensure_pyinstaller()
    build()
