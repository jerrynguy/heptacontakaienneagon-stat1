"""Hộp thoại: tạo/sửa trường, quản lý trường chung, chọn icon."""
from __future__ import annotations

import re

from PySide6.QtWidgets import (QButtonGroup, QComboBox, QDialog, QDialogButtonBox, QFileDialog,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget,
                               QListWidgetItem, QMessageBox, QPushButton, QRadioButton,
                               QVBoxLayout, QWidget)

from .icons import image_file_to_icon
from .model import FIELD_KINDS, FieldDef, Project


class FieldDialog(QDialog):
    """Tạo mới hoặc sửa định nghĩa một trường."""

    def __init__(self, parent: QWidget | None = None, field: FieldDef | None = None,
                 allow_scope: bool = True, attr_name: str = ""):
        super().__init__(parent)
        self.setWindowTitle("Sửa trường" if field else "Thêm trường mới")
        self.setMinimumWidth(420)
        form = QFormLayout()
        self.label = QLineEdit(field.label if field else "")
        self.label.setPlaceholderText("Ví dụ: Cấp độ kỹ năng, Vũ khí khắc chế, Điểm yếu…")
        self.kind = QComboBox()
        for k, name in FIELD_KINDS.items():
            self.kind.addItem(name, k)
        if field:
            self.kind.setCurrentIndex(list(FIELD_KINDS).index(field.kind))
        self.options = QLineEdit(", ".join(field.options) if field else "")
        self.options.setPlaceholderText("Các lựa chọn, cách nhau bằng dấu phẩy")
        form.addRow("Tên trường:", self.label)
        form.addRow("Kiểu dữ liệu:", self.kind)
        form.addRow("Lựa chọn:", self.options)
        self.kind.currentIndexChanged.connect(self._sync)
        self._sync()

        lay = QVBoxLayout(self)
        lay.addLayout(form)
        self.scope_all = None
        if allow_scope:
            self.scope_one = QRadioButton(f"Chỉ cho thuộc tính này ({attr_name})" if attr_name
                                          else "Chỉ cho thuộc tính đang chọn")
            self.scope_all = QRadioButton("Trường chung cho cả 79 thuộc tính")
            self.scope_all.setChecked(True)
            grp = QButtonGroup(self)
            grp.addButton(self.scope_one)
            grp.addButton(self.scope_all)
            lay.addWidget(QLabel("Phạm vi:"))
            lay.addWidget(self.scope_all)
            lay.addWidget(self.scope_one)
        bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        bb.accepted.connect(self._accept)
        bb.rejected.connect(self.reject)
        lay.addWidget(bb)

    def _sync(self) -> None:
        self.options.setEnabled(self.kind.currentData() == "choice")

    def _accept(self) -> None:
        if not self.label.text().strip():
            QMessageBox.warning(self, "Thiếu tên", "Hãy nhập tên trường.")
            return
        self.accept()

    def is_global(self) -> bool:
        return self.scope_all is None or self.scope_all.isChecked()

    def apply_to(self, field: FieldDef) -> FieldDef:
        field.label = self.label.text().strip()
        field.kind = self.kind.currentData()
        field.options = [o.strip() for o in self.options.text().split(",") if o.strip()]
        return field

    def result_field(self) -> FieldDef:
        return self.apply_to(FieldDef(label=""))


class FieldManagerDialog(QDialog):
    """Quản lý danh sách trường chung (áp dụng cho mọi thuộc tính)."""

    def __init__(self, project: Project, parent: QWidget | None = None):
        super().__init__(parent)
        self.project = project
        self.changed = False
        self.setWindowTitle("Quản lý trường chung")
        self.resize(460, 420)
        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(lambda _i: self._edit())
        btns = QVBoxLayout()
        for text, fn in [("Thêm…", self._add), ("Sửa…", self._edit), ("Xóa", self._delete),
                         ("▲ Lên", lambda: self._move(-1)), ("▼ Xuống", lambda: self._move(1))]:
            b = QPushButton(text)
            b.clicked.connect(fn)
            btns.addWidget(b)
        btns.addStretch()
        top = QHBoxLayout()
        top.addWidget(self.list, 1)
        top.addLayout(btns)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Các trường này xuất hiện ở <b>mọi</b> thuộc tính của <b>mọi</b> nhân vật."))
        lay.addLayout(top)
        bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        bb.rejected.connect(self.accept)
        bb.accepted.connect(self.accept)
        lay.addWidget(bb)
        self._refresh()

    def _refresh(self, row: int | None = None) -> None:
        self.list.clear()
        for f in self.project.global_fields:
            it = QListWidgetItem(f"{f.label}    ·    {FIELD_KINDS[f.kind]}")
            self.list.addItem(it)
        if row is not None and 0 <= row < self.list.count():
            self.list.setCurrentRow(row)

    def _add(self) -> None:
        d = FieldDialog(self, allow_scope=False)
        if d.exec():
            self.project.global_fields.append(d.result_field())
            self.changed = True
            self._refresh(len(self.project.global_fields) - 1)

    def _edit(self) -> None:
        r = self.list.currentRow()
        if r < 0:
            return
        f = self.project.global_fields[r]
        d = FieldDialog(self, field=f, allow_scope=False)
        if d.exec():
            d.apply_to(f)
            self.changed = True
            self._refresh(r)

    def _delete(self) -> None:
        r = self.list.currentRow()
        if r < 0:
            return
        f = self.project.global_fields[r]
        if QMessageBox.question(self, "Xóa trường",
                                f"Xóa trường “{f.label}” khỏi tất cả thuộc tính?\n"
                                "Dữ liệu đã nhập trong trường này cũng sẽ bị xóa.") \
                != QMessageBox.StandardButton.Yes:
            return
        del self.project.global_fields[r]
        for ch in self.project.characters:
            for st in ch.stats.values():
                st.values.pop(f.key, None)
        self.changed = True
        self._refresh(min(r, len(self.project.global_fields) - 1))

    def _move(self, delta: int) -> None:
        r = self.list.currentRow()
        j = r + delta
        fs = self.project.global_fields
        if r < 0 or not 0 <= j < len(fs):
            return
        fs[r], fs[j] = fs[j], fs[r]
        self.changed = True
        self._refresh(j)


class EmojiDialog(QDialog):
    """Nhập emoji / ký tự bất kỳ làm icon."""

    QUICK = "⚔️🗡️🛡️🏹🔥❄️⚡🌙☀️💀👁️🧠💪❤️🔮✨🌿🐉🦅🐺🕯️📜🔱⚜️🗝️💎🌀🩸🌑🍂"

    def __init__(self, current: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Đổi icon bằng emoji / ký tự")
        self.edit = QLineEdit("" if current.startswith("img:") else current)
        self.edit.setMaxLength(16)
        f = self.edit.font()
        f.setPointSize(20)
        self.edit.setFont(f)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Gõ hoặc dán emoji (Windows: phím Win + . để mở bảng emoji):"))
        lay.addWidget(self.edit)
        lay.addWidget(QLabel("Gợi ý nhanh:"))
        row = None
        items = re.findall(r".️?", self.QUICK)
        for i, em in enumerate(items):
            if i % 10 == 0:
                row = QHBoxLayout()
                row.setSpacing(2)
                lay.addLayout(row)
            b = QPushButton(em)
            b.setFixedSize(36, 32)
            b.clicked.connect(lambda _=False, e=em: self.edit.setText(e))
            row.addWidget(b)
        bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        lay.addWidget(bb)

    def value(self) -> str:
        return self.edit.text().strip()


def pick_image_icon(parent: QWidget) -> str | None:
    path, _ = QFileDialog.getOpenFileName(parent, "Chọn ảnh làm icon", "",
                                          "Ảnh (*.png *.jpg *.jpeg *.bmp *.gif *.webp *.svg *.ico)")
    if not path:
        return None
    icon = image_file_to_icon(path)
    if icon is None:
        QMessageBox.warning(parent, "Không đọc được ảnh", f"Không mở được file:\n{path}")
    return icon

