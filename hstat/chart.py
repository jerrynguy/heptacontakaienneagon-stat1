"""Widget vẽ biểu đồ radar N cạnh (mặc định 79 = heptacontakaienneagon)."""
from __future__ import annotations

import math
import unicodedata

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import (QBrush, QColor, QFont, QFontMetricsF, QImage, QPainter, QPen,
                           QPolygonF, QRadialGradient)
from PySide6.QtWidgets import QWidget

from .attributes import ATTRIBUTES, GROUP_BY_KEY, GROUPS, AttributeDef
from .icons import draw_icon
from .model import Character, Project
from .polygon_names import polygon_name

BG = QColor("#121317")
GRID = QColor("#343842")
GOLD = QColor("#C8A55A")
TEXT = QColor("#E8E2D4")
MUTED = QColor("#8C8F98")
COMPARE = QColor("#6FB7FF")


def _font(px: float, bold: bool = False, spacing: float = 0) -> QFont:
    f = QFont()
    f.setPixelSize(max(7, int(px)))
    f.setBold(bold)
    if spacing:
        f.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, spacing)
    return f


def _alpha(c: QColor, a: int) -> QColor:
    c = QColor(c)
    c.setAlpha(a)
    return c


class StatChart(QWidget):
    attributeSelected = Signal(str)
    attributeHovered = Signal(object)  # str | None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project: Project | None = None
        self.character: Character | None = None
        self.compare: Character | None = None
        self.visible_groups: set[str] = {g.key for g in GROUPS}
        self.selected_key: str | None = None
        self.hover_key: str | None = None
        self.show_overlays = True
        self.zoom = 1.0
        self.pan = QPointF(0, 0)
        self._press: QPointF | None = None
        self._pan_start = QPointF(0, 0)
        self._dragging = False
        self._geom = None  # (center, R, r_icon, icon_size, attrs)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMinimumSize(520, 480)

    # ------------------------------------------------------------------ data
    def set_data(self, project: Project, character: Character) -> None:
        self.project, self.character = project, character
        self.update()

    def set_compare(self, character: Character | None) -> None:
        self.compare = character
        self.update()

    def set_visible_groups(self, keys: set[str]) -> None:
        self.visible_groups = set(keys)
        self.update()

    def select(self, key: str | None) -> None:
        self.selected_key = key
        self.update()

    def visible_attrs(self) -> list[AttributeDef]:
        return [a for a in ATTRIBUTES if a.group in self.visible_groups]

    def reset_view(self) -> None:
        self.zoom, self.pan = 1.0, QPointF(0, 0)
        self.update()

    # ------------------------------------------------------------- geometry
    @staticmethod
    def _angle(i: int, n: int) -> float:
        return -math.pi / 2 + 2 * math.pi * i / n

    @staticmethod
    def _pt(c: QPointF, r: float, a: float) -> QPointF:
        return QPointF(c.x() + r * math.cos(a), c.y() + r * math.sin(a))

    @staticmethod
    def _icon_size(r: float, n: int) -> float:
        return max(9.0, min(52.0, 2 * math.pi * r / max(n, 1) * 0.70))

    def _layout(self, rect: QRectF, n: int, interactive: bool):
        half = min(rect.width(), rect.height()) / 2 - 10
        r = half - 60
        for _ in range(3):  # bán kính + vòng icon + nhãn cong phải vừa khung
            r = max(60.0, half - 54 - self._icon_size(r, n))
        c = rect.center()
        if interactive:
            c = c + self.pan
            r *= self.zoom
        return c, r

    # ------------------------------------------------------------ painting
    def paintEvent(self, _e) -> None:
        p = QPainter(self)
        self.render_chart(p, QRectF(self.rect()), interactive=True)
        p.end()

    def export_image(self, path: str, width: int = 1400, height: int = 1100, scale: int = 2) -> bool:
        img = QImage(width * scale, height * scale, QImage.Format.Format_ARGB32_Premultiplied)
        img.fill(BG)
        p = QPainter(img)
        p.scale(scale, scale)
        self.render_chart(p, QRectF(0, 0, width, height), interactive=False)
        p.end()
        return img.save(path)

    def render_chart(self, p: QPainter, rect: QRectF, interactive: bool) -> None:
        p.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing
                         | QPainter.RenderHint.SmoothPixmapTransform)
        bg = QRadialGradient(rect.center(), max(rect.width(), rect.height()) * 0.7)
        bg.setColorAt(0, QColor("#1b1d23"))
        bg.setColorAt(1, BG)
        p.fillRect(rect, bg)
        if not (self.project and self.character):
            return
        attrs = self.visible_attrs()
        n = len(attrs)
        if n == 0:
            p.setPen(MUTED)
            p.setFont(_font(16))
            p.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Hãy bật ít nhất một nhóm thuộc tính")
            self._geom = None
            return

        mx = self.project.max_value
        full = rect
        if not interactive:  # ảnh xuất: dành dải trên cùng cho tiêu đề
            self._header(p, QRectF(rect.left(), rect.top(), rect.width(), 92), attrs)
            rect = rect.adjusted(0, 92, 0, 0)
        c, R = self._layout(rect, n, interactive)
        step = 2 * math.pi / n
        icon = self._icon_size(R, n)
        r_icon = R + icon * 0.5 + 9
        r_ring = r_icon + icon * 0.5 + 9
        if interactive:
            self._geom = (c, R, r_icon, icon, attrs)
        ang = [self._angle(i, n) for i in range(n)]
        vert = [self._pt(c, R, a) for a in ang]

        # Gom các thuộc tính liên tiếp thành dải theo nhóm
        spans: list[tuple[str, int, int]] = []
        for i, a in enumerate(attrs):
            if spans and spans[-1][0] == a.group:
                spans[-1] = (a.group, spans[-1][1], i)
            else:
                spans.append((a.group, i, i))

        # 1) Nền hình quạt cho từng nhóm (bám đúng biên đa giác)
        p.setPen(Qt.PenStyle.NoPen)
        for gk, s, e in spans:
            col = QColor(GROUP_BY_KEY[gk].color)
            if n >= 3 and len(spans) > 1:
                poly = QPolygonF([c, (vert[(s - 1) % n] + vert[s]) / 2, *vert[s:e + 1],
                                  (vert[e] + vert[(e + 1) % n]) / 2])
            else:
                poly = QPolygonF(vert if n >= 3 else [])
            grad = QRadialGradient(c, R)
            grad.setColorAt(0, _alpha(col, 0))
            grad.setColorAt(1, _alpha(col, 46))
            p.setBrush(QBrush(grad))
            p.drawPolygon(poly)

        # 2) Lưới: các vòng đa giác đồng tâm
        rings = [0.2, 0.4, 0.6, 0.8, 1.0]
        p.setBrush(Qt.BrushStyle.NoBrush)
        for k, fr in enumerate(rings):
            p.setPen(QPen(_alpha(GOLD, 150) if fr == 1.0 else GRID, 1.6 if fr == 1.0 else 1.0))
            if n >= 3:
                p.drawPolygon(QPolygonF([self._pt(c, R * fr, a) for a in ang]))
            else:
                p.drawEllipse(c, R * fr, R * fr)

        # 3) Nan hoa
        for i, a in enumerate(ang):
            hl = attrs[i].key in (self.selected_key, self.hover_key)
            p.setPen(QPen(_alpha(GOLD, 220) if hl else _alpha(GRID, 170), 2 if hl else 0.8))
            p.drawLine(c, vert[i])

        # 4) Nhãn giá trị trên vòng lưới
        p.setFont(_font(max(9, min(12, R / 28))))
        p.setPen(MUTED)
        lab_a = ang[0] + step / 2
        for fr in rings:
            pt = self._pt(c, R * fr, lab_a)
            p.drawText(QRectF(pt.x() + 3, pt.y() - 8, 40, 16), Qt.AlignmentFlag.AlignLeft
                       | Qt.AlignmentFlag.AlignVCenter, str(round(mx * fr)))

        def poly_for(ch: Character, use_base: bool = False) -> QPolygonF:
            pts = []
            for i, a in enumerate(attrs):
                st = ch.stats[a.key]
                v = max(0, min(mx, st.base)) if use_base else st.total(mx)
                pts.append(self._pt(c, R * v / mx, ang[i]))
            return QPolygonF(pts)

        # 5) Nhân vật so sánh
        if self.compare is not None and self.compare is not self.character:
            p.setBrush(_alpha(COMPARE, 28))
            pen = QPen(COMPARE, 1.8, Qt.PenStyle.DashLine)
            p.setPen(pen)
            p.drawPolygon(poly_for(self.compare))

        # 6) Lớp base (khi có bonus)
        has_bonus = any(self.character.stats[a.key].bonus for a in attrs)
        if has_bonus:
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(_alpha(TEXT, 120), 1.0, Qt.PenStyle.DotLine))
            p.drawPolygon(poly_for(self.character, use_base=True))

        # 7) Đa giác chính
        main = poly_for(self.character)
        fill = QRadialGradient(c, R)
        fill.setColorAt(0, _alpha(GOLD, 60))
        fill.setColorAt(1, _alpha(GOLD, 120))
        p.setBrush(QBrush(fill))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPolygon(main)
        for i in range(n):
            j = (i + 1) % n
            if n < 3 and j == 0:
                continue
            p.setPen(QPen(QColor(GROUP_BY_KEY[attrs[i].group].color).lighter(115), 2.2,
                          Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            p.drawLine(main[i], main[j])

        # 8) Đỉnh
        dot = max(2.2, min(5.0, icon * 0.16))
        for i, a in enumerate(attrs):
            col = QColor(GROUP_BY_KEY[a.group].color)
            hl = a.key in (self.selected_key, self.hover_key)
            p.setPen(QPen(QColor("#ffffff") if hl else BG, 1.2))
            p.setBrush(col.lighter(130) if hl else col)
            rr = dot * (1.7 if hl else 1)
            p.drawEllipse(main[i], rr, rr)

        # 9) Icon bao quanh
        for i, a in enumerate(attrs):
            col = QColor(GROUP_BY_KEY[a.group].color)
            pc = self._pt(c, r_icon, ang[i])
            hl = a.key in (self.selected_key, self.hover_key)
            rad = icon * 0.62
            p.setBrush(_alpha(col, 95 if hl else 48))
            p.setPen(QPen(GOLD if a.key == self.selected_key else _alpha(col, 200),
                          2.2 if hl else 1.0))
            p.drawEllipse(pc, rad, rad)
            s = icon * 0.80
            draw_icon(p, self.project.icon_for(a.key), QRectF(pc.x() - s / 2, pc.y() - s / 2, s, s))

        # 10) Vòng nhóm + nhãn
        for gk, s, e in spans:
            g = GROUP_BY_KEY[gk]
            col = QColor(g.color)
            if len(spans) == 1:  # chỉ một nhóm: vòng kín, nhãn đặt ở đỉnh
                a0, a1 = -3 * math.pi / 2, math.pi / 2 - 0.0001
            else:
                gap = min(step * 0.18, 0.02)
                a0, a1 = ang[s] - step / 2 + gap, ang[e] + step / 2 - gap
            box = QRectF(c.x() - r_ring, c.y() - r_ring, 2 * r_ring, 2 * r_ring)
            p.setPen(QPen(col, 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawArc(box, int(-math.degrees(a0) * 16), int(-math.degrees(a1 - a0) * 16))

            totals = [self.character.stats[attrs[k].key].total(mx) for k in range(s, e + 1)]
            avg = sum(totals) / len(totals)
            r_txt = r_ring + 14
            candidates = [f"{g.numeral} · {g.short_en} · {g.short_vi} · TB {avg:.0f}",
                          f"{g.numeral} · {g.short_en} · TB {avg:.0f}",
                          f"{g.numeral} · {g.short_en}", g.numeral]
            self._arc_text(p, c, r_txt, (a0 + a1) / 2, (a1 - a0) * r_txt * 0.94,
                           [t.upper() for t in candidates], QColor(g.color).lighter(125))

        if self.show_overlays:
            self._overlays(p, full, attrs, interactive)

    def _arc_text(self, p: QPainter, c: QPointF, r: float, am: float, max_len: float,
                  candidates: list[str], color: QColor) -> None:
        """Vẽ chữ uốn theo cung tròn; chọn phiên bản dài nhất còn vừa cung."""
        px = max(9.0, min(14.0, r / 30))
        font = _font(px, bold=True, spacing=0.8)
        fm = QFontMetricsF(font)
        text = candidates[-1]
        for t in candidates:
            if fm.horizontalAdvance(t) <= max_len:
                text = t
                break
        text = unicodedata.normalize("NFC", text)
        widths = [fm.horizontalAdvance(ch) for ch in text]
        span = sum(widths) / r
        bottom = math.sin(am) > 0.12  # nửa dưới: lật chữ để đọc từ trái sang phải
        sign = -1 if bottom else 1
        a = am - sign * span / 2
        base_y = (fm.ascent() - fm.descent()) / 2
        p.setFont(font)
        p.setPen(color)
        for ch, w in zip(text, widths):
            ac = a + sign * (w / 2) / r
            pt = self._pt(c, r, ac)
            p.save()
            p.translate(pt)
            p.rotate(math.degrees(ac) + (-90 if bottom else 90))
            p.drawText(QPointF(-w / 2, base_y), ch)
            p.restore()
            a += sign * w / r

    def _header(self, p: QPainter, rect: QRectF, attrs: list[AttributeDef]) -> None:
        n = len(attrs)
        mx = self.project.max_value
        p.setPen(GOLD)
        p.setFont(_font(24, bold=True, spacing=2.0))
        p.drawText(QRectF(rect.left() + 24, rect.top() + 14, rect.width() - 48, 30),
                   Qt.AlignmentFlag.AlignLeft, f"{polygon_name(n).upper()} STAT")
        p.setPen(MUTED)
        p.setFont(_font(13))
        groups = len({a.group for a in attrs})
        p.drawText(QRectF(rect.left() + 24, rect.top() + 48, rect.width() - 48, 20),
                   Qt.AlignmentFlag.AlignLeft, f"Đa giác {n} cạnh · {groups} nhóm · thang 0–{mx}")
        p.setPen(TEXT)
        p.setFont(_font(20, bold=True))
        p.drawText(QRectF(rect.left() + 24, rect.top() + 14, rect.width() - 48, 30),
                   Qt.AlignmentFlag.AlignRight, self.character.name)
        p.setPen(MUTED)
        p.setFont(_font(13))
        p.drawText(QRectF(rect.left() + 24, rect.top() + 48, rect.width() - 48, 20),
                   Qt.AlignmentFlag.AlignRight, self._summary(attrs)[0])
        p.setPen(QPen(_alpha(GOLD, 90), 1))
        p.drawLine(QPointF(rect.left() + 24, rect.bottom() - 8), QPointF(rect.right() - 24, rect.bottom() - 8))

    def _summary(self, attrs: list[AttributeDef]) -> list[str]:
        mx = self.project.max_value
        totals = [(self.character.stats[a.key].total(mx), a) for a in attrs]
        s = sum(t for t, _ in totals)
        hi = max(totals, key=lambda t: t[0])
        lo = min(totals, key=lambda t: t[0])
        return [f"Tổng: {s}  ·  Trung bình: {s / len(attrs):.1f}",
                f"Cao nhất: {hi[1].name_en} ({hi[0]})",
                f"Thấp nhất: {lo[1].name_en} ({lo[0]})"]

    def _overlays(self, p: QPainter, rect: QRectF, attrs: list[AttributeDef], interactive: bool) -> None:
        if interactive:
            p.setFont(_font(12))
            lines = self._summary(attrs)
            y = rect.bottom() - 14 - 18 * len(lines)
            for ln in lines:
                p.setPen(MUTED)
                p.drawText(QRectF(rect.left() + 14, y, rect.width() * 0.45, 18), Qt.AlignmentFlag.AlignLeft, ln)
                y += 18

        # Chú thích
        legend = [(GOLD, Qt.PenStyle.SolidLine, f"{self.character.name} (tổng)")]
        if any(self.character.stats[a.key].bonus for a in attrs):
            legend.append((_alpha(TEXT, 160), Qt.PenStyle.DotLine, "Base (chưa cộng bonus)"))
        if self.compare is not None and self.compare is not self.character:
            legend.append((COMPARE, Qt.PenStyle.DashLine, f"So sánh: {self.compare.name}"))
        p.setFont(_font(12))
        y = rect.bottom() - 14 - 18 * len(legend)
        for col, style, txt in legend:
            x = rect.right() - 250
            p.setPen(QPen(col, 2.2, style))
            p.drawLine(QPointF(x, y + 9), QPointF(x + 26, y + 9))
            p.setPen(TEXT)
            p.drawText(QRectF(x + 34, y, 216, 18), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, txt)
            y += 18

    # ---------------------------------------------------------- interaction
    def _hit(self, pos: QPointF) -> str | None:
        if not self._geom:
            return None
        c, R, r_icon, icon, attrs = self._geom
        dx, dy = pos.x() - c.x(), pos.y() - c.y()
        d = math.hypot(dx, dy)
        if d < 6 or d > r_icon + icon * 0.7:
            return None
        n = len(attrs)
        a = (math.atan2(dy, dx) + math.pi / 2) % (2 * math.pi)
        return attrs[int(round(a / (2 * math.pi / n))) % n].key

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            self._press = e.position()
            self._pan_start = QPointF(self.pan)
            self._dragging = False

    def mouseMoveEvent(self, e) -> None:
        pos = e.position()
        if self._press is not None and (e.buttons() & Qt.MouseButton.LeftButton):
            if (pos - self._press).manhattanLength() > 5:
                self._dragging = True
                self.setCursor(Qt.CursorShape.ClosedHandCursor)
            if self._dragging:
                self.pan = self._pan_start + (pos - self._press)
                self.update()
                return
        key = self._hit(pos)
        if key != self.hover_key:
            self.hover_key = key
            self.setCursor(Qt.CursorShape.PointingHandCursor if key else Qt.CursorShape.ArrowCursor)
            self.update()
            self.attributeHovered.emit(key)

    def mouseReleaseEvent(self, e) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            if not self._dragging:
                key = self._hit(e.position())
                if key:
                    self.select(key)
                    self.attributeSelected.emit(key)
            self._press, self._dragging = None, False
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseDoubleClickEvent(self, e) -> None:
        if not self._hit(e.position()):
            self.reset_view()

    def leaveEvent(self, _e) -> None:
        if self.hover_key:
            self.hover_key = None
            self.update()
            self.attributeHovered.emit(None)

    def wheelEvent(self, e) -> None:
        factor = 1.15 ** (e.angleDelta().y() / 120)
        new_zoom = max(0.4, min(8.0, self.zoom * factor))
        factor = new_zoom / self.zoom
        # Zoom quanh vị trí con trỏ
        base_c = QRectF(self.rect()).center()
        c = base_c + self.pan
        m = e.position()
        c2 = m - (m - c) * factor
        self.pan = c2 - base_c
        self.zoom = new_zoom
        self.update()

    def keyPressEvent(self, e) -> None:
        attrs = self.visible_attrs()
        k = e.key()
        if k in (Qt.Key.Key_Left, Qt.Key.Key_Right) and attrs:
            keys = [a.key for a in attrs]
            i = keys.index(self.selected_key) if self.selected_key in keys else -1
            i = (i + (1 if k == Qt.Key.Key_Right else -1)) % len(keys)
            self.select(keys[i])
            self.attributeSelected.emit(keys[i])
        elif k in (Qt.Key.Key_Plus, Qt.Key.Key_Equal):
            self.zoom = min(8.0, self.zoom * 1.2)
            self.update()
        elif k == Qt.Key.Key_Minus:
            self.zoom = max(0.4, self.zoom / 1.2)
            self.update()
        elif k == Qt.Key.Key_0:
            self.reset_view()
        else:
            super().keyPressEvent(e)
