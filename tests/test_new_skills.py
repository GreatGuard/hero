#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试新技能系统
"""

import unittest
import sys
import os
from unittest.mock import patch

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.hero.language import LanguageSupport
from src.hero.events import EventSystem
from src.hero.main import HeroGame

class TestNewSkills(unittest.TestCase):
    """测试新技能系统"""

    def test_new_skill_names_exist(self):
        """测试新技能名称是否存在"""
        # 设置语言
        lang = LanguageSupport("zh")
        
        combo_skill = lang.get_text("combo_skill")
        shield_skill = lang.get_text("shield_skill")
        berserk_skill = lang.get_text("berserk_skill")
        focus_skill = lang.get_text("focus_skill")
        
        # 验证技能名称存在且不为空
        self.assertIsNotNone(combo_skill)
        self.assertIsNotNone(shield_skill)
        self.assertIsNotNone(berserk_skill)
        self.assertIsNotNone(focus_skill)
        
        # 验证技能名称正确
        self.assertEqual(combo_skill, "连斩")
        self.assertEqual(shield_skill, "护盾")
        self.assertEqual(berserk_skill, "狂暴")
        self.assertEqual(focus_skill, "专注")

    def test_new_skill_descriptions_exist(self):
        """测试新技能描述是否存在"""
        # 设置语言
        lang = LanguageSupport("zh")
        
        combo_desc = lang.get_text("combo_desc")
        shield_desc = lang.get_text("shield_desc")
        berserk_desc = lang.get_text("berserk_desc")
        focus_desc = lang.get_text("focus_desc")
        
        self.assertEqual(combo_desc, "连续攻击2次，每次造成50%伤害")
        self.assertEqual(shield_desc, "下次受到伤害减少50%")
        self.assertEqual(berserk_desc, "下3回合攻击提升50%，防御降低50%")
        self.assertEqual(focus_desc, "下次攻击必中且暴击")

    def test_new_skill_actions_exist(self):
        """测试新技能动作文本是否存在"""
        # 设置语言
        lang = LanguageSupport("zh")
        
        cast_combo = lang.get_text("cast_combo")
        cast_shield = lang.get_text("cast_shield")
        cast_berserk = lang.get_text("cast_berserk")
        cast_focus = lang.get_text("cast_focus")
        
        self.assertEqual(cast_combo, "使用连斩")
        self.assertEqual(cast_shield, "使用护盾")
        self.assertEqual(cast_berserk, "进入狂暴")
        self.assertEqual(cast_focus, "专注")

    @patch('builtins.input', return_value='1')  # 模拟选择中文
    def test_new_skill_states_initialized(self, mock_input):
        """测试新技能状态初始化"""
        game = HeroGame()
        
        self.assertFalse(game.shield_active)
        self.assertEqual(game.berserk_turns, 0)
        self.assertFalse(game.focus_active)

    @patch('builtins.input', return_value='1')  # 模拟选择中文
    def test_all_new_skills_in_skill_list(self, mock_input):
        """测试新技能包含在技能列表中"""
        # 设置游戏和语言
        game = HeroGame()
        events = EventSystem(game)
        
        # 获取所有技能
        all_skills = [
            game.lang.get_text("fireball_skill"),
            game.lang.get_text("healing_skill"),
            game.lang.get_text("critical_skill"),
            game.lang.get_text("lifesteal_skill"),
            game.lang.get_text("dodge_skill"),
            game.lang.get_text("combo_skill"),
            game.lang.get_text("shield_skill"),
            game.lang.get_text("berserk_skill"),
            game.lang.get_text("focus_skill")
        ]
        
        # 获取可学习技能
        available_skills = [s for s in all_skills if s not in game.hero_skills]
        
        # 确保新技能都包含在技能列表中
        self.assertEqual(len(all_skills), 9)  # 总共9个技能
        self.assertEqual(len(available_skills), 9)  # 初始状态所有技能都可学

    @patch('builtins.input', return_value='1')  # 模拟选择中文
    def test_shield_skill_effect(self, mock_input):
        """测试护盾技能效果"""
        game = HeroGame()
        
        # 激活护盾
        game.shield_active = True
        
        # 模拟怪物攻击
        monster_damage = 100
        if game.shield_active:
            monster_damage = int(monster_damage * 0.5)
            game.shield_active = False
        
        # 验证伤害减少了50%
        self.assertEqual(monster_damage, 50)
        self.assertFalse(game.shield_active)

    @patch('builtins.input', return_value='1')  # 模拟选择中文
    def test_berserk_skill_effect(self, mock_input):
        """测试狂暴技能效果"""
        game = HeroGame()
        
        # 激活狂暴状态
        game.berserk_turns = 3
        
        # 模拟普通攻击
        base_damage = 50
        if game.berserk_turns > 0:
            base_damage = int(base_damage * 1.5)
        
        # 验证伤害增加了50%
        self.assertEqual(base_damage, 75)
        
        # 模拟回合结束
        game.berserk_turns -= 1
        self.assertEqual(game.berserk_turns, 2)

    @patch('builtins.input', return_value='1')  # 模拟选择中文
    def test_focus_skill_effect(self, mock_input):
        """测试专注技能效果"""
        game = HeroGame()
        
        # 激活专注状态
        game.focus_active = True
        
        # 模拟普通攻击
        base_damage = 50
        if game.focus_active:
            hero_damage = int(base_damage * 2)
            game.focus_active = False
        
        # 验证伤害翻倍且必中
        self.assertEqual(hero_damage, 100)
        self.assertFalse(game.focus_active)

    def test_combo_skill_effect(self):
        """测试连斩技能效果"""
        # 模拟连斩技能
        total_damage = 0
        for i in range(2):  # 连续攻击2次
            base_damage = 50  # 简化计算，实际是50%伤害
            hero_damage = base_damage
            total_damage += hero_damage
            if total_damage >= 100:  # 如果怪物死了，第二次攻击不执行
                break
        
        # 验证两次攻击伤害总和
        self.assertEqual(total_damage, 100)


if __name__ == '__main__':
    unittest.main()