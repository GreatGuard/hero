#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试套装效果多语言显示问题
"""

from src.hero.language import LanguageSupport
from src.hero.game_config import EQUIPMENT_SETS

def debug_set_bonus():
    """调试套装效果显示"""
    lang = LanguageSupport('zh')
    
    # 模拟套装激活的显示逻辑
    set_name = "assassin_set"
    set_info = EQUIPMENT_SETS[set_name]
    
    print("=== 套装效果显示调试 ===")
    print(f"套装名称: {set_name}")
    print(f"配置信息: {set_info}")
    
    # 获取键名
    set_name_key = set_info["name_key"]
    effect = set_info["effects"]["2_piece"]
    bonus_name_key = effect["name_key"]
    
    print(f"\n套装名称键: {set_name_key}")
    print(f"效果名称键: {bonus_name_key}")
    
    # 尝试获取多语言文本
    try:
        set_name_text = lang.get_text(set_name_key)
        bonus_name_text = lang.get_text(bonus_name_key)
        activated_text = lang.get_text('set_bonus_activated')
        
        print(f"\n多语言文本获取结果:")
        print(f"套装名称文本: {set_name_text}")
        print(f"效果名称文本: {bonus_name_text}")
        print(f"激活文本: {activated_text}")
        
        # 模拟完整的显示语句
        display_text = f"✨ {activated_text} {set_name_text}: {bonus_name_text}"
        print(f"\n显示文本: {display_text}")
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    debug_set_bonus()