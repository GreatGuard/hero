# -*- coding: utf-8 -*-
"""
测试成就系统功能
"""

import unittest
import os
import json
import tempfile
import shutil
from src.hero.achievements import AchievementSystem
from src.hero.language import LanguageSupport


class MockGame:
    """模拟游戏类用于测试"""
    
    def __init__(self):
        self.language = "zh"
        self.lang = LanguageSupport(self.language)
        
        # 模拟统计系统
        class MockStatistics:
            def __init__(self):
                self.total_steps = 0
                self.total_battles_won = 0
                self.total_monsters_defeated = 0
                self.total_bosses_defeated = 0
                self.max_win_streak = 0
                self.total_gold_earned = 0
                self.total_potions_obtained = 0
                self.total_equipment_obtained = 0
                self.equipment_by_rarity = {"legendary": 0}
                
                # 模拟装备
                self.equipment = {"weapon": None, "armor": None, "accessory": None}
                
        self.statistics = MockStatistics()
        self.hero_level = 1
        self.hero_skills = []
        self.victory = False
        self.difficulty = "normal"
        self.equipment = {"weapon": None, "armor": None, "accessory": None}


class TestAchievements(unittest.TestCase):
    """测试成就系统"""
    
    def setUp(self):
        """测试前准备"""
        self.game = MockGame()
        
        # 创建临时目录用于测试存档
        self.temp_dir = tempfile.mkdtemp()
        self.achievement_file = os.path.join(self.temp_dir, "achievements.json")
        
        # 创建成就系统实例
        self.achievements = AchievementSystem(self.game)
        self.achievements.achievement_data_file = self.achievement_file
        
    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_achievements_initialization(self):
        """测试成就系统初始化"""
        # 检查成就是否正确加载
        self.assertIsNotNone(self.achievements.achievements)
        self.assertIsInstance(self.achievements.achievements, dict)
        
        # 检查成就数量
        self.assertGreater(len(self.achievements.achievements), 10)
        
        # 检查已解锁成就是否为空
        self.assertEqual(len(self.achievements.unlocked_achievements), 0)
    
    def test_achievement_unlocking(self):
        """测试成就解锁功能"""
        # 模拟移动一步
        self.game.statistics.total_steps = 1
        
        # 检查成就
        new_achievements = self.achievements.check_achievements()
        
        # 应该解锁第一个成就
        self.assertGreater(len(new_achievements), 0)
        self.assertIn("first_step", new_achievements)
        self.assertIn("first_step", self.achievements.unlocked_achievements)
    
    def test_achievement_progress(self):
        """测试成就进度获取"""
        # 获取成就进度信息
        progress_info = self.achievements.get_achievement_progress("first_step")
        
        # 检查进度信息结构
        self.assertIsNotNone(progress_info)
        self.assertIn("name", progress_info)
        self.assertIn("description", progress_info)
        self.assertIn("icon", progress_info)
        self.assertIn("rarity", progress_info)
        self.assertIn("unlocked", progress_info)
        self.assertIn("progress", progress_info)
        
        # 初始状态下成就应该未解锁
        self.assertFalse(progress_info["unlocked"])
        self.assertEqual(progress_info["progress"], 0)
    
    def test_achievement_saving_loading(self):
        """测试成就保存和加载"""
        # 解锁一个成就
        self.game.statistics.total_steps = 1
        self.achievements.check_achievements()
        
        # 检查成就文件是否存在
        self.assertTrue(os.path.exists(self.achievement_file))
        
        # 读取文件内容
        with open(self.achievement_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查文件内容
        self.assertIn("unlocked_achievements", data)
        self.assertIn("last_updated", data)
        self.assertIn("first_step", data["unlocked_achievements"])
    
    def test_achievement_conditions(self):
        """测试成就条件判断"""
        # 测试多个成就条件
        
        # 1. 移动相关成就
        self.game.statistics.total_steps = 100
        new_achievements = self.achievements.check_achievements()
        self.assertIn("explorer", new_achievements)
        
        # 2. 战斗相关成就
        self.game.statistics.total_battles_won = 1
        new_achievements = self.achievements.check_achievements()
        self.assertIn("first_blood", new_achievements)
        
        # 3. 资源相关成就
        self.game.statistics.total_gold_earned = 1
        new_achievements = self.achievements.check_achievements()
        self.assertIn("first_gold", new_achievements)
    
    def test_achievement_summary(self):
        """测试成就摘要功能"""
        summary = self.achievements.get_achievement_summary()
        
        # 检查摘要结构
        self.assertIn("total", summary)
        self.assertIn("unlocked", summary)
        self.assertIn("progress", summary)
        
        # 初始状态下应该没有解锁成就
        self.assertEqual(summary["unlocked"], 0)
        self.assertEqual(summary["progress"], 0)
    
    def test_invalid_achievement_id(self):
        """测试无效成就ID处理"""
        progress_info = self.achievements.get_achievement_progress("invalid_achievement")
        self.assertIsNone(progress_info)
    
    def test_achievement_categories(self):
        """测试成就分类功能"""
        # 这个方法主要测试UI显示功能，我们检查成就分类映射是否正确
        
        # 检查是否所有成就都有对应的分类
        all_achievements = set(self.achievements.achievements.keys())
        categorized_achievements = set()
        
        # 从分类映射中获取所有成就
        category_mapping = {
            "progress": ["first_step", "explorer", "master_explorer"],
            "combat": ["first_blood", "monster_slayer", "boss_hunter", "undefeated"],
            "resources": ["first_gold", "rich_adventurer", "potion_collector"],
            "equipment": ["first_equipment", "fully_equipped", "legendary_collector"],
            "skills": ["first_skill", "skill_master"],
            "special": ["level_up", "veteran", "game_completion", "survivor"]
        }
        
        for category_achievements in category_mapping.values():
            categorized_achievements.update(category_achievements)
        
        # 检查是否有未分类的成就
        uncategorized = all_achievements - categorized_achievements
        self.assertEqual(len(uncategorized), 0, f"Uncategorized achievements: {uncategorized}")


if __name__ == "__main__":
    unittest.main()