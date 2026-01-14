#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
游戏设置模块测试
"""

import unittest
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hero.settings import GameSettings


class TestGameSettings(unittest.TestCase):
    """游戏设置测试类"""
    
    def setUp(self):
        """测试前初始化"""
        self.settings = GameSettings("zh")
    
    def test_default_values(self):
        """测试默认值"""
        self.assertEqual(self.settings.language, "zh")
        self.assertEqual(self.settings.text_speed, 30)
        self.assertEqual(self.settings.auto_save_interval, 0)
        self.assertEqual(self.settings.event_detail_level, 1)
        self.assertTrue(self.settings.combat_animations)
        self.assertFalse(self.settings.sound_effects)
        self.assertEqual(self.settings.combat_log_level, 1)
    
    def test_text_delay_calculation(self):
        """测试文本延迟计算"""
        self.settings.text_speed = 0
        self.assertEqual(self.settings.get_text_delay(), 0)
        
        self.settings.text_speed = 30
        self.assertEqual(self.settings.get_text_delay(), 0.03)
        
        self.settings.text_speed = 100
        self.assertEqual(self.settings.get_text_delay(), 0.1)
    
    def test_auto_save_check(self):
        """测试自动存档检查"""
        self.settings.auto_save_interval = 0
        self.assertFalse(self.settings.should_auto_save(10))
        
        self.settings.auto_save_interval = 5
        self.assertTrue(self.settings.should_auto_save(10))
        self.assertFalse(self.settings.should_auto_save(12))
        
        self.settings.auto_save_interval = 10
        self.assertTrue(self.settings.should_auto_save(20))
        self.assertFalse(self.settings.should_auto_save(25))
    
    def test_to_dict(self):
        """测试序列化"""
        data_dict = self.settings.to_dict()
        
        expected_keys = [
            'text_speed', 'auto_save_interval', 'event_detail_level',
            'combat_animations', 'sound_effects', 'combat_log_level'
        ]
        
        for key in expected_keys:
            self.assertIn(key, data_dict)
        
        self.assertEqual(data_dict['text_speed'], 30)
        self.assertEqual(data_dict['auto_save_interval'], 0)
        self.assertEqual(data_dict['event_detail_level'], 1)
        self.assertTrue(data_dict['combat_animations'])
        self.assertFalse(data_dict['sound_effects'])
        self.assertEqual(data_dict['combat_log_level'], 1)
    
    def test_from_dict(self):
        """测试反序列化"""
        test_data = {
            'text_speed': 50,
            'auto_save_interval': 10,
            'event_detail_level': 2,
            'combat_animations': False,
            'sound_effects': True,
            'combat_log_level': 0
        }
        
        self.settings.from_dict(test_data)
        
        self.assertEqual(self.settings.text_speed, 50)
        self.assertEqual(self.settings.auto_save_interval, 10)
        self.assertEqual(self.settings.event_detail_level, 2)
        self.assertFalse(self.settings.combat_animations)
        self.assertTrue(self.settings.sound_effects)
        self.assertEqual(self.settings.combat_log_level, 0)
    
    def test_from_dict_empty(self):
        """测试从空字典加载"""
        original_values = {
            'text_speed': self.settings.text_speed,
            'auto_save_interval': self.settings.auto_save_interval,
            'event_detail_level': self.settings.event_detail_level,
            'combat_animations': self.settings.combat_animations,
            'sound_effects': self.settings.sound_effects,
            'combat_log_level': self.settings.combat_log_level
        }
        
        self.settings.from_dict({})
        
        # 确保值没有改变
        self.assertEqual(self.settings.text_speed, original_values['text_speed'])
        self.assertEqual(self.settings.auto_save_interval, original_values['auto_save_interval'])
        self.assertEqual(self.settings.event_detail_level, original_values['event_detail_level'])
        self.assertEqual(self.settings.combat_animations, original_values['combat_animations'])
        self.assertEqual(self.settings.sound_effects, original_values['sound_effects'])
        self.assertEqual(self.settings.combat_log_level, original_values['combat_log_level'])
    
    def test_format_text_with_speed(self):
        """测试文本格式化"""
        text = "测试文本"
        result = self.settings.format_text_with_speed(text)
        self.assertEqual(result, text)
        
        # 修改速度后再次测试
        self.settings.text_speed = 50
        result = self.settings.format_text_with_speed(text)
        self.assertEqual(result, text)
    
    def test_english_settings(self):
        """测试英文设置"""
        settings_en = GameSettings("en")
        self.assertEqual(settings_en.language, "en")
        
        # 测试其他默认值是否一致
        self.assertEqual(settings_en.text_speed, 30)
        self.assertEqual(settings_en.auto_save_interval, 0)
        self.assertEqual(settings_en.event_detail_level, 1)


if __name__ == '__main__':
    unittest.main()