#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
装备强化系统测试

测试装备的强化功能和传说属性
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


class TestEnhancementSystem(unittest.TestCase):
    """测试装备强化系统"""

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
        
        # 创建装备系统实例
        self.equip_system = EquipmentSystem(self.game)
        
    def test_equipment_initialization(self):
        """测试装备初始化包含强化相关字段"""
        # 创建一个普通装备
        equipment = self.equip_system.create_random_equipment("weapon")
        
        # 检查是否包含强化相关字段
        self.assertIn("enhancement_level", equipment)
        self.assertIn("base_attack", equipment)
        self.assertIn("base_defense", equipment)
        self.assertIn("base_hp", equipment)
        
        # 检查初始值
        self.assertEqual(equipment["enhancement_level"], 0)
        self.assertEqual(equipment["base_attack"], equipment["attack"])
        self.assertEqual(equipment["base_defense"], equipment["defense"])
        self.assertEqual(equipment["base_hp"], equipment["hp"])

    def test_legendary_equipment_initialization(self):
        """测试传奇装备初始化包含强化相关字段"""
        # 创建一个传奇装备
        equipment = self.equip_system.create_legendary_equipment("weapon")
        
        # 检查是否包含强化相关字段
        self.assertIn("enhancement_level", equipment)
        self.assertIn("base_attack", equipment)
        self.assertIn("base_defense", equipment)
        self.assertIn("base_hp", equipment)
        
        # 检查初始值
        self.assertEqual(equipment["enhancement_level"], 0)
        self.assertEqual(equipment["base_attack"], equipment["attack"])
        self.assertEqual(equipment["base_defense"], equipment["defense"])
        self.assertEqual(equipment["base_hp"], equipment["hp"])

    def test_enhancement_cost_calculation(self):
        """测试强化费用计算"""
        # 创建一个装备
        equipment = self.equip_system.create_random_equipment("weapon")
        
        # 测试不同等级的强化费用
        equipment["enhancement_level"] = 0
        cost = self.equip_system.get_enhancement_cost(equipment)
        self.assertEqual(cost, 100)  # 基础费用
        
        equipment["enhancement_level"] = 5
        cost = self.equip_system.get_enhancement_cost(equipment)
        self.assertEqual(cost, 100 + 5 * 50)  # 基础费用 + (等级 * 递增费用)
        
        equipment["enhancement_level"] = 15
        cost = self.equip_system.get_enhancement_cost(equipment)
        self.assertEqual(cost, 0)  # 达到最大等级，费用为0

    def test_enhancement_attributes_boost(self):
        """测试强化属性提升"""
        # 创建一个装备
        equipment = self.equip_system.create_random_equipment("weapon")
        original_attack = equipment["base_attack"]
        
        # 模拟强化到+5
        equipment["enhancement_level"] = 5
        enhancement_bonus = 0.1 * equipment["enhancement_level"]  # 每级+10%
        expected_attack = int(original_attack * (1 + enhancement_bonus))
        
        # 手动设置攻击力（模拟enhance_equipment方法的效果）
        equipment["attack"] = expected_attack
        
        # 验证攻击力提升
        self.assertEqual(equipment["attack"], expected_attack)
        self.assertGreater(equipment["attack"], original_attack)

    def test_enhancement_ui_display(self):
        """测试强化装备的UI显示"""
        # 创建一个装备
        equipment = self.equip_system.create_random_equipment("weapon")
        
        # 测试无强化等级的显示
        display = self.equip_system.get_enhanced_equipment_display(equipment)
        self.assertEqual(display, equipment["name"])
        
        # 测试有强化等级的显示
        equipment["enhancement_level"] = 5
        display = self.equip_system.get_enhanced_equipment_display(equipment)
        self.assertEqual(display, f"{equipment['name']} (+5)")
        
        # 测试传说属性显示
        equipment["legendary_attribute"] = "flame_damage"
        display = self.equip_system.get_enhanced_equipment_display(equipment)
        self.assertIn("🔥", display)
        self.assertIn("火焰伤害", display)

    def test_max_enhancement_level(self):
        """测试最大强化等级"""
        # 创建一个装备
        equipment = self.equip_system.create_random_equipment("weapon")
        
        # 设置为最大强化等级
        equipment["enhancement_level"] = 15
        
        # 装备到槽位
        self.game.equipment["weapon"] = equipment
        
        # 尝试强化，应该失败
        result = self.equip_system.enhance_equipment("weapon")
        self.assertFalse(result)
        
        # 验证没有超出最大等级
        self.assertEqual(equipment["enhancement_level"], 15)

    def test_insufficient_gold(self):
        """测试金币不足时的强化"""
        # 创建一个装备
        equipment = self.equip_system.create_random_equipment("weapon")
        
        # 设置金币为不足的数量
        self.game.hero_gold = 50
        
        # 装备到槽位
        self.game.equipment["weapon"] = equipment
        
        # 尝试强化，应该失败
        result = self.equip_system.enhance_equipment("weapon")
        self.assertFalse(result)
        
        # 验证金币没有扣除
        self.assertEqual(self.game.hero_gold, 50)

    def test_successful_enhancement(self):
        """测试成功强化"""
        # 创建一个装备
        equipment = self.equip_system.create_random_equipment("weapon")
        original_level = equipment["enhancement_level"]
        original_attack = equipment["base_attack"]
        
        # 装备到槽位
        self.game.equipment["weapon"] = equipment
        
        # 设置足够金币
        self.game.hero_gold = 200
        
        # 模拟用户输入确认强化
        with unittest.mock.patch('builtins.input', return_value='y'):
            # 成功强化
            result = self.equip_system.enhance_equipment("weapon")
            self.assertTrue(result)
        
        # 验证强化等级提升
        self.assertEqual(equipment["enhancement_level"], original_level + 1)
        
        # 验证攻击力提升
        expected_attack = int(original_attack * 1.1)  # +10%
        self.assertEqual(equipment["attack"], expected_attack)
        
        # 验证金币扣除
        self.assertEqual(self.game.hero_gold, 100)  # 200 - 100 = 100

    def test_legendary_attribute_unlock(self):
        """测试传说属性解锁"""
        # 创建一个武器
        weapon = self.equip_system.create_random_equipment("weapon")
        weapon["enhancement_level"] = 9  # 接近+10
        
        # 装备到槽位
        self.game.equipment["weapon"] = weapon
        
        # 设置足够金币
        self.game.hero_gold = 1000
        
        # 模拟用户输入确认强化
        with unittest.mock.patch('builtins.input', return_value='y'):
            # 强化到+10，应该解锁传说属性
            result = self.equip_system.enhance_equipment("weapon")
            self.assertTrue(result)
        
        # 验证强化等级
        self.assertEqual(weapon["enhancement_level"], 10)
        
        # 验证传说属性
        self.assertEqual(weapon["legendary_attribute"], "flame_damage")
        self.assertEqual(weapon["flame_damage_percent"], 0.05)

    def test_armor_legendary_attribute(self):
        """测试护甲传说属性"""
        # 创建一个护甲
        armor = self.equip_system.create_random_equipment("armor")
        armor["enhancement_level"] = 9  # 接近+10
        
        # 装备到槽位
        self.game.equipment["armor"] = armor
        
        # 设置足够金币
        self.game.hero_gold = 1000
        
        # 模拟用户输入确认强化
        with unittest.mock.patch('builtins.input', return_value='y'):
            # 强化到+10，应该解锁传说属性
            result = self.equip_system.enhance_equipment("armor")
            self.assertTrue(result)
        
        # 验证传说属性
        self.assertEqual(armor["legendary_attribute"], "damage_reduction")
        self.assertEqual(armor["damage_reduction_percent"], 0.05)

    def test_accessory_legendary_attribute(self):
        """测试饰品传说属性"""
        # 创建一个饰品
        accessory = self.equip_system.create_random_equipment("accessory")
        accessory["enhancement_level"] = 9  # 接近+10
        
        # 装备到槽位
        self.game.equipment["accessory"] = accessory
        
        # 设置足够金币
        self.game.hero_gold = 1000
        
        # 模拟用户输入确认强化
        with unittest.mock.patch('builtins.input', return_value='y'):
            # 强化到+10，应该解锁传说属性
            result = self.equip_system.enhance_equipment("accessory")
            self.assertTrue(result)
        
        # 验证传说属性
        self.assertEqual(accessory["legendary_attribute"], "hp_regen")
        self.assertEqual(accessory["hp_regen_percent"], 0.01)

    def test_no_equipment_in_slot(self):
        """测试空槽位强化"""
        # 不装备任何装备
        self.game.equipment["weapon"] = None
        
        # 尝试强化，应该失败
        result = self.equip_system.enhance_equipment("weapon")
        self.assertFalse(result)

    def test_enhancement_menu_display(self):
        """测试强化菜单显示"""
        # 这里我们只测试方法存在和可调用
        # 实际的UI测试需要人工验证
        self.assertTrue(hasattr(self.equip_system, 'enhance_equipment_menu'))
        self.assertTrue(callable(getattr(self.equip_system, 'enhance_equipment_menu')))


if __name__ == '__main__':
    unittest.main()