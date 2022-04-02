import os
import sys
from pathlib import Path
import subprocess
import shutil


try:
    import PyInstaller.__main__ as pyi
    if sys.platform == "darwin":
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
    try:
        pyi.run([
            "--name", "TicTacToe_windows",
            "--clean",
            "--onefile",
            "--icon", "Images/tictactoe.ico",
            "--log-level", "WARN",
            "main.py"
        ])
    except Exception as e:
        print("{}: {}".format(type(e).__name__, e))

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
    except Exception as e:
        print("{}: {}".format(type(e).__name__, e))
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
    except Exception as e:
        print("{}: {}".format(type(e).__name__, e))

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
    except Exception as e:
        print("{}: {}".format(type(e).__name__, e))

else:
    # Build for other OSes, probably Linux
    print("Building executable for Linux...")
    try:
        pyi.run([
            "--name", "TicTacToe",
            "--clean",
            "--onefile",
            "--log-level", "WARN",
            "main.py"
        ])
    except Exception as e:
        print("{}: {}".format(type(e).__name__, e))

print("Built successfully! Clearing temporary files...")
try:
    shutil.rmtree("./build")
except Exception as e:
    print(type(e).__name__, e)
    pass

print("Done! Executable is located in the `dist` folder!")
spec_clean = input("Clean spec files? (y/n): ").lower()
if spec_clean == "y":
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
else:
    print("Moving spec files to `spec_files` folder...")
    spec_files = [f for f in os.listdir(".") if f.endswith(".spec")]
    if not os.path.exists("spec_files"):
        os.mkdir("spec_files")
    for f in spec_files:
        print("Moving spec file:", f)
        try:
            shutil.copy(f, "spec_files", )  # we copy and not move because if moving, it errors out if the file already exists
        except Exception as e:
            print(type(e).__name__, e)
        os.remove(f)  # remove the original file after copying
    print("Spec files moved!")
