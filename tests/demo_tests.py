# -*- coding: utf-8 -*-
"""
测试演示脚本 - 展示如何运行可用测试
"""

import sys
import os

# 添加项目路径
project_root = os.path.join(os.path.dirname(__file__), '..')
src_path = os.path.join(project_root, 'src')
hero_path = os.path.join(src_path, 'hero')
sys.path.insert(0, hero_path)
sys.path.insert(0, src_path)

import unittest


def run_demo_tests():
    """运行演示测试"""
    print("=" * 70)
    print("英雄无敌游戏 - 测试演示")
    print("=" * 70)
    print()
    
    # 导入测试模块
    import test_game_config
    import test_language
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加游戏配置测试
    print("添加游戏配置测试...")
    suite.addTests(loader.loadTestsFromModule(test_game_config))
    
    # 添加语言支持测试
    print("添加语言支持测试...")
    suite.addTests(loader.loadTestsFromModule(test_language))
    
    print()
    print("开始运行测试...")
    print("-" * 70)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出摘要
    print()
    print("=" * 70)
    print("测试摘要")
    print("=" * 70)
    print(f"总测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.wasSuccessful():
        print()
        print("🎉 所有测试通过！")
    else:
        print()
        print("⚠️  部分测试失败，请检查详细信息")
    
    print("=" * 70)
    
    return result.wasSuccessful()


def show_test_coverage():
    """显示测试覆盖情况"""
    print()
    print("=" * 70)
    print("测试覆盖情况")
    print("=" * 70)
    print()
    
    print("✅ 完全可用 (13个测试)")
    print("   - test_game_config.py (5个测试)")
    print("   - test_language.py (8个测试)")
    print()
    
    print("⚠️  需要调整 (以下模块需要根据实际实现调整测试)")
    print("   - test_combat.py")
    print("   - test_equipment.py")
    print("   - test_events.py")
    print("   - test_newbie_village.py")
    print("   - test_main.py")
    print("   - integration/test_game_flow.py")
    print()
    
    print("📚 测试工具和基础设施 (100%完成)")
    print("   - fixtures/game_data.py")
    print("   - utils/test_helpers.py")
    print("   - utils/mock_classes.py")
    print("   - run_tests.py")
    print("   - README.md")
    print("   - TESTING_SUMMARY.md")
    print()
    print("=" * 70)


if __name__ == '__main__':
    # 运行演示测试
    success = run_demo_tests()
    
    # 显示测试覆盖情况
    show_test_coverage()
    
    # 返回退出码
    sys.exit(0 if success else 1)
