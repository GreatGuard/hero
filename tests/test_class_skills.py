#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
职业技能系统测试
测试职业技能差异的实现
"""

import sys
import os
import unittest
from unittest.mock import Mock

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.hero.game_config import CLASS_DEFINITIONS
from src.hero.combat import CombatSystem


class TestClassSkills(unittest.TestCase):
    """职业技能系统测试类"""

    def setUp(self):
        """测试前准备"""
        # 创建模拟游戏对象
        self.mock_game = Mock()
        self.mock_game.hero_class = "warrior"
        self.mock_game.hero_max_hp = 100
        self.mock_game.hero_hp = 80
        self.mock_game.hero_attack = 20
        self.mock_game.hero_defense = 10
        self.mock_game.special_effects = {
            "crit_rate": 0.1,
            "crit_damage": 0.0,
            "lifesteal_rate": 0.0,
            "damage_reduction": 0.0,
            "backstab_damage": 0.0,
            "ice_damage": 0.0,
            "fire_damage": 0.0,
            "dodge_rate": 0.0
        }
        
        # 创建模拟语言对象
        self.mock_lang = Mock()
        self.mock_lang.get_text = Mock(side_effect=lambda key: key)
        self.mock_game.lang = self.mock_lang
        
        # 创建战斗系统
        self.combat_system = CombatSystem(self.mock_game)

    def test_class_definitions_exist(self):
        """测试职业配置是否存在"""
        self.assertIn("warrior", CLASS_DEFINITIONS)
        self.assertIn("mage", CLASS_DEFINITIONS)
        self.assertIn("assassin", CLASS_DEFINITIONS)
        
        # 检查每个职业是否有必要的配置
        for class_name, class_config in CLASS_DEFINITIONS.items():
            self.assertIn("base_attributes", class_config)
            self.assertIn("growth_multipliers", class_config)
            self.assertIn("class_skills", class_config)
            self.assertIn("passive_effects", class_config)

    def test_warrior_passive_effects(self):
        """测试战士被动效果"""
        warrior_config = CLASS_DEFINITIONS["warrior"]
        passive_effects = warrior_config["passive_effects"]
        
        self.assertIn("damage_reduction", passive_effects)
        self.assertIn("hp_regen_per_turn", passive_effects)
        self.assertIn("counter_attack_chance", passive_effects)
        
        # 验证数值范围
        self.assertGreater(passive_effects["damage_reduction"], 0)
        self.assertLess(passive_effects["damage_reduction"], 0.5)
        self.assertGreater(passive_effects["hp_regen_per_turn"], 0)

    def test_mage_passive_effects(self):
        """测试法师被动效果"""
        mage_config = CLASS_DEFINITIONS["mage"]
        passive_effects = mage_config["passive_effects"]
        
        self.assertIn("spell_power", passive_effects)
        self.assertIn("mana_regen", passive_effects)
        self.assertIn("elemental_resistance", passive_effects)
        
        # 验证法师有法力值系统
        self.assertTrue(mage_config.get("mana_system", False))

    def test_assassin_passive_effects(self):
        """测试刺客被动效果"""
        assassin_config = CLASS_DEFINITIONS["assassin"]
        passive_effects = assassin_config["passive_effects"]
        
        self.assertIn("crit_rate", passive_effects)
        self.assertIn("dodge_chance", passive_effects)
        self.assertIn("first_turn_damage", passive_effects)
        
        # 验证刺客有高暴击率
        self.assertGreater(passive_effects["crit_rate"], 0.1)

    def test_class_skills_exist(self):
        """测试职业技能存在"""
        for class_name, class_config in CLASS_DEFINITIONS.items():
            class_skills = class_config["class_skills"]
            self.assertGreater(len(class_skills), 0)
            
            # 检查每个职业都有至少2个专属技能
            self.assertGreaterEqual(len(class_skills), 2)

    def test_apply_class_passives(self):
        """测试应用职业被动效果"""
        # 测试战士被动效果
        self.mock_game.hero_class = "warrior"
        self.combat_system.apply_class_passives()
        
        # 验证战士的特殊效果被设置
        warrior_config = CLASS_DEFINITIONS["warrior"]
        passive_effects = warrior_config["passive_effects"]
        
        self.assertEqual(
            self.mock_game.special_effects["damage_reduction"],
            passive_effects["damage_reduction"]
        )

    def test_handle_normal_attack(self):
        """测试普通攻击处理"""
        monster_hp = 50
        result_hp = self.combat_system.handle_normal_attack("测试怪物", monster_hp, 1)
        
        # 验证怪物血量减少
        self.assertLess(result_hp, monster_hp)

    def test_handle_class_skill(self):
        """测试职业技能处理"""
        # 测试战士的盾击技能
        self.mock_game.hero_class = "warrior"
        monster_hp = 50
        
        result_hp = self.combat_system.handle_class_skill("shield_bash", "测试怪物", monster_hp, 1)
        
        # 验证技能效果
        self.assertLess(result_hp, monster_hp)

    def test_skill_affinity(self):
        """测试技能亲和性"""
        for class_name, class_config in CLASS_DEFINITIONS.items():
            skill_affinity = class_config["skill_affinity"]
            self.assertGreater(len(skill_affinity), 0)
            
            # 验证技能亲和性包含职业专属技能
            class_skills = class_config["class_skills"]
            for skill in class_skills:
                self.assertIn(skill, skill_affinity)

    def test_equipment_preference(self):
        """测试装备偏好"""
        for class_name, class_config in CLASS_DEFINITIONS.items():
            equipment_preference = class_config["equipment_preference"]
            
            self.assertIn("weapon", equipment_preference)
            self.assertIn("armor", equipment_preference)
            self.assertIn("accessory", equipment_preference)

    def test_class_growth_multipliers(self):
        """测试职业成长倍率"""
        for class_name, class_config in CLASS_DEFINITIONS.items():
            growth_multipliers = class_config["growth_multipliers"]
            
            self.assertIn("attack", growth_multipliers)
            self.assertIn("defense", growth_multipliers)
            self.assertIn("max_hp", growth_multipliers)
            
            # 验证成长倍率合理
            self.assertGreater(growth_multipliers["attack"], 0.8)
            self.assertLess(growth_multipliers["attack"], 1.5)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClassSkills)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()


if __name__ == "__main__":
    # 运行测试
    success = run_tests()
    
    if success:
        print("\n✅ 职业技能系统测试通过！")
        sys.exit(0)
    else:
        print("\n❌ 职业技能系统测试失败！")
        sys.exit(1)