# -*- coding: utf-8 -*-
"""
安全的用户输入模块 - 提供统一的输入验证和错误处理
"""

from typing import Optional


def safe_input(prompt: str, valid_options: list = None, allow_empty: bool = False) -> Optional[str]:
    """安全的用户输入函数，支持参数验证和错误处理
    
    Args:
        prompt: 输入提示信息
        valid_options: 有效选项列表
        allow_empty: 是否允许空输入
        
    Returns:
        用户输入的内容，None 表示输入被中断或出错
    """
    while True:
        try:
            user_input = input(prompt)
            
            # 验证输入
            if valid_options is not None:
                if allow_empty and (user_input == "" or user_input in valid_options):
                    return user_input
                elif user_input in valid_options:
                    return user_input
                else:
                    print("无效输入，请重新选择。")
                    continue
            
            return user_input
        except (KeyboardInterrupt, EOFError):
            # 用户中断输入（Ctrl+C）或文件结束
            print("\n操作被用户中断。")
            return None
        except Exception as e:
            # 处理其他可能的输入异常
            print(f"输入过程中发生错误：{e}")
            return None