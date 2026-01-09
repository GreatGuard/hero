# -*- coding: utf-8 -*-
"""
存档数据模块 - 处理游戏存档的数据结构
"""

import json
import os
from datetime import datetime
from .statistics import GameStatistics


class SaveData:
    """存档数据类 - 包含所有需要序列化的游戏状态"""

    def __init__(self, game=None):
        """
        初始化存档数据

        Args:
            game: HeroGame实例，如果提供则从游戏实例提取数据
        """
        # 时间戳
        self.save_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.version = "3.0"

        if game:
            # 英雄基础属性
            self.hero_name = game.hero_name
            self.hero_class = game.hero_class
            self.hero_level = game.hero_level
            self.hero_exp = game.hero_exp

            # 英雄当前状态
            self.hero_hp = game.hero_hp
            self.hero_max_hp = game.hero_max_hp
            self.hero_attack = game.hero_attack
            self.hero_defense = game.hero_defense

            # 基础属性（不包含装备加成）
            self.base_attack = game.base_attack
            self.base_defense = game.base_defense
            self.base_max_hp = game.base_max_hp

            # 游戏进度
            self.hero_position = game.hero_position
            self.game_over = game.game_over
            self.victory = game.victory

            # 资源
            self.hero_gold = game.hero_gold
            self.hero_potions = game.hero_potions

            # 装备和背包
            self.equipment = {
                "weapon": game.equipment["weapon"],
                "armor": game.equipment["armor"],
                "accessory": game.equipment["accessory"]
            }
            self.inventory = game.inventory

            # 技能
            self.hero_skills = game.hero_skills

            # 游戏设置
            self.difficulty = game.difficulty
            self.map_type = game.map_type
            self.language = game.language
            self.map_length = game.map_length

            # 统计数据
            self.monsters_defeated = game.monsters_defeated
            self.events_encountered = game.events_encountered
            self.visited_positions = game.visited_positions

            # 游戏统计
            if hasattr(game, 'statistics') and game.statistics is not None:
                self.statistics_data = game.statistics.to_dict()
            else:
                self.statistics_data = {}
            
            # 状态效果
            if hasattr(game, 'status_effects') and game.status_effects is not None:
                self.status_effects = game.status_effects
            else:
                self.status_effects = {
                    "poison": 0,
                    "frostbite": 0,
                    "frost": 0
                }
                
            # 技能状态
            self.shield_active = getattr(game, 'shield_active', False)
            self.berserk_turns = getattr(game, 'berserk_turns', 0)
            self.focus_active = getattr(game, 'focus_active', False)
            
            # 职业系统相关属性
            self.class_mana = getattr(game, 'class_mana', 0)
            self.class_max_mana = getattr(game, 'class_max_mana', 0)
            
            # 任务系统
            if hasattr(game, 'quest_system') and game.quest_system is not None:
                self.quest_data = game.quest_system.to_dict()
            else:
                self.quest_data = {
                    'active_quests': [],
                    'completed_quests': [],
                    'quest_counter': 0
                }

    def to_dict(self):
        """
        将存档数据转换为字典

        Returns:
            dict: 包含所有存档数据的字典
        """
        return {
            "save_time": self.save_time,
            "version": self.version,

            # 英雄基础属性
            "hero_name": self.hero_name,
            "hero_class": self.hero_class,
            "hero_level": self.hero_level,
            "hero_exp": self.hero_exp,

            # 英雄当前状态
            "hero_hp": self.hero_hp,
            "hero_max_hp": self.hero_max_hp,
            "hero_attack": self.hero_attack,
            "hero_defense": self.hero_defense,

            # 基础属性
            "base_attack": self.base_attack,
            "base_defense": self.base_defense,
            "base_max_hp": self.base_max_hp,

            # 游戏进度
            "hero_position": self.hero_position,
            "game_over": self.game_over,
            "victory": self.victory,

            # 资源
            "hero_gold": self.hero_gold,
            "hero_potions": self.hero_potions,

            # 装备和背包
            "equipment": self.equipment,
            "inventory": self.inventory,

            # 技能
            "hero_skills": self.hero_skills,
            
            # 职业系统相关属性
            "class_mana": getattr(self, 'class_mana', 0),
            "class_max_mana": getattr(self, 'class_max_mana', 0),

            # 游戏设置
            "difficulty": self.difficulty,
            "map_type": self.map_type,
            "language": self.language,
            "map_length": self.map_length,

            # 统计数据
            "monsters_defeated": self.monsters_defeated,
            "events_encountered": self.events_encountered,
            "visited_positions": self.visited_positions,

            # 游戏统计
            "statistics_data": self.statistics_data,
            
            # 状态效果
            "status_effects": self.status_effects,
            
            # 技能状态
            "shield_active": self.shield_active,
            "berserk_turns": self.berserk_turns,
            "focus_active": self.focus_active,
            
            # 任务系统
            "quest_data": self.quest_data
        }

    @classmethod
    def from_dict(cls, data):
        """
        从字典创建SaveData实例

        Args:
            data: 包含存档数据的字典

        Returns:
            SaveData: 存档数据实例
        """
        save_data = cls()
        save_data.save_time = data.get("save_time", "")
        save_data.version = data.get("version", "3.0")

        # 英雄基础属性
        save_data.hero_name = data.get("hero_name", "")
        save_data.hero_class = data.get("hero_class", "")
        save_data.hero_level = data.get("hero_level", 1)
        save_data.hero_exp = data.get("hero_exp", 0)

        # 英雄当前状态
        save_data.hero_hp = data.get("hero_hp", 100)
        save_data.hero_max_hp = data.get("hero_max_hp", 100)
        save_data.hero_attack = data.get("hero_attack", 20)
        save_data.hero_defense = data.get("hero_defense", 5)

        # 基础属性
        save_data.base_attack = data.get("base_attack", 20)
        save_data.base_defense = data.get("base_defense", 5)
        save_data.base_max_hp = data.get("base_max_hp", 100)

        # 游戏进度
        save_data.hero_position = data.get("hero_position", 0)
        save_data.game_over = data.get("game_over", False)
        save_data.victory = data.get("victory", False)

        # 资源
        save_data.hero_gold = data.get("hero_gold", 0)
        save_data.hero_potions = data.get("hero_potions", 0)

        # 装备和背包
        save_data.equipment = data.get("equipment", {
            "weapon": None,
            "armor": None,
            "accessory": None
        })
        save_data.inventory = data.get("inventory", [])

        # 技能
        save_data.hero_skills = data.get("hero_skills", [])

        # 游戏设置
        save_data.difficulty = data.get("difficulty", "normal")
        save_data.map_type = data.get("map_type", "plains")
        save_data.language = data.get("language", "zh")
        save_data.map_length = data.get("map_length", 50)

        # 统计数据
        save_data.monsters_defeated = data.get("monsters_defeated", 0)
        save_data.events_encountered = data.get("events_encountered", [])
        save_data.visited_positions = data.get("visited_positions", [])
        
        # 状态效果
        save_data.status_effects = data.get("status_effects", {
            "poison": 0,
            "frostbite": 0,
            "frost": 0
        })
        
        # 技能状态
        save_data.shield_active = data.get("shield_active", False)
        save_data.berserk_turns = data.get("berserk_turns", 0)
        save_data.focus_active = data.get("focus_active", False)
        
        # 职业系统相关属性
        save_data.class_mana = data.get("class_mana", 0)
        save_data.class_max_mana = data.get("class_max_mana", 0)

        # 游戏统计
        save_data.statistics_data = data.get("statistics_data", {})
        
        # 任务系统
        save_data.quest_data = data.get("quest_data", {
            'active_quests': [],
            'completed_quests': [],
            'quest_counter': 0
        })

        return save_data


class SaveManager:
    """存档管理器 - 处理存档的保存和加载"""

    def __init__(self, save_dir="saves"):
        """
        初始化存档管理器

        Args:
            save_dir: 存档目录路径
        """
        self.save_dir = save_dir
        self.max_slots = 5  # 最多5个存档槽位

        # 确保存档目录存在
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def get_save_path(self, slot_number):
        """
        获取存档文件路径

        Args:
            slot_number: 存档槽位号（1-5）

        Returns:
            str: 存档文件路径
        """
        if slot_number < 1 or slot_number > self.max_slots:
            raise ValueError(f"Slot number must be between 1 and {self.max_slots}")
        return os.path.join(self.save_dir, f"save_slot_{slot_number}.json")

    def save_game(self, save_data, slot_number):
        """
        保存游戏到指定槽位

        Args:
            save_data: SaveData实例
            slot_number: 存档槽位号（1-5）

        Returns:
            bool: 保存是否成功

        Raises:
            ValueError: 如果槽位号无效
        """
        try:
            save_path = self.get_save_path(slot_number)

            # 转换为字典并保存为JSON
            data_dict = save_data.to_dict()

            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, ensure_ascii=False, indent=2)

            return True

        except ValueError:
            # 重新抛出ValueError（槽位号无效等）
            raise
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, slot_number):
        """
        从指定槽位加载游戏

        Args:
            slot_number: 存档槽位号（1-5）

        Returns:
            SaveData or None: 存档数据实例，加载失败返回None
        """
        try:
            save_path = self.get_save_path(slot_number)

            # 检查文件是否存在
            if not os.path.exists(save_path):
                return None

            # 读取JSON文件
            with open(save_path, 'r', encoding='utf-8') as f:
                data_dict = json.load(f)

            # 验证基本数据完整性
            if not self._validate_save_data(data_dict):
                return None

            # 创建SaveData实例
            return SaveData.from_dict(data_dict)

        except json.JSONDecodeError:
            print("Error: Save file is corrupted")
            return None
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    def _validate_save_data(self, data):
        """
        验证存档数据的完整性

        Args:
            data: 存档数据字典

        Returns:
            bool: 数据是否有效
        """
        # 检查必需的字段
        required_fields = [
            "hero_name", "hero_level", "hero_exp",
            "hero_hp", "hero_max_hp",
            "difficulty", "map_type", "language"
        ]

        for field in required_fields:
            if field not in data:
                return False

        return True

    def list_save_slots(self):
        """
        列出所有存档槽位的摘要信息

        Returns:
            list: 存档摘要列表，每个元素包含槽位号、英雄名、等级、保存时间等信息
        """
        slots = []

        for slot_num in range(1, self.max_slots + 1):
            save_path = self.get_save_path(slot_num)

            if os.path.exists(save_path):
                try:
                    with open(save_path, 'r', encoding='utf-8') as f:
                        data_dict = json.load(f)

                    slots.append({
                        "slot": slot_num,
                        "hero_name": data_dict.get("hero_name", "Unknown"),
                        "hero_level": data_dict.get("hero_level", 1),
                        "map_type": data_dict.get("map_type", "plains"),
                        "difficulty": data_dict.get("difficulty", "normal"),
                        "save_time": data_dict.get("save_time", ""),
                        "position": data_dict.get("hero_position", 0),
                        "map_length": data_dict.get("map_length", 50)
                    })
                except:
                    # 读取失败，跳过该槽位
                    pass
            else:
                slots.append({
                    "slot": slot_num,
                    "empty": True
                })

        return slots

    def delete_save(self, slot_number):
        """
        删除指定槽位的存档

        Args:
            slot_number: 存档槽位号（1-5）

        Returns:
            bool: 删除是否成功
        """
        try:
            save_path = self.get_save_path(slot_number)

            if os.path.exists(save_path):
                os.remove(save_path)
                return True
            else:
                return False

        except Exception as e:
            print(f"Error deleting save: {e}")
            return False
