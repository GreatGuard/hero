#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
技能树系统测试
测试技能升级和技能树功能
"""

import sys
import os
import unittest
from unittest.mock import Mock

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.hero.skill_tree import SkillNode, SkillTree
from src.hero.game_config import SKILL_TREES


class TestSkillNode(unittest.TestCase):
    """技能节点测试类"""

    def setUp(self):
        """测试前准备"""
        self.skill_data = {
            "name": "测试技能",
            "description": "这是一个测试技能",
            "max_level": 5,
            "prerequisites": [],
            "cost_per_level": 1,
            "effects_per_level": [2],
            "class_requirement": None
        }
        self.skill_node = SkillNode("test_skill", self.skill_data)

    def test_skill_node_initialization(self):
        """测试技能节点初始化"""
        self.assertEqual(self.skill_node.skill_id, "test_skill")
        self.assertEqual(self.skill_node.current_level, 0)
        self.assertEqual(self.skill_node.max_level, 5)
        self.assertFalse(self.skill_node.is_maxed)

    def test_can_upgrade_with_no_prerequisites(self):
        """测试无前置技能的升级条件"""
        self.assertTrue(self.skill_node.can_upgrade(1, {}))
        self.assertTrue(self.skill_node.can_upgrade(5, {}))
        self.assertFalse(self.skill_node.can_upgrade(0, {}))

    def test_can_upgrade_with_prerequisites(self):
        """测试有前置技能的升级条件"""
        skill_data_with_prereq = {
            "name": "测试技能2",
            "max_level": 3,
            "prerequisites": [("test_skill", 2)],
            "cost_per_level": 1,
            "effects_per_level": [3],
            "class_requirement": None
        }
        skill_node = SkillNode("test_skill2", skill_data_with_prereq)
        
        # 前置技能未满足
        self.assertFalse(skill_node.can_upgrade(1, {"test_skill": 1}))
        self.assertFalse(skill_node.can_upgrade(1, {}))
        
        # 前置技能已满足
        self.assertTrue(skill_node.can_upgrade(1, {"test_skill": 2}))
        self.assertTrue(skill_node.can_upgrade(1, {"test_skill": 3}))

    def test_can_upgrade_when_maxed(self):
        """测试已满级技能的升级条件"""
        self.skill_node.current_level = 5
        self.skill_node._update_status()
        
        self.assertFalse(self.skill_node.can_upgrade(5, {}))
        self.assertFalse(self.skill_node.can_upgrade(10, {}))

    def test_upgrade_success(self):
        """测试技能升级成功"""
        initial_level = self.skill_node.current_level
        result = self.skill_node.upgrade()
        
        self.assertTrue(result)
        self.assertEqual(self.skill_node.current_level, initial_level + 1)

    def test_upgrade_when_maxed(self):
        """测试已满级技能的升级"""
        self.skill_node.current_level = 5
        self.skill_node._update_status()
        
        result = self.skill_node.upgrade()
        
        self.assertFalse(result)
        self.assertEqual(self.skill_node.current_level, 5)

    def test_get_effect_value(self):
        """测试获取效果值"""
        self.skill_node.current_level = 3
        
        effect_value = self.skill_node.get_effect_value(0)
        self.assertEqual(effect_value, 6)  # 3 * 2
        
        # 不存在的效果索引
        non_existent_effect = self.skill_node.get_effect_value(5)
        self.assertEqual(non_existent_effect, 0)

    def test_to_dict(self):
        """测试转换为字典"""
        self.skill_node.current_level = 3
        data = self.skill_node.to_dict()
        
        expected_data = {
            "skill_id": "test_skill",
            "current_level": 3
        }
        self.assertEqual(data, expected_data)


class TestSkillTree(unittest.TestCase):
    """技能树测试类"""

    def setUp(self):
        """测试前准备"""
        self.mock_lang = Mock()
        self.mock_lang.get_text = Mock(side_effect=lambda key, default="": key)
        
        # 使用战士职业的技能树进行测试
        self.hero_class = "warrior"
        self.skill_tree = SkillTree(self.hero_class, self.mock_lang)

    def test_skill_tree_initialization(self):
        """测试技能树初始化"""
        self.assertEqual(self.skill_tree.hero_class, "warrior")
        self.assertEqual(self.skill_tree.lang, self.mock_lang)
        
        # 检查是否包含了所有战士技能
        warrior_skills = SKILL_TREES["warrior"]
        for skill_id in warrior_skills:
            self.assertIn(skill_id, self.skill_tree.skill_nodes)
            self.assertIn(skill_id, self.skill_tree.learned_skills)

    def test_can_upgrade_skill(self):
        """测试技能升级条件检查"""
        # 初始技能点为0时，应该无法升级
        self.assertFalse(self.skill_tree.can_upgrade_skill("power_strike", 0))
        
        # 有技能点时，应该可以升级初始技能
        self.assertTrue(self.skill_tree.can_upgrade_skill("power_strike", 1))

    def test_upgrade_skill_success(self):
        """测试技能升级成功"""
        initial_points = 5
        initial_level = self.skill_tree.learned_skills["power_strike"]
        
        success, remaining_points = self.skill_tree.upgrade_skill("power_strike", initial_points)
        
        self.assertTrue(success)
        self.assertEqual(remaining_points, initial_points - 1)  # 消耗1点技能点
        self.assertEqual(self.skill_tree.learned_skills["power_strike"], initial_level + 1)

    def test_upgrade_skill_failure(self):
        """测试技能升级失败"""
        initial_points = 0
        
        success, remaining_points = self.skill_tree.upgrade_skill("power_strike", initial_points)
        
        self.assertFalse(success)
        self.assertEqual(remaining_points, initial_points)  # 技能点不变

    def test_upgrade_with_prerequisites(self):
        """测试有前置要求的技能升级"""
        # 先升级前置技能到2级
        self.skill_tree.upgrade_skill("power_strike", 10)
        self.skill_tree.upgrade_skill("power_strike", 9)
        
        # 现在应该可以升级shield_bash
        self.assertTrue(self.skill_tree.can_upgrade_skill("shield_bash", 8))
        
        # 升级shield_bash
        success, _ = self.skill_tree.upgrade_skill("shield_bash", 8)
        self.assertTrue(success)
        self.assertEqual(self.skill_tree.learned_skills["shield_bash"], 1)

    def test_get_skill_effect(self):
        """测试获取技能效果"""
        # 升级技能到3级
        self.skill_tree.learned_skills["power_strike"] = 3
        self.skill_tree.skill_nodes["power_strike"].current_level = 3
        
        # 获取效果值
        effect_value = self.skill_tree.get_skill_effect("power_strike", 0)
        
        # 根据配置，power_strike每级增加2点攻击力
        self.assertEqual(effect_value, 6)  # 3 * 2

    def test_format_tree(self):
        """测试技能树格式化"""
        tree_text = self.skill_tree.format_tree()
        
        # 检查是否包含标题
        self.assertIn("skill_tree_title", tree_text)
        
        # 检查是否包含职业信息
        self.assertIn("current_class", tree_text)
        self.assertIn("class_warrior", tree_text)
        
        # 检查是否包含技能分类
        self.assertIn("skill_category_core", tree_text)
        
        # 检查是否包含技能
        self.assertIn("power_strike", tree_text)

    def test_to_dict(self):
        """测试技能树转换为字典"""
        # 升级一个技能
        self.skill_tree.upgrade_skill("power_strike", 5)
        
        data = self.skill_tree.to_dict()
        
        # 检查字典结构
        self.assertIn("hero_class", data)
        self.assertIn("learned_skills", data)
        self.assertEqual(data["hero_class"], "warrior")
        
        # 检查学习技能数据
        self.assertIn("power_strike", data["learned_skills"])
        self.assertEqual(data["learned_skills"]["power_strike"]["current_level"], 1)

    def test_from_dict(self):
        """测试从字典创建技能树"""
        # 创建测试数据
        test_data = {
            "hero_class": "warrior",
            "learned_skills": {
                "power_strike": {
                    "skill_id": "power_strike",
                    "current_level": 3
                }
            }
        }
        
        # 从字典创建技能树
        restored_tree = SkillTree.from_dict(test_data, self.mock_lang)
        
        # 检查恢复的数据
        self.assertEqual(restored_tree.hero_class, "warrior")
        self.assertEqual(restored_tree.learned_skills["power_strike"], 3)
        self.assertEqual(restored_tree.skill_nodes["power_strike"].current_level, 3)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTest(unittest.makeSuite(TestSkillNode))
    suite.addTest(unittest.makeSuite(TestSkillTree))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()


if __name__ == "__main__":
    # 运行测试
    success = run_tests()
    
    if success:
        print("\n✅ 技能树系统测试通过！")
        sys.exit(0)
    else:
        print("\n❌ 技能树系统测试失败！")
        sys.exit(1)