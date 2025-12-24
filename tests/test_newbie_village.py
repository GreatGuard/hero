# -*- coding: utf-8 -*-
"""
新手村测试
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

from hero.newbie_village import NewbieVillage


class TestNewbieVillage(unittest.TestCase):
    """测试新手村"""
    
    def setUp(self):
        """测试数据准备"""
        # 创建模拟游戏对象
        self.mock_game = Mock()
        self.mock_game.hero_hp = 100
        self.mock_game.hero_max_hp = 100
        self.mock_game.hero_level = 1
        self.mock_game.hero_exp = 0
        self.mock_game.hero_gold = 50
        self.mock_game.hero_skills = []
        self.mock_game.lang = Mock()
        self.mock_game.lang.get_text.return_value = "test_text"
        self.mock_game.lang.format_text.return_value = "formatted_text"
        self.mock_game.clear_screen = Mock()
        
        # 创建新手村实例
        self.newbie_village = NewbieVillage(self.mock_game)
    
    def test_newbie_village_initialization(self):
        """测试新手村初始化"""
        self.assertEqual(self.newbie_village.game, self.mock_game)
        self.assertTrue(hasattr(self.newbie_village, 'training_ground'))
        self.assertTrue(hasattr(self.newbie_village, 'village_shop'))
        self.assertTrue(hasattr(self.newbie_village, 'village_clinic'))
        self.assertTrue(hasattr(self.newbie_village, 'elder_advice'))
    
    def test_training_ground(self):
        """测试训练场"""
        # 测试训练场方法存在
        self.assertTrue(hasattr(self.newbie_village, 'training_ground'))
        self.assertTrue(callable(self.newbie_village.training_ground))
    
    def test_village_shop(self):
        """测试村庄商店"""
        # 测试村庄商店方法存在
        self.assertTrue(hasattr(self.newbie_village, 'village_shop'))
        self.assertTrue(callable(self.newbie_village.village_shop))
    
    def test_village_clinic(self):
        """测试村庄诊所"""
        # 测试村庄诊所方法存在
        self.assertTrue(hasattr(self.newbie_village, 'village_clinic'))
        self.assertTrue(callable(self.newbie_village.village_clinic))
    
    def test_elder_advice(self):
        """测试长老建议"""
        # 测试长老建议方法存在
        self.assertTrue(hasattr(self.newbie_village, 'elder_advice'))
        self.assertTrue(callable(self.newbie_village.elder_advice))
    
    def test_practice_combat(self):
        """测试战斗练习"""
        # 测试战斗练习方法存在
        self.assertTrue(hasattr(self.newbie_village, 'practice_combat'))
        self.assertTrue(callable(self.newbie_village.practice_combat))
    
    def test_learn_skill_training(self):
        """测试技能学习训练"""
        # 测试技能学习训练方法存在
        self.assertTrue(hasattr(self.newbie_village, 'learn_skill_training'))
        self.assertTrue(callable(self.newbie_village.learn_skill_training))


if __name__ == '__main__':
    unittest.main()
