# -*- coding: utf-8 -*-
"""
技能树系统模块 - 处理技能升级和技能树相关功能
"""

import json
from typing import Dict, List, Optional, Tuple


class SkillNode:
    """技能节点类，表示技能树中的单个技能"""
    
    def __init__(self, skill_id: str, skill_data: Dict):
        """
        初始化技能节点
        
        Args:
            skill_id: 技能ID
            skill_data: 技能配置数据
        """
        self.skill_id = skill_id
        self.name = skill_data.get("name", skill_id)
        self.description = skill_data.get("description", "")
        self.max_level = skill_data.get("max_level", 5)
        self.current_level = 0
        self.prerequisites = skill_data.get("prerequisites", [])  # 前置技能要求
        self.cost_per_level = skill_data.get("cost_per_level", 1)  # 每级技能点消耗
        self.effects_per_level = skill_data.get("effects_per_level", [])  # 每级效果
        self.class_requirement = skill_data.get("class_requirement", None)  # 职业要求
        
        # 技能状态标志
        self.is_available = False  # 是否可学习
        self.is_maxed = False  # 是否已满级
        
        self._update_status()
    
    def _update_status(self):
        """更新技能状态"""
        # 检查是否已满级
        self.is_maxed = (self.current_level >= self.max_level)
    
    def can_upgrade(self, skill_points: int, learned_skills: Dict[str, int]) -> bool:
        """
        检查是否可以升级
        
        Args:
            skill_points: 当前技能点
            learned_skills: 已学习的技能和等级
            
        Returns:
            bool: 是否可以升级
        """
        # 已满级
        if self.is_maxed:
            return False
        
        # 技能点不足
        if skill_points < self.cost_per_level:
            return False
        
        # 检查前置技能
        for prereq_skill, req_level in self.prerequisites:
            if learned_skills.get(prereq_skill, 0) < req_level:
                return False
        
        return True
    
    def upgrade(self) -> bool:
        """
        升级技能
        
        Returns:
            bool: 是否升级成功
        """
        if self.is_maxed:
            return False
        
        self.current_level += 1
        self._update_status()
        return True
    
    def get_effect_value(self, effect_index: int) -> float:
        """
        获取指定效果的当前值
        
        Args:
            effect_index: 效果索引
            
        Returns:
            float: 效果当前值
        """
        if effect_index >= len(self.effects_per_level):
            return 0.0
        
        return self.effects_per_level[effect_index] * self.current_level
    
    def to_dict(self) -> Dict:
        """
        转换为字典（用于序列化）
        
        Returns:
            Dict: 技能节点数据字典
        """
        return {
            "skill_id": self.skill_id,
            "current_level": self.current_level
        }
    
    @classmethod
    def from_dict(cls, data: Dict, skill_tree_config: Dict) -> 'SkillNode':
        """
        从字典创建技能节点（用于反序列化）
        
        Args:
            data: 技能节点数据字典
            skill_tree_config: 技能树配置
            
        Returns:
            SkillNode: 技能节点实例
        """
        skill_id = data["skill_id"]
        current_level = data["current_level"]
        
        # 从配置获取技能数据
        skill_data = skill_tree_config[skill_id]
        node = cls(skill_id, skill_data)
        node.current_level = current_level
        node._update_status()
        
        return node


class SkillTree:
    """技能树类，管理整个技能树系统"""
    
    def __init__(self, hero_class: str, lang):
        """
        初始化技能树
        
        Args:
            hero_class: 英雄职业
            lang: 语言支持对象
        """
        self.hero_class = hero_class
        self.lang = lang
        self.skill_nodes: Dict[str, SkillNode] = {}
        self.learned_skills: Dict[str, int] = {}  # 技能ID -> 等级
        
        # 从配置加载技能树
        self._load_skill_tree()
    
    def _load_skill_tree(self):
        """从配置加载技能树"""
        from .game_config import SKILL_TREES
        
        # 获取当前职业的技能树配置
        if self.hero_class not in SKILL_TREES:
            raise ValueError(f"Skill tree configuration not found for class {self.hero_class}")
        
        skill_tree_config = SKILL_TREES[self.hero_class]
        
        # 创建技能节点
        for skill_id, skill_data in skill_tree_config.items():
            self.skill_nodes[skill_id] = SkillNode(skill_id, skill_data)
            self.learned_skills[skill_id] = 0  # 初始等级为0
        
        # 更新技能可用性
        self._update_skill_availability()
    
    def _update_skill_availability(self):
        """更新技能可用性"""
        for skill_id, skill_node in self.skill_nodes.items():
            # 初始技能默认可用
            is_available = True
            
            # 检查前置技能
            for prereq_skill, req_level in skill_node.prerequisites:
                if self.learned_skills.get(prereq_skill, 0) < req_level:
                    is_available = False
                    break
            
            # 检查职业要求
            if skill_node.class_requirement and skill_node.class_requirement != self.hero_class:
                is_available = False
            
            skill_node.is_available = is_available
    
    def can_upgrade_skill(self, skill_id: str, skill_points: int) -> bool:
        """
        检查是否可以升级指定技能
        
        Args:
            skill_id: 技能ID
            skill_points: 当前技能点
            
        Returns:
            bool: 是否可以升级
        """
        if skill_id not in self.skill_nodes:
            return False
        
        return self.skill_nodes[skill_id].can_upgrade(skill_points, self.learned_skills)
    
    def upgrade_skill(self, skill_id: str, skill_points: int) -> Tuple[bool, int]:
        """
        升级指定技能
        
        Args:
            skill_id: 技能ID
            skill_points: 当前技能点
            
        Returns:
            Tuple[bool, int]: (是否升级成功, 剩余技能点)
        """
        if not self.can_upgrade_skill(skill_id, skill_points):
            return (False, skill_points)
        
        skill_node = self.skill_nodes[skill_id]
        if skill_node.upgrade():
            # 更新学习技能列表
            self.learned_skills[skill_id] = skill_node.current_level
            
            # 更新技能可用性
            self._update_skill_availability()
            
            # 返回结果
            return (True, skill_points - skill_node.cost_per_level)
        
        return (False, skill_points)
    
    def get_skill_effect(self, skill_id: str, effect_index: int) -> float:
        """
        获取指定技能的效果值
        
        Args:
            skill_id: 技能ID
            effect_index: 效果索引
            
        Returns:
            float: 效果值
        """
        if skill_id not in self.skill_nodes:
            return 0.0
        
        return self.skill_nodes[skill_id].get_effect_value(effect_index)
    
    def format_tree(self, show_all: bool = False) -> str:
        """
        格式化技能树为文本
        
        Args:
            show_all: 是否显示所有技能（包括未解锁的）
            
        Returns:
            str: 格式化的技能树文本
        """
        from .game_config import SKILL_TREES
        
        result = []
        result.append(f"=== {self.lang.get_text('skill_tree_title')} ===")
        result.append(f"{self.lang.get_text('current_class')}: {self.lang.get_text('class_' + self.hero_class)}")
        result.append("")
        
        # 技能分类显示
        categories = {
            "core": f"{self.lang.get_text('skill_category_core')}",
            "combat": f"{self.lang.get_text('skill_category_combat')}",
            "passive": f"{self.lang.get_text('skill_category_passive')}",
            "ultimate": f"{self.lang.get_text('skill_category_ultimate')}"
        }
        
        for category, title in categories.items():
            # 获取该类别的技能
            category_skills = [
                skill_id for skill_id, skill_node in self.skill_nodes.items()
                if SKILL_TREES.get(self.hero_class, {}).get(skill_id, {}).get("category", "core") == category
            ]
            
            if not category_skills:
                continue
                
            result.append(f"【{title}】")
            
            for skill_id in sorted(category_skills):
                skill_node = self.skill_nodes[skill_id]
                
                # 是否显示
                if not show_all and not skill_node.is_available and skill_node.current_level == 0:
                    continue
                
                # 技能状态图标
                if skill_node.is_maxed:
                    status = "✅"
                elif skill_node.current_level > 0:
                    status = "🌟"
                elif skill_node.is_available:
                    status = "🔓"
                else:
                    status = "🔒"
                
                # 技能信息
                # 检查技能ID是否已经包含"_skill"后缀
                if skill_id.endswith("_skill"):
                    skill_name_key = skill_id
                else:
                    skill_name_key = f"skill_{skill_id}"
                skill_name = self.lang.get_text(skill_name_key)
                level_text = f"Lv.{skill_node.current_level}/{skill_node.max_level}"
                
                # 技能描述（简化版）
                # 检查技能ID是否已经包含"_skill"后缀
                if skill_id.endswith("_skill"):
                    desc_key = f"{skill_id}_desc"
                else:
                    desc_key = f"skill_{skill_id}_desc"
                description = self.lang.get_text(desc_key)
                if len(description) > 40:
                    description = description[:37] + "..."
                
                result.append(f"  {status} [{skill_id}] {skill_name} ({level_text})")
                result.append(f"    {description}")
                
                # 前置技能
                if skill_node.prerequisites:
                    prereq_skills = []
                    for p, l in skill_node.prerequisites:
                        # 检查前置技能ID是否已经包含"_skill"后缀
                        if p.endswith("_skill"):
                            prereq_key = p
                        else:
                            prereq_key = f"skill_{p}"
                        prereq_skills.append(f"{self.lang.get_text(prereq_key)} Lv.{l}")
                    prereq_text = ", ".join(prereq_skills)
                    result.append(f"    {self.lang.get_text('skill_prerequisites')}: {prereq_text}")
                
                result.append("")
        
        return "\n".join(result)
    
    def to_dict(self) -> Dict:
        """
        转换为字典（用于序列化）
        
        Returns:
            Dict: 技能树数据字典
        """
        return {
            "hero_class": self.hero_class,
            "learned_skills": {
                skill_id: skill_node.to_dict()
                for skill_id, skill_node in self.skill_nodes.items()
                if skill_node.current_level > 0
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict, lang) -> 'SkillTree':
        """
        从字典创建技能树（用于反序列化）
        
        Args:
            data: 技能树数据字典
            lang: 语言支持对象
            
        Returns:
            SkillTree: 技能树实例
        """
        hero_class = data["hero_class"]
        skill_tree = cls(hero_class, lang)
        
        # 恢复学习技能
        for skill_id, skill_data in data.get("learned_skills", {}).items():
            if skill_id in skill_tree.skill_nodes:
                skill_tree.skill_nodes[skill_id].current_level = skill_data["current_level"]
                skill_tree.learned_skills[skill_id] = skill_data["current_level"]
        
        # 更新技能可用性
        skill_tree._update_skill_availability()
        
        return skill_tree