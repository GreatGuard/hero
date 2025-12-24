# -*- coding: utf-8 -*-
"""
游戏配置模块 - 难度和地图设置
"""

DIFFICULTY_SETTINGS = {
    "easy": {
        "map_length": 50,
        "gold_multiplier": 1.5,
        "exp_multiplier": 1.5,
        "enemy_multiplier": 0.7,
        "gold_start": 30,
        "potions_start": 3,
        "name": "easy"
    },
    "normal": {
        "map_length": 100,
        "gold_multiplier": 1.0,
        "exp_multiplier": 1.0,
        "enemy_multiplier": 1.0,
        "gold_start": 20,
        "potions_start": 2,
        "name": "normal"
    },
    "hard": {
        "map_length": 150,
        "gold_multiplier": 0.8,
        "exp_multiplier": 1.2,
        "enemy_multiplier": 1.3,
        "gold_start": 15,
        "potions_start": 1,
        "name": "hard"
    },
    "nightmare": {
        "map_length": 200,
        "gold_multiplier": 0.6,
        "exp_multiplier": 1.5,
        "enemy_multiplier": 1.6,
        "gold_start": 10,
        "potions_start": 1,
        "name": "nightmare"
    }
}

MAP_TYPES = {
    "plains": {
        "name": "plains",
        "description": "plains_desc",
        "special_events": ["find_bun", "find_chest", "find_spring"],
        "monsters": ["goblin", "slime", "wolf"]
    },
    "forest": {
        "name": "forest",
        "description": "forest_desc",
        "special_events": ["find_herbs", "find_equipment", "find_potion"],
        "monsters": ["wolf", "beast", "spider"]
    },
    "desert": {
        "name": "desert",
        "description": "desert_desc",
        "special_events": ["find_oasis", "find_treasure", "find_equipment"],
        "monsters": ["scorpion", "sand_worm", "golem"]
    },
    "dungeon": {
        "name": "dungeon",
        "description": "dungeon_desc",
        "special_events": ["find_chest", "find_equipment", "mysterious_merchant"],
        "monsters": ["skeleton", "ghost", "demon"]
    },
    "mountain": {
        "name": "mountain",
        "description": "mountain_desc",
        "special_events": ["find_gem", "find_equipment", "dragon_encounter"],
        "monsters": ["giant", "dragon", "titan"]
    }
}
