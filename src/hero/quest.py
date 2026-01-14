#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
任务系统模块
负责随机任务的生成、追踪和管理
"""

import random


class Quest:
    """任务类"""
    
    def __init__(self, quest_id, quest_type, target_value, reward_gold, reward_exp, description_key):
        """
        初始化任务
        
        Args:
            quest_id: 任务ID
            quest_type: 任务类型 ('kill_monster', 'collect_gold', 'reach_position', 'use_potion')
            target_value: 目标值
            reward_gold: 金币奖励
            reward_exp: 经验奖励
            description_key: 描述文本键
        """
        self.quest_id = quest_id
        self.quest_type = quest_type
        self.target_value = target_value
        self.current_value = 0
        self.reward_gold = reward_gold
        self.reward_exp = reward_exp
        self.description_key = description_key
        self.completed = False
    
    def update_progress(self, value=1):
        """更新任务进度"""
        if not self.completed:
            self.current_value += value
            if self.current_value >= self.target_value:
                self.completed = True
                return True
        return False
    
    def get_progress_percentage(self):
        """获取进度百分比"""
        if self.target_value == 0:
            return 0
        return min(100, int((self.current_value / self.target_value) * 100))
    
    def to_dict(self):
        """转换为字典（用于序列化）"""
        return {
            'quest_id': self.quest_id,
            'quest_type': self.quest_type,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'reward_gold': self.reward_gold,
            'reward_exp': self.reward_exp,
            'description_key': self.description_key,
            'completed': self.completed
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建任务"""
        quest = cls(
            quest_id=data['quest_id'],
            quest_type=data['quest_type'],
            target_value=data['target_value'],
            reward_gold=data['reward_gold'],
            reward_exp=data['reward_exp'],
            description_key=data['description_key']
        )
        quest.current_value = data['current_value']
        quest.completed = data['completed']
        return quest


class QuestSystem:
    """任务系统类"""
    
    def __init__(self):
        """初始化任务系统"""
        self.active_quests = []  # 当前活动任务（最多3个）
        self.completed_quests = []  # 已完成任务
        self.quest_counter = 0  # 任务计数器（用于生成唯一ID）
        
        # 任务类型配置
        self.quest_types = [
            ('kill_monster', 'kill_monster_quest', 3, 10),  # 击杀怪物，目标3-10只
            ('collect_gold', 'collect_gold_quest', 50, 200),  # 收集金币，目标50-200
            ('reach_position', 'reach_position_quest', 5, 15),  # 到达位置，目标5-15步
            ('use_potion', 'use_potion_quest', 1, 3)  # 使用药剂，目标1-3次
        ]
    
    def generate_random_quest(self, hero_level):
        """
        生成随机任务
        
        Args:
            hero_level: 英雄等级（用于难度缩放）
            
        Returns:
            Quest: 生成的任务对象
        """
        if len(self.active_quests) >= 3:
            return None
        
        quest_type, description_key, min_target, max_target = random.choice(self.quest_types)
        
        # 根据英雄等级调整目标值
        level_multiplier = 1 + (hero_level - 1) * 0.2
        target_value = int(random.randint(min_target, max_target) * level_multiplier)
        
        # 根据目标值计算奖励
        reward_multiplier = 1 + (hero_level - 1) * 0.3
        reward_gold = int(target_value * 5 * reward_multiplier)
        reward_exp = int(target_value * 10 * reward_multiplier)
        
        self.quest_counter += 1
        quest_id = f"quest_{self.quest_counter}"
        
        return Quest(quest_id, quest_type, target_value, reward_gold, reward_exp, description_key)
    
    def add_quest(self, quest):
        """添加任务到活动列表"""
        if len(self.active_quests) < 3 and quest:
            self.active_quests.append(quest)
            return True
        return False
    
    def update_quest_progress(self, quest_type, value=1):
        """更新指定类型任务的进度"""
        completed_quests = []
        
        for quest in self.active_quests:
            if quest.quest_type == quest_type and not quest.completed:
                if quest.update_progress(value):
                    # 任务完成
                    completed_quests.append(quest)
        
        # 处理已完成任务
        for quest in completed_quests:
            self.active_quests.remove(quest)
            self.completed_quests.append(quest)
        
        return completed_quests
    
    def get_quest_rewards(self, quest):
        """获取任务奖励"""
        return quest.reward_gold, quest.reward_exp
    
    def format_quests_list(self, lang):
        """格式化任务列表显示"""
        if not self.active_quests:
            return lang.get_text("no_active_quests")
        
        result = []
        for i, quest in enumerate(self.active_quests, 1):
            description = lang.get_text(quest.description_key).format(
                target=quest.target_value,
                current=quest.current_value
            )
            progress = f"({quest.get_progress_percentage()}%)"
            reward = lang.get_text("quest_reward").format(
                gold=quest.reward_gold,
                exp=quest.reward_exp
            )
            result.append(f"{i}. {description} {progress}\n   {reward}")
        
        return "\n".join(result)
    
    def to_dict(self):
        """转换为字典（用于序列化）"""
        return {
            'active_quests': [quest.to_dict() for quest in self.active_quests],
            'completed_quests': [quest.to_dict() for quest in self.completed_quests],
            'quest_counter': self.quest_counter
        }
    
    def from_dict(self, data):
        """从字典恢复任务系统状态"""
        self.active_quests = [Quest.from_dict(quest_data) for quest_data in data['active_quests']]
        self.completed_quests = [Quest.from_dict(quest_data) for quest_data in data['completed_quests']]
        self.quest_counter = data['quest_counter']


# 测试代码
if __name__ == "__main__":
    # 简单测试任务系统
    quest_system = QuestSystem()
    
    # 生成几个测试任务
    for i in range(3):
        quest = quest_system.generate_random_quest(1)
        if quest:
            quest_system.add_quest(quest)
    
    print("Quest system test completed")