from typing import Callable, Dict, List

try:
    from .characters import Archer, Character, Mage, Paladin, Warrior
except ImportError:
    from characters import Archer, Character, Mage, Paladin, Warrior


CharacterFactory = Callable[[str], Character]

CLASS_OPTIONS: Dict[str, tuple[str, CharacterFactory]] = {
    "1": ("Warrior", Warrior),
    "2": ("Mage", Mage),
    "3": ("Archer", Archer),
    "4": ("Paladin", Paladin),
}


def get_class_menu_lines() -> List[str]:
    lines = ["Choose your character class:"]
    lines.extend(f"{key}. {label}" for key, (label, _) in CLASS_OPTIONS.items())
    return lines


def build_character(class_choice: str, name: str) -> tuple[Character, List[str]]:
    messages: List[str] = []
    normalized_choice = class_choice.strip()
    normalized_name = name.strip() or "Hero"

    if normalized_choice not in CLASS_OPTIONS:
        messages.append("Invalid choice. Defaulting to Warrior.")
        normalized_choice = "1"

    _, character_factory = CLASS_OPTIONS[normalized_choice]
    return character_factory(normalized_name), messages
