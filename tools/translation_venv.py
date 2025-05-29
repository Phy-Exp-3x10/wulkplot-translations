import os
import subprocess
import sys
import shutil
from pathlib import Path

TRANSLATIONS_DIR = Path(__file__).resolve().parent.parent
VENV_DIR = TRANSLATIONS_DIR / ".venv-translations"
PYTHON_BIN = VENV_DIR / "Scripts" / "python.exe" if os.name == "nt" else VENV_DIR / "bin" / "python"

def create_venv():
    print(f"[Setup] Creating virtual environment at {VENV_DIR}...")
    subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)

def install_pyqt6_tools():
    print(f"[Setup] Installing pyqt6-tools in {VENV_DIR}...")
    subprocess.run([str(PYTHON_BIN), "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([str(PYTHON_BIN), "-m", "pip", "install", "--pre", "pyqt6-tools"], check=True)

def run_pyqt6_tools_tool(args):
    tool = ["qt6-tools"] + args
    print(f"[Running] {' '.join(tool)}")
    subprocess.run([str(PYTHON_BIN)] + ["-m"] + tool, check=True)

def main():
    if not VENV_DIR.exists():
        create_venv()
        install_pyqt6_tools()

    if not shutil.which("qt6-tools"):
        print("[Info] Executing within virtual environment.")
        run_pyqt6_tools_tool(sys.argv[1:])
    else:
        print("Unexpected: qt6-tools found globally, using system environment.")
        subprocess.run(["qt6-tools"] + sys.argv[1:], check=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python translation_venv.py [pylupdate6|lrelease|linguist] <args>")
        sys.exit(1)
    main()