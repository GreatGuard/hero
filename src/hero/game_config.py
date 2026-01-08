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

# 传奇装备配置 - 使用统一的多语言键名
LEGENDARY_EQUIPMENT = {
    "weapon": [
        {
            "name_key": "legendary_sword_dragon_god",
            "attack": 25,
            "defense": 5,
            "hp": 10,
            "special_effects": ["crit_rate", "lifesteal"],
            "crit_rate": 0.15,
            "lifesteal_rate": 0.2
        },
        {
            "name_key": "legendary_staff_frost",
            "attack": 18,
            "defense": 0,
            "hp": 0,
            "special_effects": ["ice_damage", "mana_boost"],
            "ice_damage": 10,
            "mana_boost": 20
        },
        {
            "name_key": "legendary_dagger_shadow",
            "attack": 22,
            "defense": 0,
            "hp": 0,
            "special_effects": ["backstab", "dodge"],
            "backstab_damage": 0.3,
            "dodge_rate": 0.15
        }
    ],
    "armor": [
        {
            "name_key": "legendary_armor_holy_light",
            "attack": 0,
            "defense": 20,
            "hp": 30,
            "special_effects": ["healing", "holy_resistance"],
            "healing_rate": 0.05,
            "holy_resistance": 0.3
        },
        {
            "name_key": "legendary_armor_dragon_scale",
            "attack": 5,
            "defense": 18,
            "hp": 25,
            "special_effects": ["fire_resistance", "counter_attack"],
            "fire_resistance": 0.4,
            "counter_attack_rate": 0.25
        },
        {
            "name_key": "legendary_cloak_shadow",
            "attack": 0,
            "defense": 15,
            "hp": 20,
            "special_effects": ["stealth", "evasion"],
            "stealth_chance": 0.2,
            "evasion_rate": 0.1
        }
    ],
    "accessory": [
        {
            "name_key": "legendary_ring_sage",
            "attack": 8,
            "defense": 8,
            "hp": 15,
            "special_effects": ["wisdom", "mana_regeneration"],
            "wisdom_bonus": 0.1,
            "mana_regeneration": 5
        },
        {
            "name_key": "legendary_charm_lucky",
            "attack": 0,
            "defense": 0,
            "hp": 10,
            "special_effects": ["luck", "crit_damage"],
            "luck_bonus": 0.15,
            "crit_damage": 0.5
        },
        {
            "name_key": "legendary_stone_eternal",
            "attack": 0,
            "defense": 0,
            "hp": 25,
            "special_effects": ["immortality", "health_regeneration"],
            "immortality_chance": 0.05,
            "health_regeneration": 3
        }
    ]
}

# 套装配置 - 使用统一的多语言键名
EQUIPMENT_SETS = {
    "warrior_set": {
        "name_key": "equipment_set_warrior",
        "pieces": ["weapon", "armor"],
        "effects": {
            "2_piece": {
                "name_key": "set_bonus_warrior_glory",
                "attack_bonus": 10,
                "defense_bonus": 5
            }
        }
    },
    "mage_set": {
        "name_key": "equipment_set_mage",
        "pieces": ["weapon", "accessory"],
        "effects": {
            "2_piece": {
                "name_key": "set_bonus_magic_mastery",
                "mana_bonus": 30,
                "spell_power": 0.15
            }
        }
    },
    "assassin_set": {
        "name_key": "equipment_set_assassin",
        "pieces": ["weapon", "accessory"],
        "effects": {
            "2_piece": {
                "name_key": "set_bonus_shadow_assault",
                "crit_rate": 0.1,
                "dodge_rate": 0.1
            }
        }
    }
}

# 新事件类型配置
EVENT_TYPES = {
    "mysterious_teleport": {
        "name_key": "event_mysterious_teleport",
        "description_key": "event_mysterious_teleport_desc",
        "min_effect": -3,
        "max_effect": 3
    },
    "sage_guidance": {
        "name_key": "event_sage_guidance",
        "description_key": "event_sage_guidance_desc",
        "min_exp": 30,
        "max_exp": 60
    },
    "robber_encounter": {
        "name_key": "event_robber_encounter",
        "description_key": "event_robber_encounter_desc",
        "min_gold_loss": 10,
        "max_gold_loss": 30,
        "combat_chance": 0.5
    },
    "mysterious_altar": {
        "name_key": "event_mysterious_altar",
        "description_key": "event_mysterious_altar_desc",
        "hp_cost_percent": 0.2,
        "attack_boost": 5,
        "defense_boost": 3
    },
    "roadside_camp": {
        "name_key": "event_roadside_camp",
        "description_key": "event_roadside_camp_desc",
        "min_heal": 20,
        "max_heal": 40
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
    },
    "swamp": {
        "name": "swamp",
        "description": "swamp_desc",
        "special_events": ["poison_cloud", "quicksand", "rare_herbs", "swamp_merchant"],
        "monsters": ["crocodile", "venom_snake", "swamp_beast"]
    },
    "snowfield": {
        "name": "snowfield",
        "description": "snowfield_desc",
        "special_events": ["frostbite", "avalanche", "ice_cave", "frost_effect"],
        "monsters": ["ice_wolf", "snow_beast", "frost_giant"]
    }
}

# 怪物模板配置
MONSTER_TEMPLATES = {
    # 普通怪物
    "goblin": {
        "name_key": "monster_goblin",
        "base_hp": (20, 35),
        "base_attack": (5, 12),
        "base_defense": (0, 3),
        "gold_reward": (5, 20),
        "exp_reward": (10, 25),
        "elite": False
    },
    "slime": {
        "name_key": "monster_slime",
        "base_hp": (25, 40),
        "base_attack": (3, 8),
        "base_defense": (2, 5),
        "gold_reward": (3, 15),
        "exp_reward": (8, 20),
        "elite": False
    },
    "wolf": {
        "name_key": "monster_wolf",
        "base_hp": (25, 40),
        "base_attack": (8, 15),
        "base_defense": (1, 4),
        "gold_reward": (8, 25),
        "exp_reward": (12, 28),
        "elite": False
    },
    "beast": {
        "name_key": "monster_beast",
        "base_hp": (30, 50),
        "base_attack": (10, 18),
        "base_defense": (3, 6),
        "gold_reward": (10, 30),
        "exp_reward": (15, 30),
        "elite": False
    },
    "spider": {
        "name_key": "monster_spider",
        "base_hp": (20, 35),
        "base_attack": (12, 20),
        "base_defense": (1, 3),
        "gold_reward": (8, 22),
        "exp_reward": (14, 26),
        "elite": False
    },
    "scorpion": {
        "name_key": "monster_scorpion",
        "base_hp": (25, 40),
        "base_attack": (10, 18),
        "base_defense": (2, 5),
        "gold_reward": (12, 28),
        "exp_reward": (16, 32),
        "elite": False
    },
    "sand_worm": {
        "name_key": "monster_sand_worm",
        "base_hp": (35, 55),
        "base_attack": (8, 15),
        "base_defense": (5, 10),
        "gold_reward": (15, 35),
        "exp_reward": (18, 35),
        "elite": False
    },
    "golem": {
        "name_key": "monster_golem",
        "base_hp": (40, 60),
        "base_attack": (10, 20),
        "base_defense": (8, 15),
        "gold_reward": (20, 40),
        "exp_reward": (20, 40),
        "elite": False
    },
    "skeleton": {
        "name_key": "monster_skeleton",
        "base_hp": (25, 40),
        "base_attack": (12, 20),
        "base_defense": (3, 8),
        "gold_reward": (12, 30),
        "exp_reward": (15, 32),
        "elite": False
    },
    "ghost": {
        "name_key": "monster_ghost",
        "base_hp": (20, 35),
        "base_attack": (15, 25),
        "base_defense": (1, 3),
        "gold_reward": (15, 35),
        "exp_reward": (18, 36),
        "elite": False
    },
    "demon": {
        "name_key": "monster_demon",
        "base_hp": (35, 55),
        "base_attack": (15, 25),
        "base_defense": (5, 10),
        "gold_reward": (20, 45),
        "exp_reward": (22, 45),
        "elite": False
    },
    "giant": {
        "name_key": "monster_giant",
        "base_hp": (40, 65),
        "base_attack": (15, 25),
        "base_defense": (8, 15),
        "gold_reward": (25, 50),
        "exp_reward": (25, 50),
        "elite": False
    },
    "dragon": {
        "name_key": "monster_dragon",
        "base_hp": (45, 70),
        "base_attack": (20, 30),
        "base_defense": (10, 18),
        "gold_reward": (30, 60),
        "exp_reward": (30, 60),
        "elite": False
    },
    "titan": {
        "name_key": "monster_titan",
        "base_hp": (50, 80),
        "base_attack": (18, 28),
        "base_defense": (12, 20),
        "gold_reward": (35, 70),
        "exp_reward": (35, 70),
        "elite": False
    },
    
    # 新地图怪物
    "crocodile": {
        "name_key": "monster_crocodile",
        "base_hp": (30, 50),
        "base_attack": (12, 22),
        "base_defense": (5, 10),
        "gold_reward": (15, 35),
        "exp_reward": (18, 38),
        "elite": False
    },
    "venom_snake": {
        "name_key": "monster_venom_snake",
        "base_hp": (20, 35),
        "base_attack": (15, 25),
        "base_defense": (2, 5),
        "gold_reward": (12, 30),
        "exp_reward": (16, 34),
        "elite": False,
        "special": "poison"  # 特殊能力：中毒
    },
    "swamp_beast": {
        "name_key": "monster_swamp_beast",
        "base_hp": (40, 65),
        "base_attack": (15, 25),
        "base_defense": (8, 15),
        "gold_reward": (20, 45),
        "exp_reward": (22, 45),
        "elite": False
    },
    "ice_wolf": {
        "name_key": "monster_ice_wolf",
        "base_hp": (28, 45),
        "base_attack": (14, 24),
        "base_defense": (4, 8),
        "gold_reward": (14, 32),
        "exp_reward": (17, 35),
        "elite": False,
        "special": "frost"  # 特殊能力：冰霜
    },
    "snow_beast": {
        "name_key": "monster_snow_beast",
        "base_hp": (35, 60),
        "base_attack": (16, 26),
        "base_defense": (7, 12),
        "gold_reward": (18, 40),
        "exp_reward": (20, 42),
        "elite": False
    },
    "frost_giant": {
        "name_key": "monster_frost_giant",
        "base_hp": (45, 75),
        "base_attack": (18, 30),
        "base_defense": (10, 18),
        "gold_reward": (25, 55),
        "exp_reward": (28, 55),
        "elite": False
    }
}



# Boss模板配置
BOSS_TEMPLATES = {
    "plains": {
        "name_key": "boss_plains_warlord",
        "base_hp": (100, 150),
        "base_attack": (25, 40),
        "base_defense": (15, 25),
        "gold_reward": (100, 200),
        "exp_reward": (100, 200),
        "skills": ["power_strike", "heal"]
    },
    "forest": {
        "name_key": "boss_ancient_treant",
        "base_hp": (120, 180),
        "base_attack": (20, 35),
        "base_defense": (20, 30),
        "gold_reward": (120, 240),
        "exp_reward": (120, 240),
        "skills": ["root_trap", "nature_heal"]
    },
    "desert": {
        "name_key": "boss_desert_sphinx",
        "base_hp": (110, 170),
        "base_attack": (30, 45),
        "base_defense": (12, 22),
        "gold_reward": (130, 260),
        "exp_reward": (130, 260),
        "skills": ["sandstorm", "riddle"]
    },
    "dungeon": {
        "name_key": "boss_demon_lord",
        "base_hp": (130, 200),
        "base_attack": (35, 50),
        "base_defense": (15, 25),
        "gold_reward": (150, 300),
        "exp_reward": (150, 300),
        "skills": ["fire_breath", "summon_minions"]
    },
    "mountain": {
        "name_key": "boss_mountain_dragon",
        "base_hp": (150, 250),
        "base_attack": (40, 60),
        "base_defense": (20, 35),
        "gold_reward": (200, 400),
        "exp_reward": (200, 400),
        "skills": ["dragon_breath", "wing_attack"]
    },
    "swamp": {
        "name_key": "boss_swamp_hydra",
        "base_hp": (140, 220),
        "base_attack": (30, 45),
        "base_defense": (18, 30),
        "gold_reward": (170, 340),
        "exp_reward": (170, 340),
        "skills": ["poison_bite", "regeneration"]
    },
    "snowfield": {
        "name_key": "boss_frost_king",
        "base_hp": (160, 240),
        "base_attack": (35, 55),
        "base_defense": (22, 35),
        "gold_reward": (180, 360),
        "exp_reward": (180, 360),
        "skills": ["blizzard", "ice_prison"]
    }
}


