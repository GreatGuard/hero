#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试游戏统计模块
"""

import unittest
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'hero'))

from statistics import GameStatistics
from language import LanguageSupport


class TestGameStatistics(unittest.TestCase):
    """测试GameStatistics类"""

    def setUp(self):
        """测试前准备"""
        self.stats = GameStatistics()
        self.lang = LanguageSupport("zh")

    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.stats.total_steps, 0)
        self.assertEqual(self.stats.total_battles, 0)
        self.assertEqual(self.stats.battles_won, 0)
        self.assertEqual(self.stats.battles_lost, 0)
        self.assertEqual(self.stats.monsters_defeated, 0)
        self.assertEqual(self.stats.total_gold_earned, 0)
        self.assertEqual(self.stats.total_exp_earned, 0)

    def test_record_step(self):
        """测试记录步数"""
        self.stats.record_step()
        self.assertEqual(self.stats.total_steps, 1)

        self.stats.record_step()
        self.stats.record_step()
        self.assertEqual(self.stats.total_steps, 3)

    def test_record_battle(self):
        """测试记录战斗"""
        # 记录战斗开始
        self.stats.record_battle_start()
        self.assertEqual(self.stats.total_battles, 1)

        # 记录胜利
        self.stats.record_battle_victory("Goblin")
        self.assertEqual(self.stats.battles_won, 1)
        self.assertEqual(self.stats.monsters_defeated, 1)
        self.assertEqual(self.stats.current_win_streak, 1)
        self.assertEqual(self.stats.max_win_streak, 1)

        # 再赢一场
        self.stats.record_battle_start()
        self.stats.record_battle_victory("Wolf")
        self.assertEqual(self.stats.battles_won, 2)
        self.assertEqual(self.stats.current_win_streak, 2)
        self.assertEqual(self.stats.max_win_streak, 2)

        # 记录失败
        self.stats.record_battle_start()
        self.stats.record_battle_defeat()
        self.assertEqual(self.stats.battles_lost, 1)
        self.assertEqual(self.stats.current_win_streak, 0)

    def test_win_rate_calculation(self):
        """测试胜率计算"""
        # 没有战斗
        self.assertEqual(self.stats.get_win_rate(), 0.0)

        # 5胜3负
        for _ in range(5):
            self.stats.record_battle_start()
            self.stats.record_battle_victory("Monster")

        for _ in range(3):
            self.stats.record_battle_start()
            self.stats.record_battle_defeat()

        win_rate = self.stats.get_win_rate()
        self.assertAlmostEqual(win_rate, 62.5, places=1)

    def test_gold_tracking(self):
        """测试金币追踪"""
        self.stats.record_gold_earned(100)
        self.assertEqual(self.stats.total_gold_earned, 100)

        self.stats.record_gold_earned(50)
        self.assertEqual(self.stats.total_gold_earned, 150)

        self.stats.record_gold_spent(30)
        self.assertEqual(self.stats.total_gold_spent, 30)

        self.stats.record_gold_spent(20)
        self.assertEqual(self.stats.total_gold_spent, 50)

    def test_exp_tracking(self):
        """测试经验追踪"""
        self.stats.record_exp_earned(50)
        self.assertEqual(self.stats.total_exp_earned, 50)

        self.stats.record_exp_earned(100)
        self.assertEqual(self.stats.total_exp_earned, 150)

    def test_event_tracking(self):
        """测试事件追踪"""
        self.stats.record_event_triggered("find_bun")
        self.stats.record_event_triggered("find_bun")
        self.stats.record_event_triggered("mine_trap")

        self.assertEqual(self.stats.total_events_triggered, 3)
        self.assertEqual(self.stats.events_by_type["find_bun"], 2)
        self.assertEqual(self.stats.events_by_type["mine_trap"], 1)

    def test_equipment_tracking(self):
        """测试装备追踪"""
        self.stats.record_equipment_found("common")
        self.stats.record_equipment_found("rare")
        self.stats.record_equipment_found("rare")
        self.stats.record_equipment_found("legendary")

        self.assertEqual(self.stats.equipment_found, 4)
        self.assertEqual(self.stats.equipment_by_rarity["common"], 1)
        self.assertEqual(self.stats.equipment_by_rarity["rare"], 2)
        self.assertEqual(self.stats.equipment_by_rarity["legendary"], 1)

    def test_potion_tracking(self):
        """测试药剂追踪"""
        self.stats.record_potion_found()
        self.stats.record_potion_found()
        self.stats.record_potion_found()

        self.stats.record_potion_used()
        self.stats.record_potion_used()

        self.assertEqual(self.stats.potions_found, 3)
        self.assertEqual(self.stats.potions_used, 2)

    def test_skill_tracking(self):
        """测试技能追踪"""
        self.stats.record_skill_learned("火球术")
        self.stats.record_skill_learned("治疗术")

        self.assertEqual(self.stats.skills_learned, 2)

        self.stats.record_skill_used("火球术")
        self.stats.record_skill_used("火球术")
        self.stats.record_skill_used("治疗术")

        self.assertEqual(self.stats.skill_uses["火球术"], 2)
        self.assertEqual(self.stats.skill_uses["治疗术"], 1)

    def test_boss_tracking(self):
        """测试Boss追踪"""
        self.stats.record_battle_start()
        self.stats.record_battle_victory("Dragon", is_boss=True)

        self.assertEqual(self.stats.bosses_defeated, 1)
        self.assertEqual(self.stats.bosses_by_type["Dragon"], 1)
        self.assertEqual(self.stats.monsters_defeated, 0)  # Boss不计入普通怪物

    def test_play_time_formatting(self):
        """测试游戏时长格式化"""
        # 模拟一些游戏时长
        self.stats.total_play_time = 3665  # 1小时1分5秒

        formatted = self.stats.get_play_time_formatted()
        self.assertIn("1h", formatted)
        self.assertIn("1m", formatted)
        self.assertIn("5s", formatted)

    def test_format_summary(self):
        """测试统计摘要格式化"""
        # 添加一些数据
        self.stats.record_step()
        self.stats.record_step()

        self.stats.record_battle_start()
        self.stats.record_battle_victory("Goblin")

        self.stats.record_gold_earned(100)

        summary = self.stats.format_summary(self.lang)

        # 验证包含关键信息
        self.assertIn("游戏时长", summary)
        self.assertIn("总移动步数", summary)
        self.assertIn("战斗统计", summary)
        self.assertIn("总战斗次数: 1", summary)
        self.assertIn("胜利次数: 1", summary)

    def test_to_dict_and_from_dict(self):
        """测试序列化和反序列化"""
        # 添加一些数据
        self.stats.record_step()
        self.stats.record_step()
        self.stats.record_step()

        self.stats.record_battle_start()
        self.stats.record_battle_victory("Goblin")
        self.stats.record_battle_victory("Wolf")

        self.stats.record_gold_earned(200)
        self.stats.record_gold_spent(50)

        # 转换为字典
        data_dict = self.stats.to_dict()

        # 创建新实例并从字典加载
        new_stats = GameStatistics.from_dict(data_dict)

        # 验证数据一致
        self.assertEqual(new_stats.total_steps, 3)
        self.assertEqual(new_stats.battles_won, 2)
        self.assertEqual(new_stats.total_gold_earned, 200)
        self.assertEqual(new_stats.total_gold_spent, 50)
        self.assertEqual(new_stats.monsters_defeated, 2)

    def test_max_win_streak(self):
        """测试最大连胜"""
        # 连胜3场
        for i in range(3):
            self.stats.record_battle_start()
            self.stats.record_battle_victory(f"Monster{i}")

        self.assertEqual(self.stats.max_win_streak, 3)

        # 输一场
        self.stats.record_battle_start()
        self.stats.record_battle_defeat()

        # 再连胜2场
        for i in range(2):
            self.stats.record_battle_start()
            self.stats.record_battle_victory(f"Monster{i+3}")

        # 最大连胜应该还是3
        self.assertEqual(self.stats.max_win_streak, 3)

    def test_shop_tracking(self):
        """测试商店追踪"""
        self.stats.record_shop_visit()
        self.stats.record_shop_visit()

        self.assertEqual(self.stats.shop_visits, 2)

        self.stats.record_item_purchased(3)
        self.stats.record_item_purchased(2)

        self.assertEqual(self.stats.items_purchased, 5)


if __name__ == '__main__':
    unittest.main()
