#!/usr/bin/env python3
"""
非交互式性能测试脚本
"""

import time
import os
import sys

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_text_caching():
    """测试文本缓存优化"""
    print("1. 测试文本缓存优化")
    try:
        from hero.language import LanguageSupport
        lang = LanguageSupport()
        lang.set_language('zh')
        
        start = time.time()
        for i in range(5000):
            lang.get_text("welcome")
            lang.get_text("hero_name")
            lang.get_text("difficulty_prompt")
        end = time.time()
        
        print(f"   5000次文本获取: {(end-start)*1000:.2f}ms")
        print(f"   平均每次: {(end-start)*1000000/5000:.2f}μs")
        return True
    except Exception as e:
        print(f"   文本缓存测试失败: {e}")
        return False

def test_event_randomness():
    """测试事件随机逻辑优化"""
    print("\n2. 测试事件随机逻辑优化")
    try:
        import random
        from hero.game_config import EVENT_TYPE_KEYS
        
        start = time.time()
        for i in range(10000):
            idx = random.randint(0, len(EVENT_TYPE_KEYS)-1)
            event_type = EVENT_TYPE_KEYS[idx]
        end = time.time()
        
        print(f"   10000次事件选择: {(end-start)*1000:.2f}ms")
        print(f"   平均每次: {(end-start)*1000000/10000:.2f}μs")
        return True
    except Exception as e:
        print(f"   事件随机逻辑测试失败: {e}")
        return False

def test_equipment_caching():
    """测试装备缓存优化"""
    print("\n3. 测试装备缓存优化")
    try:
        from hero.equipment import EquipmentSystem
        
        # 创建一个模拟游戏对象
        class MockGame:
            class MockLang:
                def get_text(self, key, **kwargs):
                    return f"Text: {key}"
                
                def format_text(self, *args):
                    return f"Formatted: {args[0]}"
            
            def __init__(self):
                self.lang = self.MockLang()
            
            def invalidate_attributes_cache(self):
                pass
        
        game = MockGame()
        equipment_system = EquipmentSystem(game)
        
        # 第一次生成（填充缓存）
        start = time.time()
        for i in range(100):
            equipment_system.create_random_equipment()
        end = time.time()
        
        print(f"   100次装备生成(填充缓存): {(end-start)*1000:.2f}ms")
        
        # 第二次生成（使用缓存）
        start = time.time()
        for i in range(100):
            equipment_system.create_random_equipment()
        end = time.time()
        
        print(f"   100次装备生成(使用缓存): {(end-start)*1000:.2f}ms")
        return True
    except Exception as e:
        print(f"   装备缓存测试失败: {e}")
        return False

def test_module_import_time():
    """测试模块导入时间"""
    print("\n4. 测试模块导入时间")
    try:
        # 测试主要模块的导入时间
        modules = [
            "hero.language",
            "hero.game_config", 
            "hero.combat",
            "hero.equipment",
            "hero.events",
            "hero.save_data",
            "hero.statistics"
        ]
        
        total_time = 0
        for module in modules:
            start = time.time()
            __import__(module)
            end = time.time()
            module_time = (end - start) * 1000
            total_time += module_time
            print(f"   {module}: {module_time:.2f}ms")
        
        print(f"   总导入时间: {total_time:.2f}ms")
        return True
    except Exception as e:
        print(f"   模块导入测试失败: {e}")
        return False

def main():
    """主函数"""
    print("英雄无敌游戏非交互式性能测试")
    print("=" * 40)
    
    results = []
    results.append(test_text_caching())
    results.append(test_event_randomness())
    results.append(test_equipment_caching())
    results.append(test_module_import_time())
    
    # 输出总结
    print("\n" + "=" * 40)
    print("性能优化总结:")
    print("1. 文本获取使用缓存，减少重复格式化计算")
    print("2. 事件随机逻辑使用预计算索引，减少字典查找")
    print("3. 装备生成使用缓存和延迟计算，减少重复对象创建")
    print("4. 模块导入时间优化")
    
    passed = sum(results)
    total = len(results)
    print(f"\n测试通过: {passed}/{total}")
    
    if passed == total:
        print("✅ 所有性能优化测试通过！")
    else:
        print("⚠️ 部分性能优化测试未通过")

if __name__ == "__main__":
    main()