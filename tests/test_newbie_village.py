# -*- coding: utf-8 -*-
"""
新手村测试
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# 添加项目路径
project_root = os.path.join(os.path.dirname(__file__), '..')
src_path = os.path.join(project_root, 'src')
hero_path = os.path.join(src_path, 'hero')
sys.path.insert(0, hero_path)
sys.path.insert(0, src_path)

from hero.newbie_village import NewbieVillage


class TestNewbieVillage(unittest.TestCase):
    """测试新手村"""
    
    def setUp(self):
        """测试数据准备"""
        self.mock_game = Mock()
        self.mock_game.hero_hp = 80
        self.mock_game.hero_max_hp = 100
        self.mock_game.hero_level = 1
        self.mock_game.hero_exp = 0
        self.mock_game.hero_gold = 50
        # 使用列表确保可以修改
        self.mock_game.hero_skills = []
        self.mock_game.hero_attack = 20
        self.mock_game.hero_potions = 2
        self.mock_game.lang = Mock()
        self.mock_game.lang.get_text = Mock(side_effect=self.mock_get_text)
        self.mock_game.lang.format_text = Mock(return_value=("【", "】"))
        self.mock_game.clear_screen = Mock()
        self.mock_game.show_hero_info = Mock()
        
        # 文本映射
        self.text_map = {
            "block_separator": "==================",
            "newbie_village": "新手村",
            "village_desc": "新手村描述",
            "training_ground": "训练场",
            "village_shop": "村庄商店",
            "village_clinic": "村庄诊所",
            "elder_advice_short": "长老建议",
            "start_adventure": "开始冒险",
            "enter_choice": "请输入选择",
            "invalid_choice": "无效选择",
            "hp_recovered": "生命值已恢复",
            "training_desc": "训练场描述",
            "practice_combat": "练习战斗",
            "learn_skill_short": "学习技能",
            "return_to_village": "返回村庄",
            "training_dummy": "训练假人",
            "hp": "生命值",
            "attack": "攻击力",
            "you_attack": "你攻击了",
            "caused_damage": "造成了",
            "point_damage": "点伤害",
            "poison": "使用药剂，恢复",
            "point_hp": "点生命值",
            "fireball_skill": "火球术",
            "fireball": "释放火球术攻击",
            "fireball_damage": "造成了",
            "full_hp_no_heal": "生命值已满，无需治疗",
            "healing_skill": "治疗术",
            "healing_spell": "施展治疗术，恢复",
            "critical_skill": "暴击技能",
            "lifesteal_skill": "吸血技能",
            "dodge_skill": "闪避技能",
            "locked": "锁定",
            "cast_fireball": "施展火球术",
            "healing_spell_short": "施展治疗术",
            "no_potion": "无药剂",
            "normal_attack": "普通攻击",
            "use_potion_short": "使用药剂",
            "invalid_action": "无效动作",
            "practice_victory": "击败了",
            "practice_reward": "获得奖励",
            "got_exp": "获得经验",
            "exp_points": "点经验",
            "gold_coins": "金币",
            "continue_prompt": "按回车继续",
            "trainer_introduction": "教练介绍",
            "learn_skill_cost": "学习技能需要",
            "gold": "金币",
            "confirm_learn": "确认学习？",
            "yes_options": ['y', 'Y', 'yes', 'Yes', '是', '好', '确定'],
            "cancel_learn": "取消学习",
            "not_enough_gold": "金币不足",
            "shopkeeper_greeting": "店主欢迎词",
            "your_gold": "你的金币",
            "mysterious_teacher": "神秘教师",
            "learn_skill_success": "学习技能成功",
            "skill_brackets": ("【", "】"),
            "learned_skill_event": "学习了技能",
            "all_skills_learned": "所有技能都已学会",
            "buy_potion": "购买药剂",
            "exit_shop": "退出商店",
            "how_many": "购买数量",
            "buy_success": "成功购买",
            "potions": "瓶药剂",
            "hp_full": "生命值已满",
            "clinic_offer": "诊所提供治疗",
            "clinic_cost": "治疗需要",
            "confirm_treatment": "确认治疗？",
            "cancel_treatment": "取消治疗",
            "treatment_success": "治疗成功",
            "elder_advice_title": "长老建议标题",
            "elder_desc": "长老描述",
            "elder_advice_1": "建议1",
            "elder_advice_2": "建议2",
            "elder_advice_3": "建议3",
            "elder_advice_4": "建议4",
            "elder_advice_5": "建议5",
            "elder_advice_6": "建议6",
            "choose_action": "选择动作",
            "practice_start": "开始练习战斗，对手是",
        }
        
        # 创建新手村实例
        self.newbie_village = NewbieVillage(self.mock_game)
    
    def mock_get_text(self, key):
        """模拟多语言文本获取"""
        return self.text_map.get(key, key)
    
    def test_newbie_village_initialization(self):
        """测试新手村初始化"""
        self.assertEqual(self.newbie_village.game, self.mock_game)
        self.assertTrue(hasattr(self.newbie_village, 'training_ground'))
        self.assertTrue(hasattr(self.newbie_village, 'village_shop'))
        self.assertTrue(hasattr(self.newbie_village, 'village_clinic'))
        self.assertTrue(hasattr(self.newbie_village, 'elder_advice'))
    
    def test_training_ground_practice_combat_attack(self):
        """测试训练场-普通攻击"""
        # 提供足够多的输入选项
        inputs = ['1', '1', '1', '1', '']
        with patch('builtins.input', side_effect=inputs):
            with patch('random.randint', return_value=15):
                with patch('builtins.print'):
                    self.newbie_village.practice_combat()
        
        self.assertEqual(self.mock_game.hero_exp, 20)
        self.assertEqual(self.mock_game.hero_gold, 60)
    
    def test_training_ground_practice_combat_with_potion(self):
        """测试训练场-使用药剂"""
        initial_potions = self.mock_game.hero_potions
        initial_hp = self.mock_game.hero_hp
        
        # 提供足够多的输入选项
        # 1. 选择战斗练习 -> '1'
        # 2. 使用药剂 -> '2'
        # 3. 多次普通攻击（每次攻击假人HP=50，每次伤害约15，需要4次）-> '1', '1', '1', '1'
        # 4. 继续提示 -> ''
        inputs = ['1', '2', '1', '1', '1', '1', '']
        with patch('builtins.input', side_effect=inputs):
            with patch('random.randint', return_value=15):
                with patch('builtins.print'):
                    self.newbie_village.practice_combat()
        
        self.assertEqual(self.mock_game.hero_potions, initial_potions - 1)
        self.assertGreater(self.mock_game.hero_hp, initial_hp)
    
    def test_training_ground_practice_combat_with_fireball(self):
        """测试训练场-使用火球术"""
        self.mock_game.hero_skills = ["火球术"]
        
        inputs = ['1', '3', '']
        with patch('builtins.input', side_effect=inputs):
            with patch('random.randint', return_value=25):
                with patch('builtins.print'):
                    self.newbie_village.practice_combat()
        
        self.assertEqual(self.mock_game.hero_exp, 20)
        self.assertEqual(self.mock_game.hero_gold, 60)
    
    def test_training_ground_practice_combat_with_healing(self):
        """测试训练场-使用治疗术"""
        self.mock_game.hero_skills = ["治疗术"]
        self.mock_game.hero_hp = 50
        
        inputs = ['1', '4', '1', '']
        with patch('builtins.input', side_effect=inputs):
            with patch('random.randint', return_value=30):
                with patch('builtins.print'):
                    self.newbie_village.practice_combat()
        
        self.assertGreater(self.mock_game.hero_hp, 50)
    
    def test_training_ground_learn_skill_success(self):
        """测试训练场-学习技能成功"""
        # 确保 hero_skills 是空列表
        self.mock_game.hero_skills = []
        self.mock_game.hero_gold = 50
        initial_gold = self.mock_game.hero_gold

        # 输入序列：确认学习(y) -> 选择技能(1) -> 继续提示
        # 注意：需要确保输入序列足够长以覆盖所有input调用
        inputs = ['y', '1', ''] + [''] * 100

        # 调试：追踪输入使用情况
        input_idx = [0]
        def debug_input(prompt=''):
            idx = input_idx[0]
            result = inputs[idx]
            print(f"  [TEST] Input #{idx}: {result!r} for: {prompt!r}")
            print(f"  [TEST] hero_skills: {self.mock_game.hero_skills}")
            input_idx[0] += 1
            return result

        with patch('builtins.input', side_effect=debug_input):
            # 不 patch print，这样可以看到调试输出
            self.newbie_village.learn_skill_training()

        # 验证扣除金币
        self.assertEqual(self.mock_game.hero_gold, initial_gold - 30)
    
    def test_training_ground_learn_skill_insufficient_gold(self):
        """测试训练场-学习技能金币不足"""
        self.mock_game.hero_gold = 20
        initial_gold = self.mock_game.hero_gold
        
        inputs = ['', '']
        with patch('builtins.input', side_effect=inputs):
            with patch('builtins.print'):
                self.newbie_village.learn_skill_training()
        
        self.assertEqual(self.mock_game.hero_gold, initial_gold)
    
    def test_training_ground_learn_skill_cancel(self):
        """测试训练场-取消学习技能"""
        self.mock_game.hero_gold = 50
        initial_gold = self.mock_game.hero_gold
        
        inputs = ['n', '']
        with patch('builtins.input', side_effect=inputs):
            with patch('builtins.print'):
                self.newbie_village.learn_skill_training()
        
        self.assertEqual(self.mock_game.hero_gold, initial_gold)
    
    def test_village_shop_buy_potion_success(self):
        """测试村庄商店-购买药剂成功"""
        self.mock_game.hero_gold = 50
        initial_gold = self.mock_game.hero_gold
        initial_potions = self.mock_game.hero_potions
        
        inputs = ['1', '2', '']
        with patch('builtins.input', side_effect=inputs):
            with patch('builtins.print'):
                self.newbie_village.village_shop()
        
        self.assertEqual(self.mock_game.hero_gold, initial_gold - 20)
        self.assertEqual(self.mock_game.hero_potions, initial_potions + 2)
    
    def test_village_shop_buy_potion_insufficient_gold(self):
        """测试村庄商店-购买药剂金币不足"""
        self.mock_game.hero_gold = 5
        initial_gold = self.mock_game.hero_gold
        initial_potions = self.mock_game.hero_potions
        
        inputs = ['1', '1', '']
        with patch('builtins.input', side_effect=inputs):
            with patch('builtins.print'):
                self.newbie_village.village_shop()
        
        self.assertEqual(self.mock_game.hero_gold, initial_gold)
        self.assertEqual(self.mock_game.hero_potions, initial_potions)
    
    def test_village_clinic_treatment_success(self):
        """测试村庄诊所-治疗成功"""
        self.mock_game.hero_hp = 60
        self.mock_game.hero_gold = 50
        initial_gold = self.mock_game.hero_gold
        
        inputs = ['y', '']
        with patch('builtins.input', side_effect=inputs):
            with patch('builtins.print'):
                self.newbie_village.village_clinic()
        
        self.assertEqual(self.mock_game.hero_hp, self.mock_game.hero_max_hp)
        self.assertEqual(self.mock_game.hero_gold, initial_gold - 15)
    
    def test_village_clinic_treatment_insufficient_gold(self):
        """测试村庄诊所-治疗金币不足"""
        self.mock_game.hero_hp = 60
        self.mock_game.hero_gold = 10
        initial_hp = self.mock_game.hero_hp
        initial_gold = self.mock_game.hero_gold
        
        inputs = ['', '']
        with patch('builtins.input', side_effect=inputs):
            with patch('builtins.print'):
                self.newbie_village.village_clinic()
        
        self.assertEqual(self.mock_game.hero_hp, initial_hp)
        self.assertEqual(self.mock_game.hero_gold, initial_gold)
    
    def test_village_clinic_hp_full(self):
        """测试村庄诊所-血量已满"""
        self.mock_game.hero_hp = self.mock_game.hero_max_hp
        initial_gold = self.mock_game.hero_gold
        
        inputs = ['', '']
        with patch('builtins.input', side_effect=inputs):
            with patch('builtins.print'):
                self.newbie_village.village_clinic()
        
        self.assertEqual(self.mock_game.hero_gold, initial_gold)
    
    def test_elder_advice(self):
        """测试长老建议"""
        inputs = ['']
        with patch('builtins.input', side_effect=inputs):
            with patch('random.sample', return_value=['建议1', '建议2', '建议3']):
                with patch('builtins.print'):
                    self.newbie_village.elder_advice()
        
        self.assertTrue(self.mock_game.clear_screen.called)
    
    def test_get_combat_action_with_potion(self):
        """测试获取战斗动作-有药剂"""
        self.mock_game.hero_potions = 2
        
        inputs = ['2']
        with patch('builtins.input', side_effect=inputs):
            action = self.newbie_village.get_combat_action()
        
        self.assertEqual(action, '2')
    
    def test_get_combat_action_without_potion(self):
        """测试获取战斗动作-无药剂"""
        self.mock_game.hero_potions = 0
        
        inputs = ['1']
        with patch('builtins.input', side_effect=inputs):
            action = self.newbie_village.get_combat_action()
        self.assertEqual(action, '1')
    
    def test_newbie_village_exit_with_full_hp_recovery(self):
        """测试退出新手村-满血恢复"""
        self.mock_game.hero_hp = 60
        
        inputs = ['', '', '', '', '']
        with patch('builtins.input', side_effect=inputs):
            with patch('time.sleep'):
                with patch('builtins.print'):
                    try:
                        self.newbie_village.newbie_village()
                    except:
                        pass
        
        self.assertEqual(self.mock_game.hero_hp, self.mock_game.hero_max_hp)


if __name__ == '__main__':
    unittest.main()
