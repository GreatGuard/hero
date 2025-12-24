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
        with patch('builtins.input', side_effect=['1', '2', '1', '']):
            with patch.object(HeroGame, 'clear_screen'):
                with patch.object(HeroGame, 'show_welcome'):
                    self.game = HeroGame()
                    self.game.hero_name = "TestHero"  # 直接设置英雄名字
    
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
    
    def test_language_selection_chinese(self):
        """测试语言选择-中文"""
        with patch('builtins.input', return_value='1'):
            with patch.object(HeroGame, 'clear_screen'):
                with patch.object(HeroGame, 'select_map_and_difficulty'):
                    game = HeroGame()
                    game.select_language()
                    self.assertEqual(game.language, "zh")
    
    def test_language_selection_english(self):
        """测试语言选择-英文"""
        with patch('builtins.input', return_value='2'):
            with patch.object(HeroGame, 'clear_screen'):
                with patch.object(HeroGame, 'select_map_and_difficulty'):
                    game = HeroGame()
                    game.select_language()
                    self.assertEqual(game.language, "en")
    
    def test_clear_screen(self):
        """测试清屏功能"""
        with patch('os.system') as mock_system:
            self.game.clear_screen()
            mock_system.assert_called_once()
    
    def test_show_hero_info(self):
        """测试显示英雄信息"""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.game.show_hero_info()
        
        output = captured_output.getvalue()
        self.assertIn(self.game.hero_name, output)
        self.assertIn(str(self.game.hero_hp), output)
        self.assertIn(str(self.game.hero_attack), output)
        
        sys.stdout = sys.__stdout__
    
    def test_draw_map(self):
        """测试绘制地图"""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.game.hero_position = 2
        self.game.map_length = 5
        
        self.game.draw_map()
        
        output = captured_output.getvalue()
        self.assertTrue(output.count("[") >= 5)
        self.assertTrue(output.count("]") >= 5)
        
        sys.stdout = sys.__stdout__
    
    def test_move_hero_forward(self):
        """测试英雄前进"""
        initial_position = self.game.hero_position
        
        with patch('builtins.input', return_value='1'):
            with patch.object(self.game, 'random_event'):
                result = self.game.move_hero()
        
        self.assertEqual(self.game.hero_position, initial_position + 1)
        self.assertTrue(result)
    
    def test_move_hero_at_end(self):
        """测试英雄在终点时尝试前进"""
        self.game.hero_position = self.game.map_length - 2
        
        with patch('builtins.input', return_value='1'):
            with patch.object(self.game, 'random_event'):
                result = self.game.move_hero()
        
        self.assertEqual(self.game.hero_position, self.game.map_length - 1)
        self.assertTrue(result)
        
        with patch('builtins.input', return_value='1'):
            result = self.game.move_hero()
        
        self.assertEqual(self.game.hero_position, self.game.map_length - 1)
        self.assertFalse(result)
    
    def test_move_hero_view_status(self):
        """测试查看状态"""
        # 第一个输入 '2' 查看状态，第二个输入 '1' 前进
        with patch('builtins.input', side_effect=['2', '1']):
            with patch('random.randint', return_value=25):  # 触发安全事件
                result = self.game.move_hero()

        self.assertTrue(result)
    
    def test_move_hero_view_history(self):
        """测试查看历史"""
        with patch('builtins.input', side_effect=['3', '', '1']):
            with patch.object(self.game.event_system, 'show_adventure_history') as mock_show_history:
                with patch('random.randint', return_value=25):  # 触发安全事件
                    result = self.game.move_hero()
                    mock_show_history.assert_called_once()
        
        self.assertTrue(result)
    
    def test_move_hero_use_potion(self):
        """测试使用药剂"""
        self.game.hero_potions = 1

        # 路径：'4' 使用药剂，'2' 查看状态，'1' 前进（触发安全事件）
        # 使用 patch 让 random.randint 返回 25，触发安全事件（不需要战斗输入）
        with patch('builtins.input', side_effect=['4', '2', '1']):
            with patch.object(self.game.event_system, 'use_potion') as mock_use_potion:
                with patch('random.randint', return_value=25):  # 触发安全事件
                    result = self.game.move_hero()
                    mock_use_potion.assert_called_once()

        self.assertTrue(result)
    
    def test_move_hero_shop(self):
        """测试商店"""
        # 第一个输入 '5' 打开商店，第二个输入 '2' 查看状态，第三个输入 '1' 前进（触发安全事件）
        with patch('builtins.input', side_effect=['5', '2', '1']):
            with patch.object(self.game.event_system, 'merchant_event') as mock_merchant:
                with patch('random.randint', return_value=25):  # 触发安全事件
                    result = self.game.move_hero()
                    mock_merchant.assert_called_once()

        self.assertTrue(result)
    
    def test_move_hero_equipment_management(self):
        """测试装备管理"""
        # 第一个输入 '6' 打开装备管理，第二个输入 '1' 前进并返回 True
        with patch('builtins.input', side_effect=['6', '1']):
            with patch.object(self.game.equipment_system, 'equipment_management') as mock_eq_mgmt:
                with patch('random.randint', return_value=25):  # 触发安全事件
                    result = self.game.move_hero()
                    mock_eq_mgmt.assert_called_once()

        self.assertTrue(result)
    
    def test_update_attributes_with_weapon(self):
        """测试属性更新-武器"""
        weapon = {"name": "TestSword", "attack": 10, "defense": 0, "hp": 0}
        self.game.equipment["weapon"] = weapon
        self.game.update_attributes()
        
        expected_attack = self.game.base_attack + 10
        self.assertEqual(self.game.hero_attack, expected_attack)
    
    def test_update_attributes_with_armor(self):
        """测试属性更新-防具"""
        armor = {"name": "TestArmor", "attack": 0, "defense": 5, "hp": 20}
        self.game.equipment["armor"] = armor
        self.game.update_attributes()
        
        expected_defense = self.game.base_defense + 5
        expected_max_hp = self.game.base_max_hp + 20
        self.assertEqual(self.game.hero_defense, expected_defense)
        self.assertEqual(self.game.hero_max_hp, expected_max_hp)
    
    def test_update_attributes_with_multiple_equipment(self):
        """测试属性更新-多件装备"""
        weapon = {"name": "TestSword", "attack": 10, "defense": 0, "hp": 0}
        armor = {"name": "TestArmor", "attack": 0, "defense": 5, "hp": 20}
        accessory = {"name": "TestRing", "attack": 5, "defense": 2, "hp": 10}
        
        self.game.equipment["weapon"] = weapon
        self.game.equipment["armor"] = armor
        self.game.equipment["accessory"] = accessory
        self.game.update_attributes()
        
        expected_attack = self.game.base_attack + 10 + 5
        expected_defense = self.game.base_defense + 5 + 2
        expected_max_hp = self.game.base_max_hp + 20 + 10
        
        self.assertEqual(self.game.hero_attack, expected_attack)
        self.assertEqual(self.game.hero_defense, expected_defense)
        self.assertEqual(self.game.hero_max_hp, expected_max_hp)
    
    def test_update_attributes_hp_cap(self):
        """测试属性更新-HP不超过最大值"""
        self.game.hero_hp = 150  # 设置为大于更新后的 hero_max_hp (80 + 50 = 130)
        self.game.base_max_hp = 80

        armor = {"name": "TestArmor", "attack": 0, "defense": 0, "hp": 50}
        self.game.equipment["armor"] = armor
        self.game.update_attributes()

        self.assertEqual(self.game.hero_hp, self.game.hero_max_hp)  # hero_hp 应该被限制为 130
    
    def test_check_game_status_game_over(self):
        """测试游戏结束状态"""
        self.game.hero_hp = 0

        with patch('builtins.input'):
            result = self.game.check_game_status()

        self.assertTrue(result)
        self.assertTrue(self.game.game_over)
    
    def test_check_game_status_victory(self):
        """测试游戏胜利状态"""
        self.game.hero_position = self.game.map_length - 1

        with patch('builtins.input'):
            result = self.game.check_game_status()

        self.assertTrue(result)
        self.assertTrue(self.game.victory)
        self.assertTrue(self.game.game_over)
    
    def test_check_game_status_continue(self):
        """测试游戏继续状态"""
        self.game.hero_hp = 50
        self.game.hero_position = 5
        
        result = self.game.check_game_status()
        
        self.assertFalse(result)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.victory)
    
    def test_restart_game_yes(self):
        """测试重新开始游戏-选择是"""
        with patch('builtins.input', return_value='y'):
            with patch.object(HeroGame, '__init__'):
                with patch.object(self.game, 'start_game'):
                    self.game.restart_game()
    
    def test_restart_game_no(self):
        """测试重新开始游戏-选择否"""
        with patch('builtins.input', return_value='n'):
            with patch('sys.exit') as mock_exit:
                self.game.restart_game()
        
        mock_exit.assert_called_once_with(0)
    
    def test_random_event_plains_safe_move(self):
        """测试随机事件-平原安全移动"""
        self.game.map_type = "plains"
        self.game.difficulty = "normal"
        self.game.difficulty_settings = {
            "normal": {"enemy_multiplier": 1.0, "gold_multiplier": 1.0}
        }
        
        initial_hp = self.game.hero_hp
        initial_gold = self.game.hero_gold
        
        with patch('random.randint', return_value=30):  # 触发安全移动
            with patch('builtins.print'):
                self.game.random_event()
        
        # 安全移动不应该影响属性
        self.assertEqual(self.game.hero_hp, initial_hp)
        self.assertEqual(self.game.hero_gold, initial_gold)
    
    def test_random_event_plains_mine_trap(self):
        """测试随机事件-平原地雷"""
        self.game.map_type = "plains"
        self.game.difficulty = "normal"
        self.game.difficulty_settings = {
            "normal": {"enemy_multiplier": 1.0, "gold_multiplier": 1.0}
        }
        
        initial_hp = self.game.hero_hp
        
        with patch('random.randint', return_value=2):  # 触发地雷
            with patch('builtins.print'):
                with patch.object(self.game, 'show_hero_info'):
                    self.game.random_event()
        
        # 地雷应该减少HP
        self.assertLess(self.game.hero_hp, initial_hp)
    
    def test_random_event_plains_find_chest(self):
        """测试随机事件-平原宝箱"""
        self.game.map_type = "plains"
        self.game.difficulty = "normal"
        self.game.difficulty_settings = {
            "normal": {"enemy_multiplier": 1.0, "gold_multiplier": 1.0}
        }
        
        initial_gold = self.game.hero_gold
        
        with patch('random.randint', return_value=10):  # 触发宝箱
            with patch('builtins.print'):
                with patch.object(self.game, 'show_hero_info'):
                    self.game.random_event()
        
        # 宝箱应该增加金币
        self.assertGreater(self.game.hero_gold, initial_gold)
    
    def test_show_welcome(self):
        """测试显示欢迎界面"""
        captured_output = StringIO()
        sys.stdout = captured_output

        with patch('builtins.input', return_value=''):  # 模拟用户按回车继续
            self.game.show_welcome()

        output = captured_output.getvalue()
        # 检查输出包含欢迎相关的内容（中英文兼容）
        self.assertTrue("英雄无敌" in output or "welcome" in output.lower())

        sys.stdout = sys.__stdout__
    
    def test_get_hero_name(self):
        """测试获取英雄名字"""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        with patch('builtins.input', return_value='TestName'):
            with patch.object(self.game, 'clear_screen'):
                self.game.get_hero_name()
        
        self.assertEqual(self.game.hero_name, 'TestName')
        
        sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()
