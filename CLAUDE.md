# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**英雄无敌 (Heroes Invincible)** is a bilingual (Chinese/English) text-based RPG adventure game written in Python. Players take on the role of a hero progressing through linear maps, encountering random events, battling monsters, and collecting equipment.

- **Version**: 3.0 (modular architecture)
- **Language**: Python 3.7+ (standard library only, no external dependencies)
- **Author**: Kevin
- **License**: MIT

## Development Commands

### Running the Game

```bash
# Direct execution
cd src/hero
python main.py

# Or install and run as console script
pip install -e .
hero
```

### Testing

The project uses Python's built-in `unittest` framework with a custom test runner.

```bash
# Run all tests
python run_tests.py

# Run with verbose output
python run_tests.py -v

# Run specific test module
python run_tests.py -m test_combat

# Run specific test class
python run_tests.py -m test_combat -c TestCombatSystem

# Run specific test method
python run_tests.py -m test_combat -c TestCombatSystem -f test_hero_attack

# Generate test report
python run_tests.py --report -o test_report.txt

# Run tests matching custom pattern
python run_tests.py -p "test_*.py"
```

**Test Coverage**: 49 tests across 5 core modules with 100% pass rate.

### Git Workflow

The README.md contains comprehensive git commands for branching, merging, and history management.

## Architecture

### Core Design Philosophy

The game follows a **modular architecture** with clear separation of concerns. The `HeroGame` class acts as the central controller, orchestrating various subsystems through composition rather than inheritance.

### System Structure

```
src/hero/
├── main.py              # Main game controller and entry point
├── language.py          # Internationalization system (zh/en)
├── game_config.py       # Game balance and configuration
├── combat.py            # Turn-based combat system
├── equipment.py         # Equipment and inventory management
├── events.py            # Random event generation and handling
└── newbie_village.py    # Tutorial/pre-adventure area
```

### Key Architectural Patterns

#### 1. **Composition over Inheritance**
`HeroGame` aggregates subsystems rather than inheriting from them:
```python
self.combat_system = CombatSystem(self)
self.equipment_system = EquipmentSystem(self)
self.event_system = EventSystem(self)
self.newbie_village = NewbieVillage(self)
```

Each subsystem receives the game instance for **dependency injection**, allowing access to shared state (hero attributes, language, equipment, etc.).

#### 2. **Strategy Pattern**
Different map types (plains, forest, desert, dungeon, mountain) and difficulty levels (simple, normal, hard, nightmare) are configured as strategies in `game_config.py`, affecting:
- Map length
- Event probabilities
- Enemy strength scaling
- Gold/XP multipliers
- Starting resources

#### 3. **Observer Pattern**
Language changes propagate through `LanguageSupport` system, dynamically updating all UI text. The `language` attribute determines text formatting for numbers, positions, and event descriptions.

#### 4. **Factory Pattern**
Equipment and monsters are procedurally generated with randomized properties, rarities, and scaling based on player level and difficulty.

### Game State Management

Core hero attributes are managed in `HeroGame`:
- **Combat Stats**: `hero_hp`, `hero_max_hp`, `hero_attack`, `hero_defense`
- **Progression**: `hero_level`, `hero_exp`, `hero_position`, `monsters_defeated`
- **Resources**: `hero_gold`, `hero_potions`, `hero_skills`
- **Equipment**: `equipment` dict (weapon/armor/accessory), `inventory` list
- **Base Attributes**: `base_attack`, `base_defense`, `base_max_hp` (for equipment calculations)

**Critical Pattern**: All stat modifications must use `update_attributes()` to recalculate totals including equipment bonuses.

### Subsystem Interactions

```
HeroGame (Main Controller)
    ├─> LanguageSupport ── Provides localized text for all UI
    ├─> CombatSystem ── Handles battles, damage calculations, skill usage
    ├─> EquipmentSystem ── Generates items, manages inventory, calculates stat bonuses
    ├─> EventSystem ── Triggers random encounters based on map type probabilities
    └─> NewbieVillage ── Tutorial area with training, shop, clinic, elder
```

**Flow**:
1. Player advances position → `event_system.trigger_event()`
2. Event may lead to combat → `combat_system.start_battle()`
3. Combat rewards → equipment/gold/XP → `equipment_system.manage_inventory()`
4. All UI text → `lang.get_text(key)` with dynamic formatting

### Configuration System

All game balance is centralized in `game_config.py`:

- **DIFFICULTY_SETTINGS**: Dict defining 4 difficulty levels with multipliers
- **MAP_TYPES**: Dict defining 5 map types with unique event profiles
- **EQUIPMENT rarities**: 5 tiers (common/exceptional/rare/epic/legendary)
- **Skills**: 5 skills with damage formulas and mechanics

**Important**: When adding new content, update these configs rather than hardcoding values in game logic.

### Internationalization

The `LanguageSupport` class provides bilingual support:
- Language selection at startup (`zh` or `en`)
- All text retrieved via `lang.get_text(key)` method
- Dynamic formatting functions for language-specific output
- Monster names and event descriptions change per language

**Best Practice**: Never hardcode user-facing text. Always add strings to both `zh_texts` and `en_texts` dictionaries in `language.py`.

## Testing Conventions

- Tests are organized by module: `test_<module>.py`
- Mock objects used for dependency isolation
- Test classes follow naming: `Test<ClassName>`
- Fixtures for common test data
- Comprehensive assertions for game state validation

## Important Implementation Notes

1. **No External Dependencies**: Uses only Python standard library
2. **UTF-8 Encoding**: All files handle Chinese characters properly
3. **Attribute Calculation**: Always call `update_attributes()` after equipment changes
4. **Language Switching**: Text retrieval methods handle language differences internally
5. **Random Events**: Probabilities defined in `MAP_TYPES`, not hardcoded in event logic
6. **Combat Skills**: Fireball interacts with crit/lifesteal mechanics
7. **Equipment Generation**: Rarity affects stat ranges and pricing

## Common Modification Patterns

### Adding New Equipment
1. Define in `EquipmentSystem.generate_equipment()`
2. Add rarity multipliers to `EQUIPMENT_RARITY`
3. Update `update_attributes()` to handle new stat types

### Adding New Map Type
1. Add entry to `MAP_TYPES` in `game_config.py`
2. Define unique event probabilities
3. Add special monster encounters if needed

### Adding New Skill
1. Add to `SKILL_DESCRIPTIONS` in `language.py`
2. Implement in `CombatSystem.use_skill()`
3. Add to random skill learning in `EventSystem`
4. Update `update_attributes()` if skill affects base stats

### Adding New Event
1. Add event type to event probability calculations
2. Implement handler in `EventSystem.trigger_event()`
3. Add all text to both languages in `language.py`
4. Update event history tracking if significant
