import subprocess
import glob
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TRANSLATIONS_DIR = BASE_DIR / "translations"
VENV_RUNNER_DIR = TRANSLATIONS_DIR  / "tools" / "venv.py"

util_qt_files = glob.glob(str(BASE_DIR / "util_qt" / "**" / "*.py"), recursive=True)
source_files = [str(BASE_DIR / "gui.py")] + util_qt_files

ts_files = [
    str(TRANSLATIONS_DIR / "wulkplot_de.ts"),
    str(TRANSLATIONS_DIR / "wulkplot_fr.ts"),
    str(TRANSLATIONS_DIR / "wulkplot_no.ts"),
    str(TRANSLATIONS_DIR / "wulkplot_ru.ts"),
]

cmd = ["python", str(VENV_RUNNER_DIR), "pylupdate6"] + source_files
for ts in ts_files:
    cmd += ["-ts", ts]

print("Running command:")
print(" ".join(cmd))

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode != 0:
    print("Error:")
    print(result.stderr)
else:
    print("pylupdate6 completed successfully.")
