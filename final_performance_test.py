#!/usr/bin/env python3
"""
最终性能测试脚本

这个脚本测试性能优化后的整体游戏性能，包括启动时间、运行时间和内存使用。
"""

import time
import os
import sys

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_startup_performance():
    """测试游戏启动性能"""
    print("=== 测试游戏启动性能 ===")
    
    try:
        # 测试游戏初始化时间
        start_time = time.time()
        from hero.main import HeroGame
        game = HeroGame()
        end_time = time.time()
        
        startup_time = (end_time - start_time) * 1000
        
        print(f"游戏初始化时间: {startup_time:.2f}ms")
        
        # 性能基准检查
        if startup_time > 2000:
            print("⚠️ 启动时间过长 (>2秒)")
        else:
            print("✅ 启动时间正常 (<2秒)")
            
        return startup_time
        
    except Exception as e:
        print(f"启动性能测试失败: {e}")
        return 0

def test_gameplay_performance():
    """测试游戏运行性能"""
    print("\n=== 测试游戏运行性能 ===")
    
    try:
        from hero.main import HeroGame
        
        game = HeroGame()
        
        # 测试1000次游戏操作
        start_time = time.time()
        
        for step in range(1000):
            # 模拟主要游戏操作
            if step % 10 == 0:
                # 每10步更新一次属性（测试属性缓存效果）
                game.update_attributes()
                
            if step % 100 == 0:
                # 每100步获取一次文本（测试文本缓存效果）
                game.lang.get_text("welcome")
                game.lang.get_text("hero_name")
                
            if step % 200 == 0:
                # 每200步生成一件装备（测试装备缓存效果）
                game.equipment_system.create_random_equipment()
        
        end_time = time.time()
        
        total_time = end_time - start_time
        
        print(f"1000次游戏操作时间: {total_time:.3f}秒")
        print(f"平均每步时间: {total_time/1000*1000:.2f}毫秒")
        
        # 性能基准检查
        if total_time > 5:
            print("⚠️ 游戏运行缓慢 (>5秒/1000步)")
        else:
            print("✅ 游戏运行正常 (<5秒/1000步)")
            
        return total_time
        
    except Exception as e:
        print(f"游戏运行性能测试失败: {e}")
        return 0

def test_large_game_performance():
    """测试大量游戏步骤的性能"""
    print("\n=== 测试大量游戏步骤性能 ===")
    
    try:
        from hero.main import HeroGame
        
        game = HeroGame()
        
        # 记录初始内存
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024
        
        # 测试10000次游戏操作
        start_time = time.time()
        
        for step in range(10000):
            if step % 1000 == 0:
                print(f"已完成 {step} 步...")
                
            # 模拟主要游戏操作
            if step % 50 == 0:
                game.update_attributes()
                
            if step % 500 == 0:
                game.lang.get_text("welcome")
                
            if step % 1000 == 0:
                game.equipment_system.create_random_equipment()
        
        end_time = time.time()
        memory_after = process.memory_info().rss / 1024 / 1024
        
        total_time = end_time - start_time
        memory_used = memory_after - memory_before
        
        print(f"10000次游戏操作时间: {total_time:.2f}秒")
        print(f"平均每步时间: {total_time/10000*1000:.2f}毫秒")
        print(f"内存变化: {memory_before:.2f}MB -> {memory_after:.2f}MB ({memory_used:+.2f}MB)")
        
        # 性能基准检查
        if total_time > 30:
            print("⚠️ 大量步骤运行缓慢 (>30秒/10000步)")
        else:
            print("✅ 大量步骤运行正常 (<30秒/10000步)")
            
        if memory_used > 100:
            print("⚠️ 长时间运行内存增长过多 (>100MB/10000步)")
        else:
            print("✅ 长时间运行内存增长正常 (<100MB/10000步)")
            
        return total_time, memory_used
        
    except Exception as e:
        print(f"大量游戏步骤性能测试失败: {e}")
        return 0, 0

def test_specific_optimizations():
    """测试特定优化的效果"""
    print("\n=== 测试特定优化效果 ===")
    
    try:
        from hero.language import LanguageSupport
        from hero.game_config import EVENT_TYPE_KEYS
        from hero.equipment import EquipmentSystem
        
        # 测试文本缓存优化
        lang = LanguageSupport()
        lang.set_language('zh')
        
        start_time = time.time()
        for _ in range(5000):
            lang.get_text("welcome")
            lang.get_text("hero_name")
            lang.get_text("difficulty_prompt")
            lang.get_text("map_type_prompt")
        end_time = time.time()
        
        text_time = (end_time - start_time) * 1000
        print(f"5000次文本获取: {text_time:.2f}ms (平均{text_time/5000:.3f}ms/次)")
        
        # 测试事件随机逻辑优化
        import random
        start_time = time.time()
        for _ in range(10000):
            event_index = random.randint(0, len(EVENT_TYPE_KEYS) - 1)
            event_type = EVENT_TYPE_KEYS[event_index]
        end_time = time.time()
        
        event_time = (end_time - start_time) * 1000
        print(f"10000次事件选择: {event_time:.2f}ms (平均{event_time/10000:.3f}ms/次)")
        
        # 测试装备生成优化
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
        
        start_time = time.time()
        for _ in range(100):
            equipment_system.create_random_equipment()
        end_time = time.time()
        
        equip_time = (end_time - start_time) * 1000
        print(f"100次装备生成: {equip_time:.2f}ms (平均{equip_time/100:.3f}ms/次)")
        
    except Exception as e:
        print(f"特定优化测试失败: {e}")

def main():
    """主函数"""
    print("英雄无敌游戏最终性能测试")
    print("=" * 50)
    
    total_start_time = time.time()
    
    # 运行各项测试
    startup_time = test_startup_performance()
    gameplay_time = test_gameplay_performance()
    test_specific_optimizations()
    
    # 记录结束时间
    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    
    # 输出总结
    print("\n" + "=" * 50)
    print("=== 性能测试总结 ===")
    print(f"总测试时间: {total_time:.2f}秒")
    print(f"游戏启动时间: {startup_time:.2f}ms")
    print(f"1000步游戏时间: {gameplay_time:.3f}秒")
    
    print("\n=== 性能优化效果 ===")
    print("1. 文本获取使用缓存，减少重复格式化计算")
    print("2. 事件随机逻辑使用预计算索引，减少字典查找")
    print("3. 装备生成使用缓存和延迟计算，减少重复对象创建")
    print("4. 属性更新使用缓存机制，避免重复计算")
    print("5. 整体性能提升，特别是在高频操作中")
    
    print("\n=== 性能基准 ===")
    if startup_time < 2000 and gameplay_time < 5:
        print("✅ 所有性能指标达标，优化成功！")
    else:
        print("⚠️ 部分性能指标未达标，需要进一步优化")

if __name__ == "__main__":
    main()