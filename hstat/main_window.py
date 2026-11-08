"""Cửa sổ chính: danh sách thuộc tính | biểu đồ 79 cạnh | panel chỉnh sửa."""
from __future__ import annotations

import html
import random
import unicodedata
from pathlib import Path

from PySide6.QtCore import QRectF, QSettings, QSize, QStandardPaths, Qt
from PySide6.QtGui import QAction, QColor, QCursor, QKeySequence, QPainter
from PySide6.QtWidgets import (QComboBox, QFileDialog, QFrame, QHBoxLayout, QHeaderView, QInputDialog, QLabel,
                               QLineEdit, QMainWindow, QMessageBox, QPlainTextEdit, QScrollArea,
                               QSplitter, QStyle, QStyledItemDelegate, QToolButton, QToolTip, QTreeWidget,
                               QTreeWidgetItem, QVBoxLayout, QWidget)

from . import __version__
from .attributes import ATTR_BY_KEY, ATTRIBUTES, GROUP_BY_KEY, GROUPS
from .chart import StatChart
from .dialogs import FieldManagerDialog
from .editor import AttributeEditor, _section
from .icons import color_dot, icon_pixmap, qicon
from .model import DEFAULT_BASE, Character, Project, new_project
from .polygon_names import polygon_name

APP_NAME = "Heptacontakaienneagon Stat"
FILE_FILTER = "Heptacontakaienneagon Stat (*.hstat.json *.json);;Tất cả (*)"
KEY_ROLE = Qt.ItemDataRole.UserRole
BAR_ROLE = Qt.ItemDataRole.UserRole + 1


def fold(s: str) -> str:
    """Bỏ dấu tiếng Việt để tìm kiếm: 'Sức mạnh' → 'suc manh'."""
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(ch for ch in unicodedata.normalize("NFD", s)
                   if unicodedata.category(ch) != "Mn").lower()


class ValueBarDelegate(QStyledItemDelegate):
    """Cột giá trị trong cây: vẽ thanh tiến độ màu theo nhóm."""

    def paint(self, painter: QPainter, option, index) -> None:
        data = index.data(BAR_ROLE)
        if index.column() != 1 or not data:
            return super().paint(painter, option, index)
        style = option.widget.style() if option.widget else None
        if style:
            style.drawPrimitive(QStyle.PrimitiveElement.PE_PanelItemViewItem, option, painter, option.widget)
        value, mx, color, label = data
        r = QRectF(option.rect).adjusted(4, option.rect.height() / 2 - 8, -6, -(option.rect.height() / 2 - 8))
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#262830"))
        painter.drawRoundedRect(r, 4, 4)
        c = QColor(color)
        c.setAlpha(210)
        painter.setBrush(c)
        painter.drawRoundedRect(QRectF(r.x(), r.y(), r.width() * max(0, min(1, value / mx)), r.height()), 4, 4)
        painter.setPen(QColor("#ffffff"))
        f = painter.font()
        f.setBold(True)
        f.setPixelSize(11)
        painter.setFont(f)
        painter.drawText(r, Qt.AlignmentFlag.AlignCenter, label)
        painter.restore()

    def sizeHint(self, option, index):
        s = super().sizeHint(option, index)
        return QSize(s.width(), max(s.height(), 24))


class MainWindow(QMainWindow):
    def __init__(self, path: str | None = None):
        super().__init__()
        self.settings = QSettings("HStat", "HeptacontakaienneagonStat")
        self.project: Project = new_project()
        self.char_index = 0
        self.path: str | None = None
        self.dirty = False
        self.selected_key: str = ATTRIBUTES[0].key
        self._sync = False
        self.tree_items: dict[str, QTreeWidgetItem] = {}
        self.group_items: dict[str, QTreeWidgetItem] = {}
        self.group_buttons: dict[str, QToolButton] = {}
        self.resize(1640, 980)
        self._build_ui()
        self._build_menus()

        start = path or self.settings.value("last_file", "")
        if start and Path(start).exists():
            self._load(start, quiet=not path)
        self.refresh_all()

    @property
    def character(self) -> Character:
        return self.project.characters[self.char_index]

    # ================================================================ UI
    def _build_ui(self) -> None:
        # ---------- Trái: nhân vật + cây thuộc tính
        left = QWidget()
        lv = QVBoxLayout(left)
        lv.setContentsMargins(10, 10, 6, 10)
        lv.addWidget(_section("NHÂN VẬT"))
        row = QHBoxLayout()
        self.char_combo = QComboBox()
        self.char_combo.currentIndexChanged.connect(self._on_char_changed)
        row.addWidget(self.char_combo, 1)
        for text, tip, fn in [("＋", "Thêm nhân vật mới", self.new_character),
                              ("⧉", "Nhân bản nhân vật", self.duplicate_character),
                              ("✎", "Đổi tên", self.rename_character),
                              ("✕", "Xóa nhân vật", self.delete_character)]:
            b = QToolButton()
            b.setText(text)
            b.setToolTip(tip)
            b.clicked.connect(fn)
            row.addWidget(b)
        lv.addLayout(row)
        self.notes = QPlainTextEdit()
        self.notes.setPlaceholderText("Ghi chú về nhân vật (class, cốt truyện, build…)")
        self.notes.setFixedHeight(64)
        self.notes.textChanged.connect(self._on_notes)
        lv.addWidget(self.notes)

        lv.addWidget(_section("79 THUỘC TÍNH"))
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍  Tìm thuộc tính (gõ không dấu cũng được)…")
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(self._apply_search)
        lv.addWidget(self.search)
        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderHidden(True)
        self.tree.setIconSize(QSize(22, 22))
        self.tree.setItemDelegate(ValueBarDelegate(self.tree))
        self.tree.setIndentation(14)
        self.tree.setUniformRowHeights(False)
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tree.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.tree.currentItemChanged.connect(self._on_tree_current)
        lv.addWidget(self.tree, 1)
        self._build_tree()

        # ---------- Giữa: biểu đồ
        center = QWidget()
        cv = QVBoxLayout(center)
        cv.setContentsMargins(6, 10, 6, 6)
        bar = QFrame()
        bar.setObjectName("infoBar")
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(14, 8, 14, 8)
        tcol = QVBoxLayout()
        tcol.setSpacing(0)
        self.chart_title = QLabel()
        self.chart_title.setObjectName("chartTitle")
        self.chart_sub = QLabel()
        self.chart_sub.setObjectName("muted")
        tcol.addWidget(self.chart_title)
        tcol.addWidget(self.chart_sub)
        bl.addLayout(tcol)
        bl.addStretch()
        self.info_icon = QLabel()
        self.info_icon.setFixedSize(40, 40)
        self.info_text = QLabel()
        self.info_text.setMinimumWidth(260)
        bl.addWidget(self.info_icon)
        bl.addWidget(self.info_text)
        cv.addWidget(bar)

        frow = QHBoxLayout()
        frow.setSpacing(4)
        lb = QLabel("Nhóm:")
        lb.setObjectName("muted")
        frow.addWidget(lb)
        for g in GROUPS:
            b = QToolButton()
            b.setText(f"{g.numeral} {g.short_en}")
            b.setCheckable(True)
            b.setChecked(True)
            b.setToolTip(f"{g.name_en} — {g.name_vi}\nBấm: bật/tắt · Chuột phải: chỉ xem nhóm này")
            b.setStyleSheet(
                f"QToolButton {{ color: #6b6f78; border: 1px solid #2c2f37; padding: 3px 7px; }}"
                f"QToolButton:checked {{ color: {g.color}; border: 1px solid {g.color};"
                f" background: {QColor(g.color).darker(400).name()}; font-weight: bold; }}")
            b.toggled.connect(self._on_group_filter)
            b.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            b.customContextMenuRequested.connect(lambda _p, k=g.key: self._solo_group(k))
            frow.addWidget(b)
            self.group_buttons[g.key] = b
        allb = QToolButton()
        allb.setText("Tất cả")
        allb.clicked.connect(lambda: self._solo_group(None))
        frow.addWidget(allb)
        frow.addStretch()
        lb2 = QLabel("So sánh:")
        lb2.setObjectName("muted")
        frow.addWidget(lb2)
        self.compare_combo = QComboBox()
        self.compare_combo.setMinimumWidth(150)
        self.compare_combo.currentIndexChanged.connect(self._on_compare)
        frow.addWidget(self.compare_combo)
        reset = QToolButton()
        reset.setText("⟲")
        reset.setToolTip("Đặt lại khung nhìn (phím 0)")
        reset.clicked.connect(lambda: self.chart.reset_view())
        frow.addWidget(reset)
        cv.addLayout(frow)

        self.chart = StatChart()
        self.chart.attributeSelected.connect(lambda k: self.select_attr(k))
        self.chart.attributeHovered.connect(self._on_chart_hover)
        cv.addWidget(self.chart, 1)
        hint = QLabel("Nhấp icon: chọn · Cuộn chuột: phóng to · Kéo: di chuyển · "
                      "Nhấp đúp nền: đặt lại · ←/→: chuyển thuộc tính")
        hint.setObjectName("muted")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cv.addWidget(hint)

        # ---------- Phải: editor
        self.editor = AttributeEditor()
        self.editor.statChanged.connect(self._on_stat_changed)
        self.editor.edited.connect(self.mark_dirty)
        self.editor.iconChanged.connect(self._on_icon_changed)
        self.editor.descriptionChanged.connect(lambda _k: self._refresh_tree_values())
        self.editor.manageFieldsRequested.connect(self.manage_fields)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.editor)
        scroll.setMinimumWidth(380)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        split = QSplitter()
        split.addWidget(left)
        split.addWidget(center)
        split.addWidget(scroll)
        split.setStretchFactor(1, 1)
        split.setSizes([320, 900, 420])
        self.setCentralWidget(split)
        self.statusBar().showMessage("Sẵn sàng")

    def _build_menus(self) -> None:
        def act(menu, text, fn, shortcut=None):
            a = QAction(text, self)
            if shortcut:
                a.setShortcut(QKeySequence(shortcut))
            a.triggered.connect(fn)
            menu.addAction(a)
            return a

        m = self.menuBar().addMenu("&Tệp")
        act(m, "Dự án mới", self.new_project, QKeySequence.StandardKey.New)
        act(m, "Mở…", self.open_file, QKeySequence.StandardKey.Open)
        act(m, "Lưu", self.save, QKeySequence.StandardKey.Save)
        act(m, "Lưu thành…", self.save_as, "Ctrl+Shift+S")
        m.addSeparator()
        act(m, "Xuất ảnh biểu đồ (PNG)…", self.export_png, "Ctrl+E")
        act(m, "Xuất bảng chỉ số (CSV/Excel)…", self.export_csv, "Ctrl+Shift+E")
        m.addSeparator()
        act(m, "Thoát", self.close, "Ctrl+Q")

        m = self.menuBar().addMenu("&Nhân vật")
        act(m, "Thêm nhân vật mới…", self.new_character)
        act(m, "Nhân bản nhân vật", self.duplicate_character, "Ctrl+D")
        act(m, "Đổi tên…", self.rename_character, "F2")
        act(m, "Xóa nhân vật", self.delete_character)
        m.addSeparator()
        act(m, "Đặt Base cho các nhóm đang hiển thị…", self.set_all_values)
        act(m, "Ngẫu nhiên hóa các nhóm đang hiển thị", self.randomize)
        act(m, "Xóa toàn bộ Bonus", self.clear_bonus)

        m = self.menuBar().addMenu("T&rường")
        act(m, "Quản lý trường chung…", self.manage_fields, "Ctrl+M")
        act(m, "Thang điểm tối đa…", self.set_max_value)

        m = self.menuBar().addMenu("Trợ &giúp")
        act(m, "Giới thiệu", self.about)

    # ========================================================= tree
    def _build_tree(self) -> None:
        self.tree.clear()
        self.tree_items.clear()
        self.group_items.clear()
        for g in GROUPS:
            gi = QTreeWidgetItem([f"{g.numeral}. {g.name_en}\n{g.name_vi}"])
            gi.setIcon(0, color_dot(g.color, 14))
            gi.setForeground(0, QColor(g.color).lighter(115))
            f = gi.font(0)
            f.setBold(True)
            gi.setFont(0, f)
            gi.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.tree.addTopLevelItem(gi)
            self.group_items[g.key] = gi
            for a in (a for a in ATTRIBUTES if a.group == g.key):
                it = QTreeWidgetItem([f"{a.name_en}\n{a.name_vi}"])
                it.setData(0, KEY_ROLE, a.key)
                gi.addChild(it)
                self.tree_items[a.key] = it
            gi.setExpanded(True)
        hdr = self.tree.header()
        hdr.setStretchLastSection(False)
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        hdr.resizeSection(1, 66)

    def _refresh_tree_values(self) -> None:
        mx = self.project.max_value
        for g in GROUPS:
            tot = []
            for a in (a for a in ATTRIBUTES if a.group == g.key):
                t = self.character.stats[a.key].total(mx)
                tot.append(t)
                it = self.tree_items[a.key]
                it.setIcon(0, qicon(self.project.icon_for(a.key), 44))
                it.setData(1, BAR_ROLE, (t, mx, g.color, str(t)))
                it.setToolTip(0, self._tooltip_html(a.key))
            avg = sum(tot) / len(tot)
            self.group_items[g.key].setData(1, BAR_ROLE, (avg, mx, g.color, f"TB {avg:.0f}"))
        self.tree.viewport().update()

    def _apply_search(self, text: str) -> None:
        q = fold(text.strip())
        for g in GROUPS:
            gi = self.group_items[g.key]
            any_visible = False
            for i in range(gi.childCount()):
                it = gi.child(i)
                a = ATTR_BY_KEY[it.data(0, KEY_ROLE)]
                ok = not q or q in fold(f"{a.name_en} {a.name_vi} {a.key}")
                it.setHidden(not ok)
                any_visible |= ok
            gi.setHidden(not any_visible)

    # ======================================================== refresh
    def refresh_all(self) -> None:
        self._sync = True
        self.char_combo.clear()
        self.char_combo.addItems([c.name for c in self.project.characters])
        self.char_index = min(self.char_index, len(self.project.characters) - 1)
        self.char_combo.setCurrentIndex(self.char_index)
        self.notes.setPlainText(self.character.notes)
        self._sync = False
        self._rebuild_compare()
        self.chart.set_data(self.project, self.character)
        self._refresh_tree_values()
        self.select_attr(self.selected_key)
        self._update_titles()

    def _rebuild_compare(self) -> None:
        prev = self.compare_combo.currentData()
        self._sync = True
        self.compare_combo.clear()
        self.compare_combo.addItem("— Không —", None)
        for i, c in enumerate(self.project.characters):
            if i != self.char_index:
                self.compare_combo.addItem(c.name, i)
        idx = self.compare_combo.findData(prev) if prev is not None else 0
        self.compare_combo.setCurrentIndex(max(0, idx))
        self._sync = False
        self._on_compare()

    def _update_titles(self) -> None:
        n = len(self.chart.visible_attrs())
        self.chart_title.setText(f"{polygon_name(n).upper()} STAT" if n else "—")
        groups = sum(b.isChecked() for b in self.group_buttons.values())
        self.chart_sub.setText(f"Đa giác {n} cạnh · {groups}/8 nhóm · thang 0–{self.project.max_value}"
                               f" · {self.character.name}")
        name = Path(self.path).name if self.path else "Chưa lưu"
        self.setWindowTitle(f"{APP_NAME} — {name}{' *' if self.dirty else ''}")

    def _tooltip_html(self, key: str, with_value: bool = False) -> str:
        a = ATTR_BY_KEY[key]
        g = GROUP_BY_KEY[a.group]
        value = ""
        if with_value:
            mx = self.project.max_value
            value = f" · <b style='color:#C8A55A'>{self.character.stats[key].total(mx)}</b>/{mx}"
        return (f"<qt><b>{a.name_en}</b> — {a.name_vi}<br>"
                f"<span style='color:{g.color}'>{g.numeral}. {g.name_en}</span>{value}"
                f"<p style='margin-top:6px'>{html.escape(self.project.description_for(key))}</p></qt>")

    def _on_chart_hover(self, key: str | None) -> None:
        self._update_info(key)
        if key:
            QToolTip.showText(QCursor.pos(), self._tooltip_html(key, with_value=True), self.chart)
        else:
            QToolTip.hideText()

    def _update_info(self, key: str | None = None) -> None:
        key = key or self.selected_key
        a = ATTR_BY_KEY[key]
        g = GROUP_BY_KEY[a.group]
        st = self.character.stats[key]
        mx = self.project.max_value
        self.info_icon.setPixmap(icon_pixmap(self.project.icon_for(key), 80).scaled(
            40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        bonus = f" <span style='color:#8C8F98'>({st.base} {'+' if st.bonus >= 0 else '−'} {abs(st.bonus)})</span>" \
            if st.bonus else ""
        self.info_text.setText(
            f"<b style='font-size:15px'>{a.name_en}</b> <span style='color:#8C8F98'>· {a.name_vi}</span><br>"
            f"<span style='color:{g.color}'>{g.numeral}. {g.short_en}</span> · "
            f"<b style='color:#C8A55A'>{st.total(mx)}</b>/{mx}{bonus}")

    def mark_dirty(self) -> None:
        if not self.dirty:
            self.dirty = True
            self._update_titles()

    # ===================================================== selection
    def select_attr(self, key: str) -> None:
        self.selected_key = key
        self.chart.select(key)
        self.editor.set_context(self.project, self.character, key)
        if not self._sync:
            self._sync = True
            self.tree.setCurrentItem(self.tree_items[key])
            self.tree.scrollToItem(self.tree_items[key])
            self._sync = False
        self._update_info()

    def _on_tree_current(self, cur: QTreeWidgetItem | None, _prev) -> None:
        if self._sync or cur is None:
            return
        key = cur.data(0, KEY_ROLE)
        if key:
            self._sync = True
            self.select_attr(key)
            self._sync = False

    def _on_stat_changed(self, _key: str) -> None:
        self.chart.update()
        self._refresh_tree_values()
        self._update_info()

    def _on_icon_changed(self, _key: str) -> None:
        self.chart.update()
        self._refresh_tree_values()
        self._update_info()

    def _on_group_filter(self) -> None:
        self.chart.set_visible_groups({k for k, b in self.group_buttons.items() if b.isChecked()})
        self._update_titles()

    def _solo_group(self, key: str | None) -> None:
        for k, b in self.group_buttons.items():
            b.blockSignals(True)
            b.setChecked(key is None or k == key)
            b.blockSignals(False)
        self._on_group_filter()

    def _on_compare(self, *_a) -> None:
        if self._sync:
            return
        idx = self.compare_combo.currentData()
        self.chart.set_compare(self.project.characters[idx] if idx is not None else None)

    def _on_char_changed(self, i: int) -> None:
        if self._sync or i < 0:
            return
        self.char_index = i
        self.refresh_all()

    def _on_notes(self) -> None:
        if self._sync:
            return
        self.character.notes = self.notes.toPlainText()
        self.mark_dirty()

    # ===================================================== characters
    def new_character(self) -> None:
        name, ok = QInputDialog.getText(self, "Nhân vật mới", "Tên nhân vật:",
                                        text=f"Nhân vật {len(self.project.characters) + 1}")
        if ok and name.strip():
            self.project.characters.append(Character(name.strip()))
            self.char_index = len(self.project.characters) - 1
            self.mark_dirty()
            self.refresh_all()

    def duplicate_character(self) -> None:
        self.project.characters.append(self.character.copy(self.character.name + " (bản sao)"))
        self.char_index = len(self.project.characters) - 1
        self.mark_dirty()
        self.refresh_all()

    def rename_character(self) -> None:
        name, ok = QInputDialog.getText(self, "Đổi tên", "Tên mới:", text=self.character.name)
        if ok and name.strip():
            self.character.name = name.strip()
            self.mark_dirty()
            self.refresh_all()

    def delete_character(self) -> None:
        if len(self.project.characters) <= 1:
            QMessageBox.information(self, "Không thể xóa", "Dự án cần ít nhất một nhân vật.")
            return
        if QMessageBox.question(self, "Xóa nhân vật", f"Xóa “{self.character.name}”?") \
                == QMessageBox.StandardButton.Yes:
            del self.project.characters[self.char_index]
            self.char_index = max(0, self.char_index - 1)
            self.compare_combo.setCurrentIndex(0)
            self.mark_dirty()
            self.refresh_all()

    def _visible(self):
        return self.chart.visible_attrs()

    def set_all_values(self) -> None:
        attrs = self._visible()
        v, ok = QInputDialog.getInt(self, "Đặt Base hàng loạt",
                                    f"Giá trị Base cho {len(attrs)} thuộc tính đang hiển thị:",
                                    min(DEFAULT_BASE, self.project.max_value), 0, self.project.max_value)
        if ok:
            for a in attrs:
                self.character.stats[a.key].base = v
            self.mark_dirty()
            self.refresh_all()

    def randomize(self) -> None:
        for a in self._visible():
            self.character.stats[a.key].base = random.randint(1, self.project.max_value)
        self.mark_dirty()
        self.refresh_all()

    def clear_bonus(self) -> None:
        for st in self.character.stats.values():
            st.bonus = 0
        self.mark_dirty()
        self.refresh_all()

    # ========================================================= fields
    def manage_fields(self) -> None:
        d = FieldManagerDialog(self.project, self)
        d.exec()
        if d.changed:
            self.mark_dirty()
            self.editor.reload()

    def set_max_value(self) -> None:
        v, ok = QInputDialog.getInt(self, "Thang điểm", "Giá trị tối đa của mỗi chỉ số:",
                                    self.project.max_value, 1, 9999)
        if ok:
            self.project.max_value = v
            self.mark_dirty()
            self.refresh_all()

    # ============================================================ files
    def _dialog_path(self, filename: str = "") -> str:
        """Thư mục mặc định cho hộp thoại: thư mục dùng lần trước, nếu không thì Documents."""
        folder = self.settings.value("last_dir", "") or QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DocumentsLocation)
        return str(Path(folder) / filename) if folder else filename

    def _remember_dir(self, path: str) -> None:
        self.settings.setValue("last_dir", str(Path(path).parent))

    def _confirm_discard(self) -> bool:
        if not self.dirty:
            return True
        r = QMessageBox.question(self, "Chưa lưu", "Dự án có thay đổi chưa lưu. Lưu lại trước không?",
                                 QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard
                                 | QMessageBox.StandardButton.Cancel)
        if r == QMessageBox.StandardButton.Save:
            return self.save()
        return r == QMessageBox.StandardButton.Discard

    def new_project(self) -> None:
        if not self._confirm_discard():
            return
        self.project, self.path, self.char_index, self.dirty = new_project(), None, 0, False
        self.refresh_all()

    def open_file(self) -> None:
        if not self._confirm_discard():
            return
        path, _ = QFileDialog.getOpenFileName(self, "Mở dự án", self._dialog_path(), FILE_FILTER)
        if path:
            self._remember_dir(path)
            self._load(path)
            self.refresh_all()

    def _load(self, path: str, quiet: bool = False) -> None:
        try:
            self.project = Project.load(path)
        except Exception as exc:  # noqa: BLE001 - báo lỗi cho người dùng
            if not quiet:
                QMessageBox.critical(self, "Lỗi mở file", f"Không mở được file:\n{exc}")
            return
        self.path, self.char_index, self.dirty = path, 0, False
        self.settings.setValue("last_file", path)
        self.statusBar().showMessage(f"Đã mở {path}", 5000)

    def save(self) -> bool:
        if not self.path:
            return self.save_as()
        try:
            self.project.save(self.path)
        except OSError as exc:
            QMessageBox.critical(self, "Lỗi lưu file", str(exc))
            return False
        self.dirty = False
        self.settings.setValue("last_file", self.path)
        self._update_titles()
        self.statusBar().showMessage(f"Đã lưu {self.path}", 5000)
        return True

    def save_as(self) -> bool:
        path, _ = QFileDialog.getSaveFileName(self, "Lưu dự án", self._dialog_path("stats.hstat.json"),
                                              FILE_FILTER)
        if not path:
            return False
        self._remember_dir(path)
        if not path.endswith(".json"):
            path += ".hstat.json"
        self.path = path
        return self.save()

    def export_png(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Xuất ảnh", self._dialog_path(f"{self.character.name}.png"),
                                              "PNG (*.png)")
        if path:
            self._remember_dir(path)
            ok = self.chart.export_image(path)
            self.statusBar().showMessage(f"Đã xuất {path}" if ok else "Xuất ảnh thất bại", 5000)

    def export_csv(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Xuất CSV", self._dialog_path(f"{self.character.name}.csv"),
                                              "CSV (*.csv)")
        if path:
            self._remember_dir(path)
            self.project.export_csv(self.character, path)
            self.statusBar().showMessage(f"Đã xuất {path}", 5000)

    def about(self) -> None:
        QMessageBox.about(self, APP_NAME, (
            f"<h3>{APP_NAME}</h3>"
            "<p>Biểu đồ radar <b>79 cạnh</b> (heptaconta-kai-ennea-gon = 70 + 9) cho "
            "<i>Hệ thống thuộc tính và năng lực nhân vật toàn diện</i>: 8 nhóm, 79 thuộc tính.</p>"
            "<p>Mỗi thuộc tính có icon (emoji hoặc ảnh), Base + Bonus và không giới hạn số trường "
            "thông tin: trường chung cho cả 79 thuộc tính hoặc trường riêng từng thuộc tính.</p>"
            "<p>Lọc nhóm để biểu đồ đổi thành đa giác tương ứng (vd. chỉ nhóm I → decagon).</p>"
            f"<p style='color:#8C8F98'>Phiên bản {__version__}</p>"))

    def closeEvent(self, e) -> None:
        if self._confirm_discard():
            e.accept()
        else:
            e.ignore()
