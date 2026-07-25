# Defeat the Evil Wizard

A small turn-based command-line battle game built as Python OOP practice.

## Current Structure

```text
Defeat_The_Evil_Wizard/
|-- __init__.py
|-- character_creation.py
|-- characters.py
|-- defeat_wizard.py
`-- game.py
tests/
`-- test_game.py
README.md
```

## How to Run

From the repository root:

```bash
python Defeat_The_Evil_Wizard/defeat_wizard.py
```

Or run it as a package:

```bash
python -m Defeat_The_Evil_Wizard.defeat_wizard
```

Run the test suite with:

```bash
python -m unittest discover -s tests
```

## Gameplay

Choose one of four classes, each with a distinct stat profile:

| Class   | Health | Attack | Defense | Playstyle              |
| ------- | ------ | ------ | ------- | ---------------------- |
| Warrior | 140    | 35     | 10      | Balanced bruiser       |
| Mage    | 100    | 50     | 0       | Glass cannon           |
| Archer  | 110    | 40     | 5       | Skirmisher             |
| Paladin | 160    | 25     | 15      | Tank — slow but sturdy |

Each turn you can:

- Attack
- Use a special ability
- Heal (drinks a potion)
- View stats

Defense reduces incoming damage flat, so armor matters against the wizard's attacks.

Healing is limited: each player carries **5 potions**, and every heal drinks
one (healing at full health doesn't waste a potion, and trying to heal with an
empty bag doesn't cost your turn). Once they're gone, it's do-or-die.

Special abilities charge up: land **5 regular attacks** to ready your special,
which deals double damage and resets the charge. The menu shows your current
charge (`2. Use Special Ability [3/5]`), and picking it before it's ready
doesn't cost your turn.

The Evil Wizard (220 HP, 5 defense) regenerates health before attacking back,
so the fight is a damage race.

## Refactor Notes

The code is now split into:

- `character_creation.py` for class selection and player construction
- `characters.py` for character definitions and combat behavior
- `game.py` for the `BattleEngine` and battle loop orchestration
- `defeat_wizard.py` as the CLI entry point
- `tests/test_game.py` for regression coverage around creation and combat flow

This keeps the game logic easier to read and makes future changes, such as adding items or enemies, less painful.

## Requirements

- Python 3.8 or higher
- No external libraries needed

## Future Improvements

- Random damage and critical hits
- More classes
- Wizard summons minions
- Items system
