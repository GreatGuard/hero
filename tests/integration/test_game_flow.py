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
    
    def setUp(self):
        """测试数据准备"""
        # 创建基本的 game 对象用于大多数测试
        # 需要提供足够的输入：语言，难度，地图，继续提示
        with patch('builtins.input', side_effect=['1', '2', '1', '']):
            with patch.object(HeroGame, 'clear_screen'):
                with patch.object(HeroGame, 'show_welcome'):
                    with patch.object(HeroGame, 'get_hero_name'):
                        with patch.object(HeroGame, 'select_hero_class'):  # 跳过职业选择
                            self.game = HeroGame()
                            # 手动设置名字和难度
                            self.game.hero_name = "TestHero"
                            self.game.difficulty = "normal"  # 手动设置难度
                            self.game.map_type = "plains"  # 手动设置地图类型
                            self.game.map_length = 100  # 手动设置地图长度
                            self.game.hero_gold = 20  # 手动设置金币
                            self.game.hero_potions = 2  # 手动设置药剂
    
    def create_test_game(self, difficulty='normal', map_type='plains'):
        """辅助方法：创建测试用的游戏对象"""
        with patch('builtins.input', side_effect=['1']):
            with patch.object(HeroGame, 'clear_screen'):
                with patch.object(HeroGame, 'show_welcome'):
                    with patch.object(HeroGame, 'get_hero_name'):
                        with patch.object(HeroGame, 'select_hero_class'):  # 跳过职业选择
                            game = HeroGame()
                            game.hero_name = "TestHero"
                            
                            # 设置难度
                            difficulty_map = {'1': 'easy', '2': 'normal', '3': 'hard', '4': 'nightmare'}
                            game.difficulty = difficulty_map.get(str(difficulty), difficulty)
                            
                            # 设置地图类型
                            map_type_map = {'1': 'plains', '2': 'forest', '3': 'desert', '4': 'dungeon',
                                           '5': 'mountain', '6': 'swamp', '7': 'snowfield'}
                            game.map_type = map_type_map.get(str(map_type), map_type)
                            
                            # 根据难度设置游戏参数
                            from hero.game_config import DIFFICULTY_SETTINGS, MAP_TYPES
                            game.difficulty_settings = DIFFICULTY_SETTINGS
                            game.map_types = MAP_TYPES
                            
                            settings = DIFFICULTY_SETTINGS[game.difficulty]
                            game.map_length = settings["map_length"]
                            game.hero_gold = settings["gold_start"]
                            game.hero_potions = settings["potions_start"]
        return game
    
    def test_full_game_flow_easy_mode(self):
        """测试完整游戏流程-简单模式"""
        game = self.create_test_game(difficulty='1', map_type='1')
        
        self.assertEqual(game.hero_name, "TestHero")
        self.assertEqual(game.difficulty, "easy")
        self.assertEqual(game.map_type, "plains")
        self.assertEqual(game.map_length, 50)
        self.assertEqual(game.hero_gold, 30)
        self.assertEqual(game.hero_potions, 3)
    
    def test_full_game_flow_nightmare_mode(self):
        """测试完整游戏流程-噩梦模式"""
        game = self.create_test_game(difficulty='4', map_type='5')
        
        self.assertEqual(game.hero_name, "TestHero")
        self.assertEqual(game.difficulty, "nightmare")
        self.assertEqual(game.map_type, "mountain")
        self.assertEqual(game.map_length, 200)
        self.assertEqual(game.hero_gold, 10)
        self.assertEqual(game.hero_potions, 1)
    
    def test_game_victory_flow(self):
        """测试游戏胜利流程"""
        game = self.game
        game.hero_position = game.map_length - 2
        game.hero_hp = 50
        
        with patch.object(game, 'random_event'):
            with patch('builtins.input', return_value='1'):
                result = game.move_hero()
                self.assertTrue(result)
        
        self.assertEqual(game.hero_position, game.map_length - 1)
        
        # patch input 避免在 pytest 中读取 stdin
        with patch('builtins.input', return_value=''):
            victory = game.check_game_status()
        
        self.assertTrue(victory)
        self.assertTrue(game.victory)
        self.assertTrue(game.game_over)
    
    def test_game_over_flow(self):
        """测试游戏失败流程"""
        game = self.game
        game.hero_hp = 1
        
        game.hero_hp = 0
        
        # patch input 避免在 pytest 中读取 stdin
        with patch('builtins.input', return_value=''):
            game_over = game.check_game_status()
        
        self.assertTrue(game_over)
        self.assertTrue(game.game_over)
        self.assertFalse(game.victory)
    
    def test_level_up_integration(self):
        """测试升级集成流程"""
        # 创建新的 game 对象，避免使用 setUp 的 game
        game = self.create_test_game(difficulty='2', map_type='1')
        
        # 设置初始状态
        game.hero_exp = 0
        game.hero_level = 1
        game.base_attack = 20
        game.base_defense = 5
        game.base_max_hp = 100
        
        # 更新属性以匹配基础值
        game.update_attributes()
        
        initial_level = game.hero_level
        initial_attack = game.hero_attack
        initial_defense = game.hero_defense
        initial_max_hp = game.hero_max_hp
        
        # 设置足够的经验值来升级（需要100点经验）
        game.hero_exp = 1000

        # 使用patch确保升级概率为100%，避免随机性影响测试
        # hero_exp = 1000 会触发 4 次升级（1->2->3->4->5），每次升级需要输入
        with patch('random.random', return_value=0.1):  # 小于0.3，触发学习技能
            with patch('builtins.input', side_effect=['', '', '', '']):  # 4 次升级需要 4 个输入
                with patch('builtins.print'):
                    game.combat_system.check_level_up()
        
        # 验证至少升级一次
        self.assertGreaterEqual(game.hero_level, initial_level + 1)
        self.assertGreater(game.hero_attack, initial_attack)
        self.assertGreater(game.hero_defense, initial_defense)
        self.assertGreater(game.hero_max_hp, initial_max_hp)
    
    def test_equipment_integration(self):
        """测试装备集成流程"""
        game = self.game
        
        initial_attack = game.hero_attack
        initial_defense = game.hero_defense
        initial_max_hp = game.hero_max_hp
        
        # 添加装备到背包
        weapon = {"name": "TestSword", "type": "weapon", "attack": 10, "defense": 0, "hp": 0, "value": 50}
        armor = {"name": "TestArmor", "type": "armor", "attack": 0, "defense": 5, "hp": 20, "value": 75}
        accessory = {"name": "TestRing", "type": "accessory", "attack": 5, "defense": 2, "hp": 10, "value": 100}
        
        game.inventory.append(weapon)
        game.inventory.append(armor)
        game.inventory.append(accessory)
        
        # 使用背包索引装备物品
        game.equipment_system.equip_item(0)
        game.equipment_system.equip_item(0)  # armor现在是索引0
        game.equipment_system.equip_item(0)  # accessory现在是索引0
        
        self.assertEqual(game.hero_attack, initial_attack + 10 + 5)
        self.assertEqual(game.hero_defense, initial_defense + 5 + 2)
        self.assertEqual(game.hero_max_hp, initial_max_hp + 20 + 10)
        
        self.assertEqual(game.equipment["weapon"]["name"], "TestSword")
        self.assertEqual(game.equipment["armor"]["name"], "TestArmor")
        self.assertEqual(game.equipment["accessory"]["name"], "TestRing")
    
    def test_newbie_village_integration(self):
        """测试新手村集成流程"""
        game = self.game
        
        initial_hp = game.hero_hp
        initial_exp = game.hero_exp
        initial_gold = game.hero_gold
        initial_potions = game.hero_potions
        
        # 使用 mock 来模拟战斗输入（选择攻击1）和继续提示（空字符串）
        # 使用循环返回值来模拟多个 input() 调用
        from unittest.mock import MagicMock
        def input_side_effect(*args, **kwargs):
            # 模拟所有可能的 input() 调用
            if not hasattr(input_side_effect, 'call_count'):
                input_side_effect.call_count = 0
            input_side_effect.call_count += 1
            
            # 返回值序列
            values = ['1', '1', '1', '']
            return values[min(input_side_effect.call_count - 1, len(values) - 1)]
        
        input_mock = MagicMock(side_effect=input_side_effect)
        with patch('builtins.input', input_mock):
            with patch('random.randint', return_value=15):
                with patch('random.random', return_value=0.5):  # 避免学习技能
                    with patch('builtins.print'):
                        with patch('time.sleep'):
                            game.newbie_village.practice_combat()
        
        self.assertGreaterEqual(game.hero_exp, initial_exp)
        
        game.hero_gold = 50
        with patch('builtins.input', side_effect=['1', '2', '']):
            with patch('builtins.print'):
                game.newbie_village.village_shop()
        
        self.assertGreaterEqual(game.hero_potions, initial_potions)
    
    def test_random_events_plains_integration(self):
        """测试平原地图随机事件集成流程"""
        game = self.create_test_game(difficulty='2', map_type='1')  # normal, plains
        
        initial_hp = game.hero_hp
        initial_gold = game.hero_gold
        initial_potions = game.hero_potions
        
        with patch('random.randint', return_value=2):
            with patch('builtins.print'):
                with patch.object(game, 'show_hero_info'):
                    game.random_event()
        
        self.assertLess(game.hero_hp, initial_hp)
        
        game.hero_hp = 100
        with patch('random.randint', return_value=10):
            with patch('builtins.print'):
                with patch.object(game, 'show_hero_info'):
                    game.random_event()
        
        self.assertGreater(game.hero_gold, initial_gold)
    
    def test_random_events_forest_integration(self):
        """测试森林地图随机事件集成流程"""
        game = self.create_test_game(difficulty='2', map_type='2')  # normal, forest
        
        initial_hp = game.hero_hp
        
        with patch('random.randint', return_value=2):
            with patch('builtins.print'):
                with patch.object(game, 'show_hero_info'):
                    game.random_event()
        
        self.assertLess(game.hero_hp, initial_hp)
    
    def test_random_events_desert_integration(self):
        """测试沙漠地图随机事件集成流程"""
        game = self.create_test_game(difficulty='2', map_type='3')  # normal, desert
        
        initial_hp = game.hero_hp
        
        with patch('random.randint', return_value=2):
            with patch('builtins.print'):
                with patch.object(game, 'show_hero_info'):
                    game.random_event()
        
        self.assertLess(game.hero_hp, initial_hp)
    
    def test_random_events_dungeon_integration(self):
        """测试地牢地图随机事件集成流程"""
        game = self.create_test_game(difficulty='2', map_type='4')  # normal, dungeon
        
        initial_hp = game.hero_hp
        
        with patch('random.randint', return_value=2):
            with patch('builtins.print'):
                with patch.object(game, 'show_hero_info'):
                    game.random_event()
        
        self.assertLess(game.hero_hp, initial_hp)
    
    def test_random_events_mountain_integration(self):
        """测试山脉地图随机事件集成流程"""
        game = self.create_test_game(difficulty='2', map_type='5')  # normal, mountain
        
        initial_gold = game.hero_gold
        
        with patch('random.randint', return_value=6):
            with patch('builtins.print'):
                with patch.object(game, 'show_hero_info'):
                    game.random_event()
        
        self.assertGreater(game.hero_gold, initial_gold)


if __name__ == '__main__':
    unittest.main()
