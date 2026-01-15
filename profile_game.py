#!/usr/bin/env python3
"""
游戏性能分析脚本

这个脚本用于分析英雄无敌游戏的性能瓶颈，并测试优化效果。
"""

import cProfile
import pstats
import io
import time
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

try:
    from src.hero.main import HeroGame
except ImportError:
    try:
        from hero.main import HeroGame
    except ImportError:
        print("错误: 无法导入HeroGame类，请检查脚本运行位置")
        sys.exit(1)


def profile_startup(iterations=10):
    """分析游戏启动性能"""
    print("=== 分析游戏启动性能 ===")
    
    total_time = 0
    for i in range(iterations):
        start_time = time.time()
        game = HeroGame()
        # 只初始化，不启动游戏
        end_time = time.time()
        total_time += (end_time - start_time)
    
    avg_time = total_time / iterations * 1000
    print(f"平均启动时间: {avg_time:.2f}毫秒")
    return avg_time


def profile_gameplay(num_steps=100):
    """分析游戏运行性能"""
    print(f"=== 分析游戏{num_steps}步性能 ===")
    
    # 创建游戏实例
    game = HeroGame()
    
    # 设置为测试模式，避免用户输入
    game.test_mode = True
    
    # 创建Profiler
    pr = cProfile.Profile()
    
    # 开始分析
    pr.enable()
    start_time = time.time()
    
    # 模拟游戏步骤
    for step in range(num_steps):
        # 随机选择一个行动
        import random
        action = random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        if action == '6':  # 购买操作可能导致异常
            continue
        if action == '7':  # 查看统计
            continue
            
        # 简化游戏逻辑，只执行关键步骤
        try:
            if action == '1':  # 前进
                game.random_event()
                game.hero_position += 1
            elif action == '2':  # 后退
                game.hero_position = max(0, game.hero_position - 1)
            elif action == '3':  # 休息
                game.hero_hp = min(game.hero_max_hp, game.hero_hp + 5)
            elif action == '4':  # 使用药水
                if game.hero_potions > 0:
                    game.hero_potions -= 1
                    game.hero_hp = min(game.hero_max_hp, game.hero_hp + 30)
            elif action == '5':  # 战斗
                game.combat()
        except:
            pass  # 忽略异常，专注于性能
    
    end_time = time.time()
    pr.disable()
    
    # 输出结果
    total_time = end_time - start_time
    print(f"总运行时间: {total_time:.3f}秒")
    print(f"平均每步时间: {total_time/num_steps*1000:.2f}毫秒")
    
    # 分析性能瓶颈
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(20)  # 打印前20个最耗时的函数
    print("性能热点:")
    print(s.getvalue())
    
    return total_time


def profile_large_game(num_steps=1000):
    """测试大量步骤游戏的性能"""
    print(f"=== 测试大量步骤游戏性能 ({num_steps}步) ===")
    
    game = HeroGame()
    game.test_mode = True
    
    start_time = time.time()
    memory_before = get_memory_usage()
    
    for step in range(num_steps):
        # 简化游戏逻辑
        if step % 100 == 0:
            print(f"已完成 {step} 步...")
        
        try:
            # 模拟主要游戏操作
            if step % 10 == 0:
                game.random_event()
            game.hero_position = step % game.map_length
        except:
            pass  # 忽略异常
    
    end_time = time.time()
    memory_after = get_memory_usage()
    
    total_time = end_time - start_time
    memory_used = memory_after - memory_before
    
    print(f"总运行时间: {total_time:.2f}秒")
    print(f"平均每步时间: {total_time/num_steps*1000:.2f}毫秒")
    print(f"内存使用: {memory_before:.2f}MB -> {memory_after:.2f}MB (+{memory_used:.2f}MB)")
    
    return total_time, memory_used


def get_memory_usage():
    """获取当前内存使用量（MB）"""
    try:
        import psutil
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    except ImportError:
        print("警告: psutil未安装，无法获取内存使用情况")
        return 0


def main():
    """主函数"""
    print("英雄无敌游戏性能分析工具")
    print("=" * 40)
    
    # 分析启动性能
    startup_time = profile_startup()
    
    print("\n")
    
    # 分析游戏运行性能
    gameplay_time = profile_gameplay(100)
    
    print("\n")
    
    # 测试大量步骤游戏性能
    large_game_time, memory_used = profile_large_game(1000)
    
    print("\n")
    print("=== 性能总结 ===")
    print(f"启动时间: {startup_time:.2f}毫秒")
    print(f"100步游戏时间: {gameplay_time:.2f}秒")
    print(f"1000步游戏时间: {large_game_time:.2f}秒")
    print(f"内存增长(1000步): {memory_used:.2f}MB")
    
    # 性能基准
    print("\n=== 性能基准 ===")
    if startup_time > 2000:
        print("⚠️ 启动时间过长 (>2秒)")
    else:
        print("✅ 启动时间正常 (<2秒)")
        
    if gameplay_time > 5:
        print("⚠️ 游戏运行缓慢 (>5秒/100步)")
    else:
        print("✅ 游戏运行正常 (<5秒/100步)")
        
    if memory_used > 100:
        print("⚠️ 内存增长过快 (>100MB/1000步)")
    else:
        print("✅ 内存使用正常 (<100MB/1000步)")


if __name__ == "__main__":
    main()