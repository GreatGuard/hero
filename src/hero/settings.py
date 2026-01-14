# -*- coding: utf-8 -*-
"""
游戏设置模块 - 管理玩家自定义游戏选项
"""

import json


class GameSettings:
    """游戏设置类 - 管理游戏的各种设置选项"""
    
    def __init__(self, language="zh"):
        """
        初始化游戏设置
        
        Args:
            language: 当前语言设置 ("zh" 或 "en")
        """
        self.language = language
        
        # 文本显示速度 (毫秒/字符)
        # 0: 即时显示, 10: 快速, 30: 正常, 50: 慢速, 100: 很慢
        self.text_speed = 30
        
        # 自动存档设置 (每N步自动存档, 0表示关闭)
        self.auto_save_interval = 0
        
        # 事件提示详细程度
        # 0: 简单提示, 1: 标准提示, 2: 详细提示
        self.event_detail_level = 1
        
        # 战斗动画效果
        self.combat_animations = True
        
        # 声音效果 (预留)
        self.sound_effects = False
        
        # 战斗日志详细程度
        # 0: 无日志, 1: 简要日志, 2: 详细日志
        self.combat_log_level = 1
    
    def to_dict(self):
        """
        将设置转换为字典，用于序列化
        
        Returns:
            dict: 包含所有设置的字典
        """
        return {
            'text_speed': self.text_speed,
            'auto_save_interval': self.auto_save_interval,
            'event_detail_level': self.event_detail_level,
            'combat_animations': self.combat_animations,
            'sound_effects': self.sound_effects,
            'combat_log_level': self.combat_log_level
        }
    
    def from_dict(self, data):
        """
        从字典加载设置
        
        Args:
            data (dict): 包含设置数据的字典
        """
        if not data:
            return
            
        self.text_speed = data.get('text_speed', 30)
        self.auto_save_interval = data.get('auto_save_interval', 0)
        self.event_detail_level = data.get('event_detail_level', 1)
        self.combat_animations = data.get('combat_animations', True)
        self.sound_effects = data.get('sound_effects', False)
        self.combat_log_level = data.get('combat_log_level', 1)
    
    def get_text_delay(self):
        """
        根据文本速度获取延迟时间
        
        Returns:
            float: 延迟时间(秒)
        """
        if self.text_speed == 0:
            return 0  # 即时显示
        return self.text_speed / 1000.0  # 转换为秒
    
    def should_auto_save(self, step_count):
        """
        判断是否应该自动存档
        
        Args:
            step_count (int): 当前步数
            
        Returns:
            bool: 是否应该自动存档
        """
        if self.auto_save_interval <= 0:
            return False
        return step_count % self.auto_save_interval == 0
    
    def format_text_with_speed(self, text):
        """
        根据文本速度格式化文本
        
        Args:
            text (str): 要格式化的文本
            
        Returns:
            str: 格式化后的文本
        """
        # 这里可以根据文本速度添加特殊标记或格式
        # 目前直接返回原文本
        return text