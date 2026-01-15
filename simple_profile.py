#!/usr/bin/env python3
"""
简化的游戏性能分析脚本
"""

import time
import os
import sys

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 测试关键模块的导入时间
def test_import_performance():
    """测试模块导入性能"""
    print("=== 测试模块导入性能 ===")
    
    modules = [
        "hero.language",
        "hero.game_config", 
        "hero.combat",
        "hero.equipment",
        "hero.events",
        "hero.newbie_village",
        "hero.save_data",
        "hero.statistics"
    ]
    
    for module in modules:
        start_time = time.time()
        try:
            __import__(module)
            end_time = time.time()
            print(f"{module}: {(end_time - start_time) * 1000:.2f}ms")
        except Exception as e:
            print(f"{module}: 导入失败 - {e}")

# 测试文本格式化性能
def test_text_formatting():
    """测试文本格式化性能"""
    print("\n=== 测试文本格式化性能 ===")
    
    try:
        from hero.language import LanguageSupport
        lang = LanguageSupport()
        lang.set_language('zh')
        
        # 测试常用文本获取性能
        start_time = time.time()
        for _ in range(1000):
            _ = lang.get_text("welcome")
            _ = lang.get_text("hero_name")
            _ = lang.get_text("difficulty_prompt")
            _ = lang.get_text("map_type_prompt")
            _ = lang.get_text("class_prompt")
        end_time = time.time()
        
        print(f"1000次文本获取: {(end_time - start_time) * 1000:.2f}ms")
        print(f"平均每次: {(end_time - start_time) * 1000000 / 1000:.2f}μs")
        
    except Exception as e:
        print(f"文本格式化测试失败: {e}")

# 测试事件随机逻辑性能
def test_event_randomness():
    """测试事件随机逻辑性能"""
    print("\n=== 测试事件随机逻辑性能 ===")
    
    try:
        import random
        from hero.game_config import EVENT_TYPES
        
        # 测试随机选择性能
        start_time = time.time()
        for _ in range(10000):
            # 模拟事件选择
            event_type = random.choice(list(EVENT_TYPES.keys()))
            events = EVENT_TYPES[event_type]
            event = random.choice(events)
        end_time = time.time()
        
        print(f"10000次事件随机选择: {(end_time - start_time) * 1000:.2f}ms")
        print(f"平均每次: {(end_time - start_time) * 1000000 / 10000:.2f}μs")
        
        # 测试预计算概率表的性能
        start_time = time.time()
        for _ in range(10000):
            # 使用预计算的索引代替随机选择
            event_index = random.randint(0, len(EVENT_TYPES) - 1)
            event_type = list(EVENT_TYPES.keys())[event_index]
            events = EVENT_TYPES[event_type]
            event_index = random.randint(0, len(events) - 1)
            event = events[event_index]
        end_time = time.time()
        
        print(f"10000次预计算事件选择: {(end_time - start_time) * 1000:.2f}ms")
        print(f"平均每次: {(end_time - start_time) * 1000000 / 10000:.2f}μs")
        
    except Exception as e:
        print(f"事件随机逻辑测试失败: {e}")

# 测试装备生成性能
def test_equipment_generation():
    """测试装备生成性能"""
    print("\n=== 测试装备生成性能 ===")
    
    try:
        from hero.equipment import EquipmentSystem
        equipment_system = EquipmentSystem(None)  # 不需要game实例
        
        # 测试装备生成性能
        start_time = time.time()
        for _ in range(1000):
            _ = equipment_system.generate_equipment(5)  # 生成5级装备
        end_time = time.time()
        
        print(f"1000次装备生成: {(end_time - start_time) * 1000:.2f}ms")
        print(f"平均每次: {(end_time - start_time) * 1000000 / 1000:.2f}μs")
        
    except Exception as e:
        print(f"装备生成测试失败: {e}")

def main():
    """主函数"""
    print("英雄无敌游戏性能分析工具(简化版)")
    print("=" * 50)
    
    test_import_performance()
    test_text_formatting()
    test_event_randomness()
    test_equipment_generation()
    
    print("\n=== 性能优化建议 ===")
    print("1. 考虑缓存语言支持中的常用文本")
    print("2. 使用预计算索引代替随机选择")
    print("3. 装备生成时延迟计算详细属性")
    print("4. 减少不必要的属性更新")

if __name__ == "__main__":
    main()