# -*- coding: utf-8 -*-
"""
战斗系统测试
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

from hero.combat import CombatSystem
from hero.main import HeroGame


class TestCombatSystem(unittest.TestCase):
    """测试战斗系统"""
    
    def setUp(self):
        """测试数据准备"""
        # 创建模拟游戏对象
        self.mock_game = Mock(spec=HeroGame)
        self.mock_game.hero_attack = 20
        self.mock_game.hero_defense = 5
        self.mock_game.hero_hp = 100
        self.mock_game.hero_max_hp = 100
        self.mock_game.hero_level = 1
        self.mock_game.hero_exp = 0
        self.mock_game.hero_gold = 0
        self.mock_game.hero_skills = []
        self.mock_game.lang = Mock()
        self.mock_game.lang.get_text.return_value = "test_text"
        self.mock_game.lang.format_text.return_value = "formatted_text"
        
        # 创建战斗系统实例
        self.combat_system = CombatSystem(self.mock_game)
    
    def test_combat_system_initialization(self):
        """测试战斗系统初始化"""
        self.assertEqual(self.combat_system.game, self.mock_game)
        self.assertIsInstance(self.combat_system.monsters, dict)
        self.assertIsInstance(self.combat_system.bosses, dict)
        self.assertGreater(len(self.combat_system.monsters), 0)
        self.assertGreater(len(self.combat_system.bosses), 0)
    
    def test_monster_generation(self):
        """测试怪物生成"""
        monster = self.combat_system.generate_monster(1.0)
        
        # 验证怪物属性
        self.assertIn("name", monster)
        self.assertIn("hp", monster)
        self.assertIn("max_hp", monster)
        self.assertIn("attack", monster)
        self.assertIn("defense", monster)
        self.assertIn("exp", monster)
        self.assertIn("gold", monster)
        
        # 验证属性值合理性
        self.assertGreater(monster["hp"], 0)
        self.assertEqual(monster["max_hp"], monster["hp"])
        self.assertGreater(monster["attack"], 0)
        self.assertGreaterEqual(monster["defense"], 0)
        self.assertGreater(monster["exp"], 0)
        self.assertGreater(monster["gold"], 0)
    
    def test_monster_generation_with_multiplier(self):
        """测试怪物生成的难度倍数影响"""
        monster_easy = self.combat_system.generate_monster(0.5)  # 简单难度
        monster_hard = self.combat_system.generate_monster(1.5)  # 困难难度
        
        # 困难模式的怪物应该更强
        self.assertGreaterEqual(monster_hard["hp"], monster_easy["hp"])
        self.assertGreaterEqual(monster_hard["attack"], monster_easy["attack"])
        self.assertGreaterEqual(monster_hard["exp"], monster_easy["exp"])
        self.assertGreaterEqual(monster_hard["gold"], monster_easy["gold"])
    
    def test_boss_generation(self):
        """测试Boss生成"""
        boss = self.combat_system.generate_boss(1.0)
        
        # 验证Boss属性
        self.assertIn("name", boss)
        self.assertIn("hp", boss)
        self.assertIn("max_hp", boss)
        self.assertIn("attack", boss)
        self.assertIn("defense", boss)
        self.assertIn("exp", boss)
        self.assertIn("gold", boss)
        
        # Boss应该比普通怪物更强
        normal_monster = self.combat_system.generate_monster(1.0)
        self.assertGreaterEqual(boss["hp"], normal_monster["hp"])
        self.assertGreaterEqual(boss["attack"], normal_monster["attack"])
        self.assertGreaterEqual(boss["exp"], normal_monster["exp"])
        self.assertGreaterEqual(boss["gold"], normal_monster["gold"])
    
    @patch('random.randint')
    def test_damage_calculation(self, mock_randint):
        """测试伤害计算"""
        # 设置随机数生成器返回固定值
        mock_randint.return_value = 5
        
        # 测试英雄对怪物的伤害
        monster = {"hp": 50, "defense": 5}
        damage = self.combat_system.calculate_damage(
            self.mock_game.hero_attack, monster["defense"]
        )
        
        # 验证伤害计算 (攻击力 - 防御力 + 随机值)
        expected_damage = max(1, self.mock_game.hero_attack - monster["defense"] + 5)
        self.assertEqual(damage, expected_damage)
        
        # 测试最小伤害保证
        monster["defense"] = 100  # 极高防御
        damage = self.combat_system.calculate_damage(
            self.mock_game.hero_attack, monster["defense"]
        )
        self.assertEqual(damage, 1)  # 最小伤害
    
    def test_combat_victory(self):
        """测试战斗胜利"""
        # 设置模拟战斗，英雄必定胜利
        monster = {
            "name": "TestMonster",
            "hp": 10,
            "max_hp": 10,
            "attack": 5,
            "defense": 0,
            "exp": 10,
            "gold": 10
        }
        
        initial_exp = self.mock_game.hero_exp
        initial_gold = self.mock_game.hero_gold
        
        # 模拟英雄每次攻击造成大量伤害
        with patch.object(self.combat_system, 'calculate_damage', return_value=15):
            # 模拟怪物不造成伤害
            with patch.object(self.combat_system, 'monster_attack', return_value=0):
                result = self.combat_system.combat_loop(monster)
        
        # 验证战斗胜利结果
        self.assertTrue(result)  # 应该返回True表示胜利
        self.assertGreater(self.mock_game.hero_exp, initial_exp)  # 经验值增加
        self.assertGreater(self.mock_game.hero_gold, initial_gold)  # 金币增加
    
    def test_combat_defeat(self):
        """测试战斗失败"""
        # 设置模拟战斗，英雄必定失败
        monster = {
            "name": "TestMonster",
            "hp": 50,
            "max_hp": 50,
            "attack": 100,
            "defense": 50,
            "exp": 10,
            "gold": 10
        }
        
        # 设置英雄初始血量较低
        self.mock_game.hero_hp = 10
        
        # 模拟英雄不造成伤害
        with patch.object(self.combat_system, 'calculate_damage', return_value=0):
            # 模拟怪物每次攻击造成致命伤害
            with patch.object(self.combat_system, 'calculate_damage', return_value=100):
                result = self.combat_system.combat_loop(monster)
        
        # 验证战斗失败结果
        self.assertFalse(result)  # 应该返回False表示失败
        self.assertLessEqual(self.mock_game.hero_hp, 0)  # 英雄血量归零
    
    def test_level_up_check(self):
        """测试升级检查"""
        # 设置接近升级的经验值
        self.mock_game.hero_exp = 95
        self.mock_game.hero_level = 1
        
        # 模拟获得经验值
        self.combat_system.gain_exp(10)
        
        # 验证升级
        self.assertEqual(self.mock_game.hero_level, 2)
        self.assertEqual(self.mock_game.hero_exp, 5)  # 经验值重置为多出的部分
        
        # 验证属性提升
        self.assertGreater(self.mock_game.base_attack, 20)  # 攻击力提升
        self.assertGreater(self.mock_game.base_defense, 5)   # 防御力提升
        self.assertGreater(self.mock_game.base_max_hp, 100) # 最大血量提升
        self.assertGreater(self.mock_game.hero_max_hp, 100) # 当前最大血量提升
    
    def test_monster_attack(self):
        """测试怪物攻击"""
        monster = {
            "name": "TestMonster",
            "attack": 15
        }
        
        initial_hp = self.mock_game.hero_hp
        
        with patch('random.randint', return_value=5):
            damage = self.combat_system.monster_attack(monster)
        
        # 验证伤害计算
        expected_damage = max(1, monster["attack"] - self.mock_game.hero_defense + 5)
        self.assertEqual(damage, expected_damage)
        self.assertEqual(self.mock_game.hero_hp, initial_hp - expected_damage)
    
    def test_skill_usage(self):
        """测试技能使用"""
        # 添加技能到英雄
        self.mock_game.hero_skills = ["fireball"]
        self.mock_game.hero_level = 3  # 足够的等级
        
        # 测试技能可用性
        skill_available = self.combat_system.can_use_skill("fireball")
        self.assertTrue(skill_available)
        
        # 测试技能使用效果
        monster = {"hp": 50, "max_hp": 50}
        with patch.object(self.combat_system, 'calculate_skill_damage', return_value=30):
            result = self.combat_system.use_skill("fireball", monster)
        
        self.assertTrue(result)  # 技能使用成功
        self.assertEqual(monster["hp"], 20)  # 怪物血量减少


if __name__ == '__main__':
    unittest.main()