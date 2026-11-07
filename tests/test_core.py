"""Kiểm thử phần lõi (không cần giao diện): python -m pytest tests"""
import csv

from hstat.attributes import ATTRIBUTES, GROUPS
from hstat.attributes import ATTR_BY_KEY
from hstat.model import DEFAULT_BASE, DEFAULT_MAX_VALUE, Character, FieldDef, Project, new_project
from hstat.polygon_names import polygon_name


def test_79_attributes_in_8_groups():
    assert len(ATTRIBUTES) == 79
    assert len(GROUPS) == 8
    sizes = {g.key: sum(a.group == g.key for a in ATTRIBUTES) for g in GROUPS}
    assert list(sizes.values()) == [10, 10, 10, 9, 11, 11, 10, 8]


def test_polygon_names():
    assert polygon_name(79) == "heptacontakaienneagon"
    assert polygon_name(6) == "hexagon"
    assert polygon_name(10) == "decagon"
    assert polygon_name(11) == "hendecagon"
    assert polygon_name(21) == "icosikaihenagon"
    assert polygon_name(40) == "tetracontagon"


def test_total_is_clamped():
    c = Character("x")
    st = c.stats["strength"]
    st.base, st.bonus = 95, 10
    assert st.total(99) == 99
    st.base, st.bonus = 3, -10
    assert st.total(99) == 0


def test_roundtrip_with_custom_fields(tmp_path):
    p = new_project()
    ch = p.characters[0]
    p.global_fields.append(FieldDef("Kháng Rot", "number", key="rot"))
    ch.stats["hp"].values["rot"] = 12.5
    ch.stats["hp"].local_fields.append(FieldDef("Flask", "choice", ["Crimson", "Cerulean"], key="flask"))
    ch.stats["hp"].values["flask"] = "Crimson"
    p.icons["hp"] = "🩸"
    path = tmp_path / "a.hstat.json"
    p.save(path)
    q = Project.load(path)
    assert q.to_dict() == p.to_dict()
    assert q.icon_for("hp") == "🩸"
    assert q.icon_for("strength") == "💪"
    assert [f.label for f in q.fields_for(q.characters[0].stats["hp"])][-2:] == ["Kháng Rot", "Flask"]


def test_csv_export(tmp_path):
    p = new_project()
    out = tmp_path / "x.csv"
    p.export_csv(p.characters[0], out)
    rows = list(csv.reader(out.open(encoding="utf-8-sig")))
    assert len(rows) == 1 + 79
    assert rows[0][:5] == ["Nhóm", "Key", "English", "Tiếng Việt", "Định nghĩa"]
    assert rows[1][4].startswith("Lực lớn nhất mà cơ bắp tạo ra")
    assert "Mô tả" not in rows[0]  # đã thay bằng cột Định nghĩa


def test_default_scale_is_999_and_demo_is_maxed():
    assert DEFAULT_MAX_VALUE == 999
    p = new_project()
    assert p.max_value == 999
    demo = p.characters[0]
    assert demo.name.startswith("Tarnished")
    for st in demo.stats.values():
        assert (st.base, st.bonus, st.total(p.max_value)) == (999, 0, 999)
        assert st.values["rank"] == "S" and st.values["maxed"] is True
    assert all(st.base == DEFAULT_BASE for st in Character("mới").stats.values())


def test_every_attribute_has_a_description_and_it_can_be_overridden(tmp_path):
    assert all(len(a.description) > 100 for a in ATTRIBUTES)
    assert ATTR_BY_KEY["empathy"].description.endswith("những điều họ không nói thành lời.")
    p = new_project()
    assert p.description_for("hp") == ATTR_BY_KEY["hp"].description
    p.descriptions["hp"] = "Máu."
    path = tmp_path / "d.hstat.json"
    p.save(path)
    q = Project.load(path)
    assert q.description_for("hp") == "Máu."
    q.descriptions.pop("hp")
    assert q.description_for("hp") == ATTR_BY_KEY["hp"].description


def test_ring_values_are_round_numbers():
    from hstat.chart import ring_values
    assert ring_values(999) == [200, 400, 600, 800, 999]
    assert ring_values(99) == [20, 40, 60, 80, 99]
