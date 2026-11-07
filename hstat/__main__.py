"""Chạy ứng dụng: python -m hstat [file.hstat.json]"""
from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from .icons import qicon
from .main_window import APP_NAME, MainWindow
from .theme import apply_theme


ICON = Path(__file__).resolve().parent / "assets" / "app.ico"


def main() -> int:
    # Khi chạy bằng python.exe: để taskbar dùng icon của app thay vì icon Python.
    # Bản .exe đóng gói đã tự có icon riêng nên không cần.
    if sys.platform == "win32" and not getattr(sys, "frozen", False):
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("HStat.HeptacontakaienneagonStat")
        except Exception:  # noqa: BLE001
            pass
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setWindowIcon(QIcon(str(ICON)) if ICON.exists() else qicon("⚔️", 64))
    apply_theme(app)
    win = MainWindow(sys.argv[1] if len(sys.argv) > 1 else None)
    win.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
