"""Giao diện tối, tông vàng kim."""
from __future__ import annotations

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

STYLE = """
QWidget { font-size: 13px; }
QMainWindow, QDialog { background: #16171c; }
QSplitter::handle { background: #23252c; width: 2px; }
QLabel#section { color: #C8A55A; font-weight: bold; letter-spacing: 1.5px; font-size: 11px;
                 padding-top: 8px; border-bottom: 1px solid #2c2f37; padding-bottom: 3px; }
QLabel#attrTitle { font-size: 19px; font-weight: bold; color: #f1e9d6; }
QLabel#muted { color: #8C8F98; }
QLabel#chartTitle { color: #C8A55A; font-size: 17px; font-weight: bold; letter-spacing: 2px; }
QFrame#infoBar { background: #1b1d23; border: 1px solid #2a2d35; border-radius: 10px; }
QTreeWidget { background: #17181d; border: 1px solid #2a2d35; border-radius: 6px; }
QTreeWidget::item { padding: 3px 2px; }
QTreeWidget::item:selected { background: #3a3220; color: #f1e9d6; }
QLineEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background: #1f2128; border: 1px solid #33363f; border-radius: 5px; padding: 4px 6px; }
QLineEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #C8A55A; }
QPushButton { background: #252730; border: 1px solid #353845; border-radius: 6px; padding: 6px 12px; }
QPushButton:hover { border-color: #C8A55A; }
QPushButton#primary { background: #4a3d1f; border-color: #C8A55A; color: #f5e7c4; font-weight: bold; }
QToolButton { border-radius: 6px; padding: 3px 6px; }
QToolButton:checked { background: #2c2e37; }
QProgressBar { background: #24262e; border: none; border-radius: 4px; text-align: center; color: #fff; }
QSlider::groove:horizontal { height: 6px; background: #2a2c34; border-radius: 3px; }
QSlider::handle:horizontal { background: #f1e9d6; width: 14px; margin: -5px 0; border-radius: 7px; }
QScrollArea { border: none; }
QCheckBox::indicator { width: 16px; height: 16px; border: 1px solid #5a5f6b; border-radius: 4px; background: #1f2128; }
QCheckBox::indicator:checked { background: #C8A55A; border-color: #e0c27a; }
QMenu { background: #1f2128; border: 1px solid #353845; }
QMenu::item:selected { background: #3a3220; }
QToolTip { background: #1f2128; color: #f1e9d6; border: 1px solid #C8A55A; }
"""


def apply_theme(app: QApplication) -> None:
    app.setStyle("Fusion")
    pal = QPalette()
    for role, col in [
        (QPalette.ColorRole.Window, "#16171c"), (QPalette.ColorRole.WindowText, "#e8e2d4"),
        (QPalette.ColorRole.Base, "#1b1c22"), (QPalette.ColorRole.AlternateBase, "#202229"),
        (QPalette.ColorRole.Text, "#e8e2d4"), (QPalette.ColorRole.Button, "#23252c"),
        (QPalette.ColorRole.ButtonText, "#e8e2d4"), (QPalette.ColorRole.Highlight, "#8a6d2f"),
        (QPalette.ColorRole.HighlightedText, "#ffffff"), (QPalette.ColorRole.ToolTipBase, "#1f2128"),
        (QPalette.ColorRole.ToolTipText, "#f1e9d6"), (QPalette.ColorRole.PlaceholderText, "#6b6f78"),
        (QPalette.ColorRole.Link, "#C8A55A"),
    ]:
        pal.setColor(role, QColor(col))
    pal.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor("#5d6068"))
    pal.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor("#5d6068"))
    app.setPalette(pal)
    app.setStyleSheet(STYLE)
