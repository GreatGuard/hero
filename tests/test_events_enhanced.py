#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试事件系统增强版本 - 提高测试覆盖率
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock, Mock

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hero.events import EventSystem


class TestEventSystemEnhanced(unittest.TestCase):
    """测试EventSystem类增强版本"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建模拟的HeroGame实例
        self.mock_game = Mock()
        self.mock_game.hero_max_hp = 100
        self.mock_game.hero_hp = 50
        self.mock_game.hero_gold = 100
        self.mock_game.hero_potions = 3
        self.mock_game.hero_level = 3
        self.mock_game.hero_attack = 20
        self.mock_game.hero_defense = 10
        self.mock_game.hero_xp = 50
        self.mock_game.hero_xp_to_next_level = 100
        self.mock_game.current_position = 5
        self.mock_game.map_length = 20
        self.mock_game.difficulty = "normal"
        self.mock_game.map_type = "forest"
        
        # 模拟语言支持
        self.mock_lang = Mock()
        self.mock_lang.get_text = lambda key: {
            "random_event": "随机事件",
            "events_title": "事件标题",
            "found_gold": "发现了金币",
            "found_potion": "发现了药剂",
            "found_item": "发现了物品",
            "merchant": "商人",
            "shrine": "神龛",
            "trap": "陷阱",
            "treasure": "宝藏",
            "mystic_portal": "神秘传送门",
            "sage_guide": "贤者指引",
            "robber_encounter": "遭遇强盗",
            "mystic_altar": "神秘祭坛",
            "roadside_camp": "路边营地",
            "poison": "中毒",
            "quicksand": "流沙",
            "rare_herbs": "罕见草药",
            "swamp_merchant": "沼泽商人",
            "frostbite": "冻伤",
            "avalanche": "雪崩",
            "ice_cave": "冰洞",
            "ice_effect": "冰霜效果",
            "enter_choice": "输入选择",
            "continue_prompt": "按任意键继续",
            "yes": "是",
            "no": "否",
            "yes_options": ["是", "y", "yes"],
            "invalid_choice": "无效选择",
            "not_enough_gold": "金币不足",
            "how_many": "多少",
            "potions": "药剂",
            "buy_success": "购买成功",
            "level_up": "升级",
            "gain_experience": "获得经验",
            "trap_damage": "陷阱伤害",
            "heal_amount": "治疗量",
            "move_forward": "前进",
            "move_backward": "后退",
            "poison_damage": "中毒伤害",
            "quicksand_damage": "流沙伤害",
            "frostbite_debuff": "冻伤减益",
            "avalanche_damage": "雪崩伤害",
            "ice_cave_heal": "冰洞治疗",
            "robber_steal": "强盗偷窃",
            "robber_fight": "与强盗战斗",
            "altar_sacrifice": "祭坛牺牲",
            "altar_refuse": "拒绝祭坛",
            "camp_rest": "营地休息"
        }.get(key, key)
        
        self.mock_game.lang = self.mock_lang
        self.mock_game.inventory = []
        self.mock_game.hero_equipment = {}
        self.mock_game.hero_skills = []
        
        # 模拟统计系统
        self.mock_statistics = Mock()
        self.mock_statistics.record_gold_found = Mock()
        self.mock_statistics.record_potion_found = Mock()
        self.mock_statistics.record_item_found = Mock()
        self.mock_statistics.record_event_triggered = Mock()
        self.mock_statistics.record_xp_gained = Mock()
        
        self.mock_game.statistics = self.mock_statistics
        
        # 创建事件系统实例
        self.event_system = EventSystem(self.mock_game)
    
    def test_init_event_system(self):
        """测试事件系统初始化"""
        self.assertEqual(self.event_system.game, self.mock_game)
        self.assertIsNotNone(self.event_system.event_weights)
    
    def test_get_random_event(self):
        """测试获取随机事件"""
        # 多次测试以确保随机性
        event_types = set()
        for _ in range(100):
            event_type = self.event_system.get_random_event()
            event_types.add(event_type)
        
        # 应该有多种事件类型
        self.assertGreater(len(event_types), 1)
    
    def test_handle_gold_event(self):
        """测试金币事件"""
        initial_gold = self.mock_game.hero_gold
        
        # 处理金币事件
        self.event_system._handle_gold_event()
        
        # 金币应该增加
        self.assertGreater(self.mock_game.hero_gold, initial_gold)
        # 统计应该被记录
        self.mock_statistics.record_gold_found.assert_called()
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_potion_event(self):
        """测试药剂事件"""
        initial_potions = self.mock_game.hero_potions
        
        # 处理药剂事件
        self.event_system._handle_potion_event()
        
        # 药剂应该增加
        self.assertGreaterEqual(self.mock_game.hero_potions, initial_potions)
        # 统计应该被记录
        self.mock_statistics.record_potion_found.assert_called()
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_item_event(self):
        """测试物品事件"""
        initial_items = len(self.mock_game.inventory)
        
        # 处理物品事件
        self.event_system._handle_item_event()
        
        # 物品应该增加
        self.assertGreaterEqual(len(self.mock_game.inventory), initial_items)
        # 统计应该被记录
        self.mock_statistics.record_item_found.assert_called()
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_merchant_event(self):
        """测试商人事件"""
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["3"]  # 离开商人
            
            # 处理商人事件
            self.event_system._handle_merchant_event()
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_handle_shrine_event(self):
        """测试神龛事件"""
        initial_hp = self.mock_game.hero_hp
        initial_xp = self.mock_game.hero_xp
        
        # 处理神龛事件
        self.event_system._handle_shrine_event()
        
        # HP或XP应该增加
        self.assertTrue(
            self.mock_game.hero_hp > initial_hp or 
            self.mock_game.hero_xp > initial_xp
        )
        # 统计应该被记录
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_trap_event(self):
        """测试陷阱事件"""
        initial_hp = self.mock_game.hero_hp
        
        # 处理陷阱事件
        self.event_system._handle_trap_event()
        
        # HP应该减少
        self.assertLess(self.mock_game.hero_hp, initial_hp)
        # 统计应该被记录
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_treasure_event(self):
        """测试宝藏事件"""
        initial_gold = self.mock_game.hero_gold
        initial_items = len(self.mock_game.inventory)
        initial_potions = self.mock_game.hero_potions
        
        # 处理宝藏事件
        self.event_system._handle_treasure_event()
        
        # 金币、物品或药剂应该增加
        self.assertTrue(
            self.mock_game.hero_gold > initial_gold or
            len(self.mock_game.inventory) > initial_items or
            self.mock_game.hero_potions > initial_potions
        )
        # 统计应该被记录
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_mystic_portal_event(self):
        """测试神秘传送门事件"""
        initial_position = self.mock_game.current_position
        
        # 处理神秘传送门事件
        self.event_system._handle_mystic_portal_event()
        
        # 位置应该改变
        self.assertNotEqual(self.mock_game.current_position, initial_position)
        # 位置应该在有效范围内
        self.assertGreaterEqual(self.mock_game.current_position, 0)
        self.assertLessEqual(self.mock_game.current_position, self.mock_game.map_length)
        # 统计应该被记录
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_sage_guide_event(self):
        """测试贤者指引事件"""
        initial_xp = self.mock_game.hero_xp
        
        # 处理贤者指引事件
        self.event_system._handle_sage_guide_event()
        
        # XP应该增加
        self.assertGreater(self.mock_game.hero_xp, initial_xp)
        # 统计应该被记录
        self.mock_statistics.record_xp_gained.assert_called()
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_robber_encounter_event(self):
        """测试遭遇强盗事件"""
        initial_gold = self.mock_game.hero_gold
        
        # 模拟战斗结果
        with patch.object(self.event_system, '_simulate_robber_combat', return_value=True):
            # 处理遭遇强盗事件
            self.event_system._handle_robber_encounter_event()
            
            # 金币应该增加（战胜强盗）
            self.assertGreaterEqual(self.mock_game.hero_gold, initial_gold)
        
        # 测试失败情况
        self.mock_game.hero_gold = initial_gold
        with patch.object(self.event_system, '_simulate_robber_combat', return_value=False):
            # 处理遭遇强盗事件
            self.event_system._handle_robber_encounter_event()
            
            # 金币应该减少（失败给强盗）
            self.assertLessEqual(self.mock_game.hero_gold, initial_gold)
        
        # 统计应该被记录
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_mystic_altar_event(self):
        """测试神秘祭坛事件"""
        initial_hp = self.mock_game.hero_hp
        initial_attack = self.mock_game.hero_attack
        initial_defense = self.mock_game.hero_defense
        
        # 模拟用户选择牺牲HP
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["1"]  # 牺牲HP
            
            # 处理神秘祭坛事件
            self.event_system._handle_mystic_altar_event()
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
            # HP应该减少
            self.assertLess(self.mock_game.hero_hp, initial_hp)
            # 攻击或防御应该增加
            self.assertTrue(
                self.mock_game.hero_attack > initial_attack or
                self.mock_game.hero_defense > initial_defense
            )
        
        # 重置状态
        self.mock_game.hero_hp = initial_hp
        self.mock_game.hero_attack = initial_attack
        self.mock_game.hero_defense = initial_defense
        
        # 模拟用户拒绝祭坛
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["2"]  # 拒绝
            
            # 处理神秘祭坛事件
            self.event_system._handle_mystic_altar_event()
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
            # 属性应该不变
            self.assertEqual(self.mock_game.hero_hp, initial_hp)
            self.assertEqual(self.mock_game.hero_attack, initial_attack)
            self.assertEqual(self.mock_game.hero_defense, initial_defense)
        
        # 统计应该被记录
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_roadside_camp_event(self):
        """测试路边营地事件"""
        initial_hp = self.mock_game.hero_hp
        
        # 处理路边营地事件
        self.event_system._handle_roadside_camp_event()
        
        # HP应该恢复
        self.assertGreaterEqual(self.mock_game.hero_hp, initial_hp)
        # HP不应该超过最大值
        self.assertLessEqual(self.mock_game.hero_hp, self.mock_game.hero_max_hp)
        # 统计应该被记录
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_poison_event(self):
        """测试中毒事件"""
        initial_hp = self.mock_game.hero_hp
        
        # 处理中毒事件
        self.event_system._handle_poison_event()
        
        # HP应该减少
        self.assertLess(self.mock_game.hero_hp, initial_hp)
        # 中毒状态应该被添加
        self.assertIn('poison', self.event_system.game.status_effects)
        # 统计应该被记录
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_quicksand_event(self):
        """测试流沙事件"""
        initial_hp = self.mock_game.hero_hp
        
        # 处理流沙事件
        self.event_system._handle_quicksand_event()
        
        # HP应该减少
        self.assertLess(self.mock_game.hero_hp, initial_hp)
        # 统计应该被记录
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_rare_herbs_event(self):
        """测试罕见草药事件"""
        initial_hp = self.mock_game.hero_hp
        
        # 处理罕见草药事件
        self.event_system._handle_rare_herbs_event()
        
        # HP应该恢复
        self.assertGreater(self.mock_game.hero_hp, initial_hp)
        # HP不应该超过最大值
        self.assertLessEqual(self.mock_game.hero_hp, self.mock_game.hero_max_hp)
        # 临时buff应该被添加
        self.assertIn('herb_buff', self.event_system.game.status_effects)
        # 统计应该被记录
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_swamp_merchant_event(self):
        """测试沼泽商人事件"""
        initial_gold = self.mock_game.hero_gold
        
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["3"]  # 离开商人
            
            # 处理沼泽商人事件
            self.event_system._handle_swamp_merchant_event()
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
            # 金币应该不变
            self.assertEqual(self.mock_game.hero_gold, initial_gold)
    
    def test_handle_frostbite_event(self):
        """测试冻伤事件"""
        initial_attack = self.mock_game.hero_attack
        
        # 处理冻伤事件
        self.event_system._handle_frostbite_event()
        
        # 攻击力应该减少
        self.assertLess(self.mock_game.hero_attack, initial_attack)
        # 冻伤状态应该被添加
        self.assertIn('frostbite', self.event_system.game.status_effects)
        # 统计应该被记录
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_avalanche_event(self):
        """测试雪崩事件"""
        initial_hp = self.mock_game.hero_hp
        
        # 处理雪崩事件
        self.event_system._handle_avalanche_event()
        
        # HP应该减少
        self.assertLess(self.mock_game.hero_hp, initial_hp)
        # 统计应该被记录
        self.mock_statistics.record_event_triggered.assert_called()
        
        # 有概率发现稀有装备
        if len(self.mock_game.inventory) > 0:
            # 最后一个物品应该是稀有装备
            last_item = self.mock_game.inventory[-1]
            self.assertEqual(last_item.get("rarity"), "rare")
    
    def test_handle_ice_cave_event(self):
        """测试冰洞事件"""
        initial_hp = self.mock_game.hero_hp
        
        # 处理冰洞事件
        self.event_system._handle_ice_cave_event()
        
        # HP应该恢复
        self.assertGreater(self.mock_game.hero_hp, initial_hp)
        # HP不应该超过最大值
        self.assertLessEqual(self.mock_game.hero_hp, self.mock_game.hero_max_hp)
        # 统计应该被记录
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_handle_ice_effect_event(self):
        """测试冰霜效果事件"""
        initial_defense = self.mock_game.hero_defense
        
        # 处理冰霜效果事件
        self.event_system._handle_ice_effect_event()
        
        # 防御力应该减少
        self.assertLess(self.mock_game.hero_defense, initial_defense)
        # 冰霜效果状态应该被添加
        self.assertIn('ice_effect', self.event_system.game.status_effects)
        # 统计应该被记录
        self.mock_statistics.record_event_triggered.assert_called()
    
    def test_simulate_robber_combat(self):
        """测试模拟强盗战斗"""
        # 模拟多次战斗，测试不同结果
        wins = 0
        losses = 0
        for _ in range(100):
            result = self.event_system._simulate_robber_combat()
            if result:
                wins += 1
            else:
                losses += 1
        
        # 应该既有胜利也有失败
        self.assertGreater(wins, 0)
        self.assertGreater(losses, 0)
    
    def test_apply_status_effects(self):
        """测试应用状态效果"""
        # 添加中毒状态
        self.event_system.game.status_effects['poison'] = 3  # 3回合
        initial_hp = self.mock_game.hero_hp
        
        # 应用状态效果
        self.event_system._apply_status_effects()
        
        # HP应该减少（中毒伤害）
        self.assertLess(self.mock_game.hero_hp, initial_hp)
        # 中毒回合数应该减少
        self.assertEqual(self.event_system.game.status_effects['poison'], 2)
        
        # 测试状态效果结束
        self.event_system.game.status_effects['poison'] = 1
        self.event_system._apply_status_effects()
        self.assertNotIn('poison', self.event_system.game.status_effects)
    
    def test_get_event_description(self):
        """测试获取事件描述"""
        # 测试金币事件
        description = self.event_system._get_event_description("found_gold", 50)
        self.assertIsNotNone(description)
        self.assertIn("50", description)
        
        # 测试药剂事件
        description = self.event_system._get_event_description("found_potion", 2)
        self.assertIsNotNone(description)
        self.assertIn("2", description)
        
        # 测试无效事件类型
        description = self.event_system._get_event_description("invalid_event", 0)
        self.assertEqual(description, "未知事件")
    
    def test_get_event_weight(self):
        """测试获取事件权重"""
        # 测试正常事件权重
        weight = self.event_system._get_event_weight("found_gold")
        self.assertGreater(weight, 0)
        
        # 测试地图特定事件权重（森林）
        self.mock_game.map_type = "forest"
        weight = self.event_system._get_event_weight("found_herb")
        self.assertGreater(weight, 0)
        
        # 测试非地图特定事件权重（沙漠）
        self.mock_game.map_type = "desert"
        weight = self.event_system._get_event_weight("found_herb")
        self.assertEqual(weight, 0)
        
        # 测试无效事件
        weight = self.event_system._get_event_weight("invalid_event")
        self.assertEqual(weight, 0)
    
    def test_get_event_weight_by_difficulty(self):
        """测试根据难度获取事件权重"""
        # 测试简单难度
        self.mock_game.difficulty = "easy"
        weight = self.event_system._get_event_weight_by_difficulty("trap", "easy")
        self.assertGreater(weight, 0)
        
        # 测试普通难度
        self.mock_game.difficulty = "normal"
        weight = self.event_system._get_event_weight_by_difficulty("trap", "normal")
        self.assertGreater(weight, 0)
        
        # 测试困难难度
        self.mock_game.difficulty = "hard"
        weight = self.event_system._get_event_weight_by_difficulty("trap", "hard")
        self.assertGreater(weight, 0)
        
        # 测试噩梦难度
        self.mock_game.difficulty = "nightmare"
        weight = self.event_system._get_event_weight_by_difficulty("trap", "nightmare")
        self.assertGreater(weight, 0)
    
    def test_apply_difficulty_modifier(self):
        """测试应用难度修正"""
        # 测试简单难度
        value = self.event_system._apply_difficulty_modifier(10, "easy")
        self.assertGreaterEqual(value, 10)
        
        # 测试普通难度
        value = self.event_system._apply_difficulty_modifier(10, "normal")
        self.assertEqual(value, 10)
        
        # 测试困难难度
        value = self.event_system._apply_difficulty_modifier(10, "hard")
        self.assertLessEqual(value, 10)
        
        # 测试噩梦难度
        value = self.event_system._apply_difficulty_modifier(10, "nightmare")
        self.assertLessEqual(value, 10)
    
    def test_format_event_output(self):
        """测试格式化事件输出"""
        # 测试正常事件
        output = self.event_system._format_event_output("found_gold", "你发现了50金币！")
        self.assertIsNotNone(output)
        self.assertIn("found_gold", output)
        self.assertIn("你发现了50金币！", output)
        
        # 测试带选项的事件
        output = self.event_system._format_event_output("merchant", "你遇到了商人", ["1. 购买", "2. 离开"])
        self.assertIsNotNone(output)
        self.assertIn("merchant", output)
        self.assertIn("你遇到了商人", output)
        self.assertIn("1. 购买", output)
        self.assertIn("2. 离开", output)
    
    def test_trigger_random_event(self):
        """测试触发随机事件"""
        # 使用模拟方法确保测试可控
        with patch.object(self.event_system, 'get_random_event', return_value="found_gold"):
            with patch.object(self.event_system, '_handle_gold_event'):
                # 触发随机事件
                result = self.event_system.trigger_random_event()
                
                # 验证事件被触发
                self.assertTrue(result)
        
        # 测试没有事件的情况
        with patch.object(self.event_system, 'get_random_event', return_value=None):
            # 触发随机事件
            result = self.event_system.trigger_random_event()
            
            # 验证没有事件被触发
            self.assertFalse(result)
    
    def test_handle_status_effects(self):
        """测试处理状态效果"""
        # 添加多个状态效果
        self.event_system.game.status_effects = {
            'poison': 3,
            'frostbite': 2,
            'ice_effect': 1
        }
        
        # 处理状态效果
        self.event_system.handle_status_effects()
        
        # 验证状态效果被处理
        self.assertIn('poison', self.event_system.game.status_effects)
        self.assertIn('frostbite', self.event_system.game.status_effects)
        # ice_effect应该被移除（只剩1回合）
        self.assertNotIn('ice_effect', self.event_system.game.status_effects)
    
    def test_get_status_effect_description(self):
        """测试获取状态效果描述"""
        # 测试中毒效果
        description = self.event_system._get_status_effect_description("poison", 3)
        self.assertIsNotNone(description)
        self.assertIn("中毒", description)
        self.assertIn("3", description)
        
        # 测试无效状态效果
        description = self.event_system._get_status_effect_description("invalid", 0)
        self.assertEqual(description, "")
    
    def test_get_active_status_effects(self):
        """测试获取活动状态效果"""
        # 添加状态效果
        self.event_system.game.status_effects = {
            'poison': 3,
            'frostbite': 2,
            'ice_effect': 1
        }
        
        # 获取活动状态效果
        effects = self.event_system.get_active_status_effects()
        
        # 验证状态效果
        self.assertIn('poison', effects)
        self.assertIn('frostbite', effects)
        self.assertIn('ice_effect', effects)
        self.assertEqual(effects['poison'], 3)
        self.assertEqual(effects['frostbite'], 2)
        self.assertEqual(effects['ice_effect'], 1)
    
    def test_remove_status_effect(self):
        """测试移除状态效果"""
        # 添加状态效果
        self.event_system.game.status_effects = {
            'poison': 3,
            'frostbite': 2,
            'ice_effect': 1
        }
        
        # 移除状态效果
        self.event_system.remove_status_effect('poison')
        
        # 验证状态效果被移除
        self.assertNotIn('poison', self.event_system.game.status_effects)
        self.assertIn('frostbite', self.event_system.game.status_effects)
        self.assertIn('ice_effect', self.event_system.game.status_effects)
        
        # 测试移除不存在的状态效果
        self.event_system.remove_status_effect('nonexistent')
        # 应该不会有错误
        self.assertNotIn('nonexistent', self.event_system.game.status_effects)
    
    def test_clear_all_status_effects(self):
        """测试清除所有状态效果"""
        # 添加状态效果
        self.event_system.game.status_effects = {
            'poison': 3,
            'frostbite': 2,
            'ice_effect': 1
        }
        
        # 清除所有状态效果
        self.event_system.clear_all_status_effects()
        
        # 验证所有状态效果被清除
        self.assertEqual(len(self.event_system.game.status_effects), 0)


if __name__ == "__main__":
    unittest.main()