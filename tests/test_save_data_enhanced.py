#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试存档系统增强版本 - 提高测试覆盖率
"""

import unittest
import sys
import os
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock, mock_open

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hero.save_data import SaveData, SaveManager


class TestSaveDataEnhanced(unittest.TestCase):
    """测试SaveData类增强版本"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建测试SaveData实例
        self.save_data = SaveData()
        
        # 设置基本属性
        self.save_data.hero_name = "测试英雄"
        self.save_data.hero_level = 5
        self.save_data.hero_xp = 250
        self.save_data.hero_xp_to_next_level = 500
        self.save_data.hero_hp = 80
        self.save_data.hero_max_hp = 100
        self.save_data.hero_attack = 25
        self.save_data.hero_defense = 15
        self.save_data.hero_gold = 200
        self.save_data.hero_potions = 4
        self.save_data.hero_class = "warrior"
        self.save_data.hero_skills = ["attack", "defend"]
        self.save_data.hero_equipment = {
            "weapon": {"name": "铁剑", "attack": 10},
            "armor": {"name": "皮甲", "defense": 5}
        }
        self.save_data.inventory = [
            {"name": "药水", "type": "potion"},
            {"name": "金币袋", "type": "accessory"}
        ]
        self.save_data.difficulty = "normal"
        self.save_data.map_type = "forest"
        self.save_data.current_position = 10
        self.save_data.map_length = 30
        self.save_data.language = "zh"
        self.save_data.status_effects = {"poison": 2}
        self.save_data.achievements = ["first_victory", "monster_hunter"]
        self.save_data.quest_progress = {"quest1": 50}
        self.save_data.skill_tree_data = {"attack": 2}
        self.save_data.game_settings = {"auto_save": True}
    
    def test_to_dict(self):
        """测试转换为字典"""
        data_dict = self.save_data.to_dict()
        
        # 验证字典包含所有必要字段
        self.assertIn("hero_name", data_dict)
        self.assertIn("hero_level", data_dict)
        self.assertIn("hero_xp", data_dict)
        self.assertIn("hero_hp", data_dict)
        self.assertIn("hero_gold", data_dict)
        self.assertIn("hero_class", data_dict)
        self.assertIn("hero_skills", data_dict)
        self.assertIn("hero_equipment", data_dict)
        self.assertIn("inventory", data_dict)
        self.assertIn("difficulty", data_dict)
        self.assertIn("map_type", data_dict)
        self.assertIn("language", data_dict)
        self.assertIn("status_effects", data_dict)
        self.assertIn("achievements", data_dict)
        self.assertIn("quest_progress", data_dict)
        self.assertIn("skill_tree_data", data_dict)
        self.assertIn("game_settings", data_dict)
        
        # 验证值
        self.assertEqual(data_dict["hero_name"], "测试英雄")
        self.assertEqual(data_dict["hero_level"], 5)
        self.assertEqual(data_dict["hero_xp"], 250)
        self.assertEqual(data_dict["hero_hp"], 80)
        self.assertEqual(data_dict["hero_gold"], 200)
        self.assertEqual(data_dict["hero_class"], "warrior")
        self.assertEqual(data_dict["difficulty"], "normal")
        self.assertEqual(data_dict["map_type"], "forest")
        self.assertEqual(data_dict["language"], "zh")
    
    def test_from_dict(self):
        """测试从字典创建"""
        data_dict = self.save_data.to_dict()
        new_save_data = SaveData.from_dict(data_dict)
        
        # 验证属性
        self.assertEqual(new_save_data.hero_name, "测试英雄")
        self.assertEqual(new_save_data.hero_level, 5)
        self.assertEqual(new_save_data.hero_xp, 250)
        self.assertEqual(new_save_data.hero_hp, 80)
        self.assertEqual(new_save_data.hero_gold, 200)
        self.assertEqual(new_save_data.hero_class, "warrior")
        self.assertEqual(new_save_data.difficulty, "normal")
        self.assertEqual(new_save_data.map_type, "forest")
        self.assertEqual(new_save_data.language, "zh")
        
        # 验证复杂对象
        self.assertEqual(new_save_data.hero_skills, ["attack", "defend"])
        self.assertEqual(new_save_data.hero_equipment["weapon"]["name"], "铁剑")
        self.assertEqual(new_save_data.hero_equipment["armor"]["name"], "皮甲")
        self.assertEqual(new_save_data.inventory[0]["name"], "药水")
        self.assertEqual(new_save_data.inventory[1]["name"], "金币袋")
        self.assertEqual(new_save_data.status_effects, {"poison": 2})
        self.assertEqual(new_save_data.achievements, ["first_victory", "monster_hunter"])
        self.assertEqual(new_save_data.quest_progress, {"quest1": 50})
        self.assertEqual(new_save_data.skill_tree_data, {"attack": 2})
        self.assertEqual(new_save_data.game_settings, {"auto_save": True})
    
    def test_from_dict_missing_fields(self):
        """测试从缺少字段的字典创建"""
        # 创建缺少字段的字典
        data_dict = {
            "hero_name": "测试英雄",
            "hero_level": 5
        }
        
        new_save_data = SaveData.from_dict(data_dict)
        
        # 验证存在的字段
        self.assertEqual(new_save_data.hero_name, "测试英雄")
        self.assertEqual(new_save_data.hero_level, 5)
        
        # 验证默认值
        self.assertEqual(new_save_data.hero_xp, 0)
        self.assertEqual(new_save_data.hero_hp, 0)
        self.assertEqual(new_save_data.hero_gold, 0)
        self.assertEqual(new_save_data.hero_class, "warrior")
        self.assertEqual(new_save_data.difficulty, "normal")
        self.assertEqual(new_save_data.map_type, "plains")
        self.assertEqual(new_save_data.language, "zh")
        self.assertEqual(new_save_data.hero_skills, [])
        self.assertEqual(new_save_data.hero_equipment, {})
        self.assertEqual(new_save_data.inventory, [])
        self.assertEqual(new_save_data.status_effects, {})
        self.assertEqual(new_save_data.achievements, [])
        self.assertEqual(new_save_data.quest_progress, {})
        self.assertEqual(new_save_data.skill_tree_data, {})
        self.assertEqual(new_save_data.game_settings, {})
    
    def test_from_dict_invalid_types(self):
        """测试从包含无效类型的字典创建"""
        # 创建包含无效类型的字典
        data_dict = {
            "hero_name": "测试英雄",
            "hero_level": 5,
            "hero_xp": "250",  # 字符串而不是数字
            "hero_hp": 80,
            "hero_gold": 200,
            "hero_class": "warrior",
            "hero_skills": "attack,defend",  # 字符串而不是列表
            "hero_equipment": "weapon:iron_sword",  # 字符串而不是字典
            "inventory": "potion,accessory",  # 字符串而不是列表
            "difficulty": "normal",
            "map_type": "forest",
            "language": "zh",
            "status_effects": "poison:2",  # 字符串而不是字典
            "achievements": "first_victory,monster_hunter",  # 字符串而不是列表
            "quest_progress": "quest1:50",  # 字符串而不是字典
            "skill_tree_data": "attack:2",  # 字符串而不是字典
            "game_settings": "auto_save:true"  # 字符串而不是字典
        }
        
        new_save_data = SaveData.from_dict(data_dict)
        
        # 验证基本字段
        self.assertEqual(new_save_data.hero_name, "测试英雄")
        self.assertEqual(new_save_data.hero_level, 5)
        
        # 验证类型转换
        self.assertEqual(new_save_data.hero_xp, 250)  # 字符串转数字
        self.assertEqual(new_save_data.hero_hp, 80)
        self.assertEqual(new_save_data.hero_gold, 200)
        
        # 验证复杂对象的类型处理
        self.assertEqual(new_save_data.hero_class, "warrior")
        self.assertEqual(new_save_data.difficulty, "normal")
        self.assertEqual(new_save_data.map_type, "forest")
        self.assertEqual(new_save_data.language, "zh")
        
        # 验证字符串分割
        self.assertEqual(new_save_data.hero_skills, ["attack", "defend"])
        self.assertEqual(new_save_data.achievements, ["first_victory", "monster_hunter"])
    
    def test_init_save_data(self):
        """测试SaveData初始化"""
        new_save_data = SaveData()
        
        # 验证默认值
        self.assertEqual(new_save_data.hero_name, "")
        self.assertEqual(new_save_data.hero_level, 1)
        self.assertEqual(new_save_data.hero_xp, 0)
        self.assertEqual(new_save_data.hero_xp_to_next_level, 100)
        self.assertEqual(new_save_data.hero_hp, 0)
        self.assertEqual(new_save_data.hero_max_hp, 0)
        self.assertEqual(new_save_data.hero_attack, 0)
        self.assertEqual(new_save_data.hero_defense, 0)
        self.assertEqual(new_save_data.hero_gold, 0)
        self.assertEqual(new_save_data.hero_potions, 0)
        self.assertEqual(new_save_data.hero_class, "warrior")
        self.assertEqual(new_save_data.hero_skills, [])
        self.assertEqual(new_save_data.hero_equipment, {})
        self.assertEqual(new_save_data.inventory, [])
        self.assertEqual(new_save_data.difficulty, "normal")
        self.assertEqual(new_save_data.map_type, "plains")
        self.assertEqual(new_save_data.current_position, 0)
        self.assertEqual(new_save_data.map_length, 30)
        self.assertEqual(new_save_data.language, "zh")
        self.assertEqual(new_save_data.status_effects, {})
        self.assertEqual(new_save_data.achievements, [])
        self.assertEqual(new_save_data.quest_progress, {})
        self.assertEqual(new_save_data.skill_tree_data, {})
        self.assertEqual(new_save_data.game_settings, {})
    
    def test_eq(self):
        """测试相等性比较"""
        # 创建相同的SaveData实例
        save_data1 = SaveData()
        save_data2 = SaveData()
        
        self.assertEqual(save_data1, save_data2)
        
        # 修改一个实例
        save_data1.hero_name = "英雄1"
        self.assertNotEqual(save_data1, save_data2)
        
        # 修改另一个实例以匹配
        save_data2.hero_name = "英雄1"
        self.assertEqual(save_data1, save_data2)
    
    def test_repr(self):
        """测试字符串表示"""
        self.save_data.hero_name = "测试英雄"
        self.save_data.hero_level = 5
        
        repr_str = repr(self.save_data)
        
        self.assertIn("SaveData", repr_str)
        self.assertIn("测试英雄", repr_str)
        self.assertIn("5", repr_str)


class TestSaveManagerEnhanced(unittest.TestCase):
    """测试SaveManager类增强版本"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建临时目录用于测试
        self.temp_dir = tempfile.mkdtemp()
        self.save_dir = os.path.join(self.temp_dir, "saves")
        os.makedirs(self.save_dir, exist_ok=True)
        
        # 创建SaveManager实例
        self.save_manager = SaveManager(save_dir=self.save_dir)
        
        # 创建测试SaveData
        self.save_data = SaveData()
        self.save_data.hero_name = "测试英雄"
        self.save_data.hero_level = 5
        self.save_data.hero_gold = 200
        self.save_data.hero_class = "warrior"
        self.save_data.difficulty = "normal"
        self.save_data.map_type = "forest"
    
    def tearDown(self):
        """清理测试环境"""
        # 删除临时目录
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_init_save_manager(self):
        """测试SaveManager初始化"""
        # 验证默认目录创建
        self.assertTrue(os.path.exists(self.save_dir))
        
        # 测试自定义目录
        custom_dir = os.path.join(self.temp_dir, "custom_saves")
        custom_manager = SaveManager(save_dir=custom_dir)
        self.assertTrue(os.path.exists(custom_dir))
    
    def test_get_save_path(self):
        """测试获取存档路径"""
        # 测试有效槽位
        save_path = self.save_manager.get_save_path(1)
        expected_path = os.path.join(self.save_dir, "save_slot_1.json")
        self.assertEqual(save_path, expected_path)
        
        # 测试无效槽位
        with self.assertRaises(ValueError):
            self.save_manager.get_save_path(0)
        
        with self.assertRaises(ValueError):
            self.save_manager.get_save_path(6)
    
    def test_save_game(self):
        """测试保存游戏"""
        # 保存游戏
        result = self.save_manager.save_game(self.save_data, 1)
        
        self.assertTrue(result)
        
        # 验证文件存在
        save_path = self.save_manager.get_save_path(1)
        self.assertTrue(os.path.exists(save_path))
        
        # 验证文件内容
        with open(save_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(data["hero_name"], "测试英雄")
            self.assertEqual(data["hero_level"], 5)
            self.assertEqual(data["hero_gold"], 200)
            self.assertEqual(data["hero_class"], "warrior")
    
    def test_save_game_invalid_slot(self):
        """测试保存游戏到无效槽位"""
        # 尝试保存到无效槽位
        with self.assertRaises(ValueError):
            self.save_manager.save_game(self.save_data, 0)
        
        with self.assertRaises(ValueError):
            self.save_manager.save_game(self.save_data, 6)
    
    @patch('builtins.open', side_effect=PermissionError("Permission denied"))
    def test_save_game_permission_error(self, mock_open):
        """测试保存游戏权限错误"""
        # 模拟权限错误
        result = self.save_manager.save_game(self.save_data, 1)
        
        self.assertFalse(result)
    
    @patch('builtins.open', side_effect=OSError("OS error"))
    def test_save_game_os_error(self, mock_open):
        """测试保存游戏系统错误"""
        # 模拟系统错误
        result = self.save_manager.save_game(self.save_data, 1)
        
        self.assertFalse(result)
    
    def test_load_game(self):
        """测试加载游戏"""
        # 先保存游戏
        self.save_manager.save_game(self.save_data, 1)
        
        # 加载游戏
        loaded_data = self.save_manager.load_game(1)
        
        # 验证加载的数据
        self.assertIsNotNone(loaded_data)
        self.assertEqual(loaded_data.hero_name, "测试英雄")
        self.assertEqual(loaded_data.hero_level, 5)
        self.assertEqual(loaded_data.hero_gold, 200)
        self.assertEqual(loaded_data.hero_class, "warrior")
        self.assertEqual(loaded_data.difficulty, "normal")
        self.assertEqual(loaded_data.map_type, "forest")
    
    def test_load_game_invalid_slot(self):
        """测试从无效槽位加载游戏"""
        # 尝试从无效槽位加载
        with self.assertRaises(ValueError):
            self.save_manager.load_game(0)
        
        with self.assertRaises(ValueError):
            self.save_manager.load_game(6)
    
    def test_load_game_file_not_exists(self):
        """测试加载不存在的存档"""
        # 加载不存在的存档
        loaded_data = self.save_manager.load_game(2)
        
        self.assertIsNone(loaded_data)
    
    def test_load_game_json_decode_error(self):
        """测试加载损坏的存档"""
        # 创建损坏的JSON文件
        save_path = self.save_manager.get_save_path(1)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write("{ invalid json content }")
        
        # 尝试加载
        loaded_data = self.save_manager.load_game(1)
        
        self.assertIsNone(loaded_data)
    
    @patch('builtins.open', side_effect=PermissionError("Permission denied"))
    def test_load_game_permission_error(self, mock_open):
        """测试加载游戏权限错误"""
        # 模拟权限错误
        loaded_data = self.save_manager.load_game(1)
        
        self.assertIsNone(loaded_data)
    
    @patch('builtins.open', side_effect=OSError("OS error"))
    def test_load_game_os_error(self, mock_open):
        """测试加载游戏系统错误"""
        # 模拟系统错误
        loaded_data = self.save_manager.load_game(1)
        
        self.assertIsNone(loaded_data)
    
    def test_load_game_corrupted_data(self):
        """测试加载损坏的数据"""
        # 先保存游戏
        self.save_manager.save_game(self.save_data, 1)
        
        # 手动损坏文件内容
        save_path = self.save_manager.get_save_path(1)
        with open(save_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            # 删除一个必要字段
            content = content.replace('"hero_name": "测试英雄",', '')
            f.seek(0)
            f.truncate()
            f.write(content)
        
        # 尝试加载
        loaded_data = self.save_manager.load_game(1)
        
        # 应该成功加载，但缺少的字段使用默认值
        self.assertIsNotNone(loaded_data)
        self.assertEqual(loaded_data.hero_name, "")  # 默认值
        self.assertEqual(loaded_data.hero_level, 5)  # 保留的字段
        self.assertEqual(loaded_data.hero_gold, 200)  # 保留的字段
    
    def test_list_save_slots(self):
        """测试列出存档槽位"""
        # 保存几个存档
        self.save_manager.save_game(self.save_data, 1)
        self.save_manager.save_game(self.save_data, 2)
        
        # 修改第二个存档的数据
        self.save_data.hero_name = "英雄2"
        self.save_data.hero_level = 10
        self.save_manager.save_game(self.save_data, 2)
        
        # 列出存档槽位
        save_slots = self.save_manager.list_save_slots()
        
        # 验证返回了5个槽位
        self.assertEqual(len(save_slots), 5)
        
        # 验证槽位1的摘要
        self.assertEqual(save_slots[0]["slot_number"], 1)
        self.assertEqual(save_slots[0]["exists"], True)
        self.assertEqual(save_slots[0]["hero_name"], "测试英雄")
        self.assertEqual(save_slots[0]["hero_level"], 5)
        self.assertEqual(save_slots[0]["hero_class"], "warrior")
        self.assertEqual(save_slots[0]["difficulty"], "normal")
        self.assertEqual(save_slots[0]["map_type"], "forest")
        
        # 验证槽位2的摘要
        self.assertEqual(save_slots[1]["slot_number"], 2)
        self.assertEqual(save_slots[1]["exists"], True)
        self.assertEqual(save_slots[1]["hero_name"], "英雄2")
        self.assertEqual(save_slots[1]["hero_level"], 10)
        
        # 验证空槽位
        self.assertEqual(save_slots[2]["slot_number"], 3)
        self.assertEqual(save_slots[2]["exists"], False)
        self.assertEqual(save_slots[2]["hero_name"], "")
        self.assertEqual(save_slots[2]["hero_level"], 0)
        
        # 验证空槽位
        self.assertEqual(save_slots[3]["slot_number"], 4)
        self.assertEqual(save_slots[3]["exists"], False)
        
        # 验证空槽位
        self.assertEqual(save_slots[4]["slot_number"], 5)
        self.assertEqual(save_slots[4]["exists"], False)
    
    def test_list_save_slots_corrupted_file(self):
        """测试列出存档槽位（包含损坏文件）"""
        # 保存一个正常存档
        self.save_manager.save_game(self.save_data, 1)
        
        # 创建一个损坏的存档文件
        save_path = self.save_manager.get_save_path(2)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write("{ invalid json content }")
        
        # 列出存档槽位
        save_slots = self.save_manager.list_save_slots()
        
        # 验证正常槽位
        self.assertEqual(save_slots[0]["slot_number"], 1)
        self.assertEqual(save_slots[0]["exists"], True)
        self.assertEqual(save_slots[0]["hero_name"], "测试英雄")
        
        # 验证损坏的槽位
        self.assertEqual(save_slots[1]["slot_number"], 2)
        self.assertEqual(save_slots[1]["exists"], False)
        self.assertEqual(save_slots[1]["hero_name"], "")
        self.assertEqual(save_slots[1]["hero_level"], 0)
    
    def test_delete_save(self):
        """测试删除存档"""
        # 保存存档
        self.save_manager.save_game(self.save_data, 1)
        
        # 验证文件存在
        save_path = self.save_manager.get_save_path(1)
        self.assertTrue(os.path.exists(save_path))
        
        # 删除存档
        result = self.save_manager.delete_save(1)
        
        self.assertTrue(result)
        self.assertFalse(os.path.exists(save_path))
    
    def test_delete_save_invalid_slot(self):
        """测试删除无效槽位的存档"""
        # 尝试删除无效槽位
        with self.assertRaises(ValueError):
            self.save_manager.delete_save(0)
        
        with self.assertRaises(ValueError):
            self.save_manager.delete_save(6)
    
    def test_delete_save_not_exists(self):
        """测试删除不存在的存档"""
        # 尝试删除不存在的存档
        result = self.save_manager.delete_save(2)
        
        self.assertFalse(result)
    
    @patch('os.remove', side_effect=PermissionError("Permission denied"))
    def test_delete_save_permission_error(self, mock_remove):
        """测试删除存档权限错误"""
        # 先保存存档
        self.save_manager.save_game(self.save_data, 1)
        
        # 模拟权限错误
        result = self.save_manager.delete_save(1)
        
        self.assertFalse(result)
    
    def test_save_exists(self):
        """测试检查存档是否存在"""
        # 初始状态
        self.assertFalse(self.save_manager.save_exists(1))
        
        # 保存存档
        self.save_manager.save_game(self.save_data, 1)
        
        # 验证存档存在
        self.assertTrue(self.save_manager.save_exists(1))
    
    def test_save_exists_invalid_slot(self):
        """测试检查无效槽位的存档是否存在"""
        # 尝试检查无效槽位
        with self.assertRaises(ValueError):
            self.save_manager.save_exists(0)
        
        with self.assertRaises(ValueError):
            self.save_manager.save_exists(6)
    
    def test_get_save_summary(self):
        """测试获取存档摘要"""
        # 保存存档
        self.save_manager.save_game(self.save_data, 1)
        
        # 获取摘要
        summary = self.save_manager.get_save_summary(1)
        
        # 验证摘要内容
        self.assertIsNotNone(summary)
        self.assertEqual(summary["slot_number"], 1)
        self.assertEqual(summary["exists"], True)
        self.assertEqual(summary["hero_name"], "测试英雄")
        self.assertEqual(summary["hero_level"], 5)
        self.assertEqual(summary["hero_class"], "warrior")
        self.assertEqual(summary["difficulty"], "normal")
        self.assertEqual(summary["map_type"], "forest")
        self.assertIn("save_time", summary)
    
    def test_get_save_summary_not_exists(self):
        """测试获取不存在存档的摘要"""
        # 获取不存在存档的摘要
        summary = self.save_manager.get_save_summary(2)
        
        # 验证摘要内容
        self.assertIsNotNone(summary)
        self.assertEqual(summary["slot_number"], 2)
        self.assertEqual(summary["exists"], False)
        self.assertEqual(summary["hero_name"], "")
        self.assertEqual(summary["hero_level"], 0)
        self.assertEqual(summary["hero_class"], "warrior")  # 默认值
        self.assertEqual(summary["difficulty"], "normal")  # 默认值
        self.assertEqual(summary["map_type"], "plains")  # 默认值
        self.assertIn("save_time", summary)
    
    def test_get_save_summary_corrupted(self):
        """测试获取损坏存档的摘要"""
        # 创建损坏的存档文件
        save_path = self.save_manager.get_save_path(1)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write("{ invalid json content }")
        
        # 获取摘要
        summary = self.save_manager.get_save_summary(1)
        
        # 验证摘要内容
        self.assertIsNotNone(summary)
        self.assertEqual(summary["slot_number"], 1)
        self.assertEqual(summary["exists"], False)
        self.assertEqual(summary["hero_name"], "")
        self.assertEqual(summary["hero_level"], 0)


if __name__ == "__main__":
    unittest.main()