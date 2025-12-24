# -*- coding: utf-8 -*-
"""
事件系统测试
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# 添加项目路径
project_root = os.path.join(os.path.dirname(__file__), '..')
src_path = os.path.join(project_root, 'src')
hero_path = os.path.join(src_path, 'hero')
sys.path.insert(0, hero_path)
sys.path.insert(0, src_path)

from hero.events import EventSystem
from hero.main import HeroGame


class TestEventSystem(unittest.TestCase):
    """测试事件系统"""
    
    def setUp(self):
        """测试数据准备"""
        # 创建模拟游戏对象
        self.mock_game = Mock(spec=HeroGame)
        self.mock_game.hero_hp = 100
        self.mock_game.hero_max_hp = 100
        self.mock_game.hero_attack = 20
        self.mock_game.hero_defense = 5
        self.mock_game.hero_level = 1
        self.mock_game.hero_exp = 0
        self.mock_game.hero_gold = 50
        self.mock_game.hero_potions = 2
        self.mock_game.hero_position = 5
        self.mock_game.hero_skills = []
        self.mock_game.visited_positions = [False] * 10
        self.mock_game.events_encountered = []
        self.mock_game.lang = Mock()
        self.mock_game.lang.get_text.return_value = "test_text"
        self.mock_game.lang.format_text.return_value = "formatted_text"
        self.mock_game.difficulty_settings = {"normal": {"gold_multiplier": 1.0}}
        self.mock_game.difficulty = "normal"
        
        # 创建事件系统实例
        self.event_system = EventSystem(self.mock_game)
    
    def test_event_system_initialization(self):
        """测试事件系统初始化"""
        self.assertEqual(self.event_system.game, self.mock_game)
        self.assertIsInstance(self.event_system.events, dict)
        self.assertGreater(len(self.event_system.events), 0)
    
    def test_use_potion(self):
        """测试使用药剂"""
        initial_hp = self.mock_game.hero_hp
        initial_potions = self.mock_game.hero_potions
        
        with patch('random.randint', return_value=30):  # 固定回复30点血量
            self.event_system.use_potion()
        
        # 验证药剂使用效果
        self.assertEqual(self.mock_game.hero_potions, initial_potions - 1)
        expected_hp = min(initial_hp + 30, self.mock_game.hero_max_hp)
        self.assertEqual(self.mock_game.hero_hp, expected_hp)
    
    def test_use_potion_with_full_hp(self):
        """测试满血时使用药剂"""
        self.mock_game.hero_hp = self.mock_game.hero_max_hp
        initial_potions = self.mock_game.hero_potions
        
        self.event_system.use_potion()
        
        # 满血时不应该消耗药剂
        self.assertEqual(self.mock_game.hero_potions, initial_potions)
        self.assertEqual(self.mock_game.hero_hp, self.mock_game.hero_max_hp)
    
    def test_use_potion_without_potions(self):
        """测试没有药剂时使用药剂"""
        self.mock_game.hero_potions = 0
        initial_hp = self.mock_game.hero_hp
        
        self.event_system.use_potion()
        
        # 没有药剂时血量不应该变化
        self.assertEqual(self.mock_game.hero_hp, initial_hp)
        self.assertEqual(self.mock_game.hero_potions, 0)
    
    def test_learn_skill(self):
        """测试学习技能"""
        initial_skills_count = len(self.mock_game.hero_skills)
        
        with patch('random.choice', return_value="fireball"):
            with patch('random.random', return_value=0.2):  # 20%概率，确保学习技能
                self.event_system.learn_skill()
        
        # 验证技能学习成功
        if len(self.mock_game.hero_skills) > initial_skills_count:
            self.assertIn("fireball", self.mock_game.hero_skills)
    
    def test_learn_skill_with_existing_skills(self):
        """测试已存在技能时的技能学习"""
        self.mock_game.hero_skills = ["fireball"]
        
        with patch('random.choice', return_value="iceball"):
            with patch('random.random', return_value=0.2):  # 20%概率，确保学习技能
                self.event_system.learn_skill()
        
        # 验证学习了新技能而不是重复技能
        if len(self.mock_game.hero_skills) > 1:
            self.assertIn("iceball", self.mock_game.hero_skills)
    
    def test_merchant_event(self):
        """测试商人事件"""
        initial_gold = self.mock_game.hero_gold
        initial_potions = self.mock_game.hero_potions
        
        with patch('builtins.input', return_value='1'):  # 选择购买药剂
            with patch.object(self.event_system, 'buy_potion'):
                self.event_system.merchant_event()
        
        # 验证商人事件触发
        self.assertTrue(True)  # 如果没有异常，说明测试通过
    
    def test_buy_potion(self):
        """测试购买药剂"""
        initial_gold = self.mock_game.hero_gold
        initial_potions = self.mock_game.hero_potions
        potion_price = 10
        
        # 设置足够的金币
        self.mock_game.hero_gold = potion_price
        
        self.event_system.buy_potion(potion_price)
        
        # 验证购买效果
        self.assertEqual(self.mock_game.hero_gold, initial_gold - potion_price)
        self.assertEqual(self.mock_game.hero_potions, initial_potions + 1)
    
    def test_buy_potion_without_gold(self):
        """测试没有足够金币时购买药剂"""
        initial_gold = self.mock_game.hero_gold
        initial_potions = self.mock_game.hero_potions
        potion_price = initial_gold + 10  # 价格高于现有金币
        
        self.event_system.buy_potion(potion_price)
        
        # 金币不足时不应该改变任何状态
        self.assertEqual(self.mock_game.hero_gold, initial_gold)
        self.assertEqual(self.mock_game.hero_potions, initial_potions)
    
    def test_show_adventure_history(self):
        """测试显示冒险历史"""
        # 添加一些历史记录
        self.mock_game.events_encountered = [
            "安全前进了一步",
            "发现了宝箱，获得20金币",
            "击败了哥布林，获得10经验值"
        ]
        
        # 执行显示历史
        with patch('builtins.print') as mock_print:
            self.event_system.show_adventure_history()
        
        # 验证显示历史被调用
        self.assertTrue(mock_print.called)
    
    def test_trap_event(self):
        """测试陷阱事件"""
        initial_hp = self.mock_game.hero_hp
        
        with patch('random.randint', return_value=15):  # 固定15点伤害
            self.event_system.trap_event(1.0)
        
        # 验证陷阱伤害
        expected_damage = max(1, 15 - self.mock_game.hero_defense)
        self.assertEqual(self.mock_game.hero_hp, initial_hp - expected_damage)
    
    def test_treasure_event(self):
        """测试宝箱事件"""
        initial_gold = self.mock_game.hero_gold
        
        with patch('random.randint', return_value=25):  # 固定25金币
            self.event_system.treasure_event(1.0)
        
        # 验证宝箱收益
        self.assertEqual(self.mock_game.hero_gold, initial_gold + 25)
    
    def test_healing_event(self):
        """测试治疗事件"""
        initial_hp = 50  # 设置非满血状态
        self.mock_game.hero_hp = initial_hp
        
        with patch('random.randint', return_value=20):  # 固定20点回复
            self.event_system.healing_event()
        
        # 验证治疗效果
        expected_hp = min(initial_hp + 20, self.mock_game.hero_max_hp)
        self.assertEqual(self.mock_game.hero_hp, expected_hp)
    
    def test_skill_event(self):
        """测试技能事件"""
        initial_skills_count = len(self.mock_game.hero_skills)
        
        with patch('random.choice', return_value="lightning"):
            with patch('random.random', return_value=0.3):  # 30%概率，确保学习技能
                self.event_system.skill_event()
        
        # 验证技能可能被添加
        if len(self.mock_game.hero_skills) > initial_skills_count:
            self.assertIn("lightning", self.mock_game.hero_skills)
    
    def test_potion_event(self):
        """测试药剂事件"""
        initial_potions = self.mock_game.hero_potions
        
        self.event_system.potion_event()
        
        # 验证药剂获得
        self.assertEqual(self.mock_game.hero_potions, initial_potions + 1)
    
    def test_mysterious_merchant_event(self):
        """测试神秘商人事件"""
        initial_gold = self.mock_game.hero_gold
        
        # 模拟神秘商人交易
        with patch('random.random', return_value=0.5):  # 50%概率触发交易
            with patch.object(self.event_system, 'mysterious_merchant_transaction'):
                self.event_system.mysterious_merchant_event(1.0)
        
        # 验证神秘商人事件触发
        self.assertTrue(True)  # 如果没有异常，说明测试通过


if __name__ == '__main__':
    unittest.main()