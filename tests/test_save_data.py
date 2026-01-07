#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试存档数据模块
"""

import unittest
import os
import sys
import json
import tempfile
import shutil

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'hero'))

from save_data import SaveData, SaveManager
from main import HeroGame


class TestSaveData(unittest.TestCase):
    """测试SaveData类"""

    def setUp(self):
        """测试前准备"""
        # 创建临时目录用于存档测试
        self.temp_dir = tempfile.mkdtemp()
        self.save_manager = SaveManager(save_dir=self.temp_dir)

    def tearDown(self):
        """测试后清理"""
        # 删除临时目录
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_save_data_creation(self):
        """测试SaveData创建"""
        # 创建一个模拟的游戏对象
        game = self._create_mock_game()

        # 从游戏创建SaveData
        save_data = SaveData(game)

        # 验证基本属性
        self.assertEqual(save_data.hero_name, "TestHero")
        self.assertEqual(save_data.hero_level, 5)
        self.assertEqual(save_data.hero_hp, 80)
        self.assertEqual(save_data.hero_max_hp, 200)
        self.assertEqual(save_data.difficulty, "normal")
        self.assertEqual(save_data.map_type, "forest")

    def test_save_data_to_dict(self):
        """测试SaveData转换为字典"""
        game = self._create_mock_game()
        save_data = SaveData(game)

        # 转换为字典
        data_dict = save_data.to_dict()

        # 验证字典包含所有必需字段
        self.assertIn("hero_name", data_dict)
        self.assertIn("hero_level", data_dict)
        self.assertIn("hero_hp", data_dict)
        self.assertIn("difficulty", data_dict)
        self.assertIn("map_type", data_dict)
        self.assertIn("equipment", data_dict)
        self.assertIn("inventory", data_dict)
        self.assertIn("statistics_data", data_dict)

        # 验证值正确
        self.assertEqual(data_dict["hero_name"], "TestHero")
        self.assertEqual(data_dict["hero_level"], 5)

    def test_save_data_from_dict(self):
        """测试从字典创建SaveData"""
        data_dict = {
            "hero_name": "TestHero2",
            "hero_level": 10,
            "hero_hp": 150,
            "hero_max_hp": 300,
            "hero_attack": 50,
            "hero_defense": 20,
            "base_attack": 30,
            "base_defense": 10,
            "base_max_hp": 200,
            "hero_position": 25,
            "game_over": False,
            "victory": False,
            "hero_gold": 500,
            "hero_potions": 5,
            "equipment": {
                "weapon": {"name": "TestWeapon", "type": "weapon", "rarity": "rare"},
                "armor": None,
                "accessory": None
            },
            "inventory": [],
            "hero_skills": ["火球术"],
            "difficulty": "hard",
            "map_type": "mountain",
            "language": "zh",
            "map_length": 100,
            "monsters_defeated": 50,
            "events_encountered": [],
            "visited_positions": [],
            "statistics_data": {}
        }

        # 从字典创建SaveData
        save_data = SaveData.from_dict(data_dict)

        # 验证数据正确
        self.assertEqual(save_data.hero_name, "TestHero2")
        self.assertEqual(save_data.hero_level, 10)
        self.assertEqual(save_data.difficulty, "hard")
        self.assertEqual(save_data.map_type, "mountain")

    def test_save_data_roundtrip(self):
        """测试SaveData往返转换"""
        game = self._create_mock_game()
        save_data1 = SaveData(game)

        # 转换为字典再转回
        data_dict = save_data1.to_dict()
        save_data2 = SaveData.from_dict(data_dict)

        # 验证数据一致性
        self.assertEqual(save_data1.hero_name, save_data2.hero_name)
        self.assertEqual(save_data1.hero_level, save_data2.hero_level)
        self.assertEqual(save_data1.hero_hp, save_data2.hero_hp)
        self.assertEqual(save_data1.difficulty, save_data2.difficulty)
        self.assertEqual(save_data1.map_type, save_data2.map_type)

    def test_save_game_and_load(self):
        """测试保存和加载游戏"""
        game = self._create_mock_game()
        save_data = SaveData(game)

        # 保存游戏
        success = self.save_manager.save_game(save_data, 1)
        self.assertTrue(success)

        # 验证文件已创建
        save_path = self.save_manager.get_save_path(1)
        self.assertTrue(os.path.exists(save_path))

        # 加载游戏
        loaded_save_data = self.save_manager.load_game(1)
        self.assertIsNotNone(loaded_save_data)

        # 验证加载的数据
        self.assertEqual(loaded_save_data.hero_name, save_data.hero_name)
        self.assertEqual(loaded_save_data.hero_level, save_data.hero_level)

    def test_save_multiple_slots(self):
        """测试多个存档槽位"""
        game1 = self._create_mock_game("Hero1", 1)
        game2 = self._create_mock_game("Hero2", 2)

        save_data1 = SaveData(game1)
        save_data2 = SaveData(game2)

        # 保存到不同槽位
        self.assertTrue(self.save_manager.save_game(save_data1, 1))
        self.assertTrue(self.save_manager.save_game(save_data2, 2))

        # 加载并验证
        loaded1 = self.save_manager.load_game(1)
        loaded2 = self.save_manager.load_game(2)

        self.assertEqual(loaded1.hero_name, "Hero1")
        self.assertEqual(loaded2.hero_name, "Hero2")

    def test_list_save_slots(self):
        """测试列出存档槽位"""
        # 保存一些游戏
        game1 = self._create_mock_game("Hero1", 1)
        game2 = self._create_mock_game("Hero2", 2)

        self.save_manager.save_game(SaveData(game1), 1)
        self.save_manager.save_game(SaveData(game2), 3)

        # 列出存档
        slots = self.save_manager.list_save_slots()

        # 验证槽位信息
        self.assertEqual(len(slots), 5)  # 5个槽位
        self.assertFalse(slots[0].get("empty"))  # 槽位1有存档
        self.assertTrue(slots[1].get("empty"))  # 槽位2为空
        self.assertFalse(slots[2].get("empty"))  # 槽位3有存档
        self.assertTrue(slots[3].get("empty"))  # 槽位4为空
        self.assertTrue(slots[4].get("empty"))  # 槽位5为空

    def test_delete_save(self):
        """测试删除存档"""
        game = self._create_mock_game()
        save_data = SaveData(game)

        # 保存游戏
        self.assertTrue(self.save_manager.save_game(save_data, 1))

        # 删除存档
        success = self.save_manager.delete_save(1)
        self.assertTrue(success)

        # 验证文件已删除
        save_path = self.save_manager.get_save_path(1)
        self.assertFalse(os.path.exists(save_path))

        # 验证加载返回None
        loaded = self.save_manager.load_game(1)
        self.assertIsNone(loaded)

    def test_load_nonexistent_slot(self):
        """测试加载不存在的槽位"""
        loaded = self.save_manager.load_game(99)
        self.assertIsNone(loaded)

    def test_save_slot_range_validation(self):
        """测试槽位号范围验证"""
        game = self._create_mock_game()
        save_data = SaveData(game)

        # 测试无效槽位号
        with self.assertRaises(ValueError):
            self.save_manager.save_game(save_data, 0)

        with self.assertRaises(ValueError):
            self.save_manager.save_game(save_data, 6)

    def _create_mock_game(self, hero_name="TestHero", hero_level=5):
        """创建模拟的游戏对象"""
        class MockGame:
            def __init__(self, name, level):
                self.hero_name = name
                self.hero_level = level
                self.hero_exp = level * 100
                self.hero_hp = 80
                self.hero_max_hp = 200
                self.hero_attack = 40
                self.hero_defense = 15
                self.base_attack = 30
                self.base_defense = 10
                self.base_max_hp = 150
                self.hero_position = 10
                self.game_over = False
                self.victory = False
                self.hero_gold = 300
                self.hero_potions = 3
                self.equipment = {
                    "weapon": {"name": "Iron Sword", "type": "weapon", "rarity": "common"},
                    "armor": None,
                    "accessory": None
                }
                self.inventory = [
                    {"name": "Potion", "type": "consumable"},
                    {"name": "Shield", "type": "armor", "rarity": "uncommon"}
                ]
                self.hero_skills = ["火球术", "治疗术"]
                self.difficulty = "normal"
                self.map_type = "forest"
                self.language = "zh"
                self.map_length = 50
                self.monsters_defeated = 20
                self.events_encountered = ["Found treasure", "Defeated goblin"]
                self.visited_positions = [True, False, True] * 10 + [False] * 17
                self.statistics = None  # 简化测试，不包含统计

        return MockGame(hero_name, hero_level)


if __name__ == '__main__':
    unittest.main()
