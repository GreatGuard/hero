#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单的测试脚本，用于检查导入错误
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from hero.game_config import CLASS_DEFINITIONS
    print("Successfully imported CLASS_DEFINITIONS")
    
    from hero.language import LanguageSupport
    print("Successfully imported LanguageSupport")
    
    from hero.main import HeroGame
    print("Successfully imported HeroGame")
    
    from hero.save_data import SaveData
    print("Successfully imported SaveData")
    
    # 创建一个游戏实例
    game = HeroGame()
    print("Successfully created HeroGame instance")
    
    # 测试职业选择
    game.hero_name = "TestHero"
    print("Successfully set hero name")
    
    # 尝试应用职业属性
    if hasattr(game, 'apply_class_attributes'):
        game.apply_class_attributes('warrior')
        print("Successfully applied warrior class attributes")
    
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()