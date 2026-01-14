#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
装备附魔系统测试

测试装备的附魔功能和附魔效果
"""

import unittest
import sys
import os
from unittest.mock import Mock

# 添加项目路径
project_root = os.path.join(os.path.dirname(__file__), '..')
src_path = os.path.join(project_root, 'src')
hero_path = os.path.join(src_path, 'hero')
sys.path.insert(0, hero_path)
sys.path.insert(0, src_path)

from hero.equipment import EquipmentSystem
from hero.language import LanguageSupport
from hero.main import HeroGame


class TestEnchantmentSystem(unittest.TestCase):
    """测试装备附魔系统"""

    def setUp(self):
        """设置测试环境"""
        # 创建模拟的HeroGame实例
        self.game = Mock(spec=HeroGame)
        
        # 设置必要的属性
        self.game.language = "zh"
        self.game.lang = LanguageSupport(self.game.language)
        self.game.difficulty = "normal"
        self.game.difficulty_settings = {
            "easy": {"enemy_multiplier": 0.7, "gold_multiplier": 1.5, "exp_multiplier": 1.0},
            "normal": {"enemy_multiplier": 1.0, "gold_multiplier": 1.0, "exp_multiplier": 1.0},
            "hard": {"enemy_multiplier": 1.3, "gold_multiplier": 0.8, "exp_multiplier": 1.2},
            "nightmare": {"enemy_multiplier": 1.6, "gold_multiplier": 0.6, "exp_multiplier": 1.5}
        }
        self.game.hero_gold = 1000  # 给予足够金币进行测试
        self.game.hero_attack = 20
        self.game.hero_defense = 10
        self.game.hero_max_hp = 100
        self.game.hero_hp = 100
        self.game.hero_level = 1
        
        # 初始化装备
        self.game.equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        self.game.inventory = []
        
        # 创建统计系统
        from hero.statistics import GameStatistics
        self.game.statistics = GameStatistics()
        
        # 创建装备系统实例
        self.equip_system = EquipmentSystem(self.game)
        
    def test_enchantment_configuration(self):
        """测试附魔配置"""
        import game_config
        
        # 检查附魔类型配置
        self.assertIn("flame_enchantment", game_config.ENCHANTMENT_TYPES)
        self.assertIn("frost_enchantment", game_config.ENCHANTMENT_TYPES)
        self.assertIn("poison_enchantment", game_config.ENCHANTMENT_TYPES)
        self.assertIn("holy_enchantment", game_config.ENCHANTMENT_TYPES)
        self.assertIn("shadow_enchantment", game_config.ENCHANTMENT_TYPES)
        
        # 检查附魔限制配置
        self.assertIn("weapon", game_config.ENCHANTMENT_RESTRICTIONS)
        self.assertIn("armor", game_config.ENCHANTMENT_RESTRICTIONS)
        self.assertIn("accessory", game_config.ENCHANTMENT_RESTRICTIONS)
        
    def test_enchantment_restrictions(self):
        """测试附魔限制"""
        import game_config
        
        # 创建一个武器
        weapon = self.equip_system.create_random_equipment("weapon")
        self.game.equipment["weapon"] = weapon
        
        # 武器应该可以附魔所有类型
        weapon_allowed = game_config.ENCHANTMENT_RESTRICTIONS["weapon"]
        self.assertEqual(len(weapon_allowed), 5)  # 所有5种附魔类型
        
        # 创建一个护甲
        armor = self.equip_system.create_random_equipment("armor")
        self.game.equipment["armor"] = armor
        
        # 护甲只能附魔冰霜和神圣
        armor_allowed = game_config.ENCHANTMENT_RESTRICTIONS["armor"]
        self.assertEqual(len(armor_allowed), 2)
        self.assertIn("frost_enchantment", armor_allowed)
        self.assertIn("holy_enchantment", armor_allowed)
        
        # 创建一个饰品
        accessory = self.equip_system.create_random_equipment("accessory")
        self.game.equipment["accessory"] = accessory
        
        # 饰品只能附魔神圣和暗影
        accessory_allowed = game_config.ENCHANTMENT_RESTRICTIONS["accessory"]
        self.assertEqual(len(accessory_allowed), 2)
        self.assertIn("holy_enchantment", accessory_allowed)
        self.assertIn("shadow_enchantment", accessory_allowed)
        
    def test_enchantment_cost_calculation(self):
        """测试附魔费用"""
        import game_config
        
        # 检查火焰附魔的费用
        flame_enchant = game_config.ENCHANTMENT_TYPES["flame_enchantment"]
        self.assertEqual(flame_enchant["cost"], 300)
        
        # 检查冰霜附魔的费用
        frost_enchant = game_config.ENCHANTMENT_TYPES["frost_enchantment"]
        self.assertEqual(frost_enchant["cost"], 250)
        
        # 检查毒素附魔的费用
        poison_enchant = game_config.ENCHANTMENT_TYPES["poison_enchantment"]
        self.assertEqual(poison_enchant["cost"], 350)
        
    def test_enchantment_success_rate(self):
        """测试附魔成功率"""
        import game_config
        
        # 创建一个传奇装备
        legendary_weapon = self.equip_system.create_random_equipment("weapon")
        legendary_weapon["rarity"] = "legendary"
        
        # 计算传奇装备的附魔成功率加成
        rarity_bonus = game_config.ENCHANTMENT_RARITY_BONUS["legendary"]
        self.assertEqual(rarity_bonus, 0.2)
        
        # 普通装备没有加成
        common_weapon = self.equip_system.create_random_equipment("weapon")
        common_weapon["rarity"] = "common"
        rarity_bonus = game_config.ENCHANTMENT_RARITY_BONUS["common"]
        self.assertEqual(rarity_bonus, 0.0)
        
    def test_already_enchanted_equipment(self):
        """测试已附魔装备"""
        # 创建一个武器并附魔
        weapon = self.equip_system.create_random_equipment("weapon")
        weapon["enchantment"] = "flame_enchantment"
        self.game.equipment["weapon"] = weapon
        
        # 尝试再次附魔应该失败
        with unittest.mock.patch('builtins.input', return_value='y'):
            result = self.equip_system.enchant_equipment("weapon", "frost_enchantment")
            self.assertFalse(result)
            
    def test_insufficient_gold_for_enchantment(self):
        """测试金币不足时的附魔"""
        # 创建一个武器
        weapon = self.equip_system.create_random_equipment("weapon")
        self.game.equipment["weapon"] = weapon
        
        # 设置金币为不足的数量
        self.game.hero_gold = 100
        
        # 尝试附魔应该失败
        with unittest.mock.patch('builtins.input', return_value='y'):
            result = self.equip_system.enchant_equipment("weapon", "flame_enchantment")
            self.assertFalse(result)
            
        # 验证金币没有扣除
        self.assertEqual(self.game.hero_gold, 100)
        
    def test_successful_enchantment(self):
        """测试成功附魔"""
        # 创建一个武器
        weapon = self.equip_system.create_random_equipment("weapon")
        self.game.equipment["weapon"] = weapon
        
        # 设置足够金币
        self.game.hero_gold = 1000
        
        # 模拟100%成功率的附魔
        import game_config
        with unittest.mock.patch('builtins.input', return_value='y'):
            with unittest.mock.patch('random.random', return_value=0.0):  # 确保成功
                result = self.equip_system.enchant_equipment("weapon", "flame_enchantment")
                self.assertTrue(result)
        
        # 验证附魔效果
        self.assertEqual(weapon["enchantment"], "flame_enchantment")
        self.assertEqual(weapon["fire_damage_percent"], 0.1)
        self.assertIn("fire_damage", weapon["special_effects"])
        
        # 验证金币扣除
        self.assertEqual(self.game.hero_gold, 700)  # 1000 - 300 = 700
        
        # 验证统计记录
        self.assertEqual(self.game.statistics.enchantments_attempted, 1)
        self.assertEqual(self.game.statistics.enchantments_successful, 1)
        self.assertEqual(self.game.statistics.enchantments_by_type["flame_enchantment"], 1)
        
    def test_failed_enchantment(self):
        """测试附魔失败"""
        # 创建一个武器
        weapon = self.equip_system.create_random_equipment("weapon")
        self.game.equipment["weapon"] = weapon
        
        # 设置足够金币
        self.game.hero_gold = 1000
        
        # 模拟0%成功率的附魔
        import game_config
        with unittest.mock.patch('builtins.input', return_value='y'):
            with unittest.mock.patch('random.random', return_value=1.0):  # 确保失败
                result = self.equip_system.enchant_equipment("weapon", "flame_enchantment")
                self.assertFalse(result)
        
        # 验证装备没有附魔
        self.assertIsNone(weapon.get("enchantment"))
        
        # 验证金币扣除（即使失败也会扣除金币）
        self.assertEqual(self.game.hero_gold, 700)  # 1000 - 300 = 700
        
        # 验证统计记录
        self.assertEqual(self.game.statistics.enchantments_attempted, 1)
        self.assertEqual(self.game.statistics.enchantments_failed, 1)
        
    def test_enchantment_effects_application(self):
        """测试附魔效果应用"""
        # 测试不同附魔类型的效果
        import game_config
        
        test_cases = [
            ("flame_enchantment", {"fire_damage_percent": 0.1, "special_effects": ["fire_damage"]}),
            ("frost_enchantment", {"enemy_attack_reduction": 0.1, "special_effects": ["ice_damage"]}),
            ("poison_enchantment", {"poison_damage_per_turn": 0.05, "special_effects": ["poison"]}),
            ("holy_enchantment", {"undead_damage_bonus": 0.2, "healing_bonus": 0.15, "special_effects": ["healing", "light_damage"]}),
            ("shadow_enchantment", {"crit_rate_bonus": 0.1, "dodge_chance_bonus": 0.08, "special_effects": ["backstab", "shadow_power"]})
        ]
        
        for enchant_type, expected_effects in test_cases:
            with self.subTest(enchantment=enchant_type):
                # 创建一个武器
                weapon = self.equip_system.create_random_equipment("weapon")
                self.game.equipment["weapon"] = weapon
                self.game.hero_gold = 1000
                
                # 模拟成功附魔
                with unittest.mock.patch('builtins.input', return_value='y'):
                    with unittest.mock.patch('random.random', return_value=0.0):
                        result = self.equip_system.enchant_equipment("weapon", enchant_type)
                        self.assertTrue(result)
                
                # 验证附魔类型
                self.assertEqual(weapon["enchantment"], enchant_type)
                
                # 验证所有效果都正确应用
                for effect_key, expected_value in expected_effects.items():
                    if effect_key != "special_effects":
                        self.assertEqual(weapon[effect_key], expected_value)
                
                # 验证特殊效果
                if "special_effects" in expected_effects:
                    for effect in expected_effects["special_effects"]:
                        self.assertIn(effect, weapon["special_effects"])
                        
    def test_enchantment_display(self):
        """测试附魔装备显示"""
        # 创建一个武器
        weapon = self.equip_system.create_random_equipment("weapon")
        
        # 测试无附魔的显示
        display = self.equip_system.get_enchantment_display(weapon)
        self.assertEqual(display, weapon["name"])
        
        # 测试有附魔的显示
        weapon["enchantment"] = "flame_enchantment"
        display = self.equip_system.get_enchantment_display(weapon)
        self.assertIn("火焰附魔", display)
        
    def test_enchantment_menu_functions(self):
        """测试附魔菜单功能"""
        # 这里我们只测试方法存在和可调用
        # 实际的UI测试需要人工验证
        self.assertTrue(hasattr(self.equip_system, 'enchant_equipment_menu'))
        self.assertTrue(callable(getattr(self.equip_system, 'enchant_equipment_menu')))
        
        self.assertTrue(hasattr(self.equip_system, 'show_enchantment_options'))
        self.assertTrue(callable(getattr(self.equip_system, 'show_enchantment_options')))


if __name__ == '__main__':
    unittest.main()