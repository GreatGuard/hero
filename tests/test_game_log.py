#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
游戏日志系统测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from hero.game_log import GameLog
from hero.language import LanguageSupport

def test_game_log_creation():
    """测试游戏日志创建"""
    print("测试游戏日志创建...")
    
    # 创建中文语言支持
    lang_zh = LanguageSupport("zh")
    game_log_zh = GameLog(lang_zh)
    
    # 创建英文语言支持
    lang_en = LanguageSupport("en")
    game_log_en = GameLog(lang_en)
    
    # 测试日志添加
    game_log_zh.log_event("combat", "战斗测试")
    game_log_zh.log_event("event", "事件测试")
    game_log_zh.log_event("item", "物品测试")
    
    game_log_en.log_event("combat", "Combat test")
    game_log_en.log_event("event", "Event test")
    game_log_en.log_event("item", "Item test")
    
    # 测试日志获取
    logs_zh = game_log_zh.get_logs()
    logs_en = game_log_en.get_logs()
    
    assert len(logs_zh) == 3, f"中文日志数量错误: {len(logs_zh)}"
    assert len(logs_en) == 3, f"英文日志数量错误: {len(logs_en)}"
    
    print("✓ 游戏日志创建测试通过")

def test_game_log_statistics():
    """测试游戏日志统计"""
    print("测试游戏日志统计...")
    
    lang = LanguageSupport("zh")
    game_log = GameLog(lang)
    
    # 添加各种类型的日志
    game_log.log_event("combat", "战斗1")
    game_log.log_event("combat", "战斗2")
    game_log.log_event("event", "事件1")
    game_log.log_event("item", "物品1")
    game_log.log_event("level", "升级1")
    game_log.log_event("movement", "移动1")
    game_log.log_event("achievement", "成就1")
    
    # 测试统计
    stats = game_log.get_statistics()
    
    assert stats['total_entries'] == 7, f"总日志数错误: {stats['total_entries']}"
    assert stats['event_types'].get('combat', 0) == 2, f"战斗日志数错误: {stats['event_types'].get('combat', 0)}"
    assert stats['event_types'].get('event', 0) == 1, f"事件日志数错误: {stats['event_types'].get('event', 0)}"
    assert stats['event_types'].get('item', 0) == 1, f"物品日志数错误: {stats['event_types'].get('item', 0)}"
    assert stats['event_types'].get('level', 0) == 1, f"升级日志数错误: {stats['event_types'].get('level', 0)}"
    assert stats['event_types'].get('movement', 0) == 1, f"移动日志数错误: {stats['event_types'].get('movement', 0)}"
    assert stats['event_types'].get('achievement', 0) == 1, f"成就日志数错误: {stats['event_types'].get('achievement', 0)}"
    
    print("✓ 游戏日志统计测试通过")

def test_game_log_filtering():
    """测试游戏日志筛选"""
    print("测试游戏日志筛选...")
    
    lang = LanguageSupport("zh")
    game_log = GameLog(lang)
    
    # 添加各种类型的日志
    game_log.log_event("combat", "战斗日志1")
    game_log.log_event("combat", "战斗日志2")
    game_log.log_event("event", "事件日志1")
    
    # 测试按类型筛选
    combat_logs = game_log.get_logs_by_type("combat")
    event_logs = game_log.get_logs_by_type("event")
    
    assert len(combat_logs) == 2, f"战斗日志筛选错误: {len(combat_logs)}"
    assert len(event_logs) == 1, f"事件日志筛选错误: {len(event_logs)}"
    
    # 测试不存在的类型
    empty_logs = game_log.get_logs_by_type("nonexistent")
    assert len(empty_logs) == 0, f"不存在的类型日志筛选错误: {len(empty_logs)}"
    
    print("✓ 游戏日志筛选测试通过")

def test_game_log_serialization():
    """测试游戏日志序列化"""
    print("测试游戏日志序列化...")
    
    lang = LanguageSupport("zh")
    game_log = GameLog(lang)
    
    # 添加一些日志
    game_log.log_event("combat", "战斗测试")
    game_log.log_event("event", "事件测试")
    
    # 序列化为字典
    log_dict = game_log.to_dict()
    
    # 从字典恢复
    new_game_log = GameLog(lang)
    new_game_log.from_dict(log_dict)
    
    # 验证恢复的日志
    original_logs = game_log.get_logs()
    restored_logs = new_game_log.get_logs()
    
    assert len(original_logs) == len(restored_logs), "日志数量不匹配"
    
    for i in range(len(original_logs)):
        assert original_logs[i]['type'] == restored_logs[i]['type'], f"日志类型不匹配: {i}"
        assert original_logs[i]['message'] == restored_logs[i]['message'], f"日志消息不匹配: {i}"
    
    print("✓ 游戏日志序列化测试通过")

def test_game_log_clear():
    """测试游戏日志清空"""
    print("测试游戏日志清空...")
    
    lang = LanguageSupport("zh")
    game_log = GameLog(lang)
    
    # 添加一些日志
    game_log.log_event("combat", "战斗测试")
    game_log.log_event("event", "事件测试")
    
    # 验证日志存在
    assert len(game_log.get_logs()) == 2, "日志添加失败"
    
    # 清空日志
    game_log.clear_log()
    
    # 验证日志已清空
    assert len(game_log.get_logs()) == 0, "日志清空失败"
    
    print("✓ 游戏日志清空测试通过")

def test_game_log_display():
    """测试游戏日志显示"""
    print("测试游戏日志显示...")
    
    lang = LanguageSupport("zh")
    game_log = GameLog(lang)
    
    # 添加一些日志
    game_log.log_event("combat", "战斗测试")
    game_log.log_event("event", "事件测试")
    game_log.log_event("item", "物品测试")
    
    # 测试显示所有日志
    print("\n显示所有日志:")
    game_log.show_all_logs()
    
    # 测试显示最近日志
    print("\n显示最近2条日志:")
    game_log.show_recent_logs(2)
    
    # 测试按类型显示
    print("\n显示战斗日志:")
    game_log.show_logs_by_type("combat")
    
    print("✓ 游戏日志显示测试通过")

def main():
    """运行所有测试"""
    print("开始游戏日志系统测试...\n")
    
    try:
        test_game_log_creation()
        test_game_log_statistics()
        test_game_log_filtering()
        test_game_log_serialization()
        test_game_log_clear()
        test_game_log_display()
        
        print("\n🎉 所有游戏日志系统测试通过！")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)