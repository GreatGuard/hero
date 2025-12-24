# -*- coding: utf-8 -*-
"""
主游戏类测试
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# 添加项目路径
project_root = os.path.join(os.path.dirname(__file__), '..')
src_path = os.path.join(project_root, 'src')
hero_path = os.path.join(src_path, 'hero')
sys.path.insert(0, hero_path)
sys.path.insert(0, src_path)

from hero.main import HeroGame


class TestHeroGame(unittest.TestCase):
    """测试主游戏类"""
    
    def setUp(self):
        """测试数据准备"""
        # 模拟输入，跳过语言和设置选择
        with patch('builtins.input', side_effect=['1', '2', '1', 'TestHero']):
            with patch.object(HeroGame, 'clear_screen'):
                with patch.object(HeroGame, 'show_welcome'):
                    self.game = HeroGame()
    
    def test_game_initialization(self):
        """测试游戏初始化"""
        # 验证基本属性初始化
        self.assertEqual(self.game.hero_name, "TestHero")
        self.assertEqual(self.game.hero_hp, 100)
        self.assertEqual(self.game.hero_max_hp, 100)
        self.assertEqual(self.game.hero_attack, 20)
        self.assertEqual(self.game.hero_defense, 5)
        self.assertEqual(self.game.hero_position, 0)
        self.assertEqual(self.game.hero_exp, 0)
        self.assertEqual(self.game.hero_level, 1)
        self.assertIsInstance(self.game.hero_skills, list)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.victory)
        
        # 验证装备初始化
        self.assertIsNone(self.game.equipment["weapon"])
        self.assertIsNone(self.game.equipment["armor"])
        self.assertIsNone(self.game.equipment["accessory"])
        self.assertIsInstance(self.game.inventory, list)
        
        # 验证子系统初始化
        self.assertIsNotNone(self.game.combat_system)
        self.assertIsNotNone(self.game.equipment_system)
        self.assertIsNotNone(self.game.event_system)
        self.assertIsNotNone(self.game.newbie_village)
    
    def test_language_selection(self):
        """测试语言选择"""
        # 测试中文选择
        with patch('builtins.input', return_value='1'):
            with patch.object(HeroGame, 'clear_screen'):
                with patch.object(HeroGame, 'select_map_and_difficulty'):
                    game = HeroGame()
                    game.select_language()
                    self.assertEqual(game.language, "zh")
        
        # 测试英文选择
        with patch('builtins.input', return_value='2'):
            with patch.object(HeroGame, 'clear_screen'):
                with patch.object(HeroGame, 'select_map_and_difficulty'):
                    game = HeroGame()
                    game.select_language()
                    self.assertEqual(game.language, "en")
    
    def test_difficulty_selection(self):
        """测试难度选择"""
        # 测试各难度选择
        test_cases = [
            ('1', 'easy'),
            ('2', 'normal'),
            ('3', 'hard'),
            ('4', 'nightmare')
        ]
        
        for input_choice, expected_difficulty in test_cases:
            with patch('builtins.input', return_value=input_choice):
                with patch.object(HeroGame, 'clear_screen'):
                    with patch.object(HeroGame, 'select_map_type'):
                        game = HeroGame()
                        game.difficulty_settings = {
                            "easy": {"map_length": 50, "gold_start": 30, "potions_start": 3},
                            "normal": {"map_length": 100, "gold_start": 20, "potions_start": 2},
                            "hard": {"map_length": 150, "gold_start": 15, "potions_start": 1},
                            "nightmare": {"map_length": 200, "gold_start": 10, "potions_start": 1}
                        }
                        game.select_difficulty()
                        self.assertEqual(game.difficulty, expected_difficulty)
    
    def test_map_type_selection(self):
        """测试地图类型选择"""
        # 测试各地图类型选择
        test_cases = [
            ('1', 'plains'),
            ('2', 'forest'),
            ('3', 'desert'),
            ('4', 'dungeon'),
            ('5', 'mountain')
        ]
        
        for input_choice, expected_map_type in test_cases:
            with patch('builtins.input', return_value=input_choice):
                with patch.object(HeroGame, 'clear_screen'):
                    game = HeroGame()
                    game.map_types = {
                        "plains": {"name": "plains"},
                        "forest": {"name": "forest"},
                        "desert": {"name": "desert"},
                        "dungeon": {"name": "dungeon"},
                        "mountain": {"name": "mountain"}
                    }
                    game.select_map_type()
                    self.assertEqual(game.map_type, expected_map_type)
    
    def test_clear_screen(self):
        """测试清屏功能"""
        # 测试清屏函数被调用
        with patch('os.system') as mock_system:
            self.game.clear_screen()
            mock_system.assert_called_once()
    
    def test_show_hero_info(self):
        """测试显示英雄信息"""
        # 捕获标准输出
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # 显示英雄信息
        self.game.show_hero_info()
        
        # 验证输出内容
        output = captured_output.getvalue()
        self.assertIn(self.game.hero_name, output)
        self.assertIn(str(self.game.hero_hp), output)
        self.assertIn(str(self.game.hero_attack), output)
        
        # 恢复标准输出
        sys.stdout = sys.__stdout__
    
    def test_draw_map(self):
        """测试绘制地图"""
        # 捕获标准输出
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # 设置游戏位置
        self.game.hero_position = 2
        self.game.map_length = 5
        
        # 绘制地图
        self.game.draw_map()
        
        # 验证输出内容
        output = captured_output.getvalue()
        # 英雄标记应该出现在正确位置
        self.assertTrue(output.count("[") == 5)  # 5个位置
        self.assertTrue(output.count("]") == 5)  # 5个位置
        
        # 恢复标准输出
        sys.stdout = sys.__stdout__
    
    def test_move_hero_forward(self):
        """测试英雄前进"""
        initial_position = self.game.hero_position
        
        # 模拟选择前进
        with patch('builtins.input', return_value='1'):
            with patch.object(self.game, 'random_event'):
                result = self.game.move_hero()
        
        # 验证位置变化
        self.assertEqual(self.game.hero_position, initial_position + 1)
        self.assertTrue(result)
    
    def test_move_hero_at_end(self):
        """测试英雄在终点时尝试前进"""
        # 设置英雄在终点前一个位置
        self.game.hero_position = self.game.map_length - 2
        
        # 第一次前进应该成功
        with patch('builtins.input', return_value='1'):
            with patch.object(self.game, 'random_event'):
                result = self.game.move_hero()
        
        self.assertEqual(self.game.hero_position, self.game.map_length - 1)
        self.assertTrue(result)
        
        # 第二次尝试前进应该失败
        with patch('builtins.input', return_value='1'):
            result = self.game.move_hero()
        
        self.assertEqual(self.game.hero_position, self.game.map_length - 1)
        self.assertFalse(result)
    
    def test_move_hero_view_status(self):
        """测试查看状态"""
        with patch('builtins.input', return_value='2'):
            with patch.object(self.game, 'show_hero_info'):
                with patch.object(self.game, 'draw_map'):
                    result = self.game.move_hero()
        
        # 查看状态应该返回False，不继续游戏循环
        self.assertFalse(result)
    
    def test_move_hero_view_history(self):
        """测试查看历史"""
        with patch('builtins.input', return_value='3'):
            with patch.object(self.game.event_system, 'show_adventure_history'):
                result = self.game.move_hero()
        
        # 查看历史应该返回False，不继续游戏循环
        self.assertFalse(result)
    
    def test_move_hero_use_potion(self):
        """测试使用药剂"""
        # 设置有药剂
        self.game.hero_potions = 1
        
        with patch('builtins.input', return_value='4'):
            with patch.object(self.game.event_system, 'use_potion'):
                result = self.game.move_hero()
        
        # 使用药剂应该返回False，不继续游戏循环
        self.assertFalse(result)
    
    def test_move_hero_shop(self):
        """测试商店"""
        with patch('builtins.input', return_value='5'):
            with patch.object(self.game.event_system, 'merchant_event'):
                result = self.game.move_hero()
        
        # 访问商店应该返回False，不继续游戏循环
        self.assertFalse(result)
    
    def test_move_hero_equipment_management(self):
        """测试装备管理"""
        with patch('builtins.input', return_value='6'):
            with patch.object(self.game.equipment_system, 'equipment_management'):
                result = self.game.move_hero()
        
        # 装备管理应该返回False，不继续游戏循环
        self.assertFalse(result)
    
    def test_update_attributes(self):
        """测试属性更新"""
        # 装备武器
        weapon = {"name": "TestSword", "attack": 10, "defense": 0, "hp": 0}
        self.game.equipment["weapon"] = weapon
        
        # 更新属性
        self.game.update_attributes()
        
        # 验证属性更新
        expected_attack = self.game.base_attack + 10
        self.assertEqual(self.game.hero_attack, expected_attack)
    
    def test_check_game_status_game_over(self):
        """测试游戏结束状态"""
        # 设置血量为0
        self.game.hero_hp = 0
        
        # 检查游戏状态
        result = self.game.check_game_status()
        
        # 验证游戏结束
        self.assertTrue(result)
        self.assertTrue(self.game.game_over)
    
    def test_check_game_status_victory(self):
        """测试游戏胜利状态"""
        # 设置位置在终点
        self.game.hero_position = self.game.map_length - 1
        
        # 检查游戏状态
        result = self.game.check_game_status()
        
        # 验证游戏胜利
        self.assertTrue(result)
        self.assertTrue(self.game.victory)
        self.assertTrue(self.game.game_over)
    
    def test_check_game_status_continue(self):
        """测试游戏继续状态"""
        # 设置正常游戏状态
        self.game.hero_hp = 50
        self.game.hero_position = 5
        
        # 检查游戏状态
        result = self.game.check_game_status()
        
        # 验证游戏继续
        self.assertFalse(result)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.victory)
    
    def test_restart_game_yes(self):
        """测试重新开始游戏-选择是"""
        # 模拟选择重新开始
        with patch('builtins.input', return_value='y'):
            with patch.object(HeroGame, '__init__'):
                with patch.object(self.game, 'start_game'):
                    self.game.restart_game()
        
        # 验证重新开始游戏被调用
        # (由于模拟的__init__，这里主要测试流程)
    
    def test_restart_game_no(self):
        """测试重新开始游戏-选择否"""
        # 模拟选择不重新开始
        with patch('builtins.input', return_value='n'):
            with patch('sys.exit') as mock_exit:
                self.game.restart_game()
        
        # 验证退出被调用
        mock_exit.assert_called_once_with(0)


if __name__ == '__main__':
    unittest.main()