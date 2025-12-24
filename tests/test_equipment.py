# -*- coding: utf-8 -*-
"""
装备系统测试 - 基于实际接口重写
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch
from io import StringIO

# 添加项目路径
project_root = os.path.join(os.path.dirname(__file__), '..')
src_path = os.path.join(project_root, 'src')
hero_path = os.path.join(src_path, 'hero')
sys.path.insert(0, hero_path)
sys.path.insert(0, src_path)

from hero.equipment import EquipmentSystem


class TestEquipmentSystem(unittest.TestCase):
    """测试装备系统"""
    
    def setUp(self):
        """测试数据准备"""
        # 创建模拟游戏对象
        self.mock_game = Mock()
        self.mock_game.hero_attack = 20
        self.mock_game.hero_defense = 5
        self.mock_game.hero_max_hp = 100
        self.mock_game.hero_hp = 100
        self.mock_game.base_attack = 20
        self.mock_game.base_defense = 5
        self.mock_game.base_max_hp = 100
        self.mock_game.hero_level = 1
        self.mock_game.hero_gold = 100
        self.mock_game.hero_potions = 2
        self.mock_game.hero_skills = []
        self.mock_game.language = "zh"
        self.mock_game.inventory = []
        self.mock_game.equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        self.mock_game.events_encountered = []
        self.mock_game.lang = Mock()
        self.mock_game.lang.get_text.return_value = "test_text"
        self.mock_game.lang.format_text.return_value = "formatted_text"
        self.mock_game.clear_screen = Mock()
        self.mock_game.update_attributes = Mock()
        self.mock_game.difficulty_settings = {
            "normal": {
                "enemy_multiplier": 1.0
            }
        }
        self.mock_game.difficulty = "normal"
        
        # 创建装备系统实例
        self.equipment_system = EquipmentSystem(self.mock_game)
    
    def test_equipment_system_initialization(self):
        """测试装备系统初始化"""
        self.assertEqual(self.equipment_system.game, self.mock_game)
        self.assertIsInstance(self.equipment_system.equipment_database, dict)
        self.assertIn("weapon", self.equipment_system.equipment_database)
        self.assertIn("armor", self.equipment_system.equipment_database)
        self.assertIn("accessory", self.equipment_system.equipment_database)
    
    def test_create_random_equipment(self):
        """测试创建随机装备"""
        # 创建武器
        weapon = self.equipment_system.create_random_equipment("weapon")
        self.assertIn("name", weapon)
        self.assertIn("type", weapon)
        self.assertIn("rarity", weapon)
        self.assertIn("attack", weapon)
        self.assertIn("defense", weapon)
        self.assertIn("hp", weapon)
        self.assertEqual(weapon["type"], "weapon")
        self.assertGreater(weapon["attack"], 0)
        
        # 创建防具
        armor = self.equipment_system.create_random_equipment("armor")
        self.assertEqual(armor["type"], "armor")
        self.assertGreater(armor["defense"], 0)
        self.assertGreater(armor["hp"], 0)
        
        # 创建饰品
        accessory = self.equipment_system.create_random_equipment("accessory")
        self.assertEqual(accessory["type"], "accessory")
        self.assertGreaterEqual(accessory["attack"], 0)
        self.assertGreaterEqual(accessory["defense"], 0)
        self.assertGreaterEqual(accessory["hp"], 0)
    
    def test_create_random_equipment_without_type(self):
        """测试不指定类型时创建随机装备"""
        # 多次调用以确保覆盖所有类型
        types_created = set()
        for _ in range(10):
            item = self.equipment_system.create_random_equipment()
            types_created.add(item["type"])
        
        # 应该至少覆盖2种类型
        self.assertGreaterEqual(len(types_created), 2)
    
    def test_equip_item_success(self):
        """测试成功装备物品"""
        # 添加一个物品到背包
        weapon = self.equipment_system.create_random_equipment("weapon")
        self.mock_game.inventory.append(weapon)
        
        # 装备该物品
        item_index = 0
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            self.equipment_system.equip_item(item_index)
        finally:
            sys.stdout = old_stdout
        
        # 验证装备效果
        self.assertEqual(self.mock_game.equipment["weapon"]["name"], weapon["name"])
        self.assertEqual(len(self.mock_game.inventory), 0)  # 物品从背包移除
        self.mock_game.update_attributes.assert_called_once()
    
    def test_equip_item_with_existing_equipment(self):
        """测试装备已有装备的槽位"""
        # 先装备一个武器
        old_weapon = self.equipment_system.create_random_equipment("weapon")
        self.mock_game.equipment["weapon"] = old_weapon
        
        # 添加新武器到背包
        new_weapon = self.equipment_system.create_random_equipment("weapon")
        self.mock_game.inventory.append(new_weapon)
        
        # 装备新武器
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            self.equipment_system.equip_item(0)
        finally:
            sys.stdout = old_stdout
        
        # 验证新武器被装备，旧武器返回背包
        self.assertEqual(self.mock_game.equipment["weapon"]["name"], new_weapon["name"])
        self.assertIn(old_weapon, self.mock_game.inventory)
        self.assertNotIn(new_weapon, self.mock_game.inventory)
    
    def test_equip_item_invalid_index(self):
        """测试无效索引"""
        # 空背包
        self.mock_game.inventory = []
        
        # 尝试装备无效索引
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            self.equipment_system.equip_item(0)
        finally:
            sys.stdout = old_stdout
        
        # 验证没有装备
        self.assertIsNone(self.mock_game.equipment["weapon"])
        self.mock_game.update_attributes.assert_not_called()
    
    def test_unequip_item_success(self):
        """测试成功卸下装备"""
        # 先装备一个武器
        weapon = self.equipment_system.create_random_equipment("weapon")
        self.mock_game.equipment["weapon"] = weapon
        
        # 卸下装备
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            self.equipment_system.unequip_item("weapon")
        finally:
            sys.stdout = old_stdout
        
        # 验证卸下效果
        self.assertIsNone(self.mock_game.equipment["weapon"])
        self.assertIn(weapon, self.mock_game.inventory)
        self.mock_game.update_attributes.assert_called_once()
    
    def test_unequip_item_no_equipment(self):
        """测试卸下空槽位"""
        # 清空装备
        self.mock_game.equipment["weapon"] = None
        
        # 尝试卸下
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            self.equipment_system.unequip_item("weapon")
        finally:
            sys.stdout = old_stdout
        
        # 验证没有变化
        self.assertIsNone(self.mock_game.equipment["weapon"])
        self.assertEqual(len(self.mock_game.inventory), 0)
    
    def test_find_equipment(self):
        """测试发现装备"""
        # 调用发现装备
        initial_inventory_count = len(self.mock_game.inventory)
        
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            self.equipment_system.find_equipment()
        finally:
            sys.stdout = old_stdout
        
        # 验证装备被添加到背包
        self.assertEqual(len(self.mock_game.inventory), initial_inventory_count + 1)
        # 验证事件被记录
        self.assertEqual(len(self.mock_game.events_encountered), 1)
    
    def test_equipment_management_exists(self):
        """测试装备管理界面存在"""
        self.assertTrue(hasattr(self.equipment_system, 'equipment_management'))
        self.assertTrue(callable(self.equipment_system.equipment_management))
    
    def test_equipment_shop_exists(self):
        """测试装备商店存在"""
        self.assertTrue(hasattr(self.equipment_system, 'equipment_shop'))
        self.assertTrue(callable(self.equipment_system.equipment_shop))
    
    def test_show_inventory_empty(self):
        """测试显示空背包"""
        self.mock_game.inventory = []
        
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            self.equipment_system.show_inventory()
        finally:
            sys.stdout = old_stdout
        
        output = captured_output.getvalue()
        # 验证显示空背包
        self.assertTrue(len(output) > 0)
    
    def test_show_inventory_with_items(self):
        """测试显示有物品的背包"""
        # 添加物品到背包
        weapon = self.equipment_system.create_random_equipment("weapon")
        armor = self.equipment_system.create_random_equipment("armor")
        self.mock_game.inventory = [weapon, armor]
        
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            self.equipment_system.show_inventory()
        finally:
            sys.stdout = old_stdout
        
        output = captured_output.getvalue()
        # 验证显示内容
        self.assertTrue(len(output) > 0)
        self.assertIn(weapon["name"], output)
        self.assertIn(armor["name"], output)
    
    def test_rarity_system(self):
        """测试稀有度系统"""
        # 测试get_rarity_name
        self.mock_game.lang.get_text.return_value = "Common"
        rarity_name = self.equipment_system.get_rarity_name("common")
        self.assertEqual(rarity_name, "Common")
        
        # 测试get_rarity_color
        color = self.equipment_system.get_rarity_color("common")
        self.assertIsInstance(color, str)
        
        # 测试所有稀有度
        rarities = ["common", "uncommon", "rare", "epic", "legendary"]
        for rarity in rarities:
            with self.subTest(rarity=rarity):
                color = self.equipment_system.get_rarity_color(rarity)
                self.assertIsInstance(color, str)


if __name__ == '__main__':
    unittest.main()
