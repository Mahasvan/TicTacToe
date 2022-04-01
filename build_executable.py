import os
import sys
from pathlib import Path
import subprocess
import shutil


try:
    import PyInstaller.__main__ as pyi
    import PyInstaller.utils.osx
except ImportError:
    print("PyInstaller is not installed. Installing now...")
    subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller", "--upgrade"])
    print("PyInstaller installed successfully. Please rerun this script.")
    sys.exit(1)

os.chdir(Path(__file__).parent.absolute())  # change directory to the main directory

if not os.path.exists("main.py"):
    print("main.py not found")
    exit(1)

print("Starting Build...")

if sys.platform == "win32":
    # Build for Windows
    print("Building for Windows")
    pyi.run([
        "--name", "TicTacToe_windows",
        "--clean",
        "--onefile",
        "--icon", "Images/tictactoe.ico",
        "--log-level", "WARN",
        "main.py"
    ])
elif sys.platform == "darwin":
    try:
        # Build x86_64
        print("Building x86_64 executable for macOS...")
        pyi.run([
            "--name", "TicTacToe_macos_x86_64",
            "--clean",
            "--onefile",
            "--icon", "Images/tictactoe.icns",
            "--target-architecture", "x86_64",
            "--log-level", "WARN",
            "main.py"
        ])
    except PyInstaller.utils.osx.IncompatibleBinaryArchError:
        print("x86_64 architecture not supported. Skipping...")

    try:
        # Build ARM64
        print("Building ARM64 executable for macOS...")
        pyi.run([
            "--name", "TicTacToe_macos_arm64",
            "--clean",
            "--onefile",
            "--icon", "Images/tictactoe.icns",
            "--target-architecture", "arm64",
            "--log-level", "WARN",
            "main.py"
        ])
    except PyInstaller.utils.osx.IncompatibleBinaryArchError:
        print("ARM64 architecture not supported. Skipping...")

    try:
        # Build universal2
        print("Building Universal2 executable for macOS...")
        pyi.run([
            "--name", "TicTacToe_macos_universal",
            "--clean",
            "--onefile",
            "--icon", "Images/tictactoe.icns",
            "--target-architecture", "universal2",
            "--log-level", "WARN",
            "main.py"
        ])
    except PyInstaller.utils.osx.IncompatibleBinaryArchError:
        print("Universal2 architecture not supported. Skipping...")

else:
    # Build for other OSes, probably Linux
    print("Building executable for Linux...")
    pyi.run([
        "--name", "TicTacToe",
        "--clean",
        "--onefile",
        "--log-level", "WARN",
        "main.py"
    ])
print("Built successfully! Clearing temporary files...")
try:
    shutil.rmtree("./build")
except Exception as e:
    print(type(e).__name__, e)
    pass

print("Done! Executable is located in the `dist` folder!")
if input("Clean spec files? (y/n) ").lower() == "y":
    spec_files = [f for f in os.listdir(".") if f.endswith(".spec")]
    print()
    for f in spec_files:
        print("Removing spec file:", f)
        try:
            os.remove(f)
        except Exception as e:
            print(type(e).__name__, e)
            pass
    print("Spec files removed!")
