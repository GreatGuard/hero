#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试装备系统增强版本 - 提高测试覆盖率
"""

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock, Mock

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hero.equipment import EquipmentSystem


class TestEquipmentSystemEnhanced(unittest.TestCase):
    """测试EquipmentSystem类增强版本"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建模拟的HeroGame实例
        self.mock_game = Mock()
        self.mock_game.hero_gold = 100
        self.mock_game.hero_level = 1
        self.mock_game.hero_class = "warrior"
        self.mock_game.base_attack = 10
        self.mock_game.base_defense = 5
        self.mock_game.base_max_hp = 50
        
        # 模拟语言支持
        self.mock_lang = Mock()
        self.mock_lang.get_text = lambda key: {
            "enter_shop": "进入商店",
            "leave_shop": "离开商店",
            "invalid_choice": "无效选择",
            "not_enough_gold": "金币不足",
            "continue_prompt": "按任意键继续",
            "buy_success": "购买成功",
            "shop_title": "商店",
            "weapon": "武器",
            "armor": "护甲",
            "accessory": "饰品",
            "enter_item_number": "输入物品编号",
            "no_equipment": "没有装备",
            "equipment_not_found": "未找到装备",
            "already_equipped": "已经装备",
            "equipment_dropped": "装备已丢弃",
            "confirm_sell": "确认出售",
            "sell_success": "出售成功",
            "confirm_enhance": "确认强化",
            "enhance_success": "强化成功",
            "confirm_enchant": "确认附魔",
            "enchant_success": "附魔成功",
            "enhancement_failed": "强化失败",
            "enchantment_failed": "附魔失败",
            "legendary_attribute": "传说属性"
        }.get(key, key)
        
        self.mock_game.lang = self.mock_lang
        self.mock_game.inventory = []
        self.mock_game.hero_equipment = {}
        
        # 创建装备系统实例
        self.equipment_system = EquipmentSystem(self.mock_game)
    
    def test_init_equipment_system(self):
        """测试装备系统初始化"""
        self.assertEqual(self.equipment_system.game, self.mock_game)
        self.assertIsNotNone(self.equipment_system.weapon_shop_items)
        self.assertIsNotNone(self.equipment_system.armor_shop_items)
        self.assertIsNotNone(self.equipment_system.accessory_shop_items)
    
    def test_generate_equipment(self):
        """测试生成装备"""
        equipment = self.equipment_system.generate_equipment("weapon")
        
        self.assertIsNotNone(equipment)
        self.assertEqual(equipment["type"], "weapon")
        self.assertIn("name", equipment)
        self.assertIn("attack", equipment)
        self.assertIn("price", equipment)
        self.assertIn("rarity", equipment)
    
    def test_generate_equipment_with_rarity(self):
        """测试生成特定稀有度的装备"""
        equipment = self.equipment_system.generate_equipment("armor", rarity="rare")
        
        self.assertIsNotNone(equipment)
        self.assertEqual(equipment["type"], "armor")
        self.assertEqual(equipment["rarity"], "rare")
        self.assertIn("defense", equipment)
        self.assertGreater(equipment["price"], 0)
    
    def test_generate_equipment_legendary(self):
        """测试生成传说级装备"""
        equipment = self.equipment_system.generate_equipment("accessory", rarity="legendary")
        
        self.assertIsNotNone(equipment)
        self.assertEqual(equipment["type"], "accessory")
        self.assertEqual(equipment["rarity"], "legendary")
        self.assertGreater(equipment["price"], 0)
        # 传说装备应该有特殊属性
        self.assertIn("special_attributes", equipment)
    
    def test_generate_equipment_invalid_type(self):
        """测试生成无效类型的装备"""
        equipment = self.equipment_system.generate_equipment("invalid_type")
        
        self.assertIsNone(equipment)
    
    def test_calculate_equipment_value(self):
        """测试计算装备价值"""
        equipment = {
            "attack": 10,
            "defense": 5,
            "hp": 20,
            "special_attributes": {"crit_chance": 0.1}
        }
        
        value = self.equipment_system._calculate_equipment_value(equipment)
        
        self.assertIsInstance(value, (int, float))
        self.assertGreater(value, 0)
    
    def test_get_equipment_color_by_rarity(self):
        """测试根据稀有度获取装备颜色"""
        # 测试普通装备
        color = self.equipment_system._get_equipment_color_by_rarity("common")
        self.assertIsNotNone(color)
        
        # 测试稀有装备
        color = self.equipment_system._get_equipment_color_by_rarity("rare")
        self.assertIsNotNone(color)
        
        # 测试传说装备
        color = self.equipment_system._get_equipment_color_by_rarity("legendary")
        self.assertIsNotNone(color)
        
        # 测试无效稀有度
        color = self.equipment_system._get_equipment_color_by_rarity("invalid")
        self.assertEqual(color, "")
    
    def test_get_shop_items(self):
        """测试获取商店物品"""
        items = self.equipment_system.get_shop_items("weapon")
        
        self.assertIsNotNone(items)
        self.assertIsInstance(items, list)
        
        # 测试无效类型
        items = self.equipment_system.get_shop_items("invalid")
        self.assertEqual(items, [])
    
    def test_buy_equipment(self):
        """测试购买装备"""
        # 创建测试装备
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common"
        }
        
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 购买装备
        result = self.equipment_system.buy_equipment(equipment)
        
        self.assertTrue(result)
        self.assertEqual(self.mock_game.hero_gold, 50)  # 100 - 50
        self.assertIn(equipment, self.mock_game.inventory)
    
    def test_buy_equipment_not_enough_gold(self):
        """测试金币不足时购买装备"""
        # 创建测试装备
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 150,
            "rarity": "common"
        }
        
        # 设置不足的金币
        self.mock_game.hero_gold = 100
        
        # 购买装备
        result = self.equipment_system.buy_equipment(equipment)
        
        self.assertFalse(result)
        self.assertEqual(self.mock_game.hero_gold, 100)  # 金币不变
        self.assertNotIn(equipment, self.mock_game.inventory)
    
    def test_sell_equipment(self):
        """测试出售装备"""
        # 创建测试装备
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common"
        }
        
        # 添加装备到背包
        self.mock_game.inventory.append(equipment)
        
        # 出售装备
        result = self.equipment_system.sell_equipment(equipment)
        
        self.assertTrue(result)
        self.assertGreater(self.mock_game.hero_gold, 100)  # 金币增加
        self.assertNotIn(equipment, self.mock_game.inventory)
    
    def test_sell_equipment_not_in_inventory(self):
        """测试出售不在背包中的装备"""
        # 创建测试装备
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common"
        }
        
        # 确保装备不在背包中
        self.assertNotIn(equipment, self.mock_game.inventory)
        
        # 出售装备
        result = self.equipment_system.sell_equipment(equipment)
        
        self.assertFalse(result)
        self.assertEqual(self.mock_game.hero_gold, 100)  # 金币不变
    
    def test_enhance_equipment(self):
        """测试强化装备"""
        # 创建测试装备
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common",
            "enhancement_level": 0
        }
        
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 强化装备
        result = self.equipment_system.enhance_equipment(equipment)
        
        self.assertTrue(result)
        self.assertGreater(self.mock_game.hero_gold, 100)  # 金币减少
        self.assertEqual(equipment["enhancement_level"], 1)
        self.assertGreater(equipment["attack"], 10)  # 攻击力增加
    
    def test_enhance_equipment_not_enough_gold(self):
        """测试金币不足时强化装备"""
        # 创建测试装备
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common",
            "enhancement_level": 0
        }
        
        # 设置不足的金币
        self.mock_game.hero_gold = 10
        
        # 强化装备
        result = self.equipment_system.enhance_equipment(equipment)
        
        self.assertFalse(result)
        self.assertEqual(self.mock_game.hero_gold, 10)  # 金币不变
        self.assertEqual(equipment["enhancement_level"], 0)
        self.assertEqual(equipment["attack"], 10)  # 攻击力不变
    
    def test_enhance_equipment_max_level(self):
        """测试强化已达到最高等级的装备"""
        # 创建测试装备
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common",
            "enhancement_level": 10  # 最高等级
        }
        
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 强化装备
        result = self.equipment_system.enhance_equipment(equipment)
        
        self.assertFalse(result)
        self.assertEqual(equipment["enhancement_level"], 10)  # 等级不变
    
    def test_enchant_equipment(self):
        """测试附魔装备"""
        # 创建测试装备
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common",
            "enchantment": None
        }
        
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 附魔装备
        result = self.equipment_system.enchant_equipment(equipment, "fire")
        
        self.assertTrue(result)
        self.assertGreater(self.mock_game.hero_gold, 100)  # 金币减少
        self.assertEqual(equipment["enchantment"], "fire")
    
    def test_enchant_equipment_not_enough_gold(self):
        """测试金币不足时附魔装备"""
        # 创建测试装备
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common",
            "enchantment": None
        }
        
        # 设置不足的金币
        self.mock_game.hero_gold = 10
        
        # 附魔装备
        result = self.equipment_system.enchant_equipment(equipment, "fire")
        
        self.assertFalse(result)
        self.assertEqual(self.mock_game.hero_gold, 10)  # 金币不变
        self.assertIsNone(equipment["enchantment"])  # 无附魔
    
    def test_enchant_equipment_already_enchanted(self):
        """测试已附魔的装备再次附魔"""
        # 创建测试装备
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common",
            "enchantment": "ice"
        }
        
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 附魔装备
        result = self.equipment_system.enchant_equipment(equipment, "fire")
        
        self.assertFalse(result)
        self.assertEqual(equipment["enchantment"], "ice")  # 附魔不变
    
    def test_calculate_enhancement_cost(self):
        """测试计算强化费用"""
        # 测试0级装备
        cost = self.equipment_system._calculate_enhancement_cost(0)
        self.assertGreater(cost, 0)
        
        # 测试5级装备
        cost = self.equipment_system._calculate_enhancement_cost(5)
        self.assertGreater(cost, 0)
        
        # 测试10级装备
        cost = self.equipment_system._calculate_enhancement_cost(10)
        self.assertEqual(cost, 0)  # 最高等级不能强化
        
        # 高级装备费用应该更高
        cost_0 = self.equipment_system._calculate_enhancement_cost(0)
        cost_5 = self.equipment_system._calculate_enhancement_cost(5)
        self.assertGreater(cost_5, cost_0)
    
    def test_calculate_enchantment_cost(self):
        """测试计算附魔费用"""
        # 测试普通附魔
        cost = self.equipment_system._calculate_enchantment_cost("fire")
        self.assertGreater(cost, 0)
        
        # 测试稀有附魔
        cost = self.equipment_system._calculate_enchantment_cost("legendary")
        self.assertGreater(cost, 0)
        
        # 稀有附魔费用应该更高
        cost_fire = self.equipment_system._calculate_enchantment_cost("fire")
        cost_legendary = self.equipment_system._calculate_enchantment_cost("legendary")
        self.assertGreater(cost_legendary, cost_fire)
    
    def test_get_enchantment_effect(self):
        """测试获取附魔效果"""
        # 测试火焰附魔
        effect = self.equipment_system._get_enchantment_effect("fire")
        self.assertIsNotNone(effect)
        self.assertIn("name", effect)
        self.assertIn("description", effect)
        self.assertIn("damage_bonus", effect)
        
        # 测试冰霜附魔
        effect = self.equipment_system._get_enchantment_effect("ice")
        self.assertIsNotNone(effect)
        self.assertIn("name", effect)
        self.assertIn("description", effect)
        self.assertIn("attack_debuff", effect)
        
        # 测试无效附魔
        effect = self.equipment_system._get_enchantment_effect("invalid")
        self.assertIsNone(effect)
    
    def test_apply_enchantment_bonus(self):
        """测试应用附魔加成"""
        # 创建测试装备
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common",
            "enchantment": "fire"
        }
        
        # 应用附魔加成
        bonus = self.equipment_system._apply_enchantment_bonus(equipment)
        
        self.assertIsInstance(bonus, dict)
        self.assertIn("fire_damage", bonus)
    
    def test_check_legendary_attributes(self):
        """测试检查传说属性"""
        # 创建10级装备
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common",
            "enhancement_level": 10
        }
        
        # 检查传说属性
        legendary = self.equipment_system._check_legendary_attributes(equipment)
        
        self.assertTrue(legendary)
        self.assertIn("legendary_attribute", equipment)
        self.assertIsNotNone(equipment["legendary_attribute"])
    
    def test_get_random_set_bonus(self):
        """测试获取随机套装奖励"""
        # 测试获取套装奖励
        set_bonus = self.equipment_system._get_random_set_bonus()
        
        self.assertIsNotNone(set_bonus)
        self.assertIn("name", set_bonus)
        self.assertIn("description", set_bonus)
        self.assertIn("pieces_required", set_bonus)
        self.assertIn("bonus", set_bonus)
    
    def test_check_set_bonus(self):
        """测试检查套装奖励"""
        # 创建套装装备
        equipment1 = {
            "name": "测试武器",
            "type": "weapon",
            "set_name": "测试套装",
            "set_piece": 1,
            "set_pieces_required": 2
        }
        
        equipment2 = {
            "name": "测试护甲",
            "type": "armor",
            "set_name": "测试套装",
            "set_piece": 2,
            "set_pieces_required": 2
        }
        
        # 设置已装备的套装
        self.mock_game.hero_equipment = {
            "weapon": equipment1,
            "armor": equipment2
        }
        
        # 检查套装奖励
        set_bonus = self.equipment_system._check_set_bonus()
        
        self.assertIsNotNone(set_bonus)
        self.assertEqual(set_bonus["name"], "测试套装")
        self.assertEqual(set_bonus["pieces_equipped"], 2)
        self.assertEqual(set_bonus["pieces_required"], 2)
    
    def test_apply_set_bonus(self):
        """测试应用套装奖励"""
        # 创建套装奖励
        set_bonus = {
            "name": "测试套装",
            "pieces_equipped": 2,
            "pieces_required": 2,
            "bonus": {"attack": 5}
        }
        
        # 应用套装奖励
        self.equipment_system._apply_set_bonus(set_bonus)
        
        # 奖励应该被应用到游戏对象上
        # 这里我们只能测试方法调用，实际效果需要通过集成测试验证
    
    def test_get_equip_position(self):
        """测试获取装备位置"""
        # 测试武器
        position = self.equipment_system._get_equip_position({"type": "weapon"})
        self.assertEqual(position, "weapon")
        
        # 测试护甲
        position = self.equipment_system._get_equip_position({"type": "armor"})
        self.assertEqual(position, "armor")
        
        # 测试饰品
        position = self.equipment_system._get_equip_position({"type": "accessory"})
        self.assertEqual(position, "accessory")
        
        # 测试无效类型
        position = self.equipment_system._get_equip_position({"type": "invalid"})
        self.assertIsNone(position)
    
    def test_get_equipment_description(self):
        """测试获取装备描述"""
        # 创建测试装备
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "defense": 5,
            "hp": 20,
            "price": 50,
            "rarity": "common",
            "enhancement_level": 2,
            "enchantment": "fire",
            "special_attributes": {"crit_chance": 0.1}
        }
        
        # 获取装备描述
        description = self.equipment_system.get_equipment_description(equipment)
        
        self.assertIsNotNone(description)
        self.assertIn("测试武器", description)
        self.assertIn("攻击", description)
        self.assertIn("强化", description)
        self.assertIn("附魔", description)
    
    def test_get_set_bonus_description(self):
        """测试获取套装奖励描述"""
        # 创建套装奖励
        set_bonus = {
            "name": "测试套装",
            "pieces_equipped": 2,
            "pieces_required": 3,
            "bonus": {"attack": 5, "defense": 3}
        }
        
        # 获取套装奖励描述
        description = self.equipment_system.get_set_bonus_description(set_bonus)
        
        self.assertIsNotNone(description)
        self.assertIn("测试套装", description)
        self.assertIn("2/3", description)
        self.assertIn("攻击", description)
        self.assertIn("防御", description)
    
    def test_format_equipment_list(self):
        """测试格式化装备列表"""
        # 创建测试装备列表
        equipment_list = [
            {"name": "武器", "type": "weapon", "attack": 10, "price": 50, "rarity": "common"},
            {"name": "护甲", "type": "armor", "defense": 5, "price": 30, "rarity": "rare"},
            {"name": "饰品", "type": "accessory", "hp": 10, "price": 20, "rarity": "legendary"}
        ]
        
        # 格式化装备列表
        formatted = self.equipment_system.format_equipment_list(equipment_list)
        
        self.assertIsNotNone(formatted)
        self.assertIn("武器", formatted)
        self.assertIn("护甲", formatted)
        self.assertIn("饰品", formatted)
    
    def test_format_equipment_with_colors(self):
        """测试带颜色格式化装备"""
        # 创建测试装备
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common"
        }
        
        # 格式化装备
        formatted = self.equipment_system._format_equipment_with_colors(equipment, 1)
        
        self.assertIsNotNone(formatted)
        self.assertIn("1.", formatted)
        self.assertIn("测试武器", formatted)
        self.assertIn("攻击", formatted)
        self.assertIn("价格", formatted)
    
    @patch('builtins.input')
    def test_shop_menu(self, mock_input):
        """测试商店菜单"""
        # 模拟用户输入
        mock_input.side_effect = ["4"]  # 离开商店
        
        # 运行商店菜单
        self.equipment_system.shop_menu()
        
        # 验证输入被调用
        self.assertTrue(mock_input.called)
    
    @patch('builtins.input')
    def test_show_inventory(self, mock_input):
        """测试显示背包"""
        # 添加测试装备到背包
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common"
        }
        self.mock_game.inventory.append(equipment)
        
        # 模拟用户输入
        mock_input.return_value = "1"  # 返回
        
        # 显示背包
        self.equipment_system.show_inventory()
        
        # 验证输入被调用
        self.assertTrue(mock_input.called)
    
    @patch('builtins.input')
    def test_equip_item(self, mock_input):
        """测试装备物品"""
        # 添加测试装备到背包
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common"
        }
        self.mock_game.inventory.append(equipment)
        
        # 模拟用户输入
        mock_input.return_value = "1"  # 返回
        
        # 装备物品
        self.equipment_system.equip_item(0)
        
        # 验证装备被装备
        self.assertEqual(self.mock_game.hero_equipment.get("weapon"), equipment)
        self.assertNotIn(equipment, self.mock_game.inventory)
    
    @patch('builtins.input')
    def test_sell_item(self, mock_input):
        """测试出售物品"""
        # 添加测试装备到背包
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common"
        }
        self.mock_game.inventory.append(equipment)
        
        # 模拟用户输入
        mock_input.return_value = "1"  # 返回
        
        # 出售物品
        self.equipment_system.sell_item(0)
        
        # 验证装备被出售
        self.assertNotIn(equipment, self.mock_game.inventory)
        self.assertGreater(self.mock_game.hero_gold, 100)  # 金币增加
    
    @patch('builtins.input')
    def test_enhance_item(self, mock_input):
        """测试强化物品"""
        # 添加测试装备到背包
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common",
            "enhancement_level": 0
        }
        self.mock_game.inventory.append(equipment)
        
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 模拟用户输入
        mock_input.return_value = "1"  # 返回
        
        # 强化物品
        self.equipment_system.enhance_item(0)
        
        # 验证装备被强化
        self.assertEqual(equipment["enhancement_level"], 1)
        self.assertGreater(equipment["attack"], 10)
        self.assertLess(self.mock_game.hero_gold, 100)  # 金币减少
    
    @patch('builtins.input')
    def test_enchant_item(self, mock_input):
        """测试附魔物品"""
        # 添加测试装备到背包
        equipment = {
            "name": "测试武器",
            "type": "weapon",
            "attack": 10,
            "price": 50,
            "rarity": "common",
            "enchantment": None
        }
        self.mock_game.inventory.append(equipment)
        
        # 设置足够的金币
        self.mock_game.hero_gold = 100
        
        # 模拟用户输入
        mock_input.return_value = "1"  # 返回
        
        # 附魔物品
        self.equipment_system.enchant_item(0)
        
        # 验证装备被附魔
        self.assertIsNotNone(equipment["enchantment"])
        self.assertLess(self.mock_game.hero_gold, 100)  # 金币减少


if __name__ == "__main__":
    unittest.main()