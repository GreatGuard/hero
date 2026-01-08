# -*- coding: utf-8 -*-
"""
成就系统模块 - 处理游戏成就的解锁和显示
"""

import json
import os
from datetime import datetime


class AchievementSystem:
    """成就系统类"""

    def __init__(self, game):
        self.game = game
        self.achievements = self._load_achievements_config()
        self.unlocked_achievements = []
        self.achievement_data_file = "achievements.json"
        
        # 加载已解锁的成就
        self._load_unlocked_achievements()

    def _load_achievements_config(self):
        """加载成就配置"""
        return {
            # 进度相关成就
            "first_step": {
                "name": {
                    "zh": "第一步",
                    "en": "First Step"
                },
                "description": {
                    "zh": "完成第一次移动",
                    "en": "Complete your first move"
                },
                "icon": "👣",
                "rarity": "common",
                "condition": lambda: self.game.statistics.total_steps >= 1
            },
            "explorer": {
                "name": {
                    "zh": "探险家",
                    "en": "Explorer"
                },
                "description": {
                    "zh": "移动超过100步",
                    "en": "Move more than 100 steps"
                },
                "icon": "🗺️",
                "rarity": "common",
                "condition": lambda: self.game.statistics.total_steps >= 100
            },
            "master_explorer": {
                "name": {
                    "zh": "探险大师",
                    "en": "Master Explorer"
                },
                "description": {
                    "zh": "移动超过500步",
                    "en": "Move more than 500 steps"
                },
                "icon": "🧭",
                "rarity": "rare",
                "condition": lambda: self.game.statistics.total_steps >= 500
            },
            
            # 战斗相关成就
            "first_blood": {
                "name": {
                    "zh": "首杀",
                    "en": "First Blood"
                },
                "description": {
                    "zh": "赢得第一场战斗",
                    "en": "Win your first battle"
                },
                "icon": "⚔️",
                "rarity": "common",
                "condition": lambda: self.game.statistics.total_battles_won >= 1
            },
            "monster_slayer": {
                "name": {
                    "zh": "怪物杀手",
                    "en": "Monster Slayer"
                },
                "description": {
                    "zh": "击败10个怪物",
                    "en": "Defeat 10 monsters"
                },
                "icon": "👹",
                "rarity": "common",
                "condition": lambda: self.game.statistics.total_monsters_defeated >= 10
            },
            "boss_hunter": {
                "name": {
                    "zh": "Boss猎人",
                    "en": "Boss Hunter"
                },
                "description": {
                    "zh": "击败第一个Boss",
                    "en": "Defeat your first boss"
                },
                "icon": "👑",
                "rarity": "rare",
                "condition": lambda: self.game.statistics.total_bosses_defeated >= 1
            },
            "undefeated": {
                "name": {
                    "zh": "不败战神",
                    "en": "Undefeated"
                },
                "description": {
                    "zh": "连续赢得10场战斗",
                    "en": "Win 10 battles in a row"
                },
                "icon": "🛡️",
                "rarity": "epic",
                "condition": lambda: self.game.statistics.max_win_streak >= 10
            },
            
            # 资源相关成就
            "first_gold": {
                "name": {
                    "zh": "第一桶金",
                    "en": "First Gold"
                },
                "description": {
                    "zh": "获得第一枚金币",
                    "en": "Earn your first gold coin"
                },
                "icon": "💰",
                "rarity": "common",
                "condition": lambda: self.game.statistics.total_gold_earned >= 1
            },
            "rich_adventurer": {
                "name": {
                    "zh": "富有冒险者",
                    "en": "Rich Adventurer"
                },
                "description": {
                    "zh": "累计获得1000金币",
                    "en": "Earn 1000 gold coins in total"
                },
                "icon": "💎",
                "rarity": "rare",
                "condition": lambda: self.game.statistics.total_gold_earned >= 1000
            },
            "potion_collector": {
                "name": {
                    "zh": "药剂收藏家",
                    "en": "Potion Collector"
                },
                "description": {
                    "zh": "获得10瓶药剂",
                    "en": "Collect 10 potions"
                },
                "icon": "🧪",
                "rarity": "common",
                "condition": lambda: self.game.statistics.total_potions_obtained >= 10
            },
            
            # 装备相关成就
            "first_equipment": {
                "name": {
                    "zh": "第一件装备",
                    "en": "First Equipment"
                },
                "description": {
                    "zh": "获得第一件装备",
                    "en": "Obtain your first equipment"
                },
                "icon": "⚒️",
                "rarity": "common",
                "condition": lambda: self.game.statistics.total_equipment_obtained >= 1
            },
            "fully_equipped": {
                "name": {
                    "zh": "全副武装",
                    "en": "Fully Equipped"
                },
                "description": {
                    "zh": "同时装备武器、护甲和饰品",
                    "en": "Equip weapon, armor and accessory at the same time"
                },
                "icon": "🛡️",
                "rarity": "rare",
                "condition": lambda: all(self.game.equipment.values())
            },
            "legendary_collector": {
                "name": {
                    "zh": "传奇收藏家",
                    "en": "Legendary Collector"
                },
                "description": {
                    "zh": "获得一件传奇装备",
                    "en": "Obtain a legendary equipment"
                },
                "icon": "🌟",
                "rarity": "epic",
                "condition": lambda: self.game.statistics.equipment_by_rarity.get("legendary", 0) >= 1
            },
            
            # 技能相关成就
            "first_skill": {
                "name": {
                    "zh": "第一项技能",
                    "en": "First Skill"
                },
                "description": {
                    "zh": "学习第一个技能",
                    "en": "Learn your first skill"
                },
                "icon": "📚",
                "rarity": "common",
                "condition": lambda: len(self.game.hero_skills) >= 1
            },
            "skill_master": {
                "name": {
                    "zh": "技能大师",
                    "en": "Skill Master"
                },
                "description": {
                    "zh": "学会所有技能",
                    "en": "Learn all skills"
                },
                "icon": "🎓",
                "rarity": "epic",
                "condition": lambda: len(self.game.hero_skills) >= 4
            },
            
            # 等级相关成就
            "level_up": {
                "name": {
                    "zh": "升级",
                    "en": "Level Up"
                },
                "description": {
                    "zh": "达到5级",
                    "en": "Reach level 5"
                },
                "icon": "⬆️",
                "rarity": "common",
                "condition": lambda: self.game.hero_level >= 5
            },
            "veteran": {
                "name": {
                    "zh": "资深冒险者",
                    "en": "Veteran Adventurer"
                },
                "description": {
                    "zh": "达到10级",
                    "en": "Reach level 10"
                },
                "icon": "⭐",
                "rarity": "rare",
                "condition": lambda: self.game.hero_level >= 10
            },
            
            # 特殊成就
            "game_completion": {
                "name": {
                    "zh": "游戏通关",
                    "en": "Game Completion"
                },
                "description": {
                    "zh": "完成游戏",
                    "en": "Complete the game"
                },
                "icon": "🏆",
                "rarity": "legendary",
                "condition": lambda: self.game.victory
            },
            "survivor": {
                "name": {
                    "zh": "生存专家",
                    "en": "Survivor"
                },
                "description": {
                    "zh": "在困难难度下完成游戏",
                    "en": "Complete the game on hard difficulty"
                },
                "icon": "💀",
                "rarity": "legendary",
                "condition": lambda: self.game.victory and self.game.difficulty == "hard"
            }
        }

    def _load_unlocked_achievements(self):
        """加载已解锁的成就"""
        try:
            if os.path.exists(self.achievement_data_file):
                with open(self.achievement_data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.unlocked_achievements = data.get("unlocked_achievements", [])
        except:
            self.unlocked_achievements = []

    def _save_unlocked_achievements(self):
        """保存已解锁的成就"""
        try:
            data = {
                "unlocked_achievements": self.unlocked_achievements,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.achievement_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            pass

    def check_achievements(self):
        """检查并解锁符合条件的成就"""
        new_achievements = []
        
        for achievement_id, achievement_data in self.achievements.items():
            if achievement_id not in self.unlocked_achievements:
                try:
                    if achievement_data["condition"]():
                        self.unlocked_achievements.append(achievement_id)
                        new_achievements.append(achievement_id)
                        
                        # 显示成就解锁通知
                        self._show_achievement_unlocked(achievement_id, achievement_data)
                except:
                    # 如果条件检查失败，跳过这个成就
                    continue
        
        if new_achievements:
            self._save_unlocked_achievements()
        
        return new_achievements

    def _show_achievement_unlocked(self, achievement_id, achievement_data):
        """显示成就解锁通知"""
        lang = self.game.language
        
        name = achievement_data["name"][lang]
        description = achievement_data["description"][lang]
        icon = achievement_data["icon"]
        rarity = achievement_data["rarity"]
        
        # 根据稀有度设置颜色
        rarity_colors = {
            "common": "",
            "rare": "",
            "epic": "",
            "legendary": ""
        }
        
        print(f"\n{'='*50}")
        print(f"🎉 {self.game.lang.get_text('achievement_unlocked')}! 🎉")
        print(f"{icon} {name}")
        print(f"📝 {description}")
        print(f"⭐ {self.game.lang.get_text('rarity')}: {rarity}")
        print(f"{'='*50}")
        
        # 添加一点延迟让玩家有时间阅读
        import time
        time.sleep(2)

    def get_achievement_progress(self, achievement_id):
        """获取成就进度信息"""
        if achievement_id not in self.achievements:
            return None
        
        achievement_data = self.achievements[achievement_id]
        is_unlocked = achievement_id in self.unlocked_achievements
        
        return {
            "id": achievement_id,
            "name": achievement_data["name"][self.game.language],
            "description": achievement_data["description"][self.game.language],
            "icon": achievement_data["icon"],
            "rarity": achievement_data["rarity"],
            "unlocked": is_unlocked,
            "progress": self._calculate_progress(achievement_id)
        }

    def _calculate_progress(self, achievement_id):
        """计算成就进度"""
        # 这里可以添加更详细的进度计算逻辑
        # 目前只返回是否解锁
        return 100 if achievement_id in self.unlocked_achievements else 0

    def show_achievements_menu(self):
        """显示成就菜单"""
        while True:
            print(f"\n{'='*40}")
            print(f"🏆 {self.game.lang.get_text('achievements')}")
            print(f"{'='*40}")
            
            # 显示成就统计
            total_achievements = len(self.achievements)
            unlocked_count = len(self.unlocked_achievements)
            progress_percent = (unlocked_count / total_achievements) * 100
            
            print(f"📊 {self.game.lang.get_text('total_achievements')}: {total_achievements}")
            print(f"✅ {self.game.lang.get_text('unlocked_achievements')}: {unlocked_count}")
            print(f"📈 {self.game.lang.get_text('completion')}: {progress_percent:.1f}%")
            print()
            
            # 显示成就分类
            categories = {
                "progress": {"name": self.game.lang.get_text('progress_achievements'), "icon": "👣"},
                "combat": {"name": self.game.lang.get_text('combat_achievements'), "icon": "⚔️"},
                "resources": {"name": self.game.lang.get_text('resource_achievements'), "icon": "💰"},
                "equipment": {"name": self.game.lang.get_text('equipment_achievements'), "icon": "⚒️"},
                "skills": {"name": self.game.lang.get_text('skill_achievements'), "icon": "📚"},
                "special": {"name": self.game.lang.get_text('special_achievements'), "icon": "🏆"}
            }
            
            for i, (category, info) in enumerate(categories.items(), 1):
                print(f"{i}. {info['icon']} {info['name']}")
            
            print(f"{len(categories) + 1}. {self.game.lang.get_text('back_to_menu')}")
            
            choice = input(f"\n{self.game.lang.get_text('enter_choice')}: ").strip()
            
            if choice == str(len(categories) + 1):
                break
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(categories):
                    category = list(categories.keys())[choice_num - 1]
                    self._show_category_achievements(category, list(categories.keys())[choice_num - 1])
                else:
                    print(f"❌ {self.game.lang.get_text('invalid_choice')}")
            except ValueError:
                print(f"❌ {self.game.lang.get_text('invalid_choice')}")

    def _show_category_achievements(self, category, category_name):
        """显示指定分类的成就"""
        # 分类映射
        category_mapping = {
            "progress": ["first_step", "explorer", "master_explorer"],
            "combat": ["first_blood", "monster_slayer", "boss_hunter", "undefeated"],
            "resources": ["first_gold", "rich_adventurer", "potion_collector"],
            "equipment": ["first_equipment", "fully_equipped", "legendary_collector"],
            "skills": ["first_skill", "skill_master"],
            "special": ["level_up", "veteran", "game_completion", "survivor"]
        }
        
        achievements_in_category = category_mapping.get(category, [])
        
        print(f"\n{'='*40}")
        print(f"🏆 {self.game.lang.get_text(category + '_achievements')}")
        print(f"{'='*40}")
        
        for achievement_id in achievements_in_category:
            progress_info = self.get_achievement_progress(achievement_id)
            if progress_info:
                status_icon = "✅" if progress_info["unlocked"] else "🔒"
                print(f"{status_icon} {progress_info['icon']} {progress_info['name']}")
                print(f"   📝 {progress_info['description']}")
                print(f"   ⭐ {self.game.lang.get_text('rarity')}: {progress_info['rarity']}")
                if not progress_info["unlocked"]:
                    print(f"   📊 {self.game.lang.get_text('progress')}: {progress_info['progress']}%")
                print()
        
        input(f"{self.game.lang.get_text('continue_prompt')}")

    def get_achievement_summary(self):
        """获取成就摘要信息"""
        total = len(self.achievements)
        unlocked = len(self.unlocked_achievements)
        progress = (unlocked / total) * 100 if total > 0 else 0
        
        return {
            "total": total,
            "unlocked": unlocked,
            "progress": progress
        }