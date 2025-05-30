import sys
from pathlib import Path

from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QMessageBox,
)

TRANSLATIONS_DIR = Path(__file__).resolve().parent.parent
VENV_RUNNER = TRANSLATIONS_DIR / "tools" / "venv.py"

class TranslateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose Translation File")

        ts_files = sorted([f.name for f in TRANSLATIONS_DIR.glob("*.ts")])
        if not ts_files:
            QMessageBox.information(
                self,
                "No Files",
                f"No .ts files found in {TRANSLATIONS_DIR}",
            )
            sys.exit(0)

        self.combo = QComboBox()
        self.combo.addItems(ts_files)

        layout = QFormLayout()
        layout.addRow(QLabel("Select a .ts file:"), self.combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.run_translation)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def run_translation(self):
        selected = self.combo.currentText()
        ts_path = TRANSLATIONS_DIR / selected

        success = QProcess.startDetached(
            sys.executable,
            [str(VENV_RUNNER), "linguist", str(ts_path)]
        )
        if not success:
            QMessageBox.critical(
                self,
                "Error",
                "Failed to launch translation process.",
            )
            return

        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = TranslateDialog()
    dialog.exec()
    sys.exit(0)