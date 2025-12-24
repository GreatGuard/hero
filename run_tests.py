# -*- coding: utf-8 -*-
"""
运行测试脚本
"""

import unittest
import sys
import os
import argparse
from io import StringIO

# 添加项目路径
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

# 将hero包目录添加到sys.path，以便支持相对导入
hero_path = os.path.join(src_path, 'hero')
if hero_path not in sys.path:
    sys.path.insert(0, hero_path)


def run_all_tests(verbosity=2, pattern='test_*.py'):
    """运行所有测试"""
    # 发现并运行测试
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern=pattern)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful(), result


def run_specific_test(test_module, test_class=None, test_method=None):
    """运行特定测试"""
    # 构建测试套件
    suite = unittest.TestSuite()
    
    if test_class and test_method:
        # 运行特定方法
        suite.addTest(test_class(test_method))
    elif test_class:
        # 运行特定类的所有方法
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    else:
        # 运行特定模块的所有测试
        tests = unittest.TestLoader().loadTestsFromModule(test_module)
        suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful(), result


def generate_test_report(result):
    """生成测试报告"""
    report = []
    report.append("=" * 70)
    report.append("英雄无敌游戏测试报告")
    report.append("=" * 70)
    
    # 测试概要
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    success_rate = (total_tests - failures - errors) / total_tests * 100 if total_tests > 0 else 0
    
    report.append(f"\n测试概要:")
    report.append(f"  总测试数: {total_tests}")
    report.append(f"  成功: {total_tests - failures - errors}")
    report.append(f"  失败: {failures}")
    report.append(f"  错误: {errors}")
    report.append(f"  跳过: {skipped}")
    report.append(f"  成功率: {success_rate:.1f}%")
    
    # 失败详情
    if failures:
        report.append(f"\n失败详情:")
        for test, traceback in result.failures:
            report.append(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    # 错误详情
    if errors:
        report.append(f"\n错误详情:")
        for test, traceback in result.errors:
            report.append(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    # 跳过详情
    if skipped:
        report.append(f"\n跳过详情:")
        for test, reason in result.skipped:
            report.append(f"  - {test}: {reason}")
    
    report.append("\n" + "=" * 70)
    report.append("测试完成")
    report.append("=" * 70)
    
    return "\n".join(report)


def save_report_to_file(report, filename="test_report.txt"):
    """保存报告到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"测试报告已保存到 {filename}")


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='英雄无敌游戏测试运行器')
    parser.add_argument('--module', '-m', help='要测试的模块')
    parser.add_argument('--class', '-c', dest='class_name', help='要测试的类')
    parser.add_argument('--method', '-f', dest='method_name', help='要测试的方法')
    parser.add_argument('--pattern', '-p', default='test_*.py', help='测试文件模式')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    parser.add_argument('--report', '-r', action='store_true', help='生成测试报告')
    parser.add_argument('--output', '-o', default='test_report.txt', help='报告输出文件')
    
    args = parser.parse_args()
    
    # 设置详细程度
    verbosity = 2 if args.verbose else 1
    
    # 运行测试
    try:
        if args.module:
            # 导入模块
            module_name = f"tests.{args.module}"
            if args.class_name:
                # 导入类
                module = __import__(module_name, fromlist=[args.class_name])
                test_class = getattr(module, args.class_name)
                
                if args.method_name:
                    # 运行特定方法
                    success, result = run_specific_test(None, test_class, args.method_name)
                else:
                    # 运行特定类
                    success, result = run_specific_test(None, test_class)
            else:
                # 运行特定模块
                module = __import__(module_name)
                success, result = run_specific_test(module)
        else:
            # 运行所有测试
            success, result = run_all_tests(verbosity, args.pattern)
        
        # 生成报告
        if args.report:
            report = generate_test_report(result)
            save_report_to_file(report, args.output)
        
        # 返回退出码
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"运行测试时出错: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()