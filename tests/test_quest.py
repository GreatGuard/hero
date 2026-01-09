#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
任务系统测试模块
"""

import unittest
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hero.quest import Quest, QuestSystem
from hero.language import LanguageSupport


class TestQuest(unittest.TestCase):
    """测试Quest类"""
    
    def setUp(self):
        """测试前准备"""
        self.quest = Quest(
            quest_id="test_quest_1",
            quest_type="kill_monster",
            target_value=5,
            reward_gold=50,
            reward_exp=100,
            description_key="kill_monster_quest"
        )
    
    def test_quest_initialization(self):
        """测试任务初始化"""
        self.assertEqual(self.quest.quest_id, "test_quest_1")
        self.assertEqual(self.quest.quest_type, "kill_monster")
        self.assertEqual(self.quest.target_value, 5)
        self.assertEqual(self.quest.current_value, 0)
        self.assertEqual(self.quest.reward_gold, 50)
        self.assertEqual(self.quest.reward_exp, 100)
        self.assertEqual(self.quest.description_key, "kill_monster_quest")
        self.assertFalse(self.quest.completed)
    
    def test_update_progress(self):
        """测试更新进度"""
        # 每次测试重新创建Quest实例
        quest = Quest(
            quest_id="test_quest_progress",
            quest_type="kill_monster",
            target_value=5,
            reward_gold=50,
            reward_exp=100,
            description_key="kill_monster_quest"
        )
        
        # 测试单次更新
        result = quest.update_progress()
        self.assertEqual(quest.current_value, 1)
        self.assertFalse(result)
        
        # 测试多次更新
        for i in range(4):
            result = quest.update_progress()
        self.assertEqual(quest.current_value, 5)
        
        # 测试任务完成
        self.assertTrue(result)
        self.assertTrue(quest.completed)
    
    def test_update_progress_with_value(self):
        """测试带值的进度更新"""
        # 每次测试重新创建Quest实例
        quest = Quest(
            quest_id="test_quest_progress_value",
            quest_type="kill_monster",
            target_value=5,
            reward_gold=50,
            reward_exp=100,
            description_key="kill_monster_quest"
        )
        
        quest.update_progress(3)
        self.assertEqual(quest.current_value, 3)
        
        result = quest.update_progress(2)
        self.assertTrue(result)
        self.assertTrue(quest.completed)
    
    def test_get_progress_percentage(self):
        """测试进度百分比计算"""
        # 每次测试重新创建Quest实例
        quest = Quest(
            quest_id="test_quest_percentage",
            quest_type="kill_monster",
            target_value=5,
            reward_gold=50,
            reward_exp=100,
            description_key="kill_monster_quest"
        )
        
        # 初始进度
        percentage = quest.get_progress_percentage()
        self.assertEqual(percentage, 0)
        
        # 部分进度
        quest.update_progress(2)
        percentage = quest.get_progress_percentage()
        self.assertEqual(percentage, 40)
        
        # 完成进度
        quest.update_progress(3)
        percentage = quest.get_progress_percentage()
        self.assertEqual(percentage, 100)
    
    def test_to_dict(self):
        """测试转换为字典"""
        # 每次测试重新创建Quest实例
        quest = Quest(
            quest_id="test_quest_dict",
            quest_type="kill_monster",
            target_value=5,
            reward_gold=50,
            reward_exp=100,
            description_key="kill_monster_quest"
        )
        
        quest.update_progress(3)
        quest_dict = quest.to_dict()
        
        expected_dict = {
            'quest_id': 'test_quest_dict',
            'quest_type': 'kill_monster',
            'target_value': 5,
            'current_value': 3,
            'reward_gold': 50,
            'reward_exp': 100,
            'description_key': 'kill_monster_quest',
            'completed': False
        }
        self.assertEqual(quest_dict, expected_dict)
    
    def test_from_dict(self):
        """测试从字典创建"""
        quest_data = {
            'quest_id': 'test_quest_2',
            'quest_type': 'collect_gold',
            'target_value': 100,
            'current_value': 50,
            'reward_gold': 200,
            'reward_exp': 150,
            'description_key': 'collect_gold_quest',
            'completed': False
        }
        
        quest = Quest.from_dict(quest_data)
        self.assertEqual(quest.quest_id, 'test_quest_2')
        self.assertEqual(quest.quest_type, 'collect_gold')
        self.assertEqual(quest.target_value, 100)
        self.assertEqual(quest.current_value, 50)
        self.assertEqual(quest.reward_gold, 200)
        self.assertEqual(quest.reward_exp, 150)
        self.assertEqual(quest.description_key, 'collect_gold_quest')
        self.assertFalse(quest.completed)


class TestQuestSystem(unittest.TestCase):
    """测试QuestSystem类"""
    
    def setUp(self):
        """测试前准备"""
        self.quest_system = QuestSystem()
        self.lang = LanguageSupport("zh")
    
    def test_quest_system_initialization(self):
        """测试任务系统初始化"""
        self.assertEqual(len(self.quest_system.active_quests), 0)
        self.assertEqual(len(self.quest_system.completed_quests), 0)
        self.assertEqual(self.quest_system.quest_counter, 0)
        self.assertEqual(len(self.quest_system.quest_types), 4)
    
    def test_generate_random_quest(self):
        """测试生成随机任务"""
        # 测试生成任务
        quest = self.quest_system.generate_random_quest(hero_level=1)
        self.assertIsNotNone(quest)
        self.assertIn(quest.quest_type, ['kill_monster', 'collect_gold', 'reach_position', 'use_potion'])
        self.assertIn(quest.description_key, ['kill_monster_quest', 'collect_gold_quest', 'reach_position_quest', 'use_potion_quest'])
        self.assertGreater(quest.target_value, 0)
        self.assertGreater(quest.reward_gold, 0)
        self.assertGreater(quest.reward_exp, 0)
        
        # 测试计数器增加
        self.assertEqual(self.quest_system.quest_counter, 1)
    
    def test_add_quest(self):
        """测试添加任务"""
        # 添加一个任务
        quest = self.quest_system.generate_random_quest(hero_level=1)
        result = self.quest_system.add_quest(quest)
        self.assertTrue(result)
        self.assertEqual(len(self.quest_system.active_quests), 1)
        
        # 添加第二个任务
        quest2 = self.quest_system.generate_random_quest(hero_level=1)
        result = self.quest_system.add_quest(quest2)
        self.assertTrue(result)
        self.assertEqual(len(self.quest_system.active_quests), 2)
        
        # 添加第三个任务
        quest3 = self.quest_system.generate_random_quest(hero_level=1)
        result = self.quest_system.add_quest(quest3)
        self.assertTrue(result)
        self.assertEqual(len(self.quest_system.active_quests), 3)
        
        # 尝试添加第四个任务（应该失败）
        quest4 = self.quest_system.generate_random_quest(hero_level=1)
        result = self.quest_system.add_quest(quest4)
        self.assertFalse(result)
        self.assertEqual(len(self.quest_system.active_quests), 3)
    
    def test_update_quest_progress(self):
        """测试更新任务进度"""
        # 添加一个击杀怪物任务
        quest = Quest(
            quest_id="test_quest_1",
            quest_type="kill_monster",
            target_value=3,
            reward_gold=50,
            reward_exp=100,
            description_key="kill_monster_quest"
        )
        self.quest_system.add_quest(quest)
        
        # 更新进度
        completed_quests = self.quest_system.update_quest_progress("kill_monster")
        self.assertEqual(len(completed_quests), 0)
        self.assertEqual(quest.current_value, 1)
        
        # 再次更新，完成任务
        completed_quests = self.quest_system.update_quest_progress("kill_monster", 2)
        self.assertEqual(len(completed_quests), 1)
        self.assertEqual(completed_quests[0].quest_id, "test_quest_1")
        self.assertEqual(len(self.quest_system.active_quests), 0)
        self.assertEqual(len(self.quest_system.completed_quests), 1)
    
    def test_get_quest_rewards(self):
        """测试获取任务奖励"""
        quest = Quest(
            quest_id="test_quest_1",
            quest_type="kill_monster",
            target_value=3,
            reward_gold=50,
            reward_exp=100,
            description_key="kill_monster_quest"
        )
        
        gold, exp = self.quest_system.get_quest_rewards(quest)
        self.assertEqual(gold, 50)
        self.assertEqual(exp, 100)
    
    def test_format_quests_list(self):
        """测试格式化任务列表"""

        self.lang.set_language("en")
        # 测试没有任务的情况
        result = self.quest_system.format_quests_list(self.lang)
        self.assertEqual(result, self.lang.get_text("no_active_quests"))
        
        # 添加一个任务
        quest = Quest(
            quest_id="test_quest_1",
            quest_type="kill_monster",
            target_value=3,
            reward_gold=50,
            reward_exp=100,
            description_key="kill_monster_quest"
        )
        self.quest_system.add_quest(quest)
        
        # 测试格式化任务列表
        result = self.quest_system.format_quests_list(self.lang)
        self.assertIn("Defeat 3 monsters", result)
        self.assertIn("Reward: 50 gold, 100 exp", result)
    
    def test_serialization(self):
        """测试序列化和反序列化"""
        # 添加任务
        quest1 = Quest(
            quest_id="test_quest_1",
            quest_type="kill_monster",
            target_value=3,
            reward_gold=50,
            reward_exp=100,
            description_key="kill_monster_quest"
        )
        quest1.update_progress(2)
        
        quest2 = Quest(
            quest_id="test_quest_2",
            quest_type="collect_gold",
            target_value=100,
            reward_gold=200,
            reward_exp=150,
            description_key="collect_gold_quest"
        )
        quest2.update_progress(50)
        
        self.quest_system.add_quest(quest1)
        self.quest_system.add_quest(quest2)
        
        # 标记一个任务为已完成
        quest2.update_progress(49)  # 完成
        completed_quests = self.quest_system.update_quest_progress("collect_gold")
        self.assertEqual(len(completed_quests), 1)
        
        # 转换为字典
        quest_system_dict = self.quest_system.to_dict()
        
        # 创建新的任务系统并从字典恢复
        new_quest_system = QuestSystem()
        new_quest_system.from_dict(quest_system_dict)
        
        # 验证恢复后的状态
        self.assertEqual(len(new_quest_system.active_quests), 1)
        self.assertEqual(len(new_quest_system.completed_quests), 1)
        self.assertEqual(new_quest_system.quest_counter, 0)  # 计数器不保存
        
        # 验证活动任务
        active_quest = new_quest_system.active_quests[0]
        self.assertEqual(active_quest.quest_id, "test_quest_1")
        self.assertEqual(active_quest.current_value, 2)
        
        # 验证已完成任务
        completed_quest = new_quest_system.completed_quests[0]
        self.assertEqual(completed_quest.quest_id, "test_quest_2")
        self.assertTrue(completed_quest.completed)


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)