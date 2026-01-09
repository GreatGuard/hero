#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
职业技能修复测试脚本
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from hero.game_config import CLASS_DEFINITIONS
from hero.language import LanguageSystem

def test_class_skills_restriction():
    """测试职业技能限制"""
    print("=== 职业技能限制测试 ===\n")
    
    # 初始化语言系统
    lang = LanguageSystem()
    
    # 测试每个职业的专属技能
    for class_name, class_info in CLASS_DEFINITIONS.items():
        class_name_display = lang.get_text(f"class_{class_name}")
        class_skills = class_info.get("class_skills", [])
        
        print(f"职业: {class_name_display}")
        print(f"专属技能: {len(class_skills)} 个")
        
        for skill_key in class_skills:
            skill_name = lang.get_text(f"{skill_key}_skill")
            print(f"  - {skill_name}")
        
        # 检查技能是否重复
        all_class_skills = []
        for other_class in CLASS_DEFINITIONS.values():
            all_class_skills.extend(other_class.get("class_skills", []))
        
        # 查找重复的专属技能
        from collections import Counter
        skill_counts = Counter(all_class_skills)
        duplicate_skills = [skill for skill, count in skill_counts.items() if count > 1]
        
        if duplicate_skills:
            print(f"⚠️  警告: 发现重复的专属技能: {duplicate_skills}")
        else:
            print("✅ 专属技能分配正确，无重复")
        
        print()

def test_skill_availability():
    """测试技能可用性"""
    print("=== 技能可用性测试 ===\n")
    
    lang = LanguageSystem()
    
    # 通用技能列表
    general_skills = ["fireball", "healing", "critical", "lifesteal", "dodge", 
                     "combo", "shield", "berserk", "focus"]
    
    print("通用技能列表:")
    for skill_key in general_skills:
        skill_name = lang.get_text(f"{skill_key}_skill")
        print(f"  - {skill_name}")
    
    print("\n职业技能检查:")
    for class_name, class_info in CLASS_DEFINITIONS.items():
        class_name_display = lang.get_text(f"class_{class_name}")
        class_skills = class_info.get("class_skills", [])
        
        # 检查是否有通用技能被错误地标记为专属技能
        conflict_skills = []
        for skill_key in class_skills:
            if skill_key in general_skills:
                conflict_skills.append(skill_key)
        
        if conflict_skills:
            print(f"⚠️  {class_name_display}: 通用技能被标记为专属技能: {conflict_skills}")
        else:
            print(f"✅ {class_name_display}: 职业技能定义正确")

def test_skill_learning():
    """测试技能学习系统"""
    print("\n=== 技能学习系统测试 ===\n")
    
    # 模拟技能学习过程
    lang = LanguageSystem()
    
    for class_name, class_info in CLASS_DEFINITIONS.items():
        class_name_display = lang.get_text(f"class_{class_name}")
        class_skills = class_info.get("class_skills", [])
        skill_affinity = class_info.get("skill_affinity", [])
        
        print(f"职业: {class_name_display}")
        print(f"专属技能数量: {len(class_skills)}")
        print(f"技能亲和度数量: {len(skill_affinity)}")
        
        # 检查专属技能是否在技能亲和度列表中
        for skill_key in class_skills:
            if skill_key in skill_affinity:
                print(f"✅ 专属技能 '{lang.get_text(f'{skill_key}_skill')}' 在技能亲和度列表中")
            else:
                print(f"⚠️  警告: 专属技能 '{lang.get_text(f'{skill_key}_skill')}' 不在技能亲和度列表中")
        
        print()

if __name__ == "__main__":
    print("职业技能修复测试\n")
    
    test_class_skills_restriction()
    test_skill_availability()
    test_skill_learning()
    
    print("测试完成！")