"""Panel chỉnh sửa một thuộc tính: icon, giá trị, và không giới hạn số trường."""
from __future__ import annotations

from typing import Any, Callable

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import (QCheckBox, QComboBox, QDoubleSpinBox, QGridLayout,
                               QHBoxLayout, QLabel, QLineEdit, QMenu, QPlainTextEdit,
                               QProgressBar, QPushButton, QSizePolicy, QSlider, QSpinBox,
                               QToolButton, QVBoxLayout, QWidget)

from .attributes import ATTR_BY_KEY, GROUP_BY_KEY
from .dialogs import EmojiDialog, FieldDialog, pick_image_icon
from .icons import qicon
from .model import Character, FieldDef, Project, StatEntry


class StarRating(QWidget):
    valueChanged = Signal(int)

    def __init__(self, value: int = 0, parent=None):
        super().__init__(parent)
        self._value = 0
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self.buttons = []
        for i in range(1, 6):
            b = QToolButton()
            b.setAutoRaise(True)
            b.setFixedSize(26, 24)
            b.clicked.connect(lambda _=False, v=i: self.setValue(0 if v == self._value else v, True))
            lay.addWidget(b)
            self.buttons.append(b)
        lay.addStretch()
        self.setValue(int(value or 0))

    def setValue(self, v: int, emit: bool = False) -> None:
        self._value = max(0, min(5, v))
        for i, b in enumerate(self.buttons, 1):
            b.setText("★" if i <= self._value else "☆")
            b.setStyleSheet(f"color: {'#E3B341' if i <= self._value else '#6b6f78'}; font-size: 17px;")
        if emit:
            self.valueChanged.emit(self._value)


def make_field_widget(f: FieldDef, value: Any, on_change: Callable[[Any], None]) -> QWidget:
    """Tạo widget phù hợp với kiểu trường, gọi on_change(value) khi người dùng sửa."""
    if f.kind == "longtext":
        w = QPlainTextEdit(str(value or ""))
        w.setFixedHeight(72)
        w.setPlaceholderText(f.label + "…")
        w.textChanged.connect(lambda: on_change(w.toPlainText()))
    elif f.kind == "number":
        w = QDoubleSpinBox()
        w.setRange(-1e9, 1e9)
        w.setDecimals(2)
        w.setValue(float(value or 0))
        w.valueChanged.connect(on_change)
    elif f.kind == "bool":
        w = QCheckBox()
        w.setChecked(bool(value))
        w.toggled.connect(on_change)
    elif f.kind == "choice":
        w = QComboBox()
        opts = list(f.options)
        if value and value not in opts:
            opts.append(str(value))
        w.addItems(opts or ["—"])
        if value:
            w.setCurrentText(str(value))
        w.currentTextChanged.connect(on_change)
    elif f.kind == "rating":
        w = StarRating(int(value or 0))
        w.valueChanged.connect(on_change)
    else:
        w = QLineEdit(str(value or ""))
        w.setPlaceholderText(f.label + "…")
        w.textChanged.connect(on_change)
    return w


def _section(title: str) -> QLabel:
    lb = QLabel(title)
    lb.setObjectName("section")
    return lb


class AttributeEditor(QWidget):
    statChanged = Signal(str)        # base/bonus đổi → vẽ lại biểu đồ
    edited = Signal()                # bất kỳ thay đổi nào → đánh dấu chưa lưu
    iconChanged = Signal(str)
    fieldsStructureChanged = Signal()
    manageFieldsRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project: Project | None = None
        self.character: Character | None = None
        self.key: str | None = None
        self._loading = False

        root = QVBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(8)

        # --- Đầu: icon + tên
        head = QHBoxLayout()
        self.icon_btn = QToolButton()
        self.icon_btn.setFixedSize(76, 76)
        self.icon_btn.setIconSize(QSize(56, 56))
        self.icon_btn.setToolTip("Bấm để đổi icon (emoji hoặc ảnh)")
        self.icon_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        menu = QMenu(self)
        for text, fn in [("Nhập emoji / ký tự…", self._icon_emoji), ("Chọn ảnh từ máy…", self._icon_image),
                         ("Khôi phục icon mặc định", self._icon_reset)]:
            act = QAction(text, self)
            act.triggered.connect(fn)
            menu.addAction(act)
        self.icon_btn.setMenu(menu)
        head.addWidget(self.icon_btn)
        names = QVBoxLayout()
        names.setSpacing(1)
        self.name_en = QLabel()
        self.name_en.setObjectName("attrTitle")
        self.name_vi = QLabel()
        self.name_vi.setObjectName("muted")
        self.group_lb = QLabel()
        for lb in (self.name_en, self.name_vi, self.group_lb):
            lb.setWordWrap(True)
        names.addWidget(self.name_en)
        names.addWidget(self.name_vi)
        names.addWidget(self.group_lb)
        head.addLayout(names, 1)
        root.addLayout(head)

        # --- Chỉ số
        root.addWidget(_section("CHỈ SỐ"))
        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.base = QSpinBox()
        self.bonus = QSpinBox()
        self.bonus.setPrefix("+ ")
        self.total_bar = QProgressBar()
        self.total_bar.setTextVisible(True)
        self.total_bar.setFixedHeight(18)
        grid.addWidget(QLabel("Base"), 0, 0)
        grid.addWidget(self.slider, 0, 1)
        grid.addWidget(self.base, 0, 2)
        grid.addWidget(QLabel("Bonus"), 1, 0)
        grid.addWidget(self.bonus, 1, 2)
        bonus_hint = QLabel("trang bị, buff, talisman…")
        bonus_hint.setObjectName("muted")
        grid.addWidget(bonus_hint, 1, 1)
        grid.addWidget(QLabel("Tổng"), 2, 0)
        grid.addWidget(self.total_bar, 2, 1, 1, 2)
        root.addLayout(grid)
        self.slider.valueChanged.connect(self._on_base_slider)
        self.base.valueChanged.connect(self._on_base_spin)
        self.bonus.valueChanged.connect(self._on_bonus)

        # --- Trường
        hdr = QHBoxLayout()
        self.fields_title = _section("TRƯỜNG THÔNG TIN")
        hdr.addWidget(self.fields_title)
        hdr.addStretch()
        root.addLayout(hdr)
        self.fields_box = QWidget()
        self.fields_grid = QGridLayout(self.fields_box)
        self.fields_grid.setContentsMargins(0, 0, 0, 0)
        self.fields_grid.setVerticalSpacing(6)
        self.fields_grid.setColumnStretch(1, 1)
        root.addWidget(self.fields_box)

        btns = QHBoxLayout()
        add = QPushButton("＋ Thêm trường")
        add.setToolTip("Thêm trường chung (cho cả 79 thuộc tính) hoặc trường riêng")
        add.setObjectName("primary")
        add.clicked.connect(self._add_field)
        manage = QPushButton("⚙ Quản lý trường")
        manage.setToolTip("Sửa, xóa, sắp xếp các trường chung")
        manage.clicked.connect(self.manageFieldsRequested.emit)
        btns.addWidget(add)
        btns.addWidget(manage)
        root.addLayout(btns)
        hint = QLabel("◆ = trường riêng của thuộc tính này. Các trường còn lại là trường chung "
                      "cho cả 79 thuộc tính.")
        hint.setObjectName("muted")
        hint.setWordWrap(True)
        root.addWidget(hint)
        root.addStretch()
        self.setEnabled(False)

    # ------------------------------------------------------------------
    def set_context(self, project: Project, character: Character, key: str | None) -> None:
        self.project, self.character, self.key = project, character, key
        self.reload()

    @property
    def entry(self) -> StatEntry:
        return self.character.stats[self.key]

    def reload(self) -> None:
        if not (self.project and self.character and self.key):
            self.setEnabled(False)
            return
        self.setEnabled(True)
        self._loading = True
        a = ATTR_BY_KEY[self.key]
        g = GROUP_BY_KEY[a.group]
        mx = self.project.max_value
        self.icon_btn.setIcon(qicon(self.project.icon_for(self.key), 112))
        self.icon_btn.setStyleSheet(f"QToolButton {{ border: 2px solid {g.color}; border-radius: 38px;"
                                    f" background: {QColor(g.color).darker(320).name()}; }}"
                                    "QToolButton::menu-indicator { image: none; }")
        self.name_en.setText(a.name_en)
        self.name_vi.setText(a.name_vi)
        self.group_lb.setText(f"<span style='color:{g.color}'>■ {g.numeral}. {g.name_en}</span><br>"
                              f"<span style='color:#8C8F98'>{g.name_vi}</span>")
        e = self.entry
        self.slider.setRange(0, mx)
        self.base.setRange(0, mx)
        self.bonus.setRange(-mx, mx)
        self.slider.setValue(min(e.base, mx))
        self.base.setValue(e.base)
        self.bonus.setValue(e.bonus)
        self.slider.setStyleSheet(f"QSlider::sub-page:horizontal {{ background: {g.color}; border-radius: 3px; }}")
        self.total_bar.setStyleSheet(f"QProgressBar::chunk {{ background: {g.color}; border-radius: 4px; }}")
        self._update_total()
        self._build_fields()
        self._loading = False

    def _build_fields(self) -> None:
        while self.fields_grid.count():
            w = self.fields_grid.takeAt(0).widget()
            if w:
                w.hide()
                w.setParent(None)
                w.deleteLater()
        e = self.entry
        fields = self.project.fields_for(e)
        self.fields_title.setText(f"TRƯỜNG THÔNG TIN ({len(fields)})")
        for row, f in enumerate(fields):
            local = f in e.local_fields
            lb = QLabel(("◆ " if local else "") + f.label)
            lb.setWordWrap(True)
            lb.setFixedWidth(118)
            lb.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
            lb.setToolTip("Trường riêng" if local else "Trường chung (áp dụng cho mọi thuộc tính)")
            w = make_field_widget(f, e.values.get(f.key, f.default_value()),
                                  lambda v, k=f.key: self._set_value(k, v))
            w.setSizePolicy(QSizePolicy.Policy.Expanding, w.sizePolicy().verticalPolicy())
            self.fields_grid.addWidget(lb, row, 0)
            self.fields_grid.addWidget(w, row, 1)
            if local:
                rm = QToolButton()
                rm.setText("✕")
                rm.setAutoRaise(True)
                rm.setToolTip("Xóa trường riêng này")
                rm.clicked.connect(lambda _=False, fd=f: self._remove_local(fd))
                self.fields_grid.addWidget(rm, row, 2)

    # ------------------------------------------------------------ handlers
    def _set_value(self, key: str, value: Any) -> None:
        if self._loading:
            return
        self.entry.values[key] = value
        self.edited.emit()

    def _update_total(self) -> None:
        mx = self.project.max_value
        t = self.entry.total(mx)
        self.total_bar.setRange(0, mx)
        self.total_bar.setValue(t)
        self.total_bar.setFormat(f"{t} / {mx}")

    def _commit_stat(self) -> None:
        self._update_total()
        if not self._loading:
            self.statChanged.emit(self.key)
            self.edited.emit()

    def _on_base_slider(self, v: int) -> None:
        if self.base.value() != v:
            self.base.setValue(v)

    def _on_base_spin(self, v: int) -> None:
        if self.slider.value() != v:
            self.slider.setValue(v)
        if self.entry.base != v:
            self.entry.base = v
            self._commit_stat()

    def _on_bonus(self, v: int) -> None:
        if self.entry.bonus != v:
            self.entry.bonus = v
            self._commit_stat()

    def _add_field(self) -> None:
        d = FieldDialog(self, attr_name=ATTR_BY_KEY[self.key].name_en)
        if not d.exec():
            return
        f = d.result_field()
        if d.is_global():
            self.project.global_fields.append(f)
        else:
            self.entry.local_fields.append(f)
        self._build_fields()
        self.fieldsStructureChanged.emit()
        self.edited.emit()

    def _remove_local(self, f: FieldDef) -> None:
        self.entry.local_fields.remove(f)
        self.entry.values.pop(f.key, None)
        self._build_fields()
        self.edited.emit()

    def _set_icon(self, icon: str | None) -> None:
        if icon:
            self.project.icons[self.key] = icon
        else:
            self.project.icons.pop(self.key, None)
        self.icon_btn.setIcon(qicon(self.project.icon_for(self.key), 112))
        self.iconChanged.emit(self.key)
        self.edited.emit()

    def _icon_emoji(self) -> None:
        d = EmojiDialog(self.project.icon_for(self.key), self)
        if d.exec() and d.value():
            self._set_icon(d.value())

    def _icon_image(self) -> None:
        icon = pick_image_icon(self)
        if icon:
            self._set_icon(icon)

    def _icon_reset(self) -> None:
        self._set_icon(None)

