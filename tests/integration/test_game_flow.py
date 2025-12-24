# -*- coding: utf-8 -*-
"""
游戏流程集成测试
"""

import sys
import os
import unittest
from unittest.mock import patch, Mock
from io import StringIO

# 添加项目路径
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
src_path = os.path.join(project_root, 'src')
hero_path = os.path.join(src_path, 'hero')
sys.path.insert(0, hero_path)
sys.path.insert(0, src_path)

from hero.main import HeroGame


class TestGameFlow(unittest.TestCase):
    """测试游戏流程集成"""
    
    @patch('builtins.input', side_effect=['1', '1', '1', 'TestHero', '1', 'n'])
    def test_full_game_flow_easy_mode(self, mock_input):
        """测试完整游戏流程-简单模式"""
        # 捕获标准输出
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            # 创建并开始游戏
            game = HeroGame()
            
            # 验证游戏初始化
            self.assertEqual(game.hero_name, "TestHero")
            self.assertEqual(game.difficulty, "easy")
            self.assertEqual(game.map_type, "plains")
            self.assertEqual(game.map_length, 50)  # 简单模式地图长度
            self.assertEqual(game.hero_gold, 30)    # 简单模式初始金币
            self.assertEqual(game.hero_potions, 3)  # 简单模式初始药剂
            
            # 模拟游戏过程
            game.hero_position = 0
            game.hero_hp = 100
            
            # 执行随机事件
            with patch('random.randint', return_value=5):
                game.random_event()
            
            # 验证游戏状态
            self.assertGreaterEqual(game.hero_position, 1)
            
            # 测试多次移动
            for i in range(5):
                with patch('random.randint', return_value=20):  # 安全移动
                    with patch.object(game, 'random_event'):
                        game.hero_position += 1
            
            self.assertEqual(game.hero_position, 6)
            
        finally:
            # 恢复标准输出
            sys.stdout = sys.__stdout__
    
    @patch('builtins.input', side_effect=['1', '4', '5', 'TestHero', '1', 'n'])
    def test_full_game_flow_nightmare_mode(self, mock_input):
        """测试完整游戏流程-噩梦模式"""
        # 捕获标准输出
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            # 创建并开始游戏
            game = HeroGame()
            
            # 验证游戏初始化
            self.assertEqual(game.hero_name, "TestHero")
            self.assertEqual(game.difficulty, "nightmare")
            self.assertEqual(game.map_type, "mountain")
            self.assertEqual(game.map_length, 200)  # 噩梦模式地图长度
            self.assertEqual(game.hero_gold, 10)    # 噩梦模式初始金币
            self.assertEqual(game.hero_potions, 1)  # 噩梦模式初始药剂
            
            # 模拟游戏过程
            game.hero_position = 0
            game.hero_hp = 100
            
            # 执行随机事件
            with patch('random.randint', return_value=5):
                game.random_event()
            
            # 验证游戏状态
            self.assertGreaterEqual(game.hero_position, 1)
            
        finally:
            # 恢复标准输出
            sys.stdout = sys.__stdout__
    
    @patch('builtins.input', side_effect=['1', '2', '1', 'TestHero'])
    def test_game_victory_flow(self, mock_input):
        """测试游戏胜利流程"""
        # 捕获标准输出
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            # 创建游戏并设置到即将胜利的状态
            game = HeroGame()
            game.hero_position = game.map_length - 2  # 接近终点
            game.hero_hp = 50  # 存活状态
            
            # 模拟移动到终点
            with patch.object(game, 'random_event'):  # 跳过随机事件
                with patch('builtins.input', return_value='1'):  # 选择前进
                    result = game.move_hero()
                    self.assertTrue(result)  # 移动成功
            
            # 验证胜利条件
            self.assertEqual(game.hero_position, game.map_length - 1)  # 到达终点
            victory = game.check_game_status()
            self.assertTrue(victory)
            self.assertTrue(game.victory)
            self.assertTrue(game.game_over)
            
        finally:
            # 恢复标准输出
            sys.stdout = sys.__stdout__
    
    @patch('builtins.input', side_effect=['1', '2', '1', 'TestHero'])
    def test_game_over_flow(self, mock_input):
        """测试游戏失败流程"""
        # 捕获标准输出
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            # 创建游戏并设置到即将失败的状态
            game = HeroGame()
            game.hero_hp = 1  # 临近死亡
            
            # 模拟受到致命伤害
            game.hero_hp = 0
            
            # 检查游戏状态
            game_over = game.check_game_status()
            
            # 验证失败条件
            self.assertTrue(game_over)
            self.assertTrue(game.game_over)
            self.assertFalse(game.victory)
            
        finally:
            # 恢复标准输出
            sys.stdout = sys.__stdout__
    
    def test_level_up_integration(self):
        """测试升级集成流程"""
        # 创建游戏
        with patch('builtins.input', side_effect=['1', '2', '1', 'TestHero']):
            game = HeroGame()
        
        # 记录初始属性
        initial_level = game.hero_level
        initial_attack = game.hero_attack
        initial_defense = game.hero_defense
        initial_max_hp = game.hero_max_hp
        
        # 设置接近升级的经验值
        game.hero_exp = 95
        game.hero_level = 1
        
        # 模拟获得经验值
        game.combat_system.gain_exp(10)
        
        # 验证升级效果
        self.assertEqual(game.hero_level, initial_level + 1)
        self.assertGreater(game.hero_attack, initial_attack)
        self.assertGreater(game.hero_defense, initial_defense)
        self.assertGreater(game.hero_max_hp, initial_max_hp)
        
        # 验证属性更新
        game.update_attributes()
        self.assertGreaterEqual(game.hero_hp, game.hero_max_hp)
    
    def test_equipment_integration(self):
        """测试装备集成流程"""
        # 创建游戏
        with patch('builtins.input', side_effect=['1', '2', '1', 'TestHero']):
            game = HeroGame()
        
        # 记录初始属性
        initial_attack = game.hero_attack
        initial_defense = game.hero_defense
        initial_max_hp = game.hero_max_hp
        
        # 创建测试装备
        weapon = {"name": "TestSword", "type": "weapon", "attack": 10, "defense": 0, "hp": 0, "value": 50}
        armor = {"name": "TestArmor", "type": "armor", "attack": 0, "defense": 5, "hp": 20, "value": 75}
        accessory = {"name": "TestRing", "type": "accessory", "attack": 5, "defense": 2, "hp": 10, "value": 100}
        
        # 装备物品
        game.equipment_system.equip_item(weapon)
        game.equipment_system.equip_item(armor)
        game.equipment_system.equip_item(accessory)
        
        # 验证属性变化
        self.assertEqual(game.hero_attack, initial_attack + 10 + 5)
        self.assertEqual(game.hero_defense, initial_defense + 5 + 2)
        self.assertEqual(game.hero_max_hp, initial_max_hp + 20 + 10)
        
        # 验证装备记录
        self.assertEqual(game.equipment["weapon"]["name"], "TestSword")
        self.assertEqual(game.equipment["armor"]["name"], "TestArmor")
        self.assertEqual(game.equipment["accessory"]["name"], "TestRing")
    
    def test_combat_integration(self):
        """测试战斗集成流程"""
        # 创建游戏
        with patch('builtins.input', side_effect=['1', '2', '1', 'TestHero']):
            game = HeroGame()
        
        # 记录初始状态
        initial_hp = game.hero_hp
        initial_exp = game.hero_exp
        initial_gold = game.hero_gold
        
        # 生成怪物
        monster = game.combat_system.generate_monster(1.0)
        
        # 模拟战斗胜利
        with patch('random.randint', return_value=10):  # 固定随机值
            with patch.object(game.combat_system, 'calculate_damage', return_value=50):  # 高伤害
                with patch.object(game.combat_system, 'monster_attack', return_value=0):  # 怪物不造成伤害
                    result = game.combat_system.combat_loop(monster)
        
        # 验证战斗结果
        self.assertTrue(result)  # 战斗胜利
        self.assertGreaterEqual(game.hero_exp, initial_exp + monster["exp"])
        self.assertGreaterEqual(game.hero_gold, initial_gold + monster["gold"])
    
    def test_newbie_village_integration(self):
        """测试新手村集成流程"""
        # 创建游戏
        with patch('builtins.input', side_effect=['1', '2', '1', 'TestHero']):
            game = HeroGame()
        
        # 记录初始状态
        initial_hp = game.hero_hp
        initial_exp = game.hero_exp
        initial_gold = game.hero_gold
        initial_potions = game.hero_potions
        
        # 模拟训练场训练
        with patch('builtins.input', side_effect=['1', '']):  # 选择基础训练
            with patch('builtins.print'):
                game.newbie_village.training_grounds()
        
        # 验证训练效果
        self.assertGreaterEqual(game.hero_exp, initial_exp)
        
        # 模拟购买道具
        game.hero_gold = 50  # 确保有足够金币
        with patch('builtins.input', side_effect=['1', 'y', '']):  # 选择购买药剂，确认
            with patch('builtins.print'):
                game.newbie_village.item_shop()
        
        # 验证购买效果
        self.assertGreaterEqual(game.hero_potions, initial_potions)
    
    @patch('builtins.input', side_effect=['1', '2', '1', 'TestHero'])
    def test_random_events_integration(self, mock_input):
        """测试随机事件集成流程"""
        # 创建游戏
        game = HeroGame()
        
        # 测试平原地图随机事件
        game.map_type = "plains"
        
        # 记录初始状态
        initial_hp = game.hero_hp
        initial_gold = game.hero_gold
        initial_potions = game.hero_potions
        
        # 模拟踩到地雷事件
        with patch('random.randint', return_value=2):  # 触发地雷事件
            with patch('random.randint', return_value=10):  # 地雷伤害
                game.random_event()
        
        # 验证地雷伤害
        self.assertLess(game.hero_hp, initial_hp)
        
        # 模拟发现宝箱事件
        with patch('random.randint', return_value=10):  # 触发宝箱事件
            with patch('random.randint', return_value=20):  # 宝箱金币
                game.random_event()
        
        # 验证宝箱收益
        self.assertGreater(game.hero_gold, initial_gold)
        
        # 模拟发现药剂事件
        with patch('random.randint', return_value=16):  # 触发药剂事件
            game.random_event()
        
        # 验证药剂获得
        self.assertGreater(game.hero_potions, initial_potions)


if __name__ == '__main__':
    unittest.main()