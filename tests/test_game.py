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
            [
                "Aria's Stats - Health: 140/140, Attack Power: 35, "
                "Defense: 10, Special: 0/5, Potions: 5/5"
            ],
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

        self.assertEqual(result.messages, ["Aria attacks The Dark Wizard for 30 damage!"])
        self.assertEqual(wizard.health, 190)

    def test_heal_returns_message(self) -> None:
        player = Warrior("Aria")
        player.take_damage(30)

        result = player.heal()

        self.assertEqual(
            result.messages,
            [
                "Aria drinks a potion and heals for 20 points! "
                "Current health: 140/140 (4 potions left)"
            ],
        )
        self.assertEqual(player.health, 140)
        self.assertEqual(player.potions, 4)

    def test_regenerate_returns_message(self) -> None:
        wizard = EvilWizard("The Dark Wizard")
        wizard.take_damage(20)

        result = wizard.regenerate()

        self.assertEqual(
            result.messages,
            ["The Dark Wizard regenerates 5 health! Current health: 210/220"],
        )
        self.assertEqual(wizard.health, 210)

    def test_engine_run_round_applies_player_and_wizard_turns(self) -> None:
        player = Warrior("Aria")
        wizard = EvilWizard("The Dark Wizard")
        engine = BattleEngine(player, wizard)
        result = engine.run_round("1")

        self.assertTrue(result.turn_consumed)
        self.assertEqual(
            result.messages,
            [
                "Aria attacks The Dark Wizard for 30 damage!",
                "The Dark Wizard regenerates 5 health! Current health: 195/220",
                "The Dark Wizard attacks Aria for 10 damage!",
            ],
        )
        self.assertEqual(wizard.health, 195)
        self.assertEqual(player.health, 130)

    def test_engine_battle_ends_with_player_victory(self) -> None:
        player = Warrior("Aria")
        wizard = EvilWizard("The Dark Wizard")
        wizard.health = 40
        engine = BattleEngine(player, wizard)
        output = io.StringIO()

        with patch("builtins.input", side_effect=["1", "1"]):
            with redirect_stdout(output):
                engine.battle()

        transcript = output.getvalue()
        self.assertEqual(wizard.health, 0)
        self.assertIn("The wizard The Dark Wizard has been defeated by Aria!", transcript)


class SpecialAbilityTests(unittest.TestCase):
    def test_special_not_ready_does_not_consume_turn(self) -> None:
        player = Warrior("Aria")
        wizard = EvilWizard("The Dark Wizard")
        engine = BattleEngine(player, wizard)

        result = engine.resolve_turn("2")

        self.assertFalse(result.turn_consumed)
        self.assertEqual(
            result.messages,
            ["Aria's special ability isn't charged yet (0/5 attacks landed)."],
        )
        self.assertEqual(wizard.health, wizard.max_health)

    def test_special_charges_after_five_attacks_and_resets(self) -> None:
        player = Warrior("Aria")
        wizard = EvilWizard("The Dark Wizard")
        engine = BattleEngine(player, wizard)

        for _ in range(5):
            player.attack(wizard)

        self.assertTrue(player.special_ready)

        wizard_health_before = wizard.health
        result = engine.resolve_turn("2")

        self.assertTrue(result.turn_consumed)
        self.assertEqual(
            result.messages,
            ["Aria uses Burning Maul on The Dark Wizard for 65 damage!"],
        )
        self.assertEqual(wizard.health, wizard_health_before - 65)
        self.assertEqual(player.special_charge, 0)
        self.assertFalse(player.special_ready)

    def test_defense_reduces_incoming_damage(self) -> None:
        player = Warrior("Aria")
        wizard = EvilWizard("The Dark Wizard")

        wizard.attack(player)

        self.assertEqual(player.health, 130)


class PotionTests(unittest.TestCase):
    def test_heal_at_full_health_does_not_consume_potion(self) -> None:
        player = Warrior("Aria")

        result = player.heal()

        self.assertEqual(result.messages, ["Aria is already at max health!"])
        self.assertEqual(player.potions, 5)

    def test_out_of_potions_does_not_consume_turn(self) -> None:
        player = Warrior("Aria")
        player.take_damage(30)
        player.potions = 0
        wizard = EvilWizard("The Dark Wizard")
        engine = BattleEngine(player, wizard)

        result = engine.resolve_turn("3")

        self.assertFalse(result.turn_consumed)
        self.assertEqual(result.messages, ["Aria is out of potions!"])
        self.assertEqual(player.health, 120)

    def test_potions_run_out_after_five_heals(self) -> None:
        player = Warrior("Aria")
        for _ in range(5):
            player.take_damage(30)
            player.heal()

        self.assertEqual(player.potions, 0)


if __name__ == "__main__":
    unittest.main()
