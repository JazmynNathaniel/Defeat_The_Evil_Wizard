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

Choose one of four classes:

- Warrior
- Mage
- Archer
- Paladin

Each turn you can:

- Attack
- Use a special ability
- Heal
- View stats

The Evil Wizard regenerates health before attacking back, so the fight is a damage race.

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
