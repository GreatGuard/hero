# -*- coding: utf-8 -*-
"""
游戏测试数据模块
"""

# 测试用英雄数据
TEST_HERO_DATA = {
    "name": "TestHero",
    "hp": 100,
    "max_hp": 100,
    "attack": 20,
    "defense": 5,
    "level": 1,
    "exp": 0,
    "gold": 20,
    "potions": 2,
    "position": 0
}

# 测试怪物数据
TEST_MONSTER_DATA = {
    "goblin": {
        "name": "Goblin",
        "hp": 30,
        "max_hp": 30,
        "attack": 10,
        "defense": 2,
        "exp": 10,
        "gold": 10
    },
    "dragon": {
        "name": "Dragon",
        "hp": 100,
        "max_hp": 100,
        "attack": 30,
        "defense": 15,
        "exp": 100,
        "gold": 200
    }
}

# 测试装备数据
TEST_EQUIPMENT_DATA = {
    "weapon": {
        "name": "TestSword",
        "type": "weapon",
        "attack": 15,
        "defense": 0,
        "hp": 0,
        "value": 100
    },
    "armor": {
        "name": "TestArmor",
        "type": "armor",
        "attack": 0,
        "defense": 10,
        "hp": 30,
        "value": 150
    },
    "accessory": {
        "name": "TestRing",
        "type": "accessory",
        "attack": 5,
        "defense": 2,
        "hp": 10,
        "value": 200
    }
}

# 测试事件序列
TEST_EVENT_SEQUENCES = {
    "victory_sequence": [
        {"type": "safe_move", "params": {}},
        {"type": "find_potion", "params": {}},
        {"type": "encounter_monster", "params": {"monster": "goblin"}},
        {"type": "safe_move", "params": {}},
        {"type": "find_chest", "params": {"gold": 20}}
    ],
    "challenge_sequence": [
        {"type": "encounter_monster", "params": {"monster": "dragon"}},
        {"type": "mine_trap", "params": {"damage": 15}},
        {"type": "encounter_boss", "params": {"boss": "dragon"}}
    ]
}

# 测试技能数据
TEST_SKILL_DATA = {
    "fireball": {
        "name": "fireball",
        "damage": 30,
        "mana_cost": 10,
        "level_required": 1
    },
    "iceball": {
        "name": "iceball",
        "damage": 25,
        "mana_cost": 8,
        "level_required": 1
    },
    "lightning": {
        "name": "lightning",
        "damage": 40,
        "mana_cost": 15,
        "level_required": 3
    }
}

# 测试商店数据
TEST_SHOP_DATA = {
    "weapons": [
        {"name": "Iron Sword", "type": "weapon", "attack": 5, "defense": 0, "hp": 0, "value": 50},
        {"name": "Steel Sword", "type": "weapon", "attack": 10, "defense": 0, "hp": 0, "value": 100},
        {"name": "Magic Sword", "type": "weapon", "attack": 15, "defense": 0, "hp": 0, "value": 200}
    ],
    "armors": [
        {"name": "Leather Armor", "type": "armor", "attack": 0, "defense": 5, "hp": 10, "value": 75},
        {"name": "Iron Armor", "type": "armor", "attack": 0, "defense": 10, "hp": 20, "value": 150},
        {"name": "Magic Armor", "type": "armor", "attack": 5, "defense": 15, "hp": 30, "value": 300}
    ],
    "potions": [
        {"name": "Small Potion", "heal": 20, "value": 10},
        {"name": "Medium Potion", "heal": 40, "value": 20},
        {"name": "Large Potion", "heal": 60, "value": 30}
    ]
}

def validate_test_data():
    """验证测试数据有效性"""
    # 验证英雄数据
    assert TEST_HERO_DATA["hp"] > 0, "英雄血量应大于0"
    assert TEST_HERO_DATA["attack"] > 0, "英雄攻击力应大于0"
    assert TEST_HERO_DATA["defense"] >= 0, "英雄防御力应大于等于0"
    assert TEST_HERO_DATA["level"] >= 1, "英雄等级应大于等于1"
    assert TEST_HERO_DATA["gold"] >= 0, "英雄金币应大于等于0"
    assert TEST_HERO_DATA["potions"] >= 0, "英雄药剂数量应大于等于0"
    assert TEST_HERO_DATA["position"] >= 0, "英雄位置应大于等于0"
    
    # 验证怪物数据
    for monster_name, monster_data in TEST_MONSTER_DATA.items():
        assert monster_data["hp"] > 0, f"{monster_name}血量应大于0"
        assert monster_data["max_hp"] == monster_data["hp"], f"{monster_name}最大血量应等于当前血量"
        assert monster_data["attack"] > 0, f"{monster_name}攻击力应大于0"
        assert monster_data["defense"] >= 0, f"{monster_name}防御力应大于等于0"
        assert monster_data["exp"] > 0, f"{monster_name}经验值应大于0"
        assert monster_data["gold"] > 0, f"{monster_name}金币应大于0"
    
    # 验证装备数据
    for equip_type, equip_data in TEST_EQUIPMENT_DATA.items():
        assert equip_data["value"] > 0, f"{equip_type}装备价值应大于0"
        assert equip_data["type"] in ["weapon", "armor", "accessory"], f"{equip_type}装备类型无效"
        assert equip_data["attack"] >= 0, f"{equip_type}装备攻击力应大于等于0"
        assert equip_data["defense"] >= 0, f"{equip_type}装备防御力应大于等于0"
        assert equip_data["hp"] >= 0, f"{equip_type}装备血量加成应大于等于0"
    
    # 验证技能数据
    for skill_name, skill_data in TEST_SKILL_DATA.items():
        assert skill_data["damage"] > 0, f"{skill_name}技能伤害应大于0"
        assert skill_data["mana_cost"] >= 0, f"{skill_name}技能法力消耗应大于等于0"
        assert skill_data["level_required"] >= 1, f"{skill_name}技能需求等级应大于等于1"
    
    # 验证商店数据
    for weapon in TEST_SHOP_DATA["weapons"]:
        assert weapon["value"] > 0, f"武器{weapon['name']}价值应大于0"
        assert weapon["type"] == "weapon", f"武器{weapon['name']}类型应为weapon"
        assert weapon["attack"] > 0, f"武器{weapon['name']}攻击力应大于0"
    
    for armor in TEST_SHOP_DATA["armors"]:
        assert armor["value"] > 0, f"防具{armor['name']}价值应大于0"
        assert armor["type"] == "armor", f"防具{armor['name']}类型应为armor"
        assert armor["defense"] > 0, f"防具{armor['name']}防御力应大于0"
    
    for potion in TEST_SHOP_DATA["potions"]:
        assert potion["value"] > 0, f"药剂{potion['name']}价值应大于0"
        assert potion["heal"] > 0, f"药剂{potion['name']}回复量应大于0"
    
    return True

# 在导入时验证测试数据
validate_test_data()