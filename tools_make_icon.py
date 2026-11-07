"""Sinh icon ứng dụng (hstat/assets/app.png + app.ico). Chạy: python tools_make_icon.py"""
import math
import random
import sys

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QGuiApplication, QImage, QPainter, QPen, QPolygonF

from hstat.attributes import ATTRIBUTES, GROUP_BY_KEY

app = QGuiApplication(sys.argv)
S = 512
img = QImage(S, S, QImage.Format.Format_ARGB32_Premultiplied)
img.fill(Qt.GlobalColor.transparent)
p = QPainter(img)
p.setRenderHint(QPainter.RenderHint.Antialiasing)
p.setPen(QPen(QColor("#C8A55A"), S * 0.018))
p.setBrush(QColor("#15161b"))
m = S * 0.03
p.drawRoundedRect(QRectF(m, m, S - 2 * m, S - 2 * m), S * 0.2, S * 0.2)

c = QPointF(S / 2, S / 2)
n = len(ATTRIBUTES)
step = 2 * math.pi / n
pt = lambda r, a: QPointF(c.x() + r * math.cos(a), c.y() + r * math.sin(a))
ang = [-math.pi / 2 + i * step for i in range(n)]

# Vòng màu 8 nhóm
r_ring = S * 0.385
box = QRectF(c.x() - r_ring, c.y() - r_ring, 2 * r_ring, 2 * r_ring)
i = 0
while i < n:
    g = ATTRIBUTES[i].group
    j = i
    while j + 1 < n and ATTRIBUTES[j + 1].group == g:
        j += 1
    a0, a1 = ang[i] - step / 2 + 0.03, ang[j] + step / 2 - 0.03
    p.setPen(QPen(QColor(GROUP_BY_KEY[g].color), S * 0.075, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap))
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawArc(box, int(-math.degrees(a0) * 16), int(-math.degrees(a1 - a0) * 16))
    i = j + 1

# Lưới 79 cạnh + đa giác chỉ số
R = S * 0.30
p.setPen(QPen(QColor("#C8A55A"), S * 0.008))
p.drawPolygon(QPolygonF([pt(R, a) for a in ang]))
rnd = random.Random(7)
vals = [0.45 + 0.5 * abs(math.sin(k * 0.55)) * rnd.uniform(0.6, 1.0) for k in range(n)]
poly = QPolygonF([pt(R * v, a) for v, a in zip(vals, ang)])
p.setPen(Qt.PenStyle.NoPen)
p.setBrush(QColor(200, 165, 90, 150))
p.drawPolygon(poly)
for k in range(n):
    p.setPen(QPen(QColor(GROUP_BY_KEY[ATTRIBUTES[k].group].color).lighter(120), S * 0.009))
    p.drawLine(poly[k], poly[(k + 1) % n])
p.end()
img.save("hstat/assets/app.png")

from PIL import Image  # noqa: E402

Image.open("hstat/assets/app.png").save(
    "hstat/assets/app.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("ok")
