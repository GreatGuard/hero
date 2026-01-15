#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏错误处理测试脚本
测试游戏中的错误处理改进
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# 添加src目录到路径，以便导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from hero.error_handler import init_error_handler, is_debug_mode
from hero.save_data import SaveManager, SaveData

class TestGameErrorHandling(unittest.TestCase):
    """测试游戏错误处理"""
    
    @classmethod
    def setUpClass(cls):
        """设置测试环境"""
        # 初始化错误处理器，启用调试模式
        init_error_handler(debug_mode=True, log_file="logs/test_game_error.log")
        
        # 创建测试存档目录
        cls.test_save_dir = "test_saves"
        if not os.path.exists(cls.test_save_dir):
            os.makedirs(cls.test_save_dir)
    
    def setUp(self):
        """每个测试前的设置"""
        # 创建SaveManager实例
        self.save_manager = SaveManager(self.test_save_dir)
        
        # 创建模拟的游戏对象
        self.mock_game = MagicMock()
        self.mock_game.hero_name = "测试英雄"
        self.mock_game.hero_class = "warrior"
        self.mock_game.hero_level = 1
        self.mock_game.hero_exp = 0
        self.mock_game.hero_hp = 100
        self.mock_game.hero_max_hp = 100
        self.mock_game.hero_attack = 20
        self.mock_game.hero_defense = 5
        self.mock_game.hero_position = 0
        self.mock_game.game_over = False
        self.mock_game.victory = False
        self.mock_game.hero_gold = 100
        self.mock_game.hero_potions = 2
        self.mock_game.skill_points = 0
        self.mock_game.skill_tree = None
        self.mock_game.equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        self.mock_game.inventory = []
        self.mock_game.hero_skills = []
        self.mock_game.difficulty = "normal"
        self.mock_game.map_type = "plains"
        self.mock_game.language = "zh"
        self.mock_game.map_length = 50
        self.mock_game.monsters_defeated = 0
        self.mock_game.events_encountered = []
        self.mock_game.visited_positions = [False] * 50
        self.mock_game.statistics = None
        self.mock_game.status_effects = {
            "poison": 0,
            "frostbite": 0,
            "frost": 0
        }
    
    def test_save_and_load_with_error_handling(self):
        """测试带有错误处理的保存和加载"""
        # 创建存档数据
        save_data = SaveData(self.mock_game)
        
        # 测试保存
        result = self.save_manager.save_game(save_data, 1)
        self.assertTrue(result, "保存应该成功")
        
        # 测试加载
        loaded_data = self.save_manager.load_game(1)
        self.assertIsNotNone(loaded_data, "加载应该成功")
        self.assertEqual(loaded_data.hero_name, "测试英雄", "英雄名称应该一致")
    
    def test_load_nonexistent_slot(self):
        """测试加载不存在的存档槽位"""
        loaded_data = self.save_manager.load_game(5)  # 空槽位
        self.assertIsNone(loaded_data, "加载空槽位应该返回None")
    
    def test_load_corrupted_file(self):
        """测试加载损坏的存档文件"""
        # 创建一个损坏的JSON文件
        corrupted_path = os.path.join(self.test_save_dir, "save_slot_2.json")
        with open(corrupted_path, 'w', encoding='utf-8') as f:
            f.write("{ invalid json content")
        
        # 尝试加载损坏的文件
        loaded_data = self.save_manager.load_game(2)
        self.assertIsNone(loaded_data, "加载损坏文件应该返回None")
    
    @classmethod
    def tearDownClass(cls):
        """清理测试环境"""
        # 删除测试文件和目录
        import shutil
        if os.path.exists(cls.test_save_dir):
            shutil.rmtree(cls.test_save_dir)
        
        # 删除日志文件
        if os.path.exists("logs/test_game_error.log"):
            os.remove("logs/test_game_error.log")

if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)