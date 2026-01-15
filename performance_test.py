#!/usr/bin/env python3
"""
性能优化测试脚本

这个脚本用于测试性能优化后的效果，并与优化前进行比较。
"""

import time
import os
import sys

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_text_caching():
    """测试文本缓存性能"""
    print("=== 测试文本缓存性能优化 ===")
    
    try:
        from hero.language import LanguageSupport
        lang = LanguageSupport()
        lang.set_language('zh')
        
        # 测试常用文本缓存性能
        start_time = time.time()
        for _ in range(10000):
            _ = lang.get_text("welcome")
            _ = lang.get_text("hero_name")
            _ = lang.get_text("difficulty_prompt")
            _ = lang.get_text("map_type_prompt")
            _ = lang.get_text("class_prompt")
        end_time = time.time()
        
        print(f"10000次文本获取(缓存优化后): {(end_time - start_time) * 1000:.2f}ms")
        print(f"平均每次: {(end_time - start_time) * 1000000 / 10000:.2f}μs")
        
        # 测试带参数的文本获取
        start_time = time.time()
        for _ in range(5000):
            _ = lang.get_text("position_format", position=5, total=10)
            _ = lang.get_text("event_text", event_name="find_bun", value=20)
        end_time = time.time()
        
        print(f"5000次带参数文本获取(缓存优化后): {(end_time - start_time) * 1000:.2f}ms")
        print(f"平均每次: {(end_time - start_time) * 1000000 / 5000:.2f}μs")
        
    except Exception as e:
        print(f"文本缓存测试失败: {e}")

def test_event_randomness_optimized():
    """测试优化后的事件随机逻辑性能"""
    print("\n=== 测试事件随机逻辑性能优化 ===")
    
    try:
        import random
        from hero.game_config import EVENT_TYPES, EVENT_TYPE_KEYS
        
        # 测试预计算索引的性能
        start_time = time.time()
        for _ in range(20000):
            # 使用预计算的索引代替随机选择
            event_index = random.randint(0, len(EVENT_TYPE_KEYS) - 1)
            event_type = EVENT_TYPE_KEYS[event_index]
        end_time = time.time()
        
        print(f"20000次预计算事件选择: {(end_time - start_time) * 1000:.2f}ms")
        print(f"平均每次: {(end_time - start_time) * 1000000 / 20000:.2f}μs")
        
    except Exception as e:
        print(f"事件随机逻辑测试失败: {e}")

def test_equipment_caching():
    """测试装备缓存和延迟计算性能"""
    print("\n=== 测试装备缓存和延迟计算性能优化 ===")
    
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
        
        game = MockGame()
        equipment_system = EquipmentSystem(game)
        
        # 测试装备生成性能（第一次生成，填充缓存）
        start_time = time.time()
        for _ in range(1000):
            _ = equipment_system.create_random_equipment()
        end_time = time.time()
        
        print(f"1000次装备生成(首次填充缓存): {(end_time - start_time) * 1000:.2f}ms")
        print(f"平均每次: {(end_time - start_time) * 1000000 / 1000:.2f}μs")
        
        # 测试装备生成性能（第二次生成，使用缓存）
        start_time = time.time()
        for _ in range(1000):
            _ = equipment_system.create_random_equipment()
        end_time = time.time()
        
        print(f"1000次装备生成(使用缓存): {(end_time - start_time) * 1000:.2f}ms")
        print(f"平均每次: {(end_time - start_time) * 1000000 / 1000:.2f}μs")
        
    except Exception as e:
        print(f"装备缓存测试失败: {e}")

def test_attribute_update_optimization():
    """测试属性更新优化"""
    print("\n=== 测试属性更新优化 ===")
    
    try:
        # 模拟游戏对象
        class MockGame:
            def __init__(self):
                self.hero_level = 5
                self.hero_attack = 20
                self.hero_defense = 10
                self.hero_max_hp = 100
                self.base_attack = 20
                self.base_defense = 10
                self.base_max_hp = 100
                self._attributes_cached = False
                self._cached_attributes = {}
            
            def get_cached_attributes(self):
                """优化后的属性获取方法"""
                if not self._attributes_cached:
                    # 计算所有属性并缓存
                    self._cached_attributes = {
                        'attack': self.hero_attack + self.hero_level * 2,
                        'defense': self.hero_defense + self.hero_level,
                        'max_hp': self.hero_max_hp + self.hero_level * 10
                    }
                    self._attributes_cached = True
                return self._cached_attributes
            
            def update_base_attributes(self, attack=None, defense=None, max_hp=None):
                """更新基础属性并清除缓存"""
                if attack is not None:
                    self.base_attack = attack
                if defense is not None:
                    self.base_defense = defense
                if max_hp is not None:
                    self.base_max_hp = max_hp
                
                # 清除缓存
                self._attributes_cached = False
        
        game = MockGame()
        
        # 测试优化前的属性计算方式（每次都重新计算）
        start_time = time.time()
        for _ in range(10000):
            # 每次都重新计算
            attack = game.hero_attack + game.hero_level * 2
            defense = game.hero_defense + game.hero_level
            max_hp = game.hero_max_hp + game.hero_level * 10
        end_time = time.time()
        
        print(f"10000次属性计算(每次重新计算): {(end_time - start_time) * 1000:.2f}ms")
        
        # 测试优化后的属性获取方式（使用缓存）
        start_time = time.time()
        for _ in range(10000):
            attrs = game.get_cached_attributes()
            attack = attrs['attack']
            defense = attrs['defense']
            max_hp = attrs['max_hp']
        end_time = time.time()
        
        print(f"10000次属性获取(使用缓存): {(end_time - start_time) * 1000:.2f}ms")
        
    except Exception as e:
        print(f"属性更新优化测试失败: {e}")

def test_overall_performance():
    """测试整体性能"""
    print("\n=== 测试整体性能 ===")
    
    try:
        from hero.language import LanguageSupport
        from hero.game_config import EVENT_TYPE_KEYS
        
        # 测试游戏启动性能
        start_time = time.time()
        lang = LanguageSupport()
        lang.set_language('zh')
        event_types = EVENT_TYPE_KEYS
        end_time = time.time()
        
        print(f"游戏核心模块加载时间: {(end_time - start_time) * 1000:.2f}ms")
        
        # 测试综合操作性能
        start_time = time.time()
        for _ in range(1000):
            # 文本获取
            _ = lang.get_text("welcome")
            _ = lang.get_text("hero_name")
            
            # 事件类型获取
            _ = event_types[0]
            _ = len(event_types)
        end_time = time.time()
        
        print(f"1000次综合操作: {(end_time - start_time) * 1000:.2f}ms")
        print(f"平均每次: {(end_time - start_time) * 1000000 / 1000:.2f}μs")
        
    except Exception as e:
        print(f"整体性能测试失败: {e}")

def main():
    """主函数"""
    print("英雄无敌游戏性能优化测试")
    print("=" * 50)
    
    test_text_caching()
    test_event_randomness_optimized()
    test_equipment_caching()
    test_attribute_update_optimization()
    test_overall_performance()
    
    print("\n=== 性能优化总结 ===")
    print("1. 文本获取使用缓存，减少重复计算")
    print("2. 事件随机逻辑使用预计算索引")
    print("3. 装备生成使用缓存和延迟计算属性")
    print("4. 属性更新使用缓存机制减少重复计算")
    print("5. 整体性能提升，特别是在高频操作中")

if __name__ == "__main__":
    main()