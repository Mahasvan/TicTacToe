import os
import sys
from pathlib import Path
import subprocess
import shutil

import PyInstaller.utils.osx

try:
    import PyInstaller.__main__ as pyi
except ImportError:
    print("PyInstaller is not installed. Installing now...")
    subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller", "--upgrade"])
    print("PyInstaller installed successfully. Please rerun this script.")
    sys.exit(1)

os.chdir(Path(__file__).parent.absolute())  # change directory to the main directory

if not os.path.exists("main.py"):
    print("main.py not found")
    exit(1)

print("Building executable...")

if sys.platform == "win32":
    pyi.run([
        "--name", "TicTacToe_windows",
        "--clean",
        "--onefile",
        "--icon", "Images/tictactoe.ico",
        "main.py"
    ])
elif sys.platform == "darwin":
    try:
    # Build x86_64
        pyi.run([
            "--name", "TicTacToe_macos_x86_64",
            "--clean",
            "--onefile",
            "--icon", "Images/tictactoe.icns",
            "--target-architecture", "x86_64",
            "main.py"
        ])
    except PyInstaller.utils.osx.IncompatibleBinaryArchError:
        print("x86_64 architecture not supported. Skipping...")

    # Build ARM64
    try:
        pyi.run([
            "--name", "TicTacToe_macos_arm64",
            "--clean",
            "--onefile",
            "--icon", "Images/tictactoe.icns",
            "--target-architecture", "arm64",
            "main.py"
        ])
    except PyInstaller.utils.osx.IncompatibleBinaryArchError:
        print("ARM64 architecture not supported. Skipping...")

    try:
        # Build universal2
        pyi.run([
            "--name", "TicTacToe_macos_universal",
            "--clean",
            "--onefile",
            "--icon", "Images/tictactoe.icns",
            "--target-architecture", "universal2",
            "main.py"
        ])
    except PyInstaller.utils.osx.IncompatibleBinaryArchError:
        print("Universal2 architecture not supported. Skipping...")

else:
    # Build for other OSes
    pyi.run([
        "--name", "TicTacToe",
        "--clean",
        "--onefile",
        "main.py"
    ])
print("Built successfully! Clearing temporary files...")
try:
    shutil.rmtree("./build")
except Exception as e:
    print(type(e).__name__, e)
    pass

print("Done! Executable is located in the `dist` folder!")
