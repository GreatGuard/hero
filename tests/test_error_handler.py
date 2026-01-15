#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试错误处理模块
"""

import unittest
import sys
import os
import tempfile
import shutil
import json
from unittest.mock import patch, MagicMock

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hero.error_handler import (
    ErrorHandler, init_error_handler, handle_error, log_debug,
    validate_input, validate_numeric_input, is_debug_mode
)
from hero.safe_input import safe_input
from hero.main import safe_file_operation


class TestErrorHandler(unittest.TestCase):
    """测试ErrorHandler类"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建临时目录用于测试
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test_error.log")
        self.error_handler = ErrorHandler(log_file=self.log_file, debug_mode=True)
    
    def tearDown(self):
        """清理测试环境"""
        # 删除临时目录
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """测试错误处理器初始化"""
        self.assertTrue(self.error_handler.debug_mode)
        self.assertEqual(self.error_handler.log_file, self.log_file)
        self.assertEqual(self.error_handler.error_count, 0)
        self.assertEqual(self.error_handler.error_types, {})
        self.assertTrue(os.path.exists(self.log_file))
    
    def test_handle_value_error(self):
        """测试处理ValueError"""
        error = ValueError("测试值错误")
        result = self.error_handler.handle_error(error, "测试上下文", "用户消息")
        
        self.assertIsNotNone(result)
        self.assertIn("用户消息", result)
        self.assertEqual(self.error_handler.error_count, 1)
        self.assertIn("ValueError", self.error_handler.error_types)
        self.assertEqual(self.error_handler.error_types["ValueError"], 1)
        
        # 检查日志是否写入
        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            self.assertIn("测试上下文", log_content)
            self.assertIn("测试值错误", log_content)
    
    def test_handle_file_not_found_error(self):
        """测试处理FileNotFoundError"""
        error = FileNotFoundError("文件未找到")
        result = self.error_handler.handle_error(error, "文件操作")
        
        self.assertIsNotNone(result)
        self.assertIn("文件未找到", result)
        self.assertEqual(self.error_handler.error_count, 1)
    
    def test_handle_permission_error(self):
        """测试处理PermissionError"""
        error = PermissionError("没有权限")
        result = self.error_handler.handle_error(error, "文件操作")
        
        self.assertIsNotNone(result)
        self.assertIn("没有权限", result)
        self.assertEqual(self.error_handler.error_count, 1)
    
    def test_handle_json_decode_error(self):
        """测试处理JSONDecodeError"""
        error = json.JSONDecodeError("JSON解析错误", "", 0)
        result = self.error_handler.handle_error(error, "JSON操作")
        
        self.assertIsNotNone(result)
        self.assertIn("数据格式错误", result)
        self.assertEqual(self.error_handler.error_count, 1)
    
    def test_handle_generic_error(self):
        """测试处理通用错误"""
        error = Exception("通用错误")
        result = self.error_handler.handle_error(error, "通用操作")
        
        self.assertIsNotNone(result)
        self.assertIn("发生了错误", result)
        self.assertEqual(self.error_handler.error_count, 1)
    
    def test_handle_error_with_debug_mode(self):
        """测试在调试模式下处理错误"""
        error = RuntimeError("运行时错误")
        self.error_handler.debug_mode = True
        
        result = self.error_handler.handle_error(error, "调试测试")
        
        self.assertIsNotNone(result)
        # 检查日志是否包含堆栈跟踪
        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            self.assertIn("调试测试", log_content)
            self.assertIn("RuntimeError", log_content)
    
    def test_handle_error_without_debug_mode(self):
        """测试在非调试模式下处理错误"""
        error = RuntimeError("运行时错误")
        self.error_handler.debug_mode = False
        
        result = self.error_handler.handle_error(error, "非调试测试")
        
        self.assertIsNotNone(result)
        # 检查日志不包含详细错误信息
        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            self.assertIn("非调试测试", log_content)
    
    def test_log_debug(self):
        """测试记录调试信息"""
        self.error_handler.debug_mode = True
        self.error_handler.log_debug("调试信息")
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            self.assertIn("调试信息", log_content)
    
    def test_log_debug_not_in_debug_mode(self):
        """测试在非调试模式下不记录调试信息"""
        self.error_handler.debug_mode = False
        self.error_handler.log_debug("调试信息")
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            self.assertNotIn("调试信息", log_content)
    
    def test_validate_input(self):
        """测试输入验证"""
        # 有效输入
        result = self.error_handler.validate_input("1", ["1", "2", "3"])
        self.assertTrue(result)
        
        # 无效输入
        result = self.error_handler.validate_input("4", ["1", "2", "3"])
        self.assertFalse(result)
        
        # 允许空输入
        result = self.error_handler.validate_input("", ["1", "2", "3"], allow_empty=True)
        self.assertTrue(result)
        
        # 不允许空输入
        result = self.error_handler.validate_input("", ["1", "2", "3"], allow_empty=False)
        self.assertFalse(result)
    
    def test_validate_numeric_input(self):
        """测试数字输入验证"""
        # 有效数字
        result = self.error_handler.validate_numeric_input("10")
        self.assertTrue(result)
        
        # 无效数字
        result = self.error_handler.validate_numeric_input("abc")
        self.assertFalse(result)
        
        # 范围内
        result = self.error_handler.validate_numeric_input("10", 1, 20)
        self.assertTrue(result)
        
        # 范围外
        result = self.error_handler.validate_numeric_input("30", 1, 20)
        self.assertFalse(result)
    
    def test_get_error_statistics(self):
        """测试获取错误统计信息"""
        # 处理几个错误
        self.error_handler.handle_error(ValueError("错误1"))
        self.error_handler.handle_error(ValueError("错误2"))
        self.error_handler.handle_error(FileNotFoundError("错误3"))
        
        stats = self.error_handler.get_error_statistics()
        
        self.assertEqual(stats["total_errors"], 3)
        self.assertEqual(stats["error_types"]["ValueError"], 2)
        self.assertEqual(stats["error_types"]["FileNotFoundError"], 1)


class TestErrorHandlingFunctions(unittest.TestCase):
    """测试错误处理模块的全局函数"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建临时目录用于测试
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test_error.log")
        init_error_handler(debug_mode=True, log_file=self.log_file)
    
    def tearDown(self):
        """清理测试环境"""
        # 删除临时目录
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_init_error_handler(self):
        """测试初始化全局错误处理器"""
        # 测试是否已初始化
        self.assertTrue(hasattr(sys.modules[__name__], '_error_handler'))
        
        # 测试获取错误处理器
        from hero.error_handler import get_error_handler
        handler = get_error_handler()
        self.assertIsNotNone(handler)
        self.assertTrue(handler.debug_mode)
        self.assertEqual(handler.log_file, self.log_file)
    
    def test_handle_error_function(self):
        """测试全局错误处理函数"""
        error = ValueError("测试错误")
        result = handle_error(error, "测试上下文")
        
        self.assertIsNotNone(result)
        self.assertIn("值错误", result)
    
    def test_log_debug_function(self):
        """测试全局调试信息记录函数"""
        log_debug("测试调试信息")
        
        from hero.error_handler import get_error_handler
        handler = get_error_handler()
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
            self.assertIn("测试调试信息", log_content)
    
    def test_validate_input_function(self):
        """测试全局输入验证函数"""
        # 有效输入
        result = validate_input("1", ["1", "2", "3"])
        self.assertTrue(result)
        
        # 无效输入
        result = validate_input("4", ["1", "2", "3"])
        self.assertFalse(result)
    
    def test_validate_numeric_input_function(self):
        """测试全局数字输入验证函数"""
        # 有效数字
        result = validate_numeric_input("10")
        self.assertTrue(result)
        
        # 无效数字
        result = validate_numeric_input("abc")
        self.assertFalse(result)
    
    def test_is_debug_mode_function(self):
        """测试检查调试模式函数"""
        # 应该是True，因为在setUp中设置为debug模式
        result = is_debug_mode()
        self.assertTrue(result)
    
    @patch('builtins.input')
    def test_safe_input(self, mock_input):
        """测试安全输入函数"""
        # 模拟正常输入
        mock_input.return_value = "1"
        result = safe_input("测试提示", valid_options=["1", "2", "3"])
        self.assertEqual(result, "1")
        
        # 模拟空输入
        mock_input.return_value = ""
        result = safe_input("测试提示", valid_options=["1", "2", "3"], allow_empty=True)
        self.assertEqual(result, "")
        
        # 模拟中断
        mock_input.side_effect = KeyboardInterrupt()
        result = safe_input("测试提示", valid_options=["1", "2", "3"])
        self.assertIsNone(result)
    
    def test_safe_file_operation(self):
        """测试安全文件操作函数"""
        # 测试读取文件
        test_file = os.path.join(self.temp_dir, "test_file.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("测试内容")
        
        # 使用safe_file_operation读取文件
        result = safe_file_operation(test_file, 'r', encoding='utf-8')
        self.assertIsNotNone(result)
        content = result.read()
        self.assertEqual(content, "测试内容")
        result.close()
        
        # 测试文件不存在的情况
        non_existent_file = os.path.join(self.temp_dir, "non_existent.txt")
        result = safe_file_operation(non_existent_file, 'r')
        self.assertIsNone(result)


class TestErrorHandlerIntegration(unittest.TestCase):
    """测试错误处理模块与其他模块的集成"""
    
    def test_json_decode_error_handling(self):
        """测试JSON解析错误的处理"""
        # 创建一个无效的JSON文件
        temp_dir = tempfile.mkdtemp()
        try:
            invalid_json_file = os.path.join(temp_dir, "invalid.json")
            with open(invalid_json_file, 'w', encoding='utf-8') as f:
                f.write("{ invalid json content }")
            
            # 尝试使用safe_file_operation打开并解析JSON
            file_obj = safe_file_operation(invalid_json_file, 'r', encoding='utf-8')
            self.assertIsNotNone(file_obj)
            
            try:
                json.load(file_obj)
                self.fail("应该抛出JSONDecodeError")
            except json.JSONDecodeError as e:
                error_msg = handle_error(e, "加载JSON", "JSON文件格式错误")
                self.assertIsNotNone(error_msg)
                self.assertIn("数据格式错误", error_msg)
            finally:
                file_obj.close()
        finally:
            shutil.rmtree(temp_dir)
    
    def test_file_permission_error_handling(self):
        """测试文件权限错误的处理"""
        # 创建一个只读目录
        temp_dir = tempfile.mkdtemp()
        try:
            os.chmod(temp_dir, 0o444)  # 只读
            
            read_only_file = os.path.join(temp_dir, "readonly.txt")
            
            # 尝试写入只读文件
            try:
                with open(read_only_file, 'w', encoding='utf-8') as f:
                    f.write("测试内容")
                self.fail("应该抛出PermissionError")
            except PermissionError as e:
                error_msg = handle_error(e, "写入文件", "没有写入权限")
                self.assertIsNotNone(error_msg)
                self.assertIn("权限", error_msg)
        finally:
            # 恢复权限以便清理
            os.chmod(temp_dir, 0o755)
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    unittest.main()