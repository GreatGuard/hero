#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试新事件类型模块
"""

import unittest
import sys
import os

# 由于run_tests.py已将src路径添加到sys.path，我们可以直接导入
from hero.game_config import EVENT_TYPES
from hero.language import LanguageSupport
from hero.events import EventSystem


class TestNewEventTypes(unittest.TestCase):
    """测试新事件类型"""

    def setUp(self):
        """设置测试环境"""
        # 创建一个简单的游戏模拟类
        class MockGame:
            def __init__(self):
                self.lang = LanguageSupport("zh")
                self.hero_position = 5
                self.map_length = 20
                self.hero_exp = 100
                self.hero_gold = 50
                self.hero_hp = 50
                self.hero_max_hp = 100
                self.base_attack = 15
                self.base_defense = 8
                self.hero_level = 1
                self.difficulty = "normal"
                self.difficulty_settings = {
                    "normal": {
                        "enemy_multiplier": 1.0,
                        "gold_multiplier": 1.0
                    }
                }
                self.events_encountered = []
                
                # 统计系统模拟
                class MockStatistics:
                    def record_event_triggered(self, event_type):
                        pass
                    
                    def record_exp_earned(self, amount):
                        pass
                
                self.statistics = MockStatistics()
                
            def update_attributes(self):
                pass
                
            def show_hero_info(self):
                pass
                
            def level_up(self):
                self.hero_level += 1
        
        self.game = MockGame()
        self.event_system = EventSystem(self.game)

    def test_event_types_config(self):
        """测试事件类型配置"""
        # 验证所有新事件类型都在配置中
        expected_events = [
            "mysterious_teleport",
            "sage_guidance",
            "robber_encounter",
            "mysterious_altar",
            "roadside_camp"
        ]
        
        for event_type in expected_events:
            self.assertIn(event_type, EVENT_TYPES, 
                          f"事件类型 {event_type} 未在配置中找到")
        
        # 验证每个事件类型都有必要的字段
        for event_type, config in EVENT_TYPES.items():
            if event_type in expected_events:
                self.assertIn("name_key", config, 
                            f"事件类型 {event_type} 缺少 name_key 字段")
                self.assertIn("description_key", config, 
                            f"事件类型 {event_type} 缺少 description_key 字段")

    def test_mysterious_teleport(self):
        """测试神秘传送事件"""
        initial_position = self.game.hero_position
        self.event_system.mysterious_teleport()
        
        # 验证位置可能改变
        position_may_change = self.game.hero_position != initial_position
        self.assertTrue(position_may_change, 
                      "神秘传送事件应该可能改变位置")
        
        # 验证事件已记录
        self.assertTrue(len(self.game.events_encountered) > 0,
                     "神秘传送事件应该记录到事件历史中")

    def test_sage_guidance(self):
        """测试贤者指引事件"""
        initial_exp = self.game.hero_exp
        self.event_system.sage_guidance()
        
        # 验证经验增加
        self.assertGreater(self.game.hero_exp, initial_exp,
                        "贤者指引事件应该增加经验值")
        
        # 验证事件已记录
        self.assertTrue(len(self.game.events_encountered) > 0,
                     "贤者指引事件应该记录到事件历史中")

    def test_robber_encounter(self):
        """测试遭遇强盗事件"""
        initial_gold = self.game.hero_gold
        # 由于需要用户输入，我们只测试方法存在性
        self.assertTrue(hasattr(self.event_system, 'robber_encounter'),
                     "EventSystem应该有robber_encounter方法")

    def test_mysterious_altar(self):
        """测试神秘祭坛事件"""
        # 由于需要用户输入，我们只测试方法存在性
        self.assertTrue(hasattr(self.event_system, 'mysterious_altar'),
                     "EventSystem应该有mysterious_altar方法")

    def test_roadside_camp(self):
        """测试路边营地事件"""
        initial_hp = self.game.hero_hp
        self.event_system.roadside_camp()
        
        # 验证血量增加（不超过最大值）
        self.assertGreaterEqual(self.game.hero_hp, initial_hp,
                             "路边营地事件应该恢复血量")
        self.assertLessEqual(self.game.hero_hp, self.game.hero_max_hp,
                           "血量不应超过最大值")
        
        # 验证事件已记录
        self.assertTrue(len(self.game.events_encountered) > 0,
                     "路边营地事件应该记录到事件历史中")

    def test_language_support(self):
        """测试多语言支持"""
        # 测试中文
        self.game.lang.set_language("zh")
        for event_type in EVENT_TYPES:
            config = EVENT_TYPES[event_type]
            name_key = config["name_key"]
            desc_key = config["description_key"]
            
            # 验证中文文本存在
            self.assertNotEqual(self.game.lang.get_text(name_key), name_key,
                             f"事件 {name_key} 缺少中文翻译")
            self.assertNotEqual(self.game.lang.get_text(desc_key), desc_key,
                             f"事件 {desc_key} 缺少中文翻译")
        
        # 测试英文
        self.game.lang.set_language("en")
        for event_type in EVENT_TYPES:
            config = EVENT_TYPES[event_type]
            name_key = config["name_key"]
            desc_key = config["description_key"]
            
            # 验证英文文本存在
            self.assertNotEqual(self.game.lang.get_text(name_key), name_key,
                             f"事件 {name_key} 缺少英文翻译")
            self.assertNotEqual(self.game.lang.get_text(desc_key), desc_key,
                             f"事件 {desc_key} 缺少英文翻译")


if __name__ == '__main__':
    unittest.main()