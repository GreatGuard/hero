#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英雄无敌 - 错误处理模块

提供统一的错误处理机制，包括错误日志记录、错误提示和调试功能。
"""

import os
import sys
import traceback
import logging
import datetime
from typing import Optional, Any, Dict


class ErrorHandler:
    """错误处理器类"""
    
    def __init__(self, log_file="logs/error.log", debug_mode=False):
        """初始化错误处理器
        
        Args:
            log_file: 错误日志文件路径
            debug_mode: 是否启用调试模式
        """
        self.debug_mode = debug_mode
        self.log_file = log_file
        self.error_count = 0
        self.error_types = {}
        
        # 创建日志目录
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 设置日志
        self._setup_logging()
    
    def _setup_logging(self):
        """设置日志系统"""
        # 创建日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 创建文件处理器
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        # 配置根日志记录器
        self.logger = logging.getLogger('hero_error_handler')
        self.logger.setLevel(logging.DEBUG if self.debug_mode else logging.ERROR)
        self.logger.addHandler(file_handler)
    
    def handle_error(self, error: Exception, context: str = "", user_message: str = ""):
        """处理错误
        
        Args:
            error: 异常对象
            context: 错误上下文信息
            user_message: 向用户显示的错误信息
        """
        self.error_count += 1
        error_type = type(error).__name__
        self.error_types[error_type] = self.error_types.get(error_type, 0) + 1
        
        # 记录错误到日志
        error_msg = f"{context}: {str(error)}"
        if self.debug_mode:
            error_msg += f"\n{traceback.format_exc()}"
        
        self.logger.error(error_msg)
        
        # 返回用户友好的错误信息
        return user_message or self._get_friendly_error_message(error)
    
    def _get_friendly_error_message(self, error: Exception) -> str:
        """根据错误类型获取用户友好的错误信息
        
        Args:
            error: 异常对象
            
        Returns:
            用户友好的错误信息
        """
        error_type = type(error).__name__
        
        # 常见错误类型的友好提示
        error_messages = {
            "FileNotFoundError": "文件未找到，请检查文件路径和权限。",
            "PermissionError": "权限不足，请检查文件和目录的读写权限。",
            "ValueError": "输入值无效，请检查输入内容。",
            "KeyError": "数据未找到，可能是配置不完整。",
            "IndexError": "索引超出范围，请检查输入的选择。",
            "TypeError": "类型错误，可能是程序内部问题。",
            "AttributeError": "属性错误，可能是配置不完整。",
            "ImportError": "模块导入失败，请检查安装。",
            "KeyboardInterrupt": "操作被用户中断。",
            "EOFError": "输入意外结束。"
        }
        
        return error_messages.get(error_type, f"发生未知错误: {str(error)}")
    
    def log_debug(self, message: str):
        """记录调试信息
        
        Args:
            message: 调试信息
        """
        if self.debug_mode:
            self.logger.debug(f"DEBUG: {message}")
    
    def validate_input(self, user_input: str, valid_options: list, allow_empty: bool = False) -> Optional[str]:
        """验证用户输入
        
        Args:
            user_input: 用户输入
            valid_options: 有效选项列表
            allow_empty: 是否允许空输入
            
        Returns:
            验证通过的输入，None表示无效
        """
        if not user_input.strip() and allow_empty:
            return ""
        
        if user_input in valid_options:
            return user_input
        
        return None
    
    def validate_numeric_input(self, user_input: str, min_val: int = None, max_val: int = None) -> Optional[int]:
        """验证数字输入
        
        Args:
            user_input: 用户输入
            min_val: 最小值
            max_val: 最大值
            
        Returns:
            验证通过的数字，None表示无效
        """
        try:
            value = int(user_input)
            
            if min_val is not None and value < min_val:
                return None
            
            if max_val is not None and value > max_val:
                return None
            
            return value
        except ValueError:
            return None
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """获取错误统计信息
        
        Returns:
            错误统计信息字典
        """
        return {
            "total_errors": self.error_count,
            "error_types": self.error_types.copy(),
            "log_file": self.log_file,
            "debug_mode": self.debug_mode
        }


# 全局错误处理器实例
_global_error_handler = None


def get_error_handler() -> ErrorHandler:
    """获取全局错误处理器实例"""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = ErrorHandler()
    return _global_error_handler


def init_error_handler(debug_mode=False, log_file="logs/error.log"):
    """初始化全局错误处理器
    
    Args:
        debug_mode: 是否启用调试模式
        log_file: 错误日志文件路径
    """
    global _global_error_handler
    _global_error_handler = ErrorHandler(log_file=log_file, debug_mode=debug_mode)


def handle_error(error: Exception, context: str = "", user_message: str = "") -> str:
    """便捷的错误处理函数
    
    Args:
        error: 异常对象
        context: 错误上下文信息
        user_message: 向用户显示的错误信息
        
    Returns:
        用户友好的错误信息
    """
    return get_error_handler().handle_error(error, context, user_message)


def log_debug(message: str):
    """便捷的调试信息记录函数
    
    Args:
        message: 调试信息
    """
    get_error_handler().log_debug(message)


def validate_input(user_input: str, valid_options: list, allow_empty: bool = False) -> Optional[str]:
    """便捷的用户输入验证函数
    
    Args:
        user_input: 用户输入
        valid_options: 有效选项列表
        allow_empty: 是否允许空输入
        
    Returns:
        验证通过的输入，None表示无效
    """
    return get_error_handler().validate_input(user_input, valid_options, allow_empty)


def validate_numeric_input(user_input: str, min_val: int = None, max_val: int = None) -> Optional[int]:
    """便捷的数字输入验证函数
    
    Args:
        user_input: 用户输入
        min_val: 最小值
        max_val: 最大值
        
    Returns:
        验证通过的数字，None表示无效
    """
    return get_error_handler().validate_numeric_input(user_input, min_val, max_val)


def is_debug_mode() -> bool:
    """检查是否处于调试模式
    
    Returns:
        是否处于调试模式
    """
    return get_error_handler().debug_mode
