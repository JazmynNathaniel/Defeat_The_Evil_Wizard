import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from Defeat_The_Evil_Wizard.characters import EvilWizard, Warrior
from Defeat_The_Evil_Wizard.character_creation import build_character
from Defeat_The_Evil_Wizard.game import (
    BattleEngine,
    create_character,
)


class CreateCharacterTests(unittest.TestCase):
    def test_build_character_defaults_invalid_class_to_warrior(self) -> None:
        character, messages = build_character("9", "Aria")

        self.assertIsInstance(character, Warrior)
        self.assertEqual(character.name, "Aria")
        self.assertEqual(messages, ["Invalid choice. Defaulting to Warrior."])

    def test_build_character_uses_hero_for_blank_name(self) -> None:
        character, messages = build_character("1", "   ")

        self.assertEqual(character.name, "Hero")
        self.assertEqual(messages, [])

    def test_invalid_class_defaults_to_warrior(self) -> None:
        with patch("builtins.input", side_effect=["9", "Aria"]):
            with redirect_stdout(io.StringIO()):
                character = create_character()

        self.assertIsInstance(character, Warrior)
        self.assertEqual(character.name, "Aria")

    def test_blank_name_falls_back_to_hero(self) -> None:
        with patch("builtins.input", side_effect=["1", "   "]):
            with redirect_stdout(io.StringIO()):
                character = create_character()

        self.assertEqual(character.name, "Hero")


class HandlePlayerTurnTests(unittest.TestCase):
    def test_engine_resolve_turn_view_stats_does_not_consume_turn(self) -> None:
        player = Warrior("Aria")
        wizard = EvilWizard("The Dark Wizard")
        engine = BattleEngine(player, wizard)

        result = engine.resolve_turn("4")

        self.assertFalse(result.turn_consumed)
        self.assertEqual(
            result.messages,
            ["Aria's Stats - Health: 140/140, Attack Power: 35"],
        )
        self.assertEqual(wizard.health, wizard.max_health)

    def test_engine_resolve_turn_invalid_input_does_not_consume_turn(self) -> None:
        player = Warrior("Aria")
        wizard = EvilWizard("The Dark Wizard")
        engine = BattleEngine(player, wizard)

        result = engine.resolve_turn("x")

        self.assertFalse(result.turn_consumed)
        self.assertEqual(result.messages, ["Invalid choice. Try again."])
        self.assertEqual(wizard.health, wizard.max_health)

    def test_engine_handle_player_turn_uses_input(self) -> None:
        player = Warrior("Aria")
        wizard = EvilWizard("The Dark Wizard")
        engine = BattleEngine(player, wizard)

        with patch("builtins.input", return_value="4"):
            with redirect_stdout(io.StringIO()):
                turn_consumed = engine.handle_player_turn()

        self.assertFalse(turn_consumed)
        self.assertEqual(wizard.health, wizard.max_health)

class BattleTests(unittest.TestCase):
    def test_attack_returns_messages_without_printing(self) -> None:
        player = Warrior("Aria")
        wizard = EvilWizard("The Dark Wizard")

        result = player.attack(wizard)

        self.assertEqual(result.messages, ["Aria attacks The Dark Wizard for 35 damage!"])
        self.assertEqual(wizard.health, 115)

    def test_heal_returns_message(self) -> None:
        player = Warrior("Aria")
        player.take_damage(20)

        result = player.heal()

        self.assertEqual(
            result.messages,
            ["Aria heals for 20 points! Current health: 140/140"],
        )
        self.assertEqual(player.health, 140)

    def test_regenerate_returns_message(self) -> None:
        wizard = EvilWizard("The Dark Wizard")
        wizard.take_damage(20)

        result = wizard.regenerate()

        self.assertEqual(
            result.messages,
            ["The Dark Wizard regenerates 5 health! Current health: 135/150"],
        )
        self.assertEqual(wizard.health, 135)

    def test_engine_run_round_applies_player_and_wizard_turns(self) -> None:
        player = Warrior("Aria")
        wizard = EvilWizard("The Dark Wizard")
        engine = BattleEngine(player, wizard)
        result = engine.run_round("2")

        self.assertTrue(result.turn_consumed)
        self.assertEqual(
            result.messages,
            [
                "Aria uses Burning Maul on The Dark Wizard for 70 damage!",
                "The Dark Wizard regenerates 5 health! Current health: 85/150",
                "The Dark Wizard attacks Aria for 15 damage!",
            ],
        )
        self.assertEqual(wizard.health, 85)
        self.assertEqual(player.health, 125)

    def test_engine_battle_ends_with_player_victory(self) -> None:
        player = Warrior("Aria")
        wizard = EvilWizard("The Dark Wizard")
        engine = BattleEngine(player, wizard)
        output = io.StringIO()

        with patch("builtins.input", side_effect=["2", "2", "1"]):
            with redirect_stdout(output):
                engine.battle()

        transcript = output.getvalue()
        self.assertEqual(wizard.health, 0)
        self.assertIn("The wizard The Dark Wizard has been defeated by Aria!", transcript)

if __name__ == "__main__":
    unittest.main()
