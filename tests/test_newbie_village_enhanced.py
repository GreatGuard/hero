#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试新手村系统增强版本 - 提高测试覆盖率
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock, Mock

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hero.newbie_village import NewbieVillage


class TestNewbieVillageEnhanced(unittest.TestCase):
    """测试NewbieVillage类增强版本"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建模拟的HeroGame实例
        self.mock_game = Mock()
        self.mock_game.hero_max_hp = 100
        self.mock_game.hero_hp = 50
        self.mock_game.hero_gold = 100
        self.mock_game.hero_potions = 3
        self.mock_game.hero_level = 1
        self.mock_game.hero_attack = 10
        self.mock_game.hero_defense = 5
        self.mock_game.hero_xp = 0
        self.mock_game.hero_xp_to_next_level = 100
        self.mock_game.current_position = 0
        self.mock_game.map_length = 20
        self.mock_game.difficulty = "normal"
        self.mock_game.map_type = "plains"
        
        # 模拟语言支持
        self.mock_lang = Mock()
        self.mock_lang.get_text = lambda key: {
            "newbie_village": "新手村",
            "village_elder": "村长",
            "weapon_smith": "武器匠",
            "armor_smith": "护甲匠",
            "potion_shop": "药剂店",
            "training_grounds": "训练场",
            "village_gate": "村门",
            "enter_choice": "输入选择",
            "continue_prompt": "按任意键继续",
            "welcome_to_village": "欢迎来到新手村",
            "elder_greeting": "村长问候",
            "elder_quest": "村长任务",
            "weapon_smith_greeting": "武器匠问候",
            "armor_smith_greeting": "护甲匠问候",
            "potion_shop_greeting": "药剂店问候",
            "training_greeting": "训练场问候",
            "village_gate_description": "村门描述",
            "level_up": "升级",
            "gain_experience": "获得经验",
            "learn_skill": "学习技能",
            "invalid_choice": "无效选择",
            "not_enough_gold": "金币不足",
            "already_known_skill": "已经学会技能",
            "how_many": "多少",
            "potions": "药剂",
            "buy_success": "购买成功",
            "sell_success": "出售成功",
            "confirm_purchase": "确认购买",
            "confirm_sell": "确认出售",
            "training_complete": "训练完成",
            "skill_learned": "技能学会",
            "quest_accepted": "任务接受",
            "quest_completed": "任务完成",
            "reward_received": "奖励获得",
            "experience_gained": "经验获得",
            "gold_gained": "金币获得",
            "item_gained": "物品获得"
        }.get(key, key)
        
        self.mock_game.lang = self.mock_lang
        self.mock_game.inventory = []
        self.mock_game.hero_equipment = {}
        self.mock_game.hero_skills = []
        
        # 模拟统计系统
        self.mock_statistics = Mock()
        self.mock_statistics.record_xp_gained = Mock()
        self.mock_statistics.record_gold_found = Mock()
        self.mock_statistics.record_item_found = Mock()
        self.mock_statistics.record_event_triggered = Mock()
        
        self.mock_game.statistics = self.mock_statistics
        
        # 创建新手村实例
        self.newbie_village = NewbieVillage(self.mock_game)
    
    def test_init_newbie_village(self):
        """测试新手村初始化"""
        self.assertEqual(self.newbie_village.game, self.mock_game)
        self.assertIsNotNone(self.newbie_village.quests)
        self.assertIsNotNone(self.newbie_village.skills)
        self.assertIsNotNone(self.newbie_village.items)
    
    def test_enter_village(self):
        """测试进入新手村"""
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["6"]  # 离开新手村
            
            # 进入新手村
            self.newbie_village.enter_village()
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_village_elder_dialogue(self):
        """测试村长对话"""
        # 初始状态，没有任务
        self.assertFalse(self.newbie_village.quests["elder_quest"]["accepted"])
        self.assertFalse(self.newbie_village.quests["elder_quest"]["completed"])
        
        # 测试接受任务
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["1"]  # 接受任务
            
            # 与村长对话
            self.newbie_village.village_elder_dialogue()
            
            # 验证任务被接受
            self.assertTrue(self.newbie_village.quests["elder_quest"]["accepted"])
            self.assertFalse(self.newbie_village.quests["elder_quest"]["completed"])
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
        
        # 测试完成任务
        self.newbie_village.quests["elder_quest"]["progress"] = 5  # 设置任务进度为完成
        
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["1"]  # 领取奖励
            
            # 与村长对话
            self.newbie_village.village_elder_dialogue()
            
            # 验证任务完成
            self.assertTrue(self.newbie_village.quests["elder_quest"]["accepted"])
            self.assertTrue(self.newbie_village.quests["elder_quest"]["completed"])
            
            # 验证奖励
            self.assertGreater(self.mock_game.hero_xp, 0)
            self.assertGreater(self.mock_game.hero_gold, 100)
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_weapon_smith_dialogue(self):
        """测试武器匠对话"""
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["3"]  # 离开武器匠
            
            # 与武器匠对话
            self.newbie_village.weapon_smith_dialogue()
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_weapon_smith_buy(self):
        """测试从武器匠购买"""
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["1", "1"]  # 购买第一件物品
            
            # 从武器匠购买
            self.newbie_village.weapon_smith_buy()
            
            # 验证金币减少
            self.assertLess(self.mock_game.hero_gold, 100)
            
            # 验证物品添加到背包
            self.assertGreater(len(self.mock_game.inventory), 0)
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_weapon_smith_buy_not_enough_gold(self):
        """测试金币不足时从武器匠购买"""
        # 设置不足的金币
        self.mock_game.hero_gold = 10
        
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["1"]  # 尝试购买第一件物品
            
            # 从武器匠购买
            self.newbie_village.weapon_smith_buy()
            
            # 验证金币不变
            self.assertEqual(self.mock_game.hero_gold, 10)
            
            # 验证背包不变
            self.assertEqual(len(self.mock_game.inventory), 0)
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_armor_smith_dialogue(self):
        """测试护甲匠对话"""
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["3"]  # 离开护甲匠
            
            # 与护甲匠对话
            self.newbie_village.armor_smith_dialogue()
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_armor_smith_buy(self):
        """测试从护甲匠购买"""
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["1", "1"]  # 购买第一件物品
            
            # 从护甲匠购买
            self.newbie_village.armor_smith_buy()
            
            # 验证金币减少
            self.assertLess(self.mock_game.hero_gold, 100)
            
            # 验证物品添加到背包
            self.assertGreater(len(self.mock_game.inventory), 0)
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_potion_shop_dialogue(self):
        """测试药剂店对话"""
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["3"]  # 离开药剂店
            
            # 与药剂店对话
            self.newbie_village.potion_shop_dialogue()
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_potion_shop_buy(self):
        """测试从药剂店购买"""
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["1", "5"]  # 购买5个药剂
            
            # 从药剂店购买
            self.newbie_village.potion_shop_buy()
            
            # 验证金币减少
            self.assertLess(self.mock_game.hero_gold, 100)
            
            # 验证药剂增加
            self.assertGreater(self.mock_game.hero_potions, 3)
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_potion_shop_buy_not_enough_gold(self):
        """测试金币不足时从药剂店购买"""
        # 设置不足的金币
        self.mock_game.hero_gold = 10
        
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["1", "1"]  # 尝试购买1个药剂
            
            # 从药剂店购买
            self.newbie_village.potion_shop_buy()
            
            # 验证金币不变
            self.assertEqual(self.mock_game.hero_gold, 10)
            
            # 验证药剂不变
            self.assertEqual(self.mock_game.hero_potions, 3)
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_training_grounds_dialogue(self):
        """测试训练场对话"""
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["3"]  # 离开训练场
            
            # 在训练场对话
            self.newbie_village.training_grounds_dialogue()
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_training_grounds_train(self):
        """测试在训练场训练"""
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["1"]  # 基础训练
            
            # 在训练场训练
            self.newbie_village.training_grounds_train()
            
            # 验证金币减少
            self.assertLess(self.mock_game.hero_gold, 100)
            
            # 验证经验增加
            self.assertGreater(self.mock_game.hero_xp, 0)
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_training_grounds_train_not_enough_gold(self):
        """测试金币不足时在训练场训练"""
        # 设置不足的金币
        self.mock_game.hero_gold = 10
        
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["1"]  # 尝试基础训练
            
            # 在训练场训练
            self.newbie_village.training_grounds_train()
            
            # 验证金币不变
            self.assertEqual(self.mock_game.hero_gold, 10)
            
            # 验证经验不变
            self.assertEqual(self.mock_game.hero_xp, 0)
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_training_grounds_learn_skill(self):
        """测试在训练场学习技能"""
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["1"]  # 学习第一个技能
            
            # 在训练场学习技能
            self.newbie_village.training_grounds_learn_skill()
            
            # 验证金币减少
            self.assertLess(self.mock_game.hero_gold, 100)
            
            # 验证技能学习
            self.assertGreater(len(self.mock_game.hero_skills), 0)
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_training_grounds_learn_skill_already_known(self):
        """测试学习已知的技能"""
        # 添加技能到已知技能列表
        self.mock_game.hero_skills.append("attack")
        
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["1"]  # 尝试学习已知的技能
            
            # 在训练场学习技能
            self.newbie_village.training_grounds_learn_skill()
            
            # 验证金币不变
            self.assertEqual(self.mock_game.hero_gold, 100)
            
            # 验证技能列表不变
            self.assertEqual(len(self.mock_game.hero_skills), 1)
            self.assertIn("attack", self.mock_game.hero_skills)
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_village_gate_dialogue(self):
        """测试村门对话"""
        # 模拟用户输入
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["2"]  # 返回村庄
            
            # 在村门对话
            self.newbie_village.village_gate_dialogue()
            
            # 验证输入被调用
            self.assertTrue(mock_input.called)
    
    def test_village_gate_leave(self):
        """测试离开村庄"""
        # 测试离开村庄
        result = self.newbie_village.village_gate_leave()
        
        self.assertTrue(result)
    
    def test_update_quest_progress(self):
        """测试更新任务进度"""
        # 接受任务
        self.newbie_village.quests["elder_quest"]["accepted"] = True
        self.newbie_village.quests["elder_quest"]["progress"] = 0
        
        # 更新任务进度
        self.newbie_village.update_quest_progress("elder_quest", 1)
        
        # 验证进度更新
        self.assertEqual(self.newbie_village.quests["elder_quest"]["progress"], 1)
        
        # 更新到完成状态
        self.newbie_village.update_quest_progress("elder_quest", 5)
        
        # 验证任务完成
        self.assertEqual(self.newbie_village.quests["elder_quest"]["progress"], 5)
        self.assertTrue(self.newbie_village.quests["elder_quest"]["completed"])
    
    def test_update_quest_progress_not_accepted(self):
        """测试更新未接受任务的进度"""
        # 确保任务未接受
        self.assertFalse(self.newbie_village.quests["elder_quest"]["accepted"])
        self.newbie_village.quests["elder_quest"]["progress"] = 0
        
        # 尝试更新任务进度
        self.newbie_village.update_quest_progress("elder_quest", 1)
        
        # 验证进度不更新
        self.assertEqual(self.newbie_village.quests["elder_quest"]["progress"], 0)
        self.assertFalse(self.newbie_village.quests["elder_quest"]["completed"])
    
    def test_get_quest_status(self):
        """测试获取任务状态"""
        # 测试未接受的任务
        status = self.newbie_village.get_quest_status("elder_quest")
        self.assertEqual(status, "not_accepted")
        
        # 测试已接受但未完成的任务
        self.newbie_village.quests["elder_quest"]["accepted"] = True
        status = self.newbie_village.get_quest_status("elder_quest")
        self.assertEqual(status, "in_progress")
        
        # 测试已完成的任务
        self.newbie_village.quests["elder_quest"]["completed"] = True
        status = self.newbie_village.get_quest_status("elder_quest")
        self.assertEqual(status, "completed")
    
    def test_get_quest_progress(self):
        """测试获取任务进度"""
        # 测试未接受的任务
        progress = self.newbie_village.get_quest_progress("elder_quest")
        self.assertEqual(progress, 0)
        
        # 测试已接受的任务
        self.newbie_village.quests["elder_quest"]["accepted"] = True
        self.newbie_village.quests["elder_quest"]["progress"] = 3
        progress = self.newbie_village.get_quest_progress("elder_quest")
        self.assertEqual(progress, 3)
    
    def test_get_quest_reward(self):
        """测试获取任务奖励"""
        # 设置足够的金币
        initial_gold = self.mock_game.hero_gold
        initial_xp = self.mock_game.hero_xp
        initial_items = len(self.mock_game.inventory)
        
        # 获取任务奖励
        self.newbie_village.get_quest_reward("elder_quest")
        
        # 验证奖励
        self.assertGreater(self.mock_game.hero_gold, initial_gold)
        self.assertGreater(self.mock_game.hero_xp, initial_xp)
        self.assertGreaterEqual(len(self.mock_game.inventory), initial_items)
    
    def test_get_skill_list(self):
        """测试获取技能列表"""
        # 获取技能列表
        skills = self.newbie_village.get_skill_list()
        
        # 验证技能列表
        self.assertIsNotNone(skills)
        self.assertIsInstance(skills, list)
        self.assertGreater(len(skills), 0)
        
        # 验证技能结构
        for skill in skills:
            self.assertIn("id", skill)
            self.assertIn("name", skill)
            self.assertIn("description", skill)
            self.assertIn("cost", skill)
    
    def test_get_available_skills(self):
        """测试获取可用技能"""
        # 获取可用技能
        skills = self.newbie_village.get_available_skills()
        
        # 验证技能列表
        self.assertIsNotNone(skills)
        self.assertIsInstance(skills, list)
        self.assertGreater(len(skills), 0)
        
        # 验证已知技能被过滤
        self.mock_game.hero_skills.append("attack")
        skills = self.newbie_village.get_available_skills()
        for skill in skills:
            self.assertNotEqual(skill["id"], "attack")
    
    def test_get_item_list(self):
        """测试获取物品列表"""
        # 获取物品列表
        items = self.newbie_village.get_item_list("weapon")
        
        # 验证物品列表
        self.assertIsNotNone(items)
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)
        
        # 验证物品结构
        for item in items:
            self.assertIn("name", item)
            self.assertIn("type", item)
            self.assertIn("price", item)
            self.assertIn("description", item)
    
    def test_get_item_list_invalid_type(self):
        """测试获取无效类型的物品列表"""
        # 获取无效类型的物品列表
        items = self.newbie_village.get_item_list("invalid_type")
        
        # 验证空列表
        self.assertEqual(items, [])
    
    def test_learn_skill(self):
        """测试学习技能"""
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 学习技能
        result = self.newbie_village.learn_skill("attack")
        
        # 验证技能学习
        self.assertTrue(result)
        self.assertIn("attack", self.mock_game.hero_skills)
        self.assertLess(self.mock_game.hero_gold, 100)
    
    def test_learn_skill_not_enough_gold(self):
        """测试金币不足时学习技能"""
        # 设置不足的金币
        self.mock_game.hero_gold = 10
        
        # 学习技能
        result = self.newbie_village.learn_skill("attack")
        
        # 验证技能未学习
        self.assertFalse(result)
        self.assertNotIn("attack", self.mock_game.hero_skills)
        self.assertEqual(self.mock_game.hero_gold, 10)
    
    def test_learn_skill_already_known(self):
        """测试学习已知的技能"""
        # 添加技能到已知技能列表
        self.mock_game.hero_skills.append("attack")
        
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 学习技能
        result = self.newbie_village.learn_skill("attack")
        
        # 验证技能未重新学习
        self.assertFalse(result)
        self.assertEqual(len(self.mock_game.hero_skills), 1)
        self.assertIn("attack", self.mock_game.hero_skills)
        self.assertEqual(self.mock_game.hero_gold, 100)
    
    def test_buy_item(self):
        """测试购买物品"""
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 购买物品
        result = self.newbie_village.buy_item("iron_sword")
        
        # 验证购买成功
        self.assertTrue(result)
        self.assertLess(self.mock_game.hero_gold, 100)
        self.assertGreater(len(self.mock_game.inventory), 0)
    
    def test_buy_item_not_enough_gold(self):
        """测试金币不足时购买物品"""
        # 设置不足的金币
        self.mock_game.hero_gold = 10
        
        # 购买物品
        result = self.newbie_village.buy_item("iron_sword")
        
        # 验证购买失败
        self.assertFalse(result)
        self.assertEqual(self.mock_game.hero_gold, 10)
        self.assertEqual(len(self.mock_game.inventory), 0)
    
    def test_buy_potion(self):
        """测试购买药剂"""
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 购买药剂
        result = self.newbie_village.buy_potion(5)
        
        # 验证购买成功
        self.assertTrue(result)
        self.assertLess(self.mock_game.hero_gold, 100)
        self.assertGreater(self.mock_game.hero_potions, 3)
    
    def test_buy_potion_not_enough_gold(self):
        """测试金币不足时购买药剂"""
        # 设置不足的金币
        self.mock_game.hero_gold = 10
        
        # 购买药剂
        result = self.newbie_village.buy_potion(5)
        
        # 验证购买失败
        self.assertFalse(result)
        self.assertEqual(self.mock_game.hero_gold, 10)
        self.assertEqual(self.mock_game.hero_potions, 3)
    
    def test_train(self):
        """测试训练"""
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 训练
        result = self.newbie_village.train("basic")
        
        # 验证训练成功
        self.assertTrue(result)
        self.assertLess(self.mock_game.hero_gold, 100)
        self.assertGreater(self.mock_game.hero_xp, 0)
    
    def test_train_not_enough_gold(self):
        """测试金币不足时训练"""
        # 设置不足的金币
        self.mock_game.hero_gold = 10
        
        # 训练
        result = self.newbie_village.train("basic")
        
        # 验证训练失败
        self.assertFalse(result)
        self.assertEqual(self.mock_game.hero_gold, 10)
        self.assertEqual(self.mock_game.hero_xp, 0)
    
    def test_get_quest_list(self):
        """测试获取任务列表"""
        # 获取任务列表
        quests = self.newbie_village.get_quest_list()
        
        # 验证任务列表
        self.assertIsNotNone(quests)
        self.assertIsInstance(quests, list)
        self.assertGreater(len(quests), 0)
        
        # 验证任务结构
        for quest in quests:
            self.assertIn("id", quest)
            self.assertIn("name", quest)
            self.assertIn("description", quest)
            self.assertIn("reward", quest)
    
    def test_get_quest_by_id(self):
        """测试根据ID获取任务"""
        # 获取任务
        quest = self.newbie_village.get_quest_by_id("elder_quest")
        
        # 验证任务
        self.assertIsNotNone(quest)
        self.assertEqual(quest["id"], "elder_quest")
        self.assertIn("name", quest)
        self.assertIn("description", quest)
        self.assertIn("reward", quest)
    
    def test_get_quest_by_invalid_id(self):
        """测试根据无效ID获取任务"""
        # 获取任务
        quest = self.newbie_village.get_quest_by_id("invalid_quest")
        
        # 验证返回None
        self.assertIsNone(quest)
    
    def test_get_skill_by_id(self):
        """测试根据ID获取技能"""
        # 获取技能
        skill = self.newbie_village.get_skill_by_id("attack")
        
        # 验证技能
        self.assertIsNotNone(skill)
        self.assertEqual(skill["id"], "attack")
        self.assertIn("name", skill)
        self.assertIn("description", skill)
        self.assertIn("cost", skill)
    
    def test_get_skill_by_invalid_id(self):
        """测试根据无效ID获取技能"""
        # 获取技能
        skill = self.newbie_village.get_skill_by_id("invalid_skill")
        
        # 验证返回None
        self.assertIsNone(skill)
    
    def test_get_item_by_id(self):
        """测试根据ID获取物品"""
        # 获取物品
        item = self.newbie_village.get_item_by_id("iron_sword")
        
        # 验证物品
        self.assertIsNotNone(item)
        self.assertEqual(item["name"], "iron_sword")
        self.assertIn("type", item)
        self.assertIn("price", item)
        self.assertIn("description", item)
    
    def test_get_item_by_invalid_id(self):
        """测试根据无效ID获取物品"""
        # 获取物品
        item = self.newbie_village.get_item_by_id("invalid_item")
        
        # 验证返回None
        self.assertIsNone(item)


if __name__ == "__main__":
    unittest.main()