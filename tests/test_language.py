# -*- coding: utf-8 -*-
"""
语言支持模块测试
"""

import sys
import os
import unittest

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hero.language import LanguageSupport


class TestLanguageSupport(unittest.TestCase):
    """测试语言支持模块"""
    
    def setUp(self):
        """测试数据准备"""
        self.zh_lang = LanguageSupport("zh")
        self.en_lang = LanguageSupport("en")
        self.required_text_keys = [
            "welcome_title", "continue_prompt", "hero_creation", 
            "enter_name", "name_empty", "game_start", "game_over", 
            "victory", "block_separator", "item_separator"
        ]
    
    def test_language_initialization(self):
        """测试语言初始化"""
        self.assertEqual(self.zh_lang.language, "zh")
        self.assertEqual(self.en_lang.language, "en")
        self.assertIsInstance(self.zh_lang.texts, dict)
        self.assertIsInstance(self.en_lang.texts, dict)
    
    def test_text_retrieval_chinese(self):
        """测试中文文本获取"""
        for key in self.required_text_keys:
            with self.subTest(key=key):
                text = self.zh_lang.get_text(key)
                self.assertIsInstance(text, str)
                self.assertTrue(len(text) > 0)
    
    def test_text_retrieval_english(self):
        """测试英文文本获取"""
        for key in self.required_text_keys:
            with self.subTest(key=key):
                text = self.en_lang.get_text(key)
                self.assertIsInstance(text, str)
                self.assertTrue(len(text) > 0)
    
    def test_language_switching(self):
        """测试语言切换"""
        lang = LanguageSupport("zh")
        self.assertEqual(lang.language, "zh")
        
        lang.set_language("en")
        self.assertEqual(lang.language, "en")
        self.assertNotEqual(lang.get_text("welcome_title"), 
                            self.zh_lang.get_text("welcome_title"))
        
        lang.set_language("zh")
        self.assertEqual(lang.language, "zh")
        self.assertEqual(lang.get_text("welcome_title"), 
                        self.zh_lang.get_text("welcome_title"))
    
    def test_format_functions(self):
        """测试格式化函数"""
        # 测试位置格式化
        position_text = self.zh_lang.format_text("position_format", 5, 10)
        self.assertIsInstance(position_text, str)
        self.assertIn("5", position_text)
        self.assertIn("10", position_text)
        
        # 测试英雄标记
        hero_marker = self.zh_lang.format_text("hero_marker")
        self.assertIsInstance(hero_marker, str)
        
        # 测试事件文本
        event_text = self.zh_lang.format_text("event_text", "find_bun", 20)
        self.assertIsInstance(event_text, str)
        self.assertIn("20", event_text)
        
        # 测试技能括号（注意：这个函数返回的是括号元组，不是格式化后的文本）
        skill_brackets = self.zh_lang.format_text("skill_brackets")
        self.assertIsInstance(skill_brackets, tuple)
        self.assertEqual(len(skill_brackets), 2)  # 开括号和闭括号
        
        # 测试装备名称（注意：这个函数需要特定的参数）
        # 由于它需要equipment_db参数，我们在这里跳过这个测试
        # 或者我们可以简单地验证它能够被调用（如果提供了正确的参数）
        pass
    
    def test_invalid_key_handling(self):
        """测试无效键处理"""
        # 测试不存在的键
        invalid_text = self.zh_lang.get_text("nonexistent_key")
        self.assertEqual(invalid_text, "nonexistent_key")
        
        # 测试无效的格式化函数（返回None）
        invalid_format = self.zh_lang.format_text("nonexistent_format", "test")
        self.assertIsNone(invalid_format)
    
    def test_yes_options(self):
        """测试是选项处理"""
        yes_options = self.zh_lang.get_text("yes_options")
        self.assertIsInstance(yes_options, list)
        self.assertIn("y", yes_options)
        self.assertIn("Y", yes_options)
        self.assertIn("yes", yes_options)
        self.assertIn("是", yes_options)
    
    def test_difficulty_and_map_texts(self):
        """测试难度和地图相关文本"""
        difficulties = ["easy", "normal", "hard", "nightmare"]
        maps = ["plains", "forest", "desert", "dungeon", "mountain"]
        
        for diff in difficulties:
            with self.subTest(difficulty=diff):
                text = self.zh_lang.get_text(f"difficulty_{diff}")
                self.assertIsInstance(text, str)
                self.assertTrue(len(text) > 0)
        
        for map_type in maps:
            with self.subTest(map_type=map_type):
                text = self.zh_lang.get_text(f"map_{map_type}")
                self.assertIsInstance(text, str)
                self.assertTrue(len(text) > 0)


if __name__ == '__main__':
    unittest.main()