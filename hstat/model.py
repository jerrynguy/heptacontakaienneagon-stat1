"""Mô hình dữ liệu: dự án → nhân vật → 79 chỉ số → các trường tùy biến."""
from __future__ import annotations

import csv
import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .attributes import ATTRIBUTES, ATTR_BY_KEY, GROUP_BY_KEY

DEFAULT_MAX_VALUE = 999   # thang điểm tối đa mặc định của mỗi chỉ số
DEFAULT_BASE = 100        # giá trị khởi đầu của nhân vật mới (10% thang điểm)

FILE_FORMAT = "heptacontakaienneagon-stat"
FILE_VERSION = 1

FIELD_KINDS = {
    "text": "Văn bản ngắn",
    "longtext": "Đoạn văn",
    "number": "Số",
    "bool": "Có / Không",
    "choice": "Danh sách chọn",
    "rating": "Đánh giá ★ (0–5)",
}


@dataclass
class FieldDef:
    label: str
    kind: str = "text"
    options: list[str] = field(default_factory=list)
    key: str = field(default_factory=lambda: uuid.uuid4().hex[:10])

    def default_value(self) -> Any:
        return {"number": 0.0, "bool": False, "rating": 0}.get(self.kind, "")

    def to_dict(self) -> dict:
        return {"key": self.key, "label": self.label, "kind": self.kind, "options": list(self.options)}

    @classmethod
    def from_dict(cls, d: dict) -> "FieldDef":
        kind = d.get("kind", "text")
        return cls(label=d.get("label", "?"), kind=kind if kind in FIELD_KINDS else "text",
                   options=list(d.get("options", [])), key=d.get("key") or uuid.uuid4().hex[:10])


def default_global_fields() -> list[FieldDef]:
    return [
        FieldDef("Hạng", "choice", ["—", "S", "A", "B", "C", "D", "E", "F"], key="rank"),
        FieldDef("Độ ưu tiên nâng cấp", "rating", key="priority"),
        FieldDef("Hiệu ứng / Ảnh hưởng", "longtext", key="effects"),
        FieldDef("Nguồn / Cách đạt được", "text", key="source"),
        FieldDef("Yêu cầu / Điều kiện", "text", key="requirements"),
        FieldDef("Trang bị liên quan", "text", key="equipment"),
        FieldDef("Tags", "text", key="tags"),
        FieldDef("Đã đạt tối đa", "bool", key="maxed"),
        FieldDef("Ghi chú", "longtext", key="notes"),
    ]


@dataclass
class StatEntry:
    base: int = DEFAULT_BASE
    bonus: int = 0
    values: dict[str, Any] = field(default_factory=dict)
    local_fields: list[FieldDef] = field(default_factory=list)

    def total(self, max_value: int) -> int:
        return max(0, min(max_value, self.base + self.bonus))

    def to_dict(self) -> dict:
        return {"base": self.base, "bonus": self.bonus, "values": dict(self.values),
                "local_fields": [f.to_dict() for f in self.local_fields]}

    @classmethod
    def from_dict(cls, d: dict) -> "StatEntry":
        return cls(base=int(d.get("base", DEFAULT_BASE)), bonus=int(d.get("bonus", 0)),
                   values=dict(d.get("values", {})),
                   local_fields=[FieldDef.from_dict(x) for x in d.get("local_fields", [])])


@dataclass
class Character:
    name: str
    notes: str = ""
    stats: dict[str, StatEntry] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for a in ATTRIBUTES:
            self.stats.setdefault(a.key, StatEntry())

    def to_dict(self) -> dict:
        return {"name": self.name, "notes": self.notes,
                "stats": {k: v.to_dict() for k, v in self.stats.items()}}

    @classmethod
    def from_dict(cls, d: dict) -> "Character":
        stats = {k: StatEntry.from_dict(v) for k, v in d.get("stats", {}).items() if k in ATTR_BY_KEY}
        return cls(name=d.get("name", "Nhân vật"), notes=d.get("notes", ""), stats=stats)

    def copy(self, name: str) -> "Character":
        return Character.from_dict({**self.to_dict(), "name": name})


@dataclass
class Project:
    max_value: int = DEFAULT_MAX_VALUE
    icons: dict[str, str] = field(default_factory=dict)      # icon tùy chỉnh theo key thuộc tính
    descriptions: dict[str, str] = field(default_factory=dict)  # mô tả đã sửa (ghi đè mặc định)
    global_fields: list[FieldDef] = field(default_factory=default_global_fields)
    characters: list[Character] = field(default_factory=list)

    def icon_for(self, attr_key: str) -> str:
        return self.icons.get(attr_key) or ATTR_BY_KEY[attr_key].icon

    def description_for(self, attr_key: str) -> str:
        return self.descriptions.get(attr_key) or ATTR_BY_KEY[attr_key].description

    def fields_for(self, entry: StatEntry) -> list[FieldDef]:
        return [*self.global_fields, *entry.local_fields]

    # ---------- I/O ----------
    def to_dict(self) -> dict:
        return {"format": FILE_FORMAT, "version": FILE_VERSION, "max_value": self.max_value,
                "icons": dict(self.icons), "descriptions": dict(self.descriptions),
                "global_fields": [f.to_dict() for f in self.global_fields],
                "characters": [c.to_dict() for c in self.characters]}

    @classmethod
    def from_dict(cls, d: dict) -> "Project":
        if d.get("format") != FILE_FORMAT:
            raise ValueError("Không phải file của Heptacontakaienneagon Stat")
        p = cls(max_value=int(d.get("max_value", DEFAULT_MAX_VALUE)), icons=dict(d.get("icons", {})),
                descriptions=dict(d.get("descriptions", {})),
                global_fields=[FieldDef.from_dict(x) for x in d.get("global_fields", [])],
                characters=[Character.from_dict(c) for c in d.get("characters", [])])
        if not p.characters:
            p.characters.append(Character("Nhân vật mới"))
        return p

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "Project":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    def export_csv(self, character: Character, path: str | Path) -> None:
        headers = ["Nhóm", "Key", "English", "Tiếng Việt", "Định nghĩa", "Icon", "Base", "Bonus", "Tổng"]
        headers += [f.label for f in self.global_fields] + ["Trường riêng"]
        with open(path, "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.writer(fh)
            w.writerow(headers)
            for a in ATTRIBUTES:
                e = character.stats[a.key]
                g = GROUP_BY_KEY[a.group]
                row = [f"{g.numeral}. {g.name_en}", a.key, a.name_en, a.name_vi, self.description_for(a.key),
                       self.icon_for(a.key),
                       e.base, e.bonus, e.total(self.max_value)]
                row += [e.values.get(f.key, f.default_value()) for f in self.global_fields]
                row.append("; ".join(f"{f.label}={e.values.get(f.key, '')}" for f in e.local_fields))
                w.writerow(row)


def max_character(name: str = "Tarnished (mẫu)", max_value: int = DEFAULT_MAX_VALUE) -> Character:
    """Nhân vật demo: tối đa ở mọi thứ (Base = thang điểm tối đa, hạng S, đã đạt tối đa)."""
    c = Character(name, notes="Nhân vật mẫu: mọi chỉ số đều đạt tối đa.")
    for st in c.stats.values():
        st.base, st.bonus = max_value, 0
        st.values.update({"rank": "S", "maxed": True})
    return c


def new_project() -> Project:
    return Project(characters=[max_character()])
