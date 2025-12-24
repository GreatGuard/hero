# -*- coding: utf-8 -*-
"""
游戏配置模块测试
"""

import sys
import os
import unittest

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hero.game_config import DIFFICULTY_SETTINGS, MAP_TYPES


class TestGameConfig(unittest.TestCase):
    """测试游戏配置模块"""
    
    def setUp(self):
        """测试数据准备"""
        self.difficulties = ["easy", "normal", "hard", "nightmare"]
        self.map_types = ["plains", "forest", "desert", "dungeon", "mountain"]
    
    def test_difficulty_settings_structure(self):
        """测试难度设置结构是否完整"""
        expected_keys = ["map_length", "gold_multiplier", "exp_multiplier", 
                         "enemy_multiplier", "gold_start", "potions_start", "name"]
        
        for difficulty in self.difficulties:
            with self.subTest(difficulty=difficulty):
                self.assertIn(difficulty, DIFFICULTY_SETTINGS)
                settings = DIFFICULTY_SETTINGS[difficulty]
                for key in expected_keys:
                    self.assertIn(key, settings)
    
    def test_difficulty_settings_values(self):
        """测试难度设置值是否合理"""
        # 简单模式应该有更多资源和更弱敌人
        easy = DIFFICULTY_SETTINGS["easy"]
        normal = DIFFICULTY_SETTINGS["normal"]
        hard = DIFFICULTY_SETTINGS["hard"]
        nightmare = DIFFICULTY_SETTINGS["nightmare"]
        
        # 验证难度递增的数值合理性
        self.assertGreaterEqual(normal["map_length"], easy["map_length"])
        self.assertGreaterEqual(hard["map_length"], normal["map_length"])
        self.assertGreaterEqual(nightmare["map_length"], hard["map_length"])
        
        self.assertGreaterEqual(easy["gold_start"], hard["gold_start"])
        self.assertGreaterEqual(easy["gold_start"], nightmare["gold_start"])
        
        self.assertLessEqual(easy["enemy_multiplier"], normal["enemy_multiplier"])
        self.assertLessEqual(normal["enemy_multiplier"], hard["enemy_multiplier"])
        self.assertLessEqual(hard["enemy_multiplier"], nightmare["enemy_multiplier"])
    
    def test_map_types_structure(self):
        """测试地图类型结构是否完整"""
        expected_keys = ["name", "description", "special_events", "monsters"]
        
        for map_type in self.map_types:
            with self.subTest(map_type=map_type):
                self.assertIn(map_type, MAP_TYPES)
                settings = MAP_TYPES[map_type]
                for key in expected_keys:
                    self.assertIn(key, settings)
                self.assertIsInstance(settings["special_events"], list)
                self.assertIsInstance(settings["monsters"], list)
                self.assertGreater(len(settings["special_events"]), 0)
                self.assertGreater(len(settings["monsters"]), 0)
    
    def test_map_types_unique_values(self):
        """测试地图类型值唯一性"""
        map_names = [MAP_TYPES[mt]["name"] for mt in self.map_types]
        self.assertEqual(len(map_names), len(set(map_names)), "地图名称应该是唯一的")
        
        descriptions = [MAP_TYPES[mt]["description"] for mt in self.map_types]
        self.assertEqual(len(descriptions), len(set(descriptions)), "地图描述应该是唯一的")
    
    def test_config_values_are_positive(self):
        """测试配置值为正数"""
        for difficulty in self.difficulties:
            settings = DIFFICULTY_SETTINGS[difficulty]
            
            self.assertGreater(settings["map_length"], 0, 
                              f"{difficulty}地图长度应该大于0")
            self.assertGreater(settings["gold_multiplier"], 0, 
                              f"{difficulty}金币倍数应该大于0")
            self.assertGreater(settings["exp_multiplier"], 0, 
                              f"{difficulty}经验倍数应该大于0")
            self.assertGreater(settings["enemy_multiplier"], 0, 
                              f"{difficulty}敌人倍数应该大于0")
            self.assertGreaterEqual(settings["gold_start"], 0, 
                                   f"{difficulty}初始金币应该大于等于0")
            self.assertGreaterEqual(settings["potions_start"], 0, 
                                   f"{difficulty}初始药剂数量应该大于等于0")


if __name__ == '__main__':
    unittest.main()