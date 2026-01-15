#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误处理测试脚本
测试新创建的错误处理模块的各种功能
"""

import sys
import os

# 添加src目录到路径，以便导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from hero.error_handler import (
    init_error_handler, handle_error, log_debug, 
    validate_input, validate_numeric_input, is_debug_mode,
    get_error_handler
)

def test_error_handling():
    """测试错误处理功能"""
    print("=== 错误处理模块测试 ===\n")
    
    # 初始化错误处理器，启用调试模式
    init_error_handler(debug_mode=True, log_file="logs/test_error.log")
    
    print(f"调试模式: {is_debug_mode()}")
    
    # 测试1: 基本错误处理
    print("\n1. 测试基本错误处理:")
    try:
        raise FileNotFoundError("测试文件不存在")
    except Exception as e:
        error_msg = handle_error(e, "测试上下文", "测试文件不存在错误。")
        print(f"   处理结果: {error_msg}")
    
    # 测试2: 数值验证
    print("\n2. 测试数值验证:")
    valid_numbers = ["1", "5", "10", "invalid", "15"]
    for num_str in valid_numbers:
        result = validate_numeric_input(num_str, 1, 10)
        print(f"   输入 '{num_str}' -> {result}")
    
    # 测试3: 选项验证
    print("\n3. 测试选项验证:")
    valid_options = ["", "1", "2", "3"]
    test_inputs = ["", "1", "4", "invalid"]
    for test_input in test_inputs:
        result = validate_input(test_input, valid_options, allow_empty=True)
        print(f"   输入 '{test_input}' -> {result}")
    
    # 测试4: 调试日志
    print("\n4. 测试调试日志:")
    log_debug("这是一条测试调试信息")
    
    # 测试5: 错误统计
    print("\n5. 错误统计信息:")
    stats = get_error_handler().get_error_statistics()
    print(f"   总错误数: {stats['total_errors']}")
    print(f"   错误类型: {stats['error_types']}")
    
    print("\n=== 错误处理模块测试完成 ===")

if __name__ == "__main__":
    test_error_handling()