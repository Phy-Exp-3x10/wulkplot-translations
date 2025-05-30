import subprocess
import glob
import os
from pathlib import Path

TRANSLATIONS_DIR = Path(__file__).resolve().parent.parent
VENV_RUNNER_DIR = TRANSLATIONS_DIR / "tools" / "venv.py"

ts_files = glob.glob(str(TRANSLATIONS_DIR / "*.ts"))
success = []
failed = []

print("Compiling .ts files to .qm:")

for ts_file in ts_files:
    qm_file = ts_file.replace(".ts", ".qm")
    cmd = ["python", str(VENV_RUNNER_DIR), "lrelease", ts_file]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"[Compiled]:\t {os.path.basename(ts_file)} → {os.path.basename(qm_file)}")
        success.append(qm_file)
    else:
        print(f"[Failed]:\t   {os.path.basename(ts_file)}")
        print(result.stderr)
        failed.append(ts_file)

print("\n--- Summary ---")
print(f"{len(success)} succeeded")
print(f"{len(failed)} failed")

if failed:
    print("\nFailed files:")
    for f in failed:
        print(" -", f)
