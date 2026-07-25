from dataclasses import dataclass
from typing import List

SPECIAL_CHARGE_REQUIRED = 5
MAX_POTIONS = 5


@dataclass
class ActionResult:
    messages: List[str]


@dataclass
class Character:
    name: str
    health: int
    attack_power: int
    defense: int = 0

    def __post_init__(self) -> None:
        self.max_health = self.health
        self.special_charge = 0
        self.potions = MAX_POTIONS

    @property
    def special_ready(self) -> bool:
        return self.special_charge >= SPECIAL_CHARGE_REQUIRED

    def take_damage(self, amount: int) -> int:
        damage_taken = max(0, amount - self.defense)
        self.health = max(0, self.health - damage_taken)
        return damage_taken

    def attack(self, opponent: "Character") -> ActionResult:
        self.special_charge = min(SPECIAL_CHARGE_REQUIRED, self.special_charge + 1)
        damage = opponent.take_damage(self.attack_power)
        messages = [f"{self.name} attacks {opponent.name} for {damage} damage!"]
        if opponent.health == 0:
            messages.append(f"{opponent.name} has been defeated!")
        return ActionResult(messages=messages)

    def use_special(self, opponent: "Character") -> ActionResult:
        self.special_charge = 0
        return self.special_ability(opponent)

    def special_ability(self, opponent: "Character") -> ActionResult:
        raise NotImplementedError(f"{self.__class__.__name__} does not define a special ability.")

    def heal(self, amount: int = 25) -> ActionResult:
        if self.health >= self.max_health:
            return ActionResult(messages=[f"{self.name} is already at max health!"])

        self.potions -= 1
        new_health = min(self.health + amount, self.max_health)
        healed_amount = new_health - self.health
        self.health = new_health
        return ActionResult(
            messages=[
                f"{self.name} drinks a potion and heals for {healed_amount} points! "
                f"Current health: {self.health}/{self.max_health} "
                f"({self.potions} potions left)"
            ]
        )

    def display_stats(self) -> ActionResult:
        return ActionResult(
            messages=[
                f"{self.name}'s Stats - "
                f"Health: {self.health}/{self.max_health}, "
                f"Attack Power: {self.attack_power}, "
                f"Defense: {self.defense}, "
                f"Special: {self.special_charge}/{SPECIAL_CHARGE_REQUIRED}, "
                f"Potions: {self.potions}/{MAX_POTIONS}"
            ]
        )


class Warrior(Character):
    """Bruiser: solid health, solid damage, decent armor."""

    def __init__(self, name: str) -> None:
        super().__init__(name, health=140, attack_power=35, defense=10)

    def special_ability(self, opponent: Character) -> ActionResult:
        damage = opponent.take_damage(self.attack_power * 2)
        return ActionResult(
            messages=[f"{self.name} uses Burning Maul on {opponent.name} for {damage} damage!"]
        )


class Mage(Character):
    """Glass cannon: highest damage, no armor, lowest health."""

    def __init__(self, name: str) -> None:
        super().__init__(name, health=100, attack_power=50, defense=0)

    def special_ability(self, opponent: Character) -> ActionResult:
        damage = opponent.take_damage(self.attack_power * 2)
        return ActionResult(messages=[f"{self.name} uses Holy on {opponent.name} for {damage} damage!"])


class Archer(Character):
    """Skirmisher: good damage, light armor, modest health."""

    def __init__(self, name: str) -> None:
        super().__init__(name, health=110, attack_power=40, defense=5)

    def special_ability(self, opponent: Character) -> ActionResult:
        damage = opponent.take_damage(self.attack_power * 2)
        return ActionResult(
            messages=[f"{self.name} uses Rain of Arrows on {opponent.name} for {damage} damage!"]
        )


class Paladin(Character):
    """Tank: highest health and armor, lowest damage."""

    def __init__(self, name: str) -> None:
        super().__init__(name, health=160, attack_power=25, defense=15)

    def special_ability(self, opponent: Character) -> ActionResult:
        damage = opponent.take_damage(self.attack_power * 2)
        return ActionResult(messages=[f"{self.name} uses Shield Bash on {opponent.name} for {damage} damage!"])


class EvilWizard(Character):
    def __init__(self, name: str) -> None:
        super().__init__(name, health=220, attack_power=20, defense=5)

    def regenerate(self, amount: int = 5) -> ActionResult:
        self.health = min(self.max_health, self.health + amount)
        return ActionResult(
            messages=[
                f"{self.name} regenerates {amount} health! "
                f"Current health: {self.health}/{self.max_health}"
            ]
        )
