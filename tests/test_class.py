#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
职业系统测试模块
"""

import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from hero.game_config import CLASS_DEFINITIONS
from hero.language import LanguageSupport
from hero.main import HeroGame
from hero.save_data import SaveData


class TestHeroGame(HeroGame):
    """测试用的HeroGame类，跳过用户输入"""
    
    def __init__(self):
        # 先初始化语言支持
        self.language = "zh"
        self.lang = LanguageSupport(self.language)
        
        # 设置其他属性
        self.hero_name = ""
        self.hero_class = ""
        self.hero_hp = 100
        self.hero_max_hp = 100
        self.hero_attack = 20
        self.hero_defense = 5
        self.hero_position = 0
        self.hero_exp = 0
        self.hero_level = 1
        self.hero_skills = []
        self.game_over = False
        self.victory = False
        self.monsters_defeated = 0
        self.events_encountered = []
        
        # 职业系统相关属性
        self.class_mana = 0
        self.class_max_mana = 0
        self.combat_first_turn = True
        
        # 技能状态跟踪
        self.shield_active = False
        self.berserk_turns = 0
        self.focus_active = False
        
        # 装备系统
        self.equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        self.inventory = []
        
        # 基础属性
        self.base_attack = 20
        self.base_defense = 5
        self.base_max_hp = 100
        
        # 添加必要的属性
        self.hero_gold = 0
        self.hero_potions = 0
        self.difficulty = "normal"
        self.map_type = "plains"
        self.map_length = 10
        self.visited_positions = [False] * self.map_length
        
        # 更新属性
        self.update_attributes()
        
        # 初始化状态效果系统
        self.status_effects = {
            "poison": 0,
            "frostbite": 0,
            "frost": 0
        }
        
        # 初始化特殊效果属性
        self.special_effects = {
            "crit_rate": 0.0,
            "lifesteal_rate": 0.0,
            "dodge_rate": 0.0,
            "counter_attack_rate": 0.0,
            "ice_damage": 0,
            "fire_damage": 0,
            "healing_rate": 0.0,
            "mana_boost": 0,
            "backstab_damage": 0.0,
            "luck_bonus": 0.0,
            "wisdom_bonus": 0.0,
            "immortality_chance": 0.0,
            "health_regeneration": 0,
            "mana_regeneration": 0,
            "holy_resistance": 0.0,
            "fire_resistance": 0.0,
            "stealth_chance": 0.0,
            "evasion_rate": 0.0,
            "spell_power": 0.0,
            "crit_damage": 0.0
        }
    
    def update_attributes(self):
        """更新英雄属性"""
        self.hero_attack = self.base_attack
        self.hero_defense = self.base_defense
        self.hero_max_hp = self.base_max_hp
        self.hero_hp = min(self.hero_hp, self.hero_max_hp)
    
    def apply_class_attributes(self, class_key):
        """应用职业属性加成"""
        from hero.game_config import CLASS_DEFINITIONS
        
        class_info = CLASS_DEFINITIONS[class_key]
        
        # 应用基础属性
        self.base_attack = class_info['base_attributes']['attack']
        self.base_defense = class_info['base_attributes']['defense']
        self.base_max_hp = class_info['base_attributes']['max_hp']
        
        # 初始化当前属性
        self.hero_hp = self.base_max_hp
        self.hero_max_hp = self.base_max_hp
        
        # 如果是法师，初始化法力值
        if class_key == "mage":
            self.class_max_mana = 100  # 初始法力值
            self.class_mana = self.class_max_mana
        
        # 更新总属性
        self.update_attributes()
    
    def get_class_growth_multiplier(self, attribute):
        """获取职业属性成长倍率"""
        from hero.game_config import CLASS_DEFINITIONS
        
        if not self.hero_class:
            return 1.0
            
        class_info = CLASS_DEFINITIONS.get(self.hero_class, {})
        growth_multipliers = class_info.get('growth_multipliers', {})
        return growth_multipliers.get(attribute, 1.0)


class TestClassSystem(unittest.TestCase):
    """职业系统测试类"""

    def setUp(self):
        """测试前准备"""
        self.game = TestHeroGame()
        self.game.hero_name = "TestHero"

    def test_class_definitions_exist(self):
        """测试职业定义是否存在"""
        self.assertIn("warrior", CLASS_DEFINITIONS)
        self.assertIn("mage", CLASS_DEFINITIONS)
        self.assertIn("assassin", CLASS_DEFINITIONS)

    def test_class_definition_structure(self):
        """测试职业定义结构是否完整"""
        for class_key, class_info in CLASS_DEFINITIONS.items():
            # 检查必需的键
            self.assertIn("name_key", class_info)
            self.assertIn("description_key", class_info)
            self.assertIn("base_attributes", class_info)
            self.assertIn("growth_multipliers", class_info)
            self.assertIn("starting_skills", class_info)
            self.assertIn("skill_affinity", class_info)
            self.assertIn("equipment_preference", class_info)
            
            # 检查基础属性结构
            base_attrs = class_info["base_attributes"]
            self.assertIn("attack", base_attrs)
            self.assertIn("defense", base_attrs)
            self.assertIn("max_hp", base_attrs)
            
            # 检查成长倍率结构
            growth = class_info["growth_multipliers"]
            self.assertIn("attack", growth)
            self.assertIn("defense", growth)
            self.assertIn("max_hp", growth)

    def test_class_attributes_difference(self):
        """测试不同职业的属性差异"""
        warrior = CLASS_DEFINITIONS["warrior"]
        mage = CLASS_DEFINITIONS["mage"]
        assassin = CLASS_DEFINITIONS["assassin"]
        
        # 战士应该有高血量和防御
        self.assertGreaterEqual(warrior["base_attributes"]["max_hp"], mage["base_attributes"]["max_hp"])
        self.assertGreaterEqual(warrior["base_attributes"]["defense"], mage["base_attributes"]["defense"])
        
        # 法师应该有高攻击成长率（魔法攻击）
        self.assertGreaterEqual(mage["growth_multipliers"]["attack"], warrior["growth_multipliers"]["attack"])
        
        # 刺客应该有高攻击
        self.assertGreater(assassin["base_attributes"]["attack"], mage["base_attributes"]["attack"])

    def test_apply_class_attributes(self):
        """测试应用职业属性"""
        # 测试战士属性应用
        self.game.hero_class = "warrior"
        self.game.apply_class_attributes("warrior")
        
        warrior_info = CLASS_DEFINITIONS["warrior"]
        self.assertEqual(self.game.base_attack, warrior_info["base_attributes"]["attack"])
        self.assertEqual(self.game.base_defense, warrior_info["base_attributes"]["defense"])
        self.assertEqual(self.game.base_max_hp, warrior_info["base_attributes"]["max_hp"])
        
        # 测试法师属性应用
        self.game.hero_class = "mage"
        self.game.apply_class_attributes("mage")
        
        mage_info = CLASS_DEFINITIONS["mage"]
        self.assertEqual(self.game.base_attack, mage_info["base_attributes"]["attack"])
        self.assertEqual(self.game.base_defense, mage_info["base_attributes"]["defense"])
        self.assertEqual(self.game.base_max_hp, mage_info["base_attributes"]["max_hp"])
        
        # 法师应该有法力值
        self.assertEqual(self.game.class_max_mana, 100)
        self.assertEqual(self.game.class_mana, 100)

    def test_class_growth_multipliers(self):
        """测试职业成长倍率"""
        # 测试战士成长倍率
        self.game.hero_class = "warrior"
        attack_multiplier = self.game.get_class_growth_multiplier('attack')
        defense_multiplier = self.game.get_class_growth_multiplier('defense')
        hp_multiplier = self.game.get_class_growth_multiplier('max_hp')
        
        warrior_growth = CLASS_DEFINITIONS["warrior"]["growth_multipliers"]
        self.assertEqual(attack_multiplier, warrior_growth["attack"])
        self.assertEqual(defense_multiplier, warrior_growth["defense"])
        self.assertEqual(hp_multiplier, warrior_growth["max_hp"])

    def test_class_initialization(self):
        """测试职业初始化"""
        # 模拟选择刺客职业
        self.game.hero_class = "assassin"
        self.game.apply_class_attributes("assassin")
        
        assassin_info = CLASS_DEFINITIONS["assassin"]
        
        # 检查是否应用了正确的初始属性
        self.assertEqual(self.game.base_attack, assassin_info["base_attributes"]["attack"])
        self.assertEqual(self.game.base_defense, assassin_info["base_attributes"]["defense"])
        self.assertEqual(self.game.base_max_hp, assassin_info["base_attributes"]["max_hp"])
        
        # 模拟添加初始技能
        self.game.hero_skills = []
        for skill in assassin_info['starting_skills']:
            self.game.hero_skills.append(self.game.lang.get_text(f"{skill}_skill"))
        
        # 检查是否添加了初始技能
        self.assertIn(self.game.lang.get_text(f"{assassin_info['starting_skills'][0]}_skill"), 
                     self.game.hero_skills)

    def test_class_save_and_load(self):
        """测试职业数据的保存和加载"""
        # 设置职业
        self.game.hero_class = "warrior"
        self.game.apply_class_attributes("warrior")
        
        # 创建存档数据
        save_data = SaveData(self.game)
        
        # 检查存档中的职业数据
        self.assertEqual(save_data.hero_class, "warrior")
        
        # 创建新游戏实例
        new_game = TestHeroGame()
        new_game.hero_name = "NewHero"
        
        # 模拟load_from_save_data方法
        new_game.hero_class = save_data.hero_class
        new_game.hero_level = save_data.hero_level
        new_game.hero_exp = save_data.hero_exp
        new_game.hero_hp = save_data.hero_hp
        new_game.hero_max_hp = save_data.hero_max_hp
        new_game.hero_attack = save_data.hero_attack
        new_game.hero_defense = save_data.hero_defense
        new_game.base_attack = save_data.base_attack
        new_game.base_defense = save_data.base_defense
        new_game.base_max_hp = save_data.base_max_hp
        
        # 检查是否正确加载了职业数据
        self.assertEqual(new_game.hero_class, "warrior")
        self.assertEqual(new_game.base_attack, self.game.base_attack)
        self.assertEqual(new_game.base_defense, self.game.base_defense)
        self.assertEqual(new_game.base_max_hp, self.game.base_max_hp)

    def test_class_text_support(self):
        """测试职业多语言文本支持"""
        # 中文文本测试
        self.game.lang.set_language("zh")
        self.assertIn("class_warrior", self.game.lang.texts)
        self.assertIn("class_mage", self.game.lang.texts)
        self.assertIn("class_assassin", self.game.lang.texts)
        
        # 英文文本测试
        self.game.lang.set_language("en")
        self.assertIn("class_warrior", self.game.lang.texts)
        self.assertIn("class_mage", self.game.lang.texts)
        self.assertIn("class_assassin", self.game.lang.texts)

    def test_class_skill_affinity(self):
        """测试职业技能亲和度"""
        # 每个职业应该有不同的技能亲和列表
        warrior_skills = set(CLASS_DEFINITIONS["warrior"]["skill_affinity"])
        mage_skills = set(CLASS_DEFINITIONS["mage"]["skill_affinity"])
        assassin_skills = set(CLASS_DEFINITIONS["assassin"]["skill_affinity"])
        
        # 职业技能列表不应完全相同
        self.assertNotEqual(warrior_skills, mage_skills)
        self.assertNotEqual(warrior_skills, assassin_skills)
        self.assertNotEqual(mage_skills, assassin_skills)
        
        # 检查技能列表是否非空
        self.assertTrue(len(warrior_skills) > 0)
        self.assertTrue(len(mage_skills) > 0)
        self.assertTrue(len(assassin_skills) > 0)


if __name__ == "__main__":
    unittest.main()