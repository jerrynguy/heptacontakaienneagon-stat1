"""Tên gọi Hy Lạp của đa giác n cạnh (1–99), ví dụ 79 → heptacontakaienneagon."""
from __future__ import annotations

_SPECIAL = {
    1: "monogon", 2: "digon", 3: "trigon", 4: "tetragon", 5: "pentagon",
    6: "hexagon", 7: "heptagon", 8: "octagon", 9: "enneagon", 10: "decagon",
    11: "hendecagon", 12: "dodecagon", 20: "icosagon", 100: "hectogon",
}
_UNIT = {1: "hena", 2: "di", 3: "tri", 4: "tetra", 5: "penta",
         6: "hexa", 7: "hepta", 8: "octa", 9: "ennea"}
_TENS = {2: "icosi", 3: "triaconta", 4: "tetraconta", 5: "pentaconta",
         6: "hexaconta", 7: "heptaconta", 8: "octaconta", 9: "enneaconta"}


def polygon_name(n: int) -> str:
    if n in _SPECIAL:
        return _SPECIAL[n]
    if 13 <= n <= 19:
        return f"{_UNIT[n - 10]}kaidecagon"
    if 21 <= n <= 99:
        tens, unit = divmod(n, 10)
        if unit == 0:
            return f"{_TENS[tens]}gon"
        return f"{_TENS[tens]}kai{_UNIT[unit]}gon"
    return f"{n}-gon"
