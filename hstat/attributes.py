"""Định nghĩa 8 nhóm và 79 thuộc tính của hệ thống."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Group:
    key: str
    numeral: str
    name_en: str
    name_vi: str
    short_en: str
    short_vi: str
    color: str


@dataclass(frozen=True)
class AttributeDef:
    key: str
    group: str
    name_en: str
    name_vi: str
    icon: str


GROUPS: list[Group] = [
    Group("physical", "I", "Physical Attributes", "Thuộc tính thể chất", "Physical", "Thể chất", "#E8663D"),
    Group("vitality", "II", "Vitality & Resistance", "Sinh lực và khả năng kháng chịu", "Vitality", "Sinh lực & Kháng", "#3BA55C"),
    Group("cognitive", "III", "Cognitive Attributes", "Thuộc tính nhận thức và trí tuệ", "Cognitive", "Nhận thức", "#3C8DDE"),
    Group("mental", "IV", "Mental Attributes", "Thuộc tính tinh thần và tâm lý", "Mental", "Tinh thần", "#A066C9"),
    Group("combat", "V", "Combat Attributes", "Thuộc tính chiến đấu", "Combat", "Chiến đấu", "#D64550"),
    Group("magical", "VI", "Magical Attributes", "Thuộc tính ma thuật", "Magical", "Ma thuật", "#2BB3C0"),
    Group("technical", "VII", "Technical & Practical Skills", "Kỹ năng kỹ thuật và thực tiễn", "Technical", "Kỹ thuật", "#C9A227"),
    Group("social", "VIII", "Social Attributes", "Thuộc tính xã hội", "Social", "Xã hội", "#E06AA6"),
]

GROUP_BY_KEY: dict[str, Group] = {g.key: g for g in GROUPS}

# (key, english, tiếng Việt, icon)
_RAW: dict[str, list[tuple[str, str, str, str]]] = {
    "physical": [
        ("strength", "Strength", "Sức mạnh cơ bắp", "💪"),
        ("endurance", "Endurance", "Sức bền thể chất", "🏃"),
        ("agility", "Agility", "Sự nhanh nhẹn", "🐆"),
        ("dexterity", "Dexterity", "Sự khéo léo và linh hoạt", "🤹"),
        ("speed", "Speed", "Tốc độ", "💨"),
        ("reflexes", "Reflexes", "Phản xạ", "⚡"),
        ("flexibility", "Flexibility", "Độ dẻo dai", "🤸"),
        ("coordination", "Coordination", "Khả năng phối hợp vận động", "🕺"),
        ("balance", "Balance", "Khả năng giữ thăng bằng", "🧘"),
        ("explosive_power", "Explosive Power", "Sức mạnh bộc phát", "💥"),
    ],
    "vitality": [
        ("hp", "HP (Health Points)", "Sinh lực", "❤️"),
        ("stamina", "Stamina", "Thể lực", "🔋"),
        ("recovery", "Recovery", "Khả năng phục hồi", "🌱"),
        ("pain_tolerance", "Pain Tolerance", "Khả năng chịu đau", "🗿"),
        ("physical_resistance", "Physical Resistance", "Kháng sát thương vật lý", "🧱"),
        ("elemental_resistance", "Elemental Resistance", "Kháng sát thương nguyên tố", "🌋"),
        ("poison_resistance", "Poison Resistance", "Khả năng kháng độc", "🐍"),
        ("disease_resistance", "Disease Resistance", "Khả năng kháng bệnh tật", "🦠"),
        ("mental_resistance", "Mental Resistance", "Kháng tác động tâm trí", "🌀"),
        ("death_resistance", "Death Resistance", "Khả năng kháng tử vong", "💀"),
    ],
    "cognitive": [
        ("intelligence", "Intelligence", "Trí thông minh", "🧠"),
        ("perception", "Perception", "Khả năng tri giác", "👀"),
        ("awareness", "Awareness", "Nhận thức tổng thể", "📡"),
        ("memory", "Memory", "Trí nhớ", "🐘"),
        ("concentration", "Concentration", "Khả năng tập trung", "🎯"),
        ("learning_ability", "Learning Ability", "Khả năng học hỏi", "🎓"),
        ("analytical_thinking", "Analytical Thinking", "Tư duy phân tích", "📊"),
        ("problem_solving", "Problem Solving", "Khả năng giải quyết vấn đề", "🧩"),
        ("prediction", "Prediction", "Khả năng dự đoán", "🔮"),
        ("spatial_awareness", "Spatial Awareness", "Nhận thức không gian", "📐"),
    ],
    "mental": [
        ("willpower", "Willpower", "Ý chí", "🔥"),
        ("determination", "Determination", "Sự quyết tâm", "🗻"),
        ("courage", "Courage", "Lòng can đảm", "🦁"),
        ("mental_fortitude", "Mental Fortitude", "Sức mạnh tinh thần", "🏰"),
        ("emotional_control", "Emotional Control", "Kiểm soát cảm xúc", "😌"),
        ("stress_resistance", "Stress Resistance", "Khả năng chịu đựng áp lực", "🧊"),
        ("fear_resistance", "Fear Resistance", "Khả năng kháng sợ hãi", "👻"),
        ("self_control", "Self-Control", "Khả năng tự kiểm soát", "🔒"),
        ("persistence", "Persistence", "Sự kiên trì", "⏳"),
    ],
    "combat": [
        ("attack_power", "Attack Power", "Sức tấn công", "⚔️"),
        ("weapon_mastery", "Weapon Mastery", "Mức độ tinh thông vũ khí", "🗡️"),
        ("combat_skill", "Combat Skill", "Kỹ năng chiến đấu", "🥋"),
        ("critical_ability", "Critical Ability", "Khả năng đòn chí mạng", "🔪"),
        ("parrying", "Parrying", "Đỡ gạt và hóa giải đòn", "🤺"),
        ("blocking", "Blocking", "Phòng thủ và đỡ đòn", "🛡️"),
        ("evasion", "Evasion", "Khả năng né tránh", "🍃"),
        ("stance_breaking", "Stance Breaking", "Khả năng phá thế đối thủ", "🔨"),
        ("counterattacking", "Counterattacking", "Khả năng phản công", "🥊"),
        ("tactical_awareness", "Tactical Awareness", "Nhận thức chiến thuật", "♟️"),
        ("combat_adaptability", "Combat Adaptability", "Thích nghi trong chiến đấu", "🦎"),
    ],
    "magical": [
        ("magic_intelligence", "Intelligence (Magic)", "Trí tuệ ma thuật", "🧙"),
        ("faith", "Faith", "Đức tin và năng lực thần thuật", "🙏"),
        ("arcane", "Arcane", "Năng lực huyền bí", "🌙"),
        ("fp", "FP (Focus Points)", "Năng lượng tinh thần cho phép thuật", "💧"),
        ("sorcery_scaling", "Sorcery Scaling", "Hệ số khuếch đại Sorcery", "💠"),
        ("incantation_scaling", "Incantation Scaling", "Hệ số khuếch đại Incantation", "🌟"),
        ("casting_speed", "Casting Speed", "Tốc độ thi triển phép thuật", "⏱️"),
        ("spell_knowledge", "Spell Knowledge", "Kiến thức về phép thuật", "📖"),
        ("spell_control", "Spell Control", "Khả năng kiểm soát phép thuật", "✨"),
        ("magical_resistance", "Magical Resistance", "Khả năng kháng ma thuật", "🧿"),
        ("summoning", "Summoning", "Khả năng triệu hồi", "🔔"),
    ],
    "technical": [
        ("crafting", "Crafting", "Chế tạo", "🧰"),
        ("smithing", "Smithing", "Rèn đúc", "⚒️"),
        ("alchemy", "Alchemy", "Giả kim thuật", "🧪"),
        ("survival", "Survival", "Kỹ năng sinh tồn", "⛺"),
        ("navigation", "Navigation", "Khả năng định hướng", "🧭"),
        ("tracking", "Tracking", "Khả năng truy dấu", "👣"),
        ("hunting", "Hunting", "Kỹ năng săn bắn", "🏹"),
        ("healing", "Healing", "Khả năng chữa trị", "🩹"),
        ("engineering", "Engineering", "Kỹ thuật chế tạo và cơ khí", "⚙️"),
        ("horsemanship", "Horsemanship", "Cưỡi và điều khiển thú cưỡi", "🐎"),
    ],
    "social": [
        ("charisma", "Charisma", "Sức hút cá nhân", "🌹"),
        ("persuasion", "Persuasion", "Khả năng thuyết phục", "💬"),
        ("leadership", "Leadership", "Khả năng lãnh đạo", "👑"),
        ("deception", "Deception", "Lừa dối và ngụy trang ý đồ", "🎭"),
        ("intimidation", "Intimidation", "Đe dọa và áp chế tâm lý", "👹"),
        ("diplomacy", "Diplomacy", "Khả năng ngoại giao", "🤝"),
        ("reputation", "Reputation", "Danh tiếng và uy tín", "🏆"),
        ("empathy", "Empathy", "Đồng cảm và thấu hiểu", "💞"),
    ],
}

ATTRIBUTES: list[AttributeDef] = [
    AttributeDef(key, group, en, vi, icon)
    for group, rows in _RAW.items()
    for key, en, vi, icon in rows
]

ATTR_BY_KEY: dict[str, AttributeDef] = {a.key: a for a in ATTRIBUTES}

assert len(ATTRIBUTES) == 79, len(ATTRIBUTES)
assert len(ATTR_BY_KEY) == 79, "trùng key thuộc tính"
assert len({a.icon for a in ATTRIBUTES}) == 79, "trùng icon"
