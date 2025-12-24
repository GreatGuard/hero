# -*- coding: utf-8 -*-
"""
测试辅助函数
"""

import os
import sys
from unittest.mock import Mock
from io import StringIO


def add_source_to_path():
    """添加源代码路径到系统路径"""
    # 获取当前文件的目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取测试目录的父目录
    parent_dir = os.path.dirname(current_dir)
    # 获取项目根目录
    project_root = os.path.dirname(parent_dir)
    # 添加源代码路径
    src_path = os.path.join(project_root, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)


def create_mock_game():
    """创建模拟游戏对象"""
    from hero.main import HeroGame
    
    mock_game = Mock(spec=HeroGame)
    
    # 设置基本属性
    mock_game.hero_name = "TestHero"
    mock_game.hero_hp = 100
    mock_game.hero_max_hp = 100
    mock_game.hero_attack = 20
    mock_game.hero_defense = 5
    mock_game.base_attack = 20
    mock_game.base_defense = 5
    mock_game.base_max_hp = 100
    mock_game.hero_level = 1
    mock_game.hero_exp = 0
    mock_game.hero_gold = 50
    mock_game.hero_potions = 2
    mock_game.hero_position = 0
    mock_game.hero_skills = []
    mock_game.map_length = 100
    mock_game.difficulty = "normal"
    mock_game.map_type = "plains"
    mock_game.game_over = False
    mock_game.victory = False
    mock_game.monsters_defeated = 0
    mock_game.events_encountered = []
    mock_game.visited_positions = [False] * 100
    
    # 设置装备属性
    mock_game.equipment = {
        "weapon": None,
        "armor": None,
        "accessory": None
    }
    mock_game.inventory = []
    
    # 设置语言属性
    mock_game.language = "zh"
    mock_game.lang = Mock()
    mock_game.lang.get_text.return_value = "test_text"
    mock_game.lang.format_text.return_value = "formatted_text"
    
    # 设置难度设置
    mock_game.difficulty_settings = {
        "easy": {
            "map_length": 50,
            "gold_multiplier": 1.5,
            "exp_multiplier": 1.5,
            "enemy_multiplier": 0.7,
            "gold_start": 30,
            "potions_start": 3
        },
        "normal": {
            "map_length": 100,
            "gold_multiplier": 1.0,
            "exp_multiplier": 1.0,
            "enemy_multiplier": 1.0,
            "gold_start": 20,
            "potions_start": 2
        },
        "hard": {
            "map_length": 150,
            "gold_multiplier": 0.8,
            "exp_multiplier": 1.2,
            "enemy_multiplier": 1.3,
            "gold_start": 15,
            "potions_start": 1
        },
        "nightmare": {
            "map_length": 200,
            "gold_multiplier": 0.6,
            "exp_multiplier": 1.5,
            "enemy_multiplier": 1.6,
            "gold_start": 10,
            "potions_start": 1
        }
    }
    
    # 设置地图类型
    mock_game.map_types = {
        "plains": {
            "name": "plains",
            "description": "plains_desc",
            "special_events": ["find_bun", "find_chest", "find_spring"],
            "monsters": ["goblin", "slime", "wolf"]
        },
        "forest": {
            "name": "forest",
            "description": "forest_desc",
            "special_events": ["find_herbs", "find_equipment", "find_potion"],
            "monsters": ["wolf", "beast", "spider"]
        },
        "desert": {
            "name": "desert",
            "description": "desert_desc",
            "special_events": ["find_oasis", "find_treasure", "find_equipment"],
            "monsters": ["scorpion", "sand_worm", "golem"]
        },
        "dungeon": {
            "name": "dungeon",
            "description": "dungeon_desc",
            "special_events": ["find_chest", "find_equipment", "mysterious_merchant"],
            "monsters": ["skeleton", "ghost", "demon"]
        },
        "mountain": {
            "name": "mountain",
            "description": "mountain_desc",
            "special_events": ["find_gem", "find_equipment", "dragon_encounter"],
            "monsters": ["giant", "dragon", "titan"]
        }
    }
    
    # 模拟方法
    mock_game.update_attributes = Mock()
    mock_game.clear_screen = Mock()
    mock_game.show_hero_info = Mock()
    mock_game.draw_map = Mock()
    mock_game.check_game_status = Mock(return_value=False)
    mock_game.restart_game = Mock()
    
    return mock_game


def capture_stdout(func, *args, **kwargs):
    """捕获函数的标准输出"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    try:
        func(*args, **kwargs)
        return captured_output.getvalue()
    finally:
        sys.stdout = old_stdout


def compare_dicts(dict1, dict2, ignore_keys=None):
    """比较两个字典，可选择忽略某些键"""
    if ignore_keys is None:
        ignore_keys = []
    
    keys1 = set(dict1.keys()) - set(ignore_keys)
    keys2 = set(dict2.keys()) - set(ignore_keys)
    
    if keys1 != keys2:
        return False, f"键不匹配: {keys1.symmetric_difference(keys2)}"
    
    for key in keys1:
        if dict1[key] != dict2[key]:
            return False, f"键 '{key}' 的值不匹配: {dict1[key]} != {dict2[key]}"
    
    return True, "字典匹配"


def create_test_monster(name="TestMonster", hp=50, attack=15, defense=5, exp=20, gold=30):
    """创建测试怪物"""
    return {
        "name": name,
        "hp": hp,
        "max_hp": hp,
        "attack": attack,
        "defense": defense,
        "exp": exp,
        "gold": gold
    }


def create_test_equipment(name="TestEquip", equip_type="weapon", attack=10, defense=0, hp=0, value=50):
    """创建测试装备"""
    return {
        "name": name,
        "type": equip_type,
        "attack": attack,
        "defense": defense,
        "hp": hp,
        "value": value
    }


def setup_test_environment():
    """设置测试环境"""
    # 添加源代码路径
    add_source_to_path()
    
    # 设置随机种子以便测试结果可重现
    import random
    random.seed(42)


def teardown_test_environment():
    """清理测试环境"""
    # 可以在这里添加清理代码
    pass


class TestContext:
    """测试上下文管理器"""
    
    def __init__(self):
        self.setup_done = False
        self.captured_output = None
    
    def __enter__(self):
        setup_test_environment()
        self.old_stdout = sys.stdout
        sys.stdout = self.captured_output = StringIO()
        self.setup_done = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.old_stdout
        teardown_test_environment()
        return False  # 不抑制异常
    
    def get_output(self):
        """获取捕获的输出"""
        if self.captured_output:
            return self.captured_output.getvalue()
        return ""


def assert_in_output(output, *strings):
    """断言输出中包含指定字符串"""
    for s in strings:
        assert s in output, f"输出中不包含字符串: '{s}'"


def assert_not_in_output(output, *strings):
    """断言输出中不包含指定字符串"""
    for s in strings:
        assert s not in output, f"输出中包含不应该出现的字符串: '{s}'"


def assert_output_count(output, substring, expected_count):
    """断言输出中子字符串出现的次数"""
    actual_count = output.count(substring)
    assert actual_count == expected_count, f"子字符串 '{substring}' 出现次数为 {actual_count}，期望为 {expected_count}"


def simulate_user_inputs(inputs):
    """模拟用户输入序列的装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            from unittest.mock import patch
            with patch('builtins.input', side_effect=inputs):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def simulate_random_values(values):
    """模拟随机值的装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            from unittest.mock import patch
            with patch('random.randint', side_effect=values):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def simulate_random_choices(values):
    """模拟随机选择的装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            from unittest.mock import patch
            with patch('random.choice', side_effect=values):
                return func(*args, **kwargs)
        return wrapper
    return decorator