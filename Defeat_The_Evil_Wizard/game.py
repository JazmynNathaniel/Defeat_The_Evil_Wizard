from dataclasses import dataclass
from typing import List

try:
    from .character_creation import build_character, get_class_menu_lines
    from .characters import MAX_POTIONS, SPECIAL_CHARGE_REQUIRED, Character, EvilWizard
except ImportError:
    from character_creation import build_character, get_class_menu_lines
    from characters import MAX_POTIONS, SPECIAL_CHARGE_REQUIRED, Character, EvilWizard


@dataclass
class TurnResult:
    turn_consumed: bool
    messages: List[str]


@dataclass
class BattleEngine:
    player: Character
    wizard: EvilWizard

    def get_turn_menu_lines(self) -> List[str]:
        if self.player.special_ready:
            special_status = "READY!"
        else:
            special_status = f"{self.player.special_charge}/{SPECIAL_CHARGE_REQUIRED}"
        return [
            "\n--- Your Turn ---",
            "1. Attack",
            f"2. Use Special Ability [{special_status}]",
            f"3. Heal [{self.player.potions} potions]",
            "4. View Stats",
        ]

    def is_over(self) -> bool:
        return self.player.health <= 0 or self.wizard.health <= 0

    def resolve_turn(self, choice: str) -> TurnResult:
        normalized_choice = choice.strip()

        if normalized_choice == "1":
            return TurnResult(turn_consumed=True, messages=self.player.attack(self.wizard).messages)
        if normalized_choice == "2":
            if not self.player.special_ready:
                return TurnResult(
                    turn_consumed=False,
                    messages=[
                        f"{self.player.name}'s special ability isn't charged yet "
                        f"({self.player.special_charge}/{SPECIAL_CHARGE_REQUIRED} attacks landed)."
                    ],
                )
            return TurnResult(turn_consumed=True, messages=self.player.use_special(self.wizard).messages)
        if normalized_choice == "3":
            if self.player.potions <= 0:
                return TurnResult(
                    turn_consumed=False,
                    messages=[f"{self.player.name} is out of potions!"],
                )
            return TurnResult(turn_consumed=True, messages=self.player.heal().messages)
        if normalized_choice == "4":
            return TurnResult(turn_consumed=False, messages=self.player.display_stats().messages)

        return TurnResult(turn_consumed=False, messages=["Invalid choice. Try again."])

    def apply_wizard_turn(self) -> List[str]:
        if self.wizard.health <= 0:
            return []

        messages = self.wizard.regenerate().messages + self.wizard.attack(self.player).messages
        if self.player.health <= 0:
            messages.append(f"{self.player.name} has been defeated!")
        return messages

    def run_round(self, choice: str) -> TurnResult:
        result = self.resolve_turn(choice)
        if self.wizard.health <= 0 or not result.turn_consumed:
            return result

        return TurnResult(
            turn_consumed=True,
            messages=result.messages + self.apply_wizard_turn(),
        )

    def handle_player_turn(self) -> bool:
        print_messages(self.get_turn_menu_lines())
        choice = input("Choose an action: ")
        result = self.run_round(choice)
        print_messages(result.messages)
        return result.turn_consumed

    def battle(self) -> None:
        while not self.is_over():
            self.handle_player_turn()

        if self.wizard.health <= 0:
            print(f"The wizard {self.wizard.name} has been defeated by {self.player.name}!")


def print_messages(messages: List[str]) -> None:
    for message in messages:
        print(message)


def create_character() -> Character:
    print_messages(get_class_menu_lines())

    class_choice = input("Enter the number of your class choice: ")
    name = input("Enter your character's name: ")
    character, messages = build_character(class_choice, name)
    print_messages(messages)
    return character


def main() -> None:
    player = create_character()
    wizard = EvilWizard("The Dark Wizard")
    BattleEngine(player, wizard).battle()
