#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试新增功能
"""

import unittest
import sys
import os
import tempfile
import shutil

# 添加项目路径到sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.hero.main import HeroGame
from src.hero.game_config import MAP_TYPES, MONSTER_TEMPLATES, BOSS_TEMPLATES


class TestNewFeatures(unittest.TestCase):
    """测试新增功能的类"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建临时目录用于测试存档
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """清理测试环境"""
        # 删除临时目录
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_swamp_map_exists(self):
        """测试沼泽地图是否存在"""
        self.assertIn("swamp", MAP_TYPES)
        
        # 检查沼泽地图配置
        swamp_config = MAP_TYPES["swamp"]
        self.assertEqual(swamp_config["name"], "swamp")
        self.assertIn("poison_cloud", swamp_config["special_events"])
        self.assertIn("quicksand", swamp_config["special_events"])
        self.assertIn("rare_herbs", swamp_config["special_events"])
        self.assertIn("swamp_merchant", swamp_config["special_events"])
        self.assertIn("crocodile", swamp_config["monsters"])
        self.assertIn("venom_snake", swamp_config["monsters"])
        self.assertIn("swamp_beast", swamp_config["monsters"])
    
    def test_snowfield_map_exists(self):
        """测试雪原地图是否存在"""
        self.assertIn("snowfield", MAP_TYPES)
        
        # 检查雪原地图配置
        snowfield_config = MAP_TYPES["snowfield"]
        self.assertEqual(snowfield_config["name"], "snowfield")
        self.assertIn("frostbite", snowfield_config["special_events"])
        self.assertIn("avalanche", snowfield_config["special_events"])
        self.assertIn("ice_cave", snowfield_config["special_events"])
        self.assertIn("frost_effect", snowfield_config["special_events"])
        self.assertIn("ice_wolf", snowfield_config["monsters"])
        self.assertIn("snow_beast", snowfield_config["monsters"])
        self.assertIn("frost_giant", snowfield_config["monsters"])
    
    def test_new_monsters_exist(self):
        """测试新怪物是否存在"""
        # 测试沼泽怪物
        self.assertIn("monster_crocodile", MONSTER_TEMPLATES)
        self.assertIn("monster_venom_snake", MONSTER_TEMPLATES)
        self.assertIn("monster_swamp_beast", MONSTER_TEMPLATES)
        
        # 测试雪原怪物
        self.assertIn("monster_ice_wolf", MONSTER_TEMPLATES)
        self.assertIn("monster_snow_beast", MONSTER_TEMPLATES)
        self.assertIn("monster_frost_giant", MONSTER_TEMPLATES)
        
        # 测试怪物特殊能力
        venom_snake = MONSTER_TEMPLATES["venom_snake"]
        self.assertEqual(venom_snake.get("special"), "poison")
        
        ice_wolf = MONSTER_TEMPLATES["ice_wolf"]
        self.assertEqual(ice_wolf.get("special"), "frost")
    
    def test_boss_templates_exist(self):
        """测试Boss模板是否存在"""
        # 测试所有地图都有对应的Boss
        self.assertIn("boss_plains_warlord", BOSS_TEMPLATES)
        self.assertIn("boss_ancient_treant", BOSS_TEMPLATES)
        self.assertIn("boss_desert_sphinx", BOSS_TEMPLATES)
        self.assertIn("boss_demon_lord", BOSS_TEMPLATES)
        self.assertIn("boss_mountain_dragon", BOSS_TEMPLATES)
        self.assertIn("boss_swamp_hydra", BOSS_TEMPLATES)
        self.assertIn("boss_frost_king", BOSS_TEMPLATES)
        
        # 测试Boss技能
        plains_boss = BOSS_TEMPLATES["plains"]
        self.assertIn("power_strike", plains_boss["skills"])
        
        swamp_boss = BOSS_TEMPLATES["swamp"]
        self.assertIn("poison_bite", swamp_boss["skills"])
        self.assertIn("regeneration", swamp_boss["skills"])
        
        snowfield_boss = BOSS_TEMPLATES["snowfield"]
        self.assertIn("blizzard", snowfield_boss["skills"])
        self.assertIn("ice_prison", snowfield_boss["skills"])
    
    def test_status_effects_initialization(self):
        """测试状态效果初始化"""
        # 创建游戏实例但不进入游戏循环
        game = HeroGame()
        
        # 检查状态效果是否正确初始化
        self.assertIn("poison", game.status_effects)
        self.assertIn("frostbite", game.status_effects)
        self.assertIn("frost", game.status_effects)
        self.assertEqual(game.status_effects["poison"], 0)
        self.assertEqual(game.status_effects["frostbite"], 0)
        self.assertEqual(game.status_effects["frost"], 0)
    
    def test_status_effects_methods(self):
        """测试状态效果方法"""
        # 创建游戏实例但不进入游戏循环
        game = HeroGame()
        
        # 测试添加状态效果
        game.add_status_effect("poison", 3)
        self.assertEqual(game.status_effects["poison"], 3)
        
        # 测试获取活跃状态效果
        active_effects = game.get_active_status_effects()
        self.assertEqual(len(active_effects), 1)
        self.assertEqual(active_effects[0][0], "poison")
        self.assertEqual(active_effects[0][1], 3)
    
    def test_status_effects_update(self):
        """测试状态效果更新"""
        # 创建游戏实例但不进入游戏循环
        game = HeroGame()
        
        # 添加中毒状态
        game.add_status_effect("poison", 3)
        game.update_status_effects()
        
        # 检查中毒状态减少一回合
        self.assertEqual(game.status_effects["poison"], 2)
        
        # 更新到0回合
        game.update_status_effects()
        self.assertEqual(game.status_effects["poison"], 1)
        
        # 再更新一次，应该变为0
        game.update_status_effects()
        self.assertEqual(game.status_effects["poison"], 0)
    
    def test_save_load_status_effects(self):
        """测试状态效果的保存和加载"""
        # 创建游戏实例
        game = HeroGame()
        
        # 添加一些状态效果
        game.add_status_effect("poison", 2)
        game.add_status_effect("frostbite", 1)
        
        # 获取存档数据
        save_data = game.get_save_data()
        
        # 检查存档中是否包含状态效果
        self.assertIn("status_effects", save_data.__dict__)
        self.assertEqual(save_data.status_effects["poison"], 2)
        self.assertEqual(save_data.status_effects["frostbite"], 1)
        
        # 创建新游戏实例
        new_game = HeroGame()
        
        # 从存档加载
        new_game.load_from_save_data(save_data)
        
        # 检查状态效果是否正确加载
        self.assertEqual(new_game.status_effects["poison"], 2)
        self.assertEqual(new_game.status_effects["frostbite"], 1)


if __name__ == '__main__':
    unittest.main()