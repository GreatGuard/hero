# -*- coding: utf-8 -*-
"""
装备系统测试
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# 添加项目路径
project_root = os.path.join(os.path.dirname(__file__), '..')
src_path = os.path.join(project_root, 'src')
hero_path = os.path.join(src_path, 'hero')
sys.path.insert(0, hero_path)
sys.path.insert(0, src_path)

from hero.equipment import EquipmentSystem
from hero.main import HeroGame


class TestEquipmentSystem(unittest.TestCase):
    """测试装备系统"""
    
    def setUp(self):
        """测试数据准备"""
        # 创建模拟游戏对象
        self.mock_game = Mock(spec=HeroGame)
        self.mock_game.hero_attack = 20
        self.mock_game.hero_defense = 5
        self.mock_game.hero_max_hp = 100
        self.mock_game.hero_hp = 100
        self.mock_game.base_attack = 20
        self.mock_game.base_defense = 5
        self.mock_game.base_max_hp = 100
        self.mock_game.equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        self.mock_game.inventory = []
        self.mock_game.hero_gold = 100
        self.mock_game.lang = Mock()
        self.mock_game.lang.get_text.return_value = "test_text"
        self.mock_game.lang.format_text.return_value = "formatted_text"
        
        # 创建装备系统实例
        self.equipment_system = EquipmentSystem(self.mock_game)
    
    def test_equipment_system_initialization(self):
        """测试装备系统初始化"""
        self.assertEqual(self.equipment_system.game, self.mock_game)
        self.assertIsInstance(self.equipment_system.weapons, dict)
        self.assertIsInstance(self.equipment_system.armors, dict)
        self.assertIsInstance(self.equipment_system.accessories, dict)
        self.assertGreater(len(self.equipment_system.weapons), 0)
        self.assertGreater(len(self.equipment_system.armors), 0)
        self.assertGreater(len(self.equipment_system.accessories), 0)
    
    def test_equipment_generation(self):
        """测试装备生成"""
        weapon = self.equipment_system.generate_equipment("weapon")
        armor = self.equipment_system.generate_equipment("armor")
        accessory = self.equipment_system.generate_equipment("accessory")
        
        # 验证武器属性
        self.assertIn("name", weapon)
        self.assertIn("type", weapon)
        self.assertIn("attack", weapon)
        self.assertIn("defense", weapon)
        self.assertIn("hp", weapon)
        self.assertIn("value", weapon)
        self.assertEqual(weapon["type"], "weapon")
        self.assertGreater(weapon["attack"], 0)
        
        # 验证防具属性
        self.assertEqual(armor["type"], "armor")
        self.assertGreater(armor["defense"], 0)
        
        # 验证饰品属性
        self.assertEqual(accessory["type"], "accessory")
    
    def test_equipping_item(self):
        """测试装备物品"""
        # 创建测试武器
        weapon = {
            "name": "TestSword",
            "type": "weapon",
            "attack": 10,
            "defense": 0,
            "hp": 0,
            "value": 50
        }
        
        # 装备武器
        original_attack = self.mock_game.hero_attack
        self.equipment_system.equip_item(weapon)
        
        # 验证装备效果
        self.assertEqual(self.mock_game.equipment["weapon"]["name"], "TestSword")
        self.assertEqual(self.mock_game.hero_attack, original_attack + 10)
    
    def test_equipping_armor(self):
        """测试装备防具"""
        # 创建测试防具
        armor = {
            "name": "TestArmor",
            "type": "armor",
            "attack": 0,
            "defense": 5,
            "hp": 20,
            "value": 75
        }
        
        # 装备防具
        original_defense = self.mock_game.hero_defense
        original_max_hp = self.mock_game.hero_max_hp
        self.equipment_system.equip_item(armor)
        
        # 验证装备效果
        self.assertEqual(self.mock_game.equipment["armor"]["name"], "TestArmor")
        self.assertEqual(self.mock_game.hero_defense, original_defense + 5)
        self.assertEqual(self.mock_game.hero_max_hp, original_max_hp + 20)
    
    def test_equipping_accessory(self):
        """测试装备饰品"""
        # 创建测试饰品
        accessory = {
            "name": "TestRing",
            "type": "accessory",
            "attack": 5,
            "defense": 2,
            "hp": 10,
            "value": 100
        }
        
        # 装备饰品
        original_attack = self.mock_game.hero_attack
        original_defense = self.mock_game.hero_defense
        original_max_hp = self.mock_game.hero_max_hp
        self.equipment_system.equip_item(accessory)
        
        # 验证装备效果
        self.assertEqual(self.mock_game.equipment["accessory"]["name"], "TestRing")
        self.assertEqual(self.mock_game.hero_attack, original_attack + 5)
        self.assertEqual(self.mock_game.hero_defense, original_defense + 2)
        self.assertEqual(self.mock_game.hero_max_hp, original_max_hp + 10)
    
    def test_unequipping_item(self):
        """测试卸下装备"""
        # 先装备一个物品
        weapon = {
            "name": "TestSword",
            "type": "weapon",
            "attack": 10,
            "defense": 0,
            "hp": 0,
            "value": 50
        }
        self.equipment_system.equip_item(weapon)
        
        # 卸下装备
        original_attack = self.mock_game.hero_attack
        self.equipment_system.unequip_item("weapon")
        
        # 验证卸下效果
        self.assertIsNone(self.mock_game.equipment["weapon"])
        self.assertEqual(self.mock_game.hero_attack, original_attack - 10)
    
    def test_attribute_calculation(self):
        """测试属性计算"""
        # 装备多个物品
        weapon = {"name": "Sword", "type": "weapon", "attack": 10, "defense": 0, "hp": 0, "value": 50}
        armor = {"name": "Armor", "type": "armor", "attack": 0, "defense": 5, "hp": 20, "value": 75}
        accessory = {"name": "Ring", "type": "accessory", "attack": 5, "defense": 2, "hp": 10, "value": 100}
        
        # 装备物品
        self.equipment_system.equip_item(weapon)
        self.equipment_system.equip_item(armor)
        self.equipment_system.equip_item(accessory)
        
        # 验证属性计算
        self.assertEqual(self.mock_game.hero_attack, 
                        self.mock_game.base_attack + 10 + 5)  # 基础+武器+饰品
        self.assertEqual(self.mock_game.hero_defense, 
                        self.mock_game.base_defense + 5 + 2)  # 基础+防具+饰品
        self.assertEqual(self.mock_game.hero_max_hp, 
                        self.mock_game.base_max_hp + 20 + 10)  # 基础+防具+饰品
    
    def test_hp_adjustment_after_max_hp_increase(self):
        """测试最大血量增加时的血量调整"""
        # 记录当前血量和最大血量
        current_hp = self.mock_game.hero_hp
        current_max_hp = self.mock_game.hero_max_hp
        
        # 装备增加血量的防具
        armor = {"name": "Armor", "type": "armor", "attack": 0, "defense": 5, "hp": 20, "value": 75}
        self.equipment_system.equip_item(armor)
        
        # 验证血量按比例增加
        expected_hp = int(current_hp * (current_max_hp + 20) / current_max_hp)
        self.assertEqual(self.mock_game.hero_hp, expected_hp)
        self.assertEqual(self.mock_game.hero_max_hp, current_max_hp + 20)
    
    def test_equipment_management_menu(self):
        """测试装备管理菜单"""
        # 模拟装备管理过程
        with patch('builtins.input', side_effect=['1', '1', '4']):  # 选择武器，装备第一件，退出
            with patch.object(self.equipment_system, 'show_equipment_list'):
                with patch.object(self.equipment_system, 'select_equipment_to_equip', return_value=0):
                    with patch.object(self.equipment_system, 'equip_item'):
                        with patch.object(self.equipment_system, 'show_hero_status'):
                            result = self.equipment_system.equipment_management()
        
        # 验证菜单正常退出
        self.assertTrue(True)  # 如果没有异常，说明测试通过
    
    def test_add_to_inventory(self):
        """测试添加物品到背包"""
        item = {"name": "TestItem", "value": 50}
        
        initial_count = len(self.mock_game.inventory)
        self.equipment_system.add_to_inventory(item)
        
        # 验证物品添加成功
        self.assertEqual(len(self.mock_game.inventory), initial_count + 1)
        self.assertIn(item, self.mock_game.inventory)
    
    def test_remove_from_inventory(self):
        """测试从背包移除物品"""
        item = {"name": "TestItem", "value": 50}
        self.mock_game.inventory.append(item)
        
        initial_count = len(self.mock_game.inventory)
        self.equipment_system.remove_from_inventory(item)
        
        # 验证物品移除成功
        self.assertEqual(len(self.mock_game.inventory), initial_count - 1)
        self.assertNotIn(item, self.mock_game.inventory)
    
    def test_find_equipment_event(self):
        """测试发现装备事件"""
        initial_equipment_count = sum(1 for eq in self.mock_game.inventory 
                                     if "type" in eq and eq["type"] in ["weapon", "armor", "accessory"])
        
        # 执行发现装备事件
        with patch('random.random', return_value=0.2):  # 20%概率，确保发现装备
            self.equipment_system.find_equipment()
        
        # 验证发现了装备
        new_equipment_count = sum(1 for eq in self.mock_game.inventory 
                                 if "type" in eq and eq["type"] in ["weapon", "armor", "accessory"])
        self.assertGreater(new_equipment_count, initial_equipment_count)


if __name__ == '__main__':
    unittest.main()