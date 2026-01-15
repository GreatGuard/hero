# -*- coding: utf-8 -*-
"""
英雄无敌游戏平衡性测试工具

该工具用于自动化测试游戏平衡性，通过真实运行多次游戏来收集统计数据。
"""

import unittest
import time
import sys
import os
import json
import statistics
from io import StringIO
from datetime import datetime

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

# 将hero包目录添加到sys.path，以便支持相对导入
hero_path = os.path.join(src_path, 'hero')
if hero_path not in sys.path:
    sys.path.insert(0, hero_path)

# 导入游戏模块
from hero.main import HeroGame
from hero.language import LanguageSupport


class BalanceTestResult:
    """平衡测试结果类"""
    
    def __init__(self, test_name, num_runs):
        self.test_name = test_name
        self.num_runs = num_runs
        self.start_time = None
        self.end_time = None
        self.results = []
        
    def start_test(self):
        """开始测试"""
        self.start_time = time.time()
        
    def end_test(self):
        """结束测试"""
        self.end_time = time.time()
        
    def add_result(self, result_data):
        """添加单个测试结果"""
        self.results.append(result_data)
        
    def get_duration(self):
        """获取测试持续时间"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0
    
    def get_summary(self):
        """获取测试摘要"""
        if not self.results:
            return {
                'total_runs': self.num_runs,
                'completed_runs': 0,
                'success_rate': 0.0,
                'average_steps': 0,
                'average_gold': 0,
                'average_exp': 0,
                'victory_rate': 0.0
            }
        
        completed_runs = len(self.results)
        victory_count = sum(1 for r in self.results if r.get('victory', False))
        
        # 只计算有效的数据
        valid_steps = [r['steps'] for r in self.results if r.get('steps', 0) > 0]
        valid_gold = [r['gold_earned'] for r in self.results if r.get('gold_earned', 0) >= 0]
        valid_exp = [r['exp_earned'] for r in self.results if r.get('exp_earned', 0) >= 0]
        
        return {
            'total_runs': self.num_runs,
            'completed_runs': completed_runs,
            'success_rate': (completed_runs / self.num_runs) * 100,
            'victory_rate': (victory_count / completed_runs) * 100 if completed_runs > 0 else 0,
            'average_steps': statistics.mean(valid_steps) if valid_steps else 0,
            'average_gold': statistics.mean(valid_gold) if valid_gold else 0,
            'average_exp': statistics.mean(valid_exp) if valid_exp else 0,
            'median_steps': statistics.median(valid_steps) if valid_steps else 0,
            'median_gold': statistics.median(valid_gold) if valid_gold else 0,
            'median_exp': statistics.median(valid_exp) if valid_exp else 0,
            'std_steps': statistics.stdev(valid_steps) if len(valid_steps) > 1 else 0,
            'std_gold': statistics.stdev(valid_gold) if len(valid_gold) > 1 else 0,
            'std_exp': statistics.stdev(valid_exp) if len(valid_exp) > 1 else 0
        }
    
    def format_report(self, lang='zh'):
        """格式化报告"""
        summary = self.get_summary()
        
        if lang == 'zh':
            report = []
            report.append("=" * 80)
            report.append(f"英雄无敌游戏平衡性测试报告 - {self.test_name}")
            report.append("=" * 80)
            report.append(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"测试时长: {self.get_duration():.2f} 秒")
            report.append(f"计划运行次数: {summary['total_runs']}")
            report.append(f"完成运行次数: {summary['completed_runs']}")
            report.append(f"测试成功率: {summary['success_rate']:.1f}%")
            report.append(f"通关率: {summary['victory_rate']:.1f}%")
            report.append("-" * 80)
            
            # 统计数据
            report.append("游戏统计数据:")
            report.append(f"  平均步数: {summary['average_steps']:.1f} ± {summary['std_steps']:.1f}")
            report.append(f"  中位数步数: {summary['median_steps']:.1f}")
            report.append(f"  平均获得金币: {summary['average_gold']:.1f} ± {summary['std_gold']:.1f}")
            report.append(f"  中位数金币: {summary['median_gold']:.1f}")
            report.append(f"  平均获得经验: {summary['average_exp']:.1f} ± {summary['std_exp']:.1f}")
            report.append(f"  中位数经验: {summary['median_exp']:.1f}")
            
            # 详细结果
            if len(self.results) <= 10:  # 只显示前10个详细结果
                report.append("-" * 80)
                report.append("详细结果:")
                for i, result in enumerate(self.results[:10], 1):
                    status = "胜利" if result.get('victory', False) else "失败"
                    report.append(f"  {i}. 步数: {result['steps']}, 金币: {result['gold_earned']}, 经验: {result['exp_earned']}, 状态: {status}")
            
            report.append("=" * 80)
            return "\n".join(report)
        else:
            # 英文报告
            report = []
            report.append("=" * 80)
            report.append(f"Heroes Invincible Balance Test Report - {self.test_name}")
            report.append("=" * 80)
            report.append(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"Test Duration: {self.get_duration():.2f} seconds")
            report.append(f"Planned Runs: {summary['total_runs']}")
            report.append(f"Completed Runs: {summary['completed_runs']}")
            report.append(f"Success Rate: {summary['success_rate']:.1f}%")
            report.append(f"Victory Rate: {summary['victory_rate']:.1f}%")
            report.append("-" * 80)
            
            # 统计数据
            report.append("Game Statistics:")
            report.append(f"  Average Steps: {summary['average_steps']:.1f} ± {summary['std_steps']:.1f}")
            report.append(f"  Median Steps: {summary['median_steps']:.1f}")
            report.append(f"  Average Gold Earned: {summary['average_gold']:.1f} ± {summary['std_gold']:.1f}")
            report.append(f"  Median Gold: {summary['median_gold']:.1f}")
            report.append(f"  Average Experience Earned: {summary['average_exp']:.1f} ± {summary['std_exp']:.1f}")
            report.append(f"  Median Experience: {summary['median_exp']:.1f}")
            
            # 详细结果
            if len(self.results) <= 10:
                report.append("-" * 80)
                report.append("Detailed Results:")
                for i, result in enumerate(self.results[:10], 1):
                    status = "Victory" if result.get('victory', False) else "Defeat"
                    report.append(f"  {i}. Steps: {result['steps']}, Gold: {result['gold_earned']}, Exp: {result['exp_earned']}, Status: {status}")
            
            report.append("=" * 80)
            return "\n".join(report)


class GameRunner:
    """游戏运行器类"""
    
    def __init__(self, fast_mode=True, max_steps=1000):
        self.fast_mode = fast_mode
        self.max_steps = max_steps
        
    def run_game(self, difficulty='normal', map_type='plains', hero_class='warrior'):
        """运行单次游戏"""
        try:
            # 导入语言支持
            from hero.language import LanguageSupport
            from hero.game_config import MAP_TYPES, DIFFICULTY_SETTINGS
            from hero.combat import CombatSystem
            from hero.equipment import EquipmentSystem
            from hero.events import EventSystem
            from hero.newbie_village import NewbieVillage
            from hero.statistics import GameStatistics
            from hero.settings import GameSettings
            
            # 手动创建游戏实例（不触发语言选择）
            game = object.__new__(HeroGame)
            
            # 初始化所有子系统
            game.lang = LanguageSupport()
            game.combat_system = CombatSystem(game)
            game.equipment_system = EquipmentSystem(game)
            game.event_system = EventSystem(game)
            game.newbie_village = NewbieVillage(game)
            game.statistics = GameStatistics()
            game.settings = GameSettings()
            
            # 设置游戏参数（跳过语言选择）
            game.language = 'zh'
            game.lang.set_language(game.language)
            game.difficulty = difficulty
            game.map_type = map_type
            game.hero_class = hero_class
            
            # 应用难度系数
            difficulty_settings = DIFFICULTY_SETTINGS[difficulty]
            map_config = MAP_TYPES[map_type]
            map_length_range = [difficulty_settings["map_length"], difficulty_settings["map_length"]]
            
            # 设置地图长度（随机）
            import random
            map_length = random.randint(map_length_range[0], map_length_range[1])
            
            # 设置英雄名称
            game.hero_name = f"TestHero_{int(time.time())}"
            
            # 初始化游戏（跳过新手村）
            game.hero_level = 1
            game.hero_exp = 0
            game.hero_max_hp = 100
            game.hero_hp = 100
            game.hero_attack = 20
            game.hero_defense = 10
            game.base_attack = 20
            game.base_defense = 10
            game.base_max_hp = 100
            game.hero_position = 0
            game.hero_gold = 0
            game.hero_potions = 0
            game.hero_skills = []
            game.equipment = {}
            game.inventory = []
            game.monsters_defeated = 0
            game.events_encountered = 0
            game.visited_positions = []
            game.map_length = map_length
            game.game_over = False
            game.victory = False
            game.inventory = []
            game.monsters_defeated = 0
            game.events_encountered = 0
            game.visited_positions = []
            game.map_length = 30
            game.game_over = False
            game.victory = False
            
            # 初始化统计系统
            game.statistics.start_time = time.time()
            
            # 初始化游戏日志系统
            from hero.game_log import GameLog
            game.game_log = GameLog()
            
            # 初始化任务系统
            from hero.quest import QuestSystem
            game.quest_system = QuestSystem()
            
            # 初始化技能树
            from hero.skill_tree import SkillTree
            game.skill_tree = SkillTree(hero_class, game.language)
            
            # 初始化状态效果变量
            game.status_effects = {}
            game.shield_active = False
            game.berserk_turns = 0
            game.focus_active = False
            
            # 运行游戏主循环
            steps = 0
            while not game.game_over and steps < self.max_steps:
                steps += 1
                
                # 随机移动（简化版）
                game.hero_position += 1
                
                # 检查是否到达终点
                if game.hero_position >= game.map_length:
                    game.victory = True
                    game.game_over = True
                    break
                
                # 随机事件（简化版）
                if steps % 3 == 0:  # 每3步触发一次事件
                    event_result = self._simplified_random_event(game)
                    if event_result == 'game_over':
                        game.game_over = True
                        break
                
                # 战斗（简化版）
                if steps % 5 == 0:  # 每5步触发一次战斗
                    battle_result = self._simplified_combat(game)
                    if battle_result == 'game_over':
                        game.game_over = True
                        break
            
            # 收集结果数据
            result_data = {
                'steps': steps,
                'victory': game.victory,
                'gold_earned': game.hero_gold,
                'exp_earned': game.hero_exp,
                'monsters_defeated': game.monsters_defeated,
                'events_encountered': game.events_encountered,
                'final_hp': game.hero_hp,
                'final_level': game.hero_level
            }
            
            return result_data
            
        except Exception as e:
            # 如果出现异常，返回错误结果
            print(f"游戏运行出错: {e}")
            return {
                'steps': 0,
                'victory': False,
                'gold_earned': 0,
                'exp_earned': 0,
                'monsters_defeated': 0,
                'events_encountered': 0,
                'final_hp': 0,
                'final_level': 1,
                'error': str(e)
            }
    
    def _simplified_random_event(self, game):
        """简化版随机事件"""
        import random
        
        event_types = ['gold', 'potion', 'trap', 'nothing']
        event_type = random.choice(event_types)
        
        if event_type == 'gold':
            gold_amount = random.randint(5, 20)
            game.hero_gold += gold_amount
            game.statistics.record_gold_earned(gold_amount)
            
        elif event_type == 'potion':
            game.hero_potions += 1
            game.statistics.record_potion_found()
            
        elif event_type == 'trap':
            damage = random.randint(5, 15)
            game.hero_hp = max(0, game.hero_hp - damage)
            if game.hero_hp <= 0:
                return 'game_over'
        
        # 记录事件
        game.events_encountered += 1
        try:
            game.statistics.record_event_triggered(event_type)
        except:
            pass  # 忽略统计错误
        
        return 'continue'
    
    def _simplified_combat(self, game):
        """简化版战斗"""
        import random
        
        # 生成怪物
        monster_hp = random.randint(20, 40)
        monster_attack = random.randint(8, 15)
        monster_defense = random.randint(3, 8)
        
        # 战斗逻辑
        while monster_hp > 0 and game.hero_hp > 0:
            # 英雄攻击
            hero_damage = max(1, game.hero_attack - monster_defense)
            monster_hp = max(0, monster_hp - hero_damage)
            
            if monster_hp <= 0:
                break
                
            # 怪物攻击
            monster_damage = max(1, monster_attack - game.hero_defense)
            game.hero_hp = max(0, game.hero_hp - monster_damage)
            
            if game.hero_hp <= 0:
                return 'game_over'
        
        # 战斗胜利
        if monster_hp <= 0:
            gold_reward = random.randint(10, 25)
            exp_reward = random.randint(5, 15)
            
            game.hero_gold += gold_reward
            game.hero_exp += exp_reward
            game.monsters_defeated += 1
            
            # 记录统计
            try:
                game.statistics.record_battle_victory("test_monster", False)
                game.statistics.record_gold_earned(gold_reward)
                game.statistics.record_exp_earned(exp_reward)
            except:
                pass  # 忽略统计错误
            
            # 检查升级
            if game.hero_exp >= 100:
                game.hero_level += 1
                game.hero_exp = 0
                game.hero_max_hp += 10
                game.hero_hp = game.hero_max_hp
                game.hero_attack += 2
                game.hero_defense += 1
        
        return 'continue'


class BalanceTester:
    """平衡测试器主类"""
    
    def __init__(self, fast_mode=True, max_steps=1000):
        self.game_runner = GameRunner(fast_mode, max_steps)
        
    def run_balance_test(self, test_name, num_runs=1000, difficulty='normal', 
                        map_type='plains', hero_class='warrior'):
        """运行平衡测试"""
        
        result = BalanceTestResult(test_name, num_runs)
        result.start_test()
        
        print(f"开始平衡测试: {test_name}")
        print(f"计划运行 {num_runs} 次游戏...")
        
        completed_count = 0
        
        for i in range(num_runs):
            if (i + 1) % 100 == 0:
                print(f"进度: {i + 1}/{num_runs} ({((i + 1) / num_runs) * 100:.1f}%)")
            
            # 运行单次游戏
            game_result = self.game_runner.run_game(difficulty, map_type, hero_class)
            
            # 添加结果
            result.add_result(game_result)
            completed_count += 1
        
        result.end_test()
        
        print(f"测试完成! 实际运行 {completed_count} 次游戏")
        print(f"总耗时: {result.get_duration():.2f} 秒")
        
        return result
    
    def run_difficulty_comparison(self, num_runs=100):
        """运行难度对比测试"""
        difficulties = ['easy', 'normal', 'hard', 'nightmare']
        results = {}
        
        for difficulty in difficulties:
            print(f"\n运行 {difficulty} 难度测试...")
            result = self.run_balance_test(
                f"难度对比_{difficulty}", 
                num_runs, 
                difficulty
            )
            results[difficulty] = result
        
        return results
    
    def run_map_comparison(self, num_runs=100):
        """运行地图对比测试"""
        map_types = ['plains', 'forest', 'desert', 'dungeon', 'mountain', 'swamp', 'snowfield']
        results = {}
        
        for map_type in map_types:
            print(f"\n运行 {map_type} 地图测试...")
            result = self.run_balance_test(
                f"地图对比_{map_type}", 
                num_runs, 
                map_type=map_type
            )
            results[map_type] = result
        
        return results
    
    def run_class_comparison(self, num_runs=100):
        """运行职业对比测试"""
        hero_classes = ['warrior', 'mage', 'assassin']
        results = {}
        
        for hero_class in hero_classes:
            print(f"\n运行 {hero_class} 职业测试...")
            result = self.run_balance_test(
                f"职业对比_{hero_class}", 
                num_runs, 
                hero_class=hero_class
            )
            results[hero_class] = result
        
        return results


class TestBalanceTest(unittest.TestCase):
    """平衡测试工具测试类"""
    
    def test_balance_test_result(self):
        """测试BalanceTestResult类"""
        result = BalanceTestResult("test", 10)
        
        # 测试基本属性
        self.assertEqual(result.test_name, "test")
        self.assertEqual(result.num_runs, 10)
        self.assertEqual(len(result.results), 0)
        
        # 测试添加结果
        test_data = {'steps': 50, 'victory': True, 'gold_earned': 100, 'exp_earned': 50}
        result.add_result(test_data)
        self.assertEqual(len(result.results), 1)
        self.assertEqual(result.results[0], test_data)
        
        # 测试摘要计算
        summary = result.get_summary()
        self.assertEqual(summary['total_runs'], 10)
        self.assertEqual(summary['completed_runs'], 1)
        self.assertEqual(summary['victory_rate'], 100.0)
        
    def test_game_runner(self):
        """测试GameRunner类"""
        runner = GameRunner(fast_mode=True, max_steps=50)
        
        # 运行一次游戏
        result = runner.run_game()
        
        # 验证结果结构
        self.assertIn('steps', result)
        self.assertIn('victory', result)
        self.assertIn('gold_earned', result)
        self.assertIn('exp_earned', result)
        
        # 验证数据类型
        self.assertIsInstance(result['steps'], int)
        self.assertIsInstance(result['victory'], bool)
        self.assertIsInstance(result['gold_earned'], int)
        
    def test_balance_tester_small_run(self):
        """测试BalanceTester小规模运行"""
        tester = BalanceTester(fast_mode=True, max_steps=50)
        
        # 运行小规模测试
        result = tester.run_balance_test("small_test", 5)
        
        # 验证结果
        self.assertEqual(result.test_name, "small_test")
        self.assertEqual(result.num_runs, 5)
        self.assertGreater(len(result.results), 0)
        self.assertGreater(result.get_duration(), 0)
        
        # 验证摘要
        summary = result.get_summary()
        self.assertIn('average_steps', summary)
        self.assertIn('victory_rate', summary)
        
    def test_report_generation(self):
        """测试报告生成"""
        result = BalanceTestResult("report_test", 10)
        
        # 添加一些测试数据
        for i in range(5):
            result.add_result({
                'steps': 30 + i * 5,
                'victory': i % 2 == 0,
                'gold_earned': 50 + i * 10,
                'exp_earned': 25 + i * 5
            })
        
        # 生成中文报告
        zh_report = result.format_report('zh')
        self.assertIn('英雄无敌游戏平衡性测试报告', zh_report)
        self.assertIn('平均步数', zh_report)
        
        # 生成英文报告
        en_report = result.format_report('en')
        self.assertIn('Heroes Invincible Balance Test Report', en_report)
        self.assertIn('Average Steps', en_report)


def run_balance_test_cli():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='英雄无敌游戏平衡性测试工具')
    parser.add_argument('--runs', '-n', type=int, default=100, help='测试运行次数')
    parser.add_argument('--difficulty', '-d', default='normal', help='游戏难度')
    parser.add_argument('--map', '-m', default='plains', help='地图类型')
    parser.add_argument('--class', '-c', dest='hero_class', default='warrior', help='英雄职业')
    parser.add_argument('--fast', '-f', action='store_true', help='快速模式')
    parser.add_argument('--max-steps', type=int, default=1000, help='最大步数')
    parser.add_argument('--compare-difficulty', action='store_true', help='对比不同难度')
    parser.add_argument('--compare-maps', action='store_true', help='对比不同地图')
    parser.add_argument('--compare-classes', action='store_true', help='对比不同职业')
    parser.add_argument('--lang', default='zh', choices=['zh', 'en'], help='报告语言')
    parser.add_argument('--output', '-o', help='输出文件')
    
    args = parser.parse_args()
    
    tester = BalanceTester(fast_mode=args.fast, max_steps=args.max_steps)
    
    if args.compare_difficulty:
        print("运行难度对比测试...")
        results = tester.run_difficulty_comparison(args.runs)
        
        for difficulty, result in results.items():
            report = result.format_report(args.lang)
            print(report)
            
            if args.output:
                filename = f"{args.output}_difficulty_{difficulty}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"报告已保存到 {filename}")
    
    elif args.compare_maps:
        print("运行地图对比测试...")
        results = tester.run_map_comparison(args.runs)
        
        for map_type, result in results.items():
            report = result.format_report(args.lang)
            print(report)
            
            if args.output:
                filename = f"{args.output}_map_{map_type}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"报告已保存到 {filename}")
    
    elif args.compare_classes:
        print("运行职业对比测试...")
        results = tester.run_class_comparison(args.runs)
        
        for hero_class, result in results.items():
            report = result.format_report(args.lang)
            print(report)
            
            if args.output:
                filename = f"{args.output}_class_{hero_class}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"报告已保存到 {filename}")
    
    else:
        # 运行单个测试
        test_name = f"balance_test_{args.difficulty}_{args.map}_{args.hero_class}"
        result = tester.run_balance_test(
            test_name, args.runs, args.difficulty, args.map, args.hero_class
        )
        
        report = result.format_report(args.lang)
        print(report)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存到 {args.output}")


if __name__ == '__main__':
    # 如果是直接运行，使用命令行接口
    run_balance_test_cli()