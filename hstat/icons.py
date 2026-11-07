"""Vẽ icon (emoji hoặc ảnh nhúng base64) thành QPixmap, có cache."""
from __future__ import annotations

import base64
import sys

from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPixmap

IMG_PREFIX = "img:"
# Ưu tiên font emoji gốc của từng hệ điều hành
if sys.platform == "win32":
    EMOJI_FAMILIES = ["Segoe UI Emoji", "Segoe UI Symbol"]
elif sys.platform == "darwin":
    EMOJI_FAMILIES = ["Apple Color Emoji"]
else:
    EMOJI_FAMILIES = ["Noto Color Emoji", "Twemoji Mozilla", "Symbola"]
_cache: dict[tuple[str, int], QPixmap] = {}


def is_image(icon: str) -> bool:
    return icon.startswith(IMG_PREFIX)


def image_file_to_icon(path: str, size: int = 96) -> str | None:
    pm = QPixmap(path)
    if pm.isNull():
        return None
    pm = pm.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    data = QByteArray()
    buf = QBuffer(data)
    buf.open(QIODevice.OpenModeFlag.WriteOnly)
    pm.save(buf, "PNG")
    return IMG_PREFIX + base64.b64encode(bytes(data)).decode("ascii")


def emoji_font(px: float) -> QFont:
    f = QFont()
    f.setFamilies(EMOJI_FAMILIES)
    f.setPixelSize(max(6, int(px)))
    return f


def draw_icon(p: QPainter, icon: str, rect: QRectF) -> None:
    """Vẽ icon vừa khít trong rect (giữ tỉ lệ)."""
    size = int(min(rect.width(), rect.height()))
    if size <= 0:
        return
    bucket = min(256, max(16, (size * 2 + 15) // 16 * 16))  # 2x cho nét, làm tròn để cache hiệu quả
    pm = icon_pixmap(icon, bucket)
    p.drawPixmap(rect, pm, QRectF(pm.rect()))


def icon_pixmap(icon: str, size: int) -> QPixmap:
    key = (icon, size)
    if key in _cache:
        return _cache[key]
    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform
                     | QPainter.RenderHint.TextAntialiasing)
    if is_image(icon):
        img = QPixmap()
        img.loadFromData(base64.b64decode(icon[len(IMG_PREFIX):]))
        if not img.isNull():
            img = img.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio,
                             Qt.TransformationMode.SmoothTransformation)
            p.drawPixmap((size - img.width()) // 2, (size - img.height()) // 2, img)
    else:
        p.setFont(emoji_font(size * 0.78))
        p.setPen(QColor("#f0e6d2"))
        p.drawText(QRectF(0, 0, size, size), Qt.AlignmentFlag.AlignCenter, icon)
    p.end()
    if len(_cache) > 2000:
        _cache.clear()
    _cache[key] = pm
    return pm


def qicon(icon: str, size: int = 32) -> QIcon:
    return QIcon(icon_pixmap(icon, size))


def color_dot(color: str, size: int = 14) -> QIcon:
    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor(color))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(1, 1, size - 2, size - 2)
    p.end()
    return QIcon(pm)
