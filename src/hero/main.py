#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
英雄无敌 - 简单文字冒险游戏 (多语言版本)
作者: Kevin
版本: 3.0 (模块化重构)
"""

import random
import time
import os
import sys
from hero.language import LanguageSupport
from hero.game_config import DIFFICULTY_SETTINGS, MAP_TYPES, EVENT_TYPES, CLASS_DEFINITIONS
from hero.combat import CombatSystem
from hero.equipment import EquipmentSystem
from hero.events import EventSystem
from hero.newbie_village import NewbieVillage
from hero.save_data import SaveData, SaveManager
from hero.statistics import GameStatistics
from hero.achievements import AchievementSystem
from hero.quest import QuestSystem
from hero.skill_tree import SkillTree


class HeroGame:
    """英雄无敌游戏主类"""

    def __init__(self):
        """初始化游戏"""
        self.language = "zh"  # 默认中文
        self.lang = LanguageSupport(self.language)

        # 先选择语言
        self.select_language()

        # 选择地图类型和难度
        # self.select_map_and_difficulty()

        # 初始化英雄属性
        self.hero_name = ""
        self.hero_class = ""  # 英雄职业
        self.hero_hp = 100  # 初始血量
        self.hero_max_hp = 100  # 最大血量
        self.hero_attack = 20  # 初始攻击力
        self.hero_defense = 5  # 初始防御力
        self.hero_position = 0  # 当前位置
        self.hero_exp = 0  # 经验值
        self.hero_level = 1  # 等级
        self.hero_skills = []  # 英雄技能
        self.skill_points = 0  # 技能点
        self.game_over = False
        self.victory = False
        self.monsters_defeated = 0  # 击败的怪物数量
        self.events_encountered = []  # 遇到的事件历史
        
        # 职业系统相关属性
        self.class_mana = 0  # 法师的法力值
        self.class_max_mana = 0  # 最大法力值
        self.combat_first_turn = True  # 战斗第一回合标记（用于刺客特性）
        
        # 技能状态跟踪
        self.shield_active = False  # 护盾状态
        self.berserk_turns = 0  # 狂暴剩余回合
        self.focus_active = False  # 专注状态

        # 注意：map_length、hero_gold、hero_potions、visited_positions 已在 select_map_and_difficulty() 中设置

        # 装备系统
        self.equipment = {
            "weapon": None,    # 武器
            "armor": None,     # 防具
            "accessory": None  # 饰品
        }
        self.inventory = []  # 背包存储物品

        # 基础属性（不包含装备加成）
        self.base_attack = 20  # 基础攻击力
        self.base_defense = 5  # 基础防御力
        self.base_max_hp = 100  # 基础最大血量

        # 初始化属性（基于基础属性和装备）
        self.update_attributes()

        # 初始化状态效果系统
        self.status_effects = {
            "poison": 0,      # 中毒剩余回合
            "frostbite": 0,    # 冻伤剩余回合（减少攻击力）
            "frost": 0         # 冰霜效果剩余回合（减少防御力）
        }
        
        # 初始化特殊效果属性
        self.special_effects = {
            "crit_rate": 0.0,      # 暴击率
            "lifesteal_rate": 0.0, # 吸血率
            "dodge_rate": 0.0,     # 闪避率
            "counter_attack_rate": 0.0, # 反击率
            "ice_damage": 0,       # 冰霜伤害
            "fire_damage": 0,      # 火焰伤害
            "healing_rate": 0.0,   # 治疗效果
            "mana_boost": 0,       # 法力提升
            "backstab_damage": 0.0, # 背刺伤害
            "luck_bonus": 0.0,     # 幸运加成
            "wisdom_bonus": 0.0,   # 智慧加成
            "immortality_chance": 0.0, # 不死概率
            "health_regeneration": 0, # 生命恢复
            "mana_regeneration": 0,   # 法力恢复
            "holy_resistance": 0.0,   # 神圣抗性
            "fire_resistance": 0.0,   # 火焰抗性
            "stealth_chance": 0.0,    # 潜行概率
            "evasion_rate": 0.0,      # 闪避率
            "spell_power": 0.0,       # 法术强度
            "crit_damage": 0.0        # 暴击伤害
        }

        # 初始化子系统
        self.combat_system = CombatSystem(self)
        self.equipment_system = EquipmentSystem(self)
        self.event_system = EventSystem(self)
        self.newbie_village = NewbieVillage(self)

        # 初始化统计系统
        self.statistics = GameStatistics()
        
        # 初始化成就系统
        self.achievements = AchievementSystem(self)
        
        # 初始化任务系统
        self.quest_system = QuestSystem()
        
        # 技能树系统将在职业选择后初始化
        self.skill_tree = None

    def select_language(self):
        """选择游戏语言"""
        self.clear_screen()
        print(self.lang.get_text("block_separator"))
        print(f"          {self.lang.get_text('choose_language')}")
        print(self.lang.get_text("block_separator"))
        print()
        print(f"1. {self.lang.get_text('chinese')}")
        print(f"2. {self.lang.get_text('english')}")
        print()

        while True:
            choice = input(f"{self.lang.get_text('enter_choice')} (1): ").strip()
            if choice == "" or choice == "1":
                self.language = "zh"
                self.lang.set_language("zh")
                break
            elif choice == "2":
                self.language = "en"
                self.lang.set_language("en")
                break
            else:
                print(f"{self.lang.get_text('invalid_choice')}")

    def select_map_and_difficulty(self):
        """选择地图类型和难度"""
        self.difficulty_settings = DIFFICULTY_SETTINGS
        self.map_types = MAP_TYPES

        self.clear_screen()
        print(self.lang.get_text("block_separator"))
        print(f"          {self.lang.get_text('select_map_difficulty')}")
        print(self.lang.get_text("block_separator"))
        print()

        print(self.lang.get_text("select_difficulty"))
        print(f"1. {self.lang.get_text('difficulty_easy')}")
        print(f"2. {self.lang.get_text('difficulty_normal')}")
        print(f"3. {self.lang.get_text('difficulty_hard')}")
        print(f"4. {self.lang.get_text('difficulty_nightmare')}")
        print()

        while True:
            choice = input(f"{self.lang.get_text('enter_choice')} (2): ").strip()
            if choice == "" or choice == "2":
                self.difficulty = "normal"
                break
            elif choice == "1":
                self.difficulty = "easy"
                break
            elif choice == "3":
                self.difficulty = "hard"
                break
            elif choice == "4":
                self.difficulty = "nightmare"
                break
            else:
                print(self.lang.get_text("invalid_choice"))

        self.clear_screen()
        print(self.lang.get_text("block_separator"))
        print(f"          {self.lang.get_text('select_map_type')}")
        print(self.lang.get_text("block_separator"))
        print()

        print(self.lang.get_text("select_map_type"))
        print(f"1. {self.lang.get_text('map_plains')} - {self.lang.get_text('plains_desc')}")
        print(f"2. {self.lang.get_text('map_forest')} - {self.lang.get_text('forest_desc')}")
        print(f"3. {self.lang.get_text('map_desert')} - {self.lang.get_text('desert_desc')}")
        print(f"4. {self.lang.get_text('map_dungeon')} - {self.lang.get_text('dungeon_desc')}")
        print(f"5. {self.lang.get_text('map_mountain')} - {self.lang.get_text('mountain_desc')}")
        print(f"6. {self.lang.get_text('map_swamp')} - {self.lang.get_text('swamp_desc')}")
        print(f"7. {self.lang.get_text('map_snowfield')} - {self.lang.get_text('snowfield_desc')}")
        print()

        while True:
            choice = input(f"{self.lang.get_text('enter_choice')} (1): ").strip()
            if choice == "" or choice == "1":
                self.map_type = "plains"
                break
            elif choice == "2":
                self.map_type = "forest"
                break
            elif choice == "3":
                self.map_type = "desert"
                break
            elif choice == "4":
                self.map_type = "dungeon"
                break
            elif choice == "5":
                self.map_type = "mountain"
                break
            elif choice == "6":
                self.map_type = "swamp"
                break
            elif choice == "7":
                self.map_type = "snowfield"
                break
            else:
                print(self.lang.get_text("invalid_choice"))

        # 应用难度设置
        settings = self.difficulty_settings[self.difficulty]
        self.map_length = settings["map_length"]
        self.hero_gold = settings["gold_start"]
        self.hero_potions = settings["potions_start"]

        # 更新visited_positions数组大小
        self.visited_positions = [False] * self.map_length

        self.clear_screen()
        print(self.lang.get_text("block_separator"))
        print(f"          {self.lang.get_text('game_settings')}")
        print(self.lang.get_text("block_separator"))
        print()
        print(f"{self.lang.get_text('difficulty')}: {self.lang.get_text('difficulty_' + self.difficulty)}")
        print(f"{self.lang.get_text('map_type')}: {self.lang.get_text('map_' + self.map_type)}")
        print(f"{self.lang.get_text('map_length')}: {self.map_length}")
        print()
        input(self.lang.get_text("continue_prompt"))

    def clear_screen(self):
        """清屏函数"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_welcome(self):
        """显示欢迎界面"""
        self.clear_screen()
        print(self.lang.get_text("block_separator"))
        print(f"          {self.lang.get_text('welcome_title')}")
        print(self.lang.get_text("block_separator"))
        print()
        print(self.lang.get_text("welcome_desc1"))
        print(self.lang.get_text("welcome_desc2"))
        print(self.lang.get_text("welcome_desc3"))
        print(self.lang.get_text("welcome_desc4"))
        print(self.lang.get_text("welcome_desc5"))
        print()
        input(self.lang.get_text("continue_prompt"))

    def get_hero_name(self):
        """获取英雄名字"""
        self.clear_screen()
        print(self.lang.get_text("block_separator"))
        print(f"          {self.lang.get_text('hero_creation')}")
        print(self.lang.get_text("block_separator"))
        print()

        while True:
            name = input(self.lang.get_text("enter_name")).strip()
            if name:
                self.hero_name = name
                break
            else:
                print(self.lang.get_text("name_empty"))
    
    def select_hero_class(self):
        """选择英雄职业"""
        self.clear_screen()
        print(self.lang.get_text("block_separator"))
        print(f"          {self.lang.get_text('class_selection')}")
        print(self.lang.get_text("block_separator"))
        print()
        
        # 显示三个职业选项
        class_options = {
            "1": "warrior",
            "2": "mage",
            "3": "assassin"
        }
        
        for num, class_key in class_options.items():
            class_info = CLASS_DEFINITIONS[class_key]
            print(f"{num}. {self.lang.get_text(class_info['name_key'])}")
            print(f"   {self.lang.get_text(class_info['description_key'])}")
            print(f"   {self.lang.get_text('class_attributes')}: {self.lang.get_text('attack')}={class_info['base_attributes']['attack']}, {self.lang.get_text('defense')}={class_info['base_attributes']['defense']}, {self.lang.get_text('max_hp')}={class_info['base_attributes']['max_hp']}")
            print()
        
        while True:
            choice = input(self.lang.get_text("choose_your_class")).strip()
            if choice in class_options:
                selected_class = class_options[choice]
                class_info = CLASS_DEFINITIONS[selected_class]
                
                # 确认选择
                print()
                class_name = self.lang.get_text(class_info['name_key'])
                confirm_text = self.lang.get_text("confirm_class_selection").format(
                    hero_class=class_name
                )
                confirm = input(confirm_text).strip().lower()
                
                if confirm in self.lang.get_text("yes_options"):
                    self.hero_class = selected_class
                    print()
                    print(self.lang.get_text("class_selected").format(
                        hero_class=class_name
                    ))
                    
                    # 应用职业基础属性
                    self.apply_class_attributes(selected_class)
                    
                    # 初始化技能树系统
                    self.skill_tree = SkillTree(selected_class, self.lang)
                    
                    # 添加职业初始技能（使用 skill_id）
                    for skill in class_info['starting_skills']:
                        self.hero_skills.append(skill)  # 存储 skill_id 而不是技能名称
                        # 学习初始技能
                        if skill in self.skill_tree.skill_nodes:
                            self.skill_tree.learned_skills[skill] = 1
                            self.skill_tree.skill_nodes[skill].current_level = 1
                    
                    # 更新技能树可用性
                    self.skill_tree._update_skill_availability()
                    
                    print()
                    input(self.lang.get_text("continue_prompt"))
                    break
            else:
                print(f"{self.lang.get_text('invalid_choice')} (1-3)")
    
    def apply_class_attributes(self, class_key):
        """应用职业属性加成"""
        class_info = CLASS_DEFINITIONS[class_key]
        
        # 应用基础属性
        self.base_attack = class_info['base_attributes']['attack']
        self.base_defense = class_info['base_attributes']['defense']
        self.base_max_hp = class_info['base_attributes']['max_hp']
        
        # 初始化当前属性
        self.hero_hp = self.base_max_hp
        self.hero_max_hp = self.base_max_hp
        
        # 如果是法师，初始化法力值
        if class_key == "mage":
            self.class_max_mana = 100  # 初始法力值
            self.class_mana = self.class_max_mana
        
        # 更新总属性（包含装备加成）
        self.update_attributes()
    
    def get_class_growth_multiplier(self, attribute):
        """获取职业属性成长倍率"""
        if not self.hero_class:
            return 1.0
            
        class_info = CLASS_DEFINITIONS.get(self.hero_class, {})
        growth_multipliers = class_info.get('growth_multipliers', {})
        return growth_multipliers.get(attribute, 1.0)

    def show_hero_info(self):
        """显示英雄信息"""
        print(f"\n【{self.hero_name}】 Lv.{self.hero_level}")
        if self.hero_class:
            class_name = self.lang.get_text(f"class_{self.hero_class}")
            print(f"⚔️  {self.lang.get_text('class')}: {class_name}")
        print(f"❤️  {self.lang.get_text('hp')}{self.lang.get_text('item_separator')}{self.hero_hp}/{self.hero_max_hp}")
        print(f"⚔️  {self.lang.get_text('attack')}{self.lang.get_text('item_separator')}{self.hero_attack}")
        print(f"🛡️  {self.lang.get_text('defense')}{self.lang.get_text('item_separator')}{self.hero_defense}")
        print(f"💰  {self.lang.get_text('gold')}{self.lang.get_text('item_separator')}{self.hero_gold}")
        print(f"⭐  {self.lang.get_text('exp')}{self.lang.get_text('item_separator')}{self.hero_exp}")
        print(f"🧪  {self.lang.get_text('potions')}{self.lang.get_text('item_separator')}{self.hero_potions}")
        
        # 如果是法师，显示法力值
        if self.hero_class == "mage" and hasattr(self, 'class_max_mana'):
            print(f"💧  {self.lang.get_text('mana')}{self.lang.get_text('item_separator')}{self.class_mana}/{self.class_max_mana}")
        
        # 显示技能点
        if self.skill_tree:
            print(f"⭐  {self.lang.get_text('skill_points')}{self.lang.get_text('item_separator')}{self.skill_points}")
        
        # 使用统一的多语言格式化函数处理位置显示
        position_text = self.lang.format_text("position_format", self.hero_position+1, self.map_length)
        print(f"📍  {self.lang.get_text('position')}{self.lang.get_text('item_separator')}{position_text}")

        # 显示装备信息
        weapon_name = self.equipment["weapon"]["name"] if self.equipment["weapon"] else self.lang.get_text("none")
        armor_name = self.equipment["armor"]["name"] if self.equipment["armor"] else self.lang.get_text("none")
        accessory_name = self.equipment["accessory"]["name"] if self.equipment["accessory"] else self.lang.get_text("none")

        print(f"🗡️  {self.lang.get_text('weapon')}{self.lang.get_text('item_separator')}{weapon_name}")
        print(f"🛡️  {self.lang.get_text('armor')}{self.lang.get_text('item_separator')}{armor_name}")
        print(f"💍  {self.lang.get_text('accessory')}{self.lang.get_text('item_separator')}{accessory_name}")

        # 显示技能（使用 skill_id 从 hero_skills 获取技能名称和等级）
        if self.hero_skills:
            skill_info = []
            # 按技能类别和优先级排序
            from hero.game_config import SKILL_TREES
            def get_skill_priority(skill_id):
                if not self.hero_class or self.hero_class not in SKILL_TREES:
                    return 0
                skill_category = SKILL_TREES[self.hero_class].get(skill_id, {}).get("category", "core")
                category_priority = {"core": 0, "combat": 1, "passive": 2, "ultimate": 3}
                return category_priority.get(skill_category, 0)
            
            # 对技能列表进行排序
            sorted_skills = sorted(self.hero_skills, key=get_skill_priority)
            
            for skill_id in sorted_skills:
                # 获取技能名称
                # 检查技能ID是否已经包含"_skill"后缀
                if skill_id.endswith("_skill"):
                    skill_name_key = skill_id
                else:
                    skill_name_key = f"{skill_id}_skill"
                skill_name = self.lang.get_text(skill_name_key)
                # 从技能树获取技能等级
                skill_level = 0
                if self.skill_tree and skill_id in self.skill_tree.learned_skills:
                    skill_level = self.skill_tree.learned_skills[skill_id]
                # 显示技能等级
                if skill_level > 0:
                    skill_info.append(f"{skill_name} Lv.{skill_level}")
                else:
                    skill_info.append(skill_name)
                
            print(f"🔥  {self.lang.get_text('skills')}{self.lang.get_text('item_separator')}{', '.join(skill_info)}")
        print()

    def draw_map(self):
        """绘制地图"""
        map_visual = ""
        # 使用统一的多语言格式化函数获取英雄标记
        hero_marker = self.lang.format_text("hero_marker")
        for i in range(self.map_length):
            if i == self.hero_position:
                map_visual += f"[{hero_marker}]"
            else:
                map_visual += "[__]"
        print(f"\n{self.lang.get_text('map')}{self.lang.get_text('item_separator')}{map_visual}")

    def start_game(self):
        """开始游戏"""
        self.show_welcome()
        self.show_main_menu()

    def show_main_menu(self):
        """显示主菜单"""
        while True:
            self.clear_screen()
            print(self.lang.get_text("block_separator"))
            print(f"          {self.lang.get_text('main_menu')}")
            print(self.lang.get_text("block_separator"))
            print()
            print(f"1. {self.lang.get_text('new_game')}")
            print(f"2. {self.lang.get_text('load_game')}")
            print(f"3. {self.lang.get_text('view_statistics')}")
            print(f"4. {self.lang.get_text('achievements')}")
            print(f"5. {self.lang.get_text('exit_game')}")
            print()

            choice = input(f"{self.lang.get_text('enter_choice')} (1): ").strip()

            if choice == "" or choice == "1":
                # 新游戏
                self.get_hero_name()
                self.select_hero_class()  # 添加职业选择
                self.select_map_and_difficulty()

                # 进入新手村
                self.newbie_village.newbie_village()

                self.clear_screen()
                print(self.lang.get_text("block_separator"))
                print(f"          {self.lang.get_text('game_start')}, {self.hero_name}!")
                print(self.lang.get_text("block_separator"))
                time.sleep(1)

                self.game_loop()
                self.restart_game()
                break

            elif choice == "2":
                # 加载存档
                if self.load_game_menu():
                    # 如果加载成功，进入游戏循环
                    self.clear_screen()
                    print(self.lang.get_text("block_separator"))
                    print(f"          {self.lang.get_text('load_success')}, {self.hero_name}!")
                    print(self.lang.get_text("block_separator"))
                    time.sleep(1)

                    self.game_loop()
                    self.restart_game()
                # 如果加载失败或取消，返回主菜单

            elif choice == "3":
                # 查看统计
                self.show_statistics_menu()

            elif choice == "4":
                # 查看成就
                self.achievements.show_achievements_menu()

            elif choice == "5":
                # 退出游戏
                print("\n" + self.lang.get_text("goodbye"))
                sys.exit(0)

            else:
                print(self.lang.get_text("invalid_choice"))
                time.sleep(1)

    def load_game_menu(self):
        """
        加载存档菜单

        Returns:
            bool: 是否成功加载存档
        """
        save_manager = SaveManager()

        while True:
            self.clear_screen()
            print(self.lang.get_text("block_separator"))
            print(f"          {self.lang.get_text('load_game')}")
            print(self.lang.get_text("block_separator"))
            print()

            # 列出所有存档槽位
            slots = save_manager.list_save_slots()

            for slot_info in slots:
                if slot_info.get("empty"):
                    print(f"{slot_info['slot']}. {self.lang.get_text('save_slot_empty')} {slot_info['slot']} - {self.lang.get_text('empty_slot')}")
                else:
                    position_text = self.lang.format_text("position_format",
                                                          slot_info['position'] + 1,
                                                          slot_info['map_length'])
                    print(f"{slot_info['slot']}. {self.lang.get_text('save_slot_info')}: {slot_info['hero_name']} | "
                          f"{self.lang.get_text('save_slot_level')}: {slot_info['hero_level']} | "
                          f"{self.lang.get_text('map_type')}: {self.lang.get_text('map_' + slot_info['map_type'])} | "
                          f"{self.lang.get_text('difficulty')}: {self.lang.get_text('difficulty_' + slot_info['difficulty'])} | "
                          f"{self.lang.get_text('save_slot_position')}: {position_text}")

            print()
            print(f"0. {self.lang.get_text('return_to_main')}")
            print()

            choice = input(f"{self.lang.get_text('enter_choice')}: ").strip()

            if choice == "0":
                return False

            try:
                slot_num = int(choice)
                if 1 <= slot_num <= 5:
                    # 尝试加载存档
                    save_data = save_manager.load_game(slot_num)

                    if save_data:
                        # 从存档数据恢复游戏
                        self.load_from_save_data(save_data)
                        return True
                    else:
                        print(f"\n{self.lang.get_text('no_save_slot')}")
                        input(f"{self.lang.get_text('continue_prompt')}")
                else:
                    print(self.lang.get_text("invalid_choice"))
                    input(f"{self.lang.get_text('continue_prompt')}")
            except ValueError:
                print(self.lang.get_text("invalid_choice"))
                input(f"{self.lang.get_text('continue_prompt')}")
    def show_statistics(self):
        """显示统计数据"""
        self.clear_screen()
        print(self.statistics.format_summary(self.lang))
        input(f"\n{self.lang.get_text('continue_prompt')}")

    def show_statistics_menu(self):
        """显示统计菜单"""
        # 这里显示当前会话的统计（因为没有正在进行的游戏）
        # 创建一个临时统计对象用于演示
        temp_stats = GameStatistics()

        self.clear_screen()
        print(temp_stats.format_summary(self.lang))
        input(f"\n{self.lang.get_text('continue_prompt')}")

    def save_game_menu(self):
        """保存游戏菜单"""
        save_manager = SaveManager()

        while True:
            self.clear_screen()
            print(self.lang.get_text("block_separator"))
            print(f"          {self.lang.get_text('save_game')}")
            print(self.lang.get_text("block_separator"))
            print()

            # 列出所有存档槽位
            slots = save_manager.list_save_slots()

            for slot_info in slots:
                if slot_info.get("empty"):
                    print(f"{slot_info['slot']}. {self.lang.get_text('save_slot_empty')} {slot_info['slot']} - {self.lang.get_text('empty_slot')}")
                else:
                    position_text = self.lang.format_text("position_format",
                                                          slot_info['position'] + 1,
                                                          slot_info['map_length'])
                    print(f"{slot_info['slot']}. {self.lang.get_text('save_slot_info')}: {slot_info['hero_name']} | "
                          f"{self.lang.get_text('save_slot_level')}: {slot_info['hero_level']} | "
                          f"{self.lang.get_text('save_slot_time')}: {slot_info['save_time']}")

            print()
            print(f"0. {self.lang.get_text('return_to_game')}")
            print()

            choice = input(f"{self.lang.get_text('enter_choice')}: ").strip()

            if choice == "0":
                return

            try:
                slot_num = int(choice)
                if 1 <= slot_num <= 5:
                    # 确认覆盖
                    if not slots[slot_num - 1].get("empty"):
                        confirm = input(f"{self.lang.get_text('overwrite_save')}? (y/n): ").strip().lower()
                        if confirm not in self.lang.get_text("yes_options"):
                            continue

                    # 保存游戏
                    save_data = self.get_save_data()
                    if save_manager.save_game(save_data, slot_num):
                        print(f"\n{self.lang.get_text('save_success')} {slot_num}!")
                        input(f"{self.lang.get_text('continue_prompt')}")
                        return
                    else:
                        print(f"\n{self.lang.get_text('save_failed')}")
                        input(f"{self.lang.get_text('continue_prompt')}")
                else:
                    print(self.lang.get_text("invalid_choice"))
                    input(f"{self.lang.get_text('continue_prompt')}")
            except ValueError:
                print(self.lang.get_text("invalid_choice"))
                input(f"{self.lang.get_text('continue_prompt')}")

    def game_loop(self):
        """游戏主循环"""
        while not self.game_over:
            self.draw_map()
            self.show_hero_info()

            if self.check_game_status():
                break

            self.move_hero()

            if self.check_game_status():
                break

            # 检查成就
            self.achievements.check_achievements()

            input(f"\n{self.lang.get_text('continue_prompt')}")
            self.clear_screen()

    def check_game_status(self):
        """检查游戏状态"""
        if self.hero_hp <= 0:
            input(f"\n{self.lang.get_text('continue_prompt')}")
            self.game_over = True
            self.clear_screen()
            print(self.lang.get_text("block_separator"))
            print(f"          {self.lang.get_text('game_over')}")
            print(self.lang.get_text("block_separator"))
            print(f"{self.hero_name} {self.lang.get_text('game_over_msg')}")
            print(self.lang.get_text("try_again"))
            return True

        if self.hero_position >= self.map_length - 1:
            input(f"\n{self.lang.get_text('continue_prompt')}")
            self.victory = True
            self.game_over = True
            self.clear_screen()
            print(self.lang.get_text("block_separator"))
            print(f"          {self.lang.get_text('victory')}")
            print(self.lang.get_text("block_separator"))
            print(f"{self.hero_name} {self.lang.get_text('victory_msg')}!")
            print(f"{self.lang.get_text('final_status')} - {self.lang.get_text('hp')}{self.lang.get_text('item_separator')}{self.hero_hp}, {self.lang.get_text('attack')}{self.lang.get_text('item_separator')}{self.hero_attack}")
            print(self.lang.get_text("real_hero"))
            return True

        return False

    def move_hero(self):
        """移动英雄"""
        print(f"\n{self.lang.get_text('choose_action')}")
        print(f"1. {self.lang.get_text('forward')}")
        print(f"2. {self.lang.get_text('view_status')}")
        print(f"3. {self.lang.get_text('view_history')}")
        if self.hero_potions > 0:
            print(f"4. {self.lang.get_text('use_potion')}")
        print(f"5. {self.lang.get_text('shop')}")
        print(f"6. {self.lang.get_text('equipment_management')}")
        print(f"7. {self.lang.get_text('save_game')}")
        print(f"8. {self.lang.get_text('view_statistics')}")
        print(f"9. {self.lang.get_text('view_quests')}")
        if self.skill_tree:
            print(f"10. {self.lang.get_text('skill_tree_title')}")
        print(f"11. {self.lang.get_text('exit_game')}")

        while True:
            choice = input(f"{self.lang.get_text('enter_choice')} (1): ").strip()

            if choice == "" or choice == "1":
                if self.hero_position < self.map_length - 1:
                    self.hero_position += 1
                    # 记录移动一步
                    self.statistics.record_step()
                    
                    # 更新状态效果
                    self.update_status_effects()
                    
                    # 更新到达位置任务进度
                    completed_quests = self.quest_system.update_quest_progress("reach_position", self.hero_position)
                    self.handle_quest_completions(completed_quests)
                    
                    # 触发随机事件
                    self.random_event()
                    return True
                else:
                    print(self.lang.get_text("already_at_end"))
                    return False
            elif choice == "2":
                self.show_hero_info()
                self.draw_map()
            elif choice == "3":
                self.event_system.show_adventure_history()
            elif choice == "4" and self.hero_potions > 0:
                self.event_system.use_potion()
                
                # 更新使用药剂任务进度
                completed_quests = self.quest_system.update_quest_progress("use_potion")
                self.handle_quest_completions(completed_quests)
            elif choice == "5":
                self.event_system.merchant_event()
            elif choice == "6":
                self.equipment_system.equipment_management()
            elif choice == "7":
                self.save_game_menu()
            elif choice == "8":
                self.show_statistics()
            elif choice == "9":
                self.show_quests()
            elif choice == "10" and self.skill_tree:
                self.show_skill_tree_menu()
            elif choice == "11" or (choice == "10" and not self.skill_tree):
                # 退出游戏循环
                self.game_over = True
                return False
            else:
                print(self.lang.get_text("invalid_choice"))

    def show_skill_tree_menu(self):
        """显示技能树菜单"""
        self.clear_screen()
        print(self.lang.get_text("block_separator"))
        print(f"          {self.lang.get_text('skill_tree_title')}")
        print(self.lang.get_text("block_separator"))
        
        show_all = False
        while True:
            self.clear_screen()
            
            # 显示技能树
            print(self.skill_tree.format_tree(show_all))
            print(f"\n{self.lang.get_text('skill_points')}: {self.skill_points}")
            print()
            
            # 显示选项
            print(f"1. {self.lang.get_text('select_skill_to_upgrade')}")
            if show_all:
                print(f"2. {self.lang.get_text('show_available_skills')}")
            else:
                print(f"2. {self.lang.get_text('show_all_skills')}")
            print(f"3. {self.lang.get_text('back_to_game')}")
            
            choice = input(f"{self.lang.get_text('enter_choice')} (1): ").strip()
            
            if choice == "" or choice == "1":
                # 获取可升级的技能列表
                upgradeable_skills = [
                    skill_id for skill_id in self.skill_tree.skill_nodes
                    if self.skill_tree.can_upgrade_skill(skill_id, self.skill_points)
                ]
                
                if not upgradeable_skills:
                    input(self.lang.get_text("not_enough_skill_points"))
                    continue
                
                # 显示可升级的技能
                print(f"\n{self.lang.get_text('select_skill_to_upgrade')}:")
                for i, skill_id in enumerate(upgradeable_skills, 1):
                    skill_node = self.skill_tree.skill_nodes[skill_id]
                    # 检查技能ID是否已经包含"_skill"后缀
                    if skill_id.endswith("_skill"):
                        skill_name_key = skill_id
                    else:
                        skill_name_key = f"skill_{skill_id}"
                    skill_name = self.lang.get_text(skill_name_key)
                    cost = skill_node.cost_per_level
                    print(f"{i}. {skill_name} (Lv.{skill_node.current_level}/{skill_node.max_level}) - {self.lang.get_text('skill_points')}: {cost}")
                
                skill_choice = input(f"{self.lang.get_text('enter_choice')}: ").strip()
                
                if skill_choice.isdigit() and 1 <= int(skill_choice) <= len(upgradeable_skills):
                    selected_skill_id = upgradeable_skills[int(skill_choice) - 1]
                    success, remaining_points = self.skill_tree.upgrade_skill(selected_skill_id, self.skill_points)
                    
                    if success:
                        self.skill_points = remaining_points
                        # 如果技能不在hero_skills列表中，则添加
                        if selected_skill_id not in self.hero_skills:
                            self.hero_skills.append(selected_skill_id)
                        # 检查技能ID是否已经包含"_skill"后缀
                        if selected_skill_id.endswith("_skill"):
                            skill_name_key = selected_skill_id
                        else:
                            skill_name_key = f"skill_{selected_skill_id}"
                        skill_name = self.lang.get_text(skill_name_key)
                        print(f"\n{self.lang.get_text('skill_upgrade_success')} - {skill_name}")
                        input(self.lang.get_text('continue_prompt'))
                    else:
                        input(self.lang.get_text("skill_upgrade_failed"))
                else:
                    input(self.lang.get_text("invalid_choice"))
            
            elif choice == "2":
                show_all = not show_all
            
            elif choice == "3":
                break
            
            else:
                input(self.lang.get_text("invalid_choice"))

    def random_event(self):
        """随机事件处理（根据地图类型和难度调整）"""
        # 根据难度获取设置
        settings = self.difficulty_settings[self.difficulty]
        enemy_multiplier = settings["enemy_multiplier"]
        gold_multiplier = settings["gold_multiplier"]

        # 根据地图类型调整事件
        map_info = self.map_types[self.map_type]

        event_num = random.randint(1, 35)
        print(f"\n{self.lang.get_text('step_forward')}")
        time.sleep(1)
        
        # 随机生成新任务（20%概率）
        if random.random() < 0.2:
            new_quest = self.quest_system.generate_random_quest(self.hero_level)
            if new_quest and self.quest_system.add_quest(new_quest):
                quest_desc = self.lang.get_text(new_quest.description_key).format(
                    target=new_quest.target_value,
                    current=new_quest.current_value
                )
                print(f"📜 {self.lang.get_text('new_quest_received')}: {quest_desc}")
                time.sleep(1)

        # 平原地图事件
        if self.map_type == "plains":
            if event_num <= 3:  # 踩到地雷
                damage = random.randint(10, 25)
                actual_damage = max(1, int(damage * enemy_multiplier) - self.hero_defense)
                self.hero_hp -= actual_damage
                print(f"💥 {self.lang.get_text('mine_trap')}{actual_damage}{self.lang.get_text('actual_damage')}")
                # 使用统一的多语言格式化函数处理地雷事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "mine_trap", actual_damage))
                # 记录事件
                self.statistics.record_event_triggered("mine_trap")
                self.show_hero_info()
            elif event_num <= 6:  # 吃到包子
                heal = random.randint(15, 30)
                self.hero_hp = min(self.hero_hp + heal, self.hero_max_hp)
                print(f"🥢 {self.lang.get_text('find_bun')} {heal} {self.lang.get_text('point_hp')}")
                # 使用统一的多语言格式化函数处理包子事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_bun", heal))
                # 记录事件
                self.statistics.record_event_triggered("find_bun")
                self.show_hero_info()
            elif event_num <= 9:  # 遇到怪物
                print("👹 " + self.lang.get_text("encounter_monster"))
                self.statistics.record_event_triggered("combat")
                self.combat_system.combat(enemy_multiplier)
                
                # 更新击杀怪物任务进度
                completed_quests = self.quest_system.update_quest_progress("kill_monster")
                self.handle_quest_completions(completed_quests)
            elif event_num <= 11:  # 发现宝箱
                gold_found = int(random.randint(10, 30) * gold_multiplier)
                self.hero_gold += gold_found
                print(f"💎 {self.lang.get_text('find_chest')} {gold_found} {self.lang.get_text('coins')}")
                # 使用统一的多语言格式化函数处理宝箱事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_chest", gold_found))
                # 记录事件和金币
                self.statistics.record_event_triggered("find_chest")
                self.statistics.record_gold_earned(gold_found)
                
                # 更新收集金币任务进度
                completed_quests = self.quest_system.update_quest_progress("collect_gold", gold_found)
                self.handle_quest_completions(completed_quests)
                
                self.show_hero_info()
            elif event_num <= 15:  # 遇到商人
                self.statistics.record_event_triggered("merchant")
                self.event_system.merchant_event(gold_multiplier)
            elif event_num <= 17:  # 发现药剂
                self.hero_potions += 1
                print("🧪 " + self.lang.get_text("find_potion"))
                # 使用统一的多语言格式化函数处理药剂事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_potion"))
                # 记录事件和药剂
                self.statistics.record_event_triggered("find_potion")
                self.statistics.record_potion_found()
                self.show_hero_info()
            elif event_num <= 19:  # 发现装备
                self.statistics.record_event_triggered("find_equipment")
                self.equipment_system.find_equipment()
            elif event_num <= 21:
                print("🐉 " + self.lang.get_text("encounter_boss"))
                self.statistics.record_event_triggered("boss_combat")
                self.combat_system.boss_combat(enemy_multiplier * 1.5)
            elif event_num <= 23:  # 神秘传送
                self.statistics.record_event_triggered("mysterious_teleport")
                self.event_system.mysterious_teleport()
            elif event_num <= 25:  # 贤者指引
                self.statistics.record_event_triggered("sage_guidance")
                self.event_system.sage_guidance()
            elif event_num <= 27:  # 遭遇强盗
                self.statistics.record_event_triggered("robber_encounter")
                self.event_system.robber_encounter()
            elif event_num <= 29:  # 神秘祭坛
                self.statistics.record_event_triggered("mysterious_altar")
                self.event_system.mysterious_altar()
            elif event_num <= 31:  # 路边营地
                self.statistics.record_event_triggered("roadside_camp")
                self.event_system.roadside_camp()
            else:
                print("✨ " + self.lang.get_text("safe_move"))
                # 使用统一的多语言格式化函数处理平安移动事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "safe_move"))
                self.statistics.record_event_triggered("safe_move")

        # 森林地图事件
        elif self.map_type == "forest":
            if event_num <= 3:
                damage = random.randint(8, 20)
                actual_damage = max(1, int(damage * enemy_multiplier) - self.hero_defense // 2)
                self.hero_hp -= actual_damage
                print(f"🌿 {self.lang.get_text('thorns_damage')}{actual_damage}{self.lang.get_text('point_damage')}")
                # 使用统一的多语言格式化函数处理荆棘伤害事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "thorns_damage", actual_damage))
                self.statistics.record_event_triggered("thorns_damage")
                self.show_hero_info()
            elif event_num <= 6:
                heal = random.randint(20, 35)
                self.hero_hp = min(self.hero_hp + heal, self.hero_max_hp)
                print(f"🌱 {self.lang.get_text('find_herbs')}{heal}{self.lang.get_text('point_hp')}")
                # 使用统一的多语言格式化函数处理草药事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_herbs", heal))
                self.statistics.record_event_triggered("find_herbs")
                self.show_hero_info()
            elif event_num <= 9:
                print("🐺 " + self.lang.get_text("encounter_monster"))
                self.statistics.record_event_triggered("combat")
                self.combat_system.combat(enemy_multiplier)
            elif event_num <= 11:
                gold_found = int(random.randint(15, 35) * gold_multiplier)
                self.hero_gold += gold_found
                print(f"💎 {self.lang.get_text('find_chest')} {gold_found} {self.lang.get_text('coins')}")
                # 使用统一的多语言格式化函数处理宝箱事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_chest", gold_found))
                self.statistics.record_event_triggered("find_chest")
                self.statistics.record_gold_earned(gold_found)
                self.show_hero_info()
            elif event_num <= 13:
                self.statistics.record_event_triggered("merchant")
                self.event_system.merchant_event(gold_multiplier)
            elif event_num <= 15:
                self.statistics.record_event_triggered("find_equipment")
                self.equipment_system.find_equipment()
            elif event_num <= 17:
                print("🐉 " + self.lang.get_text("encounter_boss"))
                self.statistics.record_event_triggered("boss_combat")
                self.combat_system.boss_combat(enemy_multiplier * 1.5)
            elif event_num <= 19:
                self.hero_potions += 1
                print("🧪 " + self.lang.get_text("find_potion"))
                # 使用统一的多语言格式化函数处理药剂事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_potion"))
                self.statistics.record_event_triggered("find_potion")
                self.statistics.record_potion_found()
                self.show_hero_info()
            elif event_num <= 21:  # 神秘传送
                self.statistics.record_event_triggered("mysterious_teleport")
                self.event_system.mysterious_teleport()
            elif event_num <= 23:  # 贤者指引
                self.statistics.record_event_triggered("sage_guidance")
                self.event_system.sage_guidance()
            elif event_num <= 25:  # 遭遇强盗
                self.statistics.record_event_triggered("robber_encounter")
                self.event_system.robber_encounter()
            elif event_num <= 27:  # 路边营地
                self.statistics.record_event_triggered("roadside_camp")
                self.event_system.roadside_camp()
            else:
                print("✨ " + self.lang.get_text("safe_move"))
                # 使用统一的多语言格式化函数处理平安移动事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "safe_move"))
                self.statistics.record_event_triggered("safe_move")

        # 沙漠地图事件
        elif self.map_type == "desert":
            if event_num <= 3:
                damage = random.randint(12, 28)
                actual_damage = max(1, int(damage * enemy_multiplier * 1.2))
                self.hero_hp -= actual_damage
                print(f"☀️ {self.lang.get_text('dehydration')}{actual_damage}{self.lang.get_text('point_damage')}")
                # 使用统一的多语言格式化函数处理脱水事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "dehydration", actual_damage))
                self.statistics.record_event_triggered("dehydration")
                self.show_hero_info()
            elif event_num <= 6:
                heal = random.randint(25, 40)
                self.hero_hp = min(self.hero_hp + heal, self.hero_max_hp)
                print(f"💧 {self.lang.get_text('find_oasis')}{heal}{self.lang.get_text('point_hp')}")
                # 使用统一的多语言格式化函数处理绿洲事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_oasis", heal))
                self.statistics.record_event_triggered("find_oasis")
                self.show_hero_info()
            elif event_num <= 9:
                print("🦂 " + self.lang.get_text("encounter_monster"))
                self.statistics.record_event_triggered("combat")
                self.combat_system.combat(enemy_multiplier * 1.1)
            elif event_num <= 11:
                gold_found = int(random.randint(20, 40) * gold_multiplier)
                self.hero_gold += gold_found
                print(f"💎 {self.lang.get_text('find_chest')} {gold_found} {self.lang.get_text('coins')}")
                # 使用统一的多语言格式化函数处理宝箱事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_chest", gold_found))
                self.statistics.record_event_triggered("find_chest")
                self.statistics.record_gold_earned(gold_found)
                self.show_hero_info()
            elif event_num <= 13:
                self.statistics.record_event_triggered("merchant")
                self.event_system.merchant_event(gold_multiplier)
            elif event_num <= 15:
                self.statistics.record_event_triggered("find_equipment")
                self.equipment_system.find_equipment()
            elif event_num <= 17:
                print("🐉 " + self.lang.get_text("encounter_boss"))
                self.statistics.record_event_triggered("boss_combat")
                self.combat_system.boss_combat(enemy_multiplier * 1.6)
            elif event_num <= 19:
                self.hero_potions += 1
                print("🧪 " + self.lang.get_text("find_potion"))
                # 使用统一的多语言格式化函数处理药剂事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_potion"))
                self.statistics.record_event_triggered("find_potion")
                self.statistics.record_potion_found()
                self.show_hero_info()
            elif event_num <= 21:  # 神秘传送
                self.statistics.record_event_triggered("mysterious_teleport")
                self.event_system.mysterious_teleport()
            elif event_num <= 23:  # 贤者指引
                self.statistics.record_event_triggered("sage_guidance")
                self.event_system.sage_guidance()
            elif event_num <= 25:  # 遭遇强盗
                self.statistics.record_event_triggered("robber_encounter")
                self.event_system.robber_encounter()
            elif event_num <= 27:  # 路边营地
                self.statistics.record_event_triggered("roadside_camp")
                self.event_system.roadside_camp()
            else:
                print("✨ " + self.lang.get_text("safe_move"))
                # 使用统一的多语言格式化函数处理平安移动事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "safe_move"))
                self.statistics.record_event_triggered("safe_move")

        # 地牢地图事件
        elif self.map_type == "dungeon":
            if event_num <= 3:
                damage = random.randint(15, 30)
                actual_damage = max(1, int(damage * enemy_multiplier * 1.3) - self.hero_defense // 2)
                self.hero_hp -= actual_damage
                print(f"🕳️ {self.lang.get_text('dungeon_trap')}{actual_damage}{self.lang.get_text('point_damage')}")
                # 使用统一的多语言格式化函数处理地牢陷阱事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "dungeon_trap", actual_damage))
                self.statistics.record_event_triggered("dungeon_trap")
                self.show_hero_info()
            elif event_num <= 5:
                print("👻 " + self.lang.get_text("encounter_ghost"))
                self.statistics.record_event_triggered("ghost_combat")
                self.combat_system.ghost_combat(enemy_multiplier)
            elif event_num <= 8:
                print("💀 " + self.lang.get_text("encounter_monster"))
                self.statistics.record_event_triggered("combat")
                self.combat_system.combat(enemy_multiplier * 1.2)
            elif event_num <= 11:
                gold_found = int(random.randint(25, 50) * gold_multiplier)
                self.hero_gold += gold_found
                print(f"💎 {self.lang.get_text('find_chest')} {gold_found} {self.lang.get_text('coins')}")
                # 使用统一的多语言格式化函数处理宝箱事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_chest", gold_found))
                self.statistics.record_event_triggered("find_chest")
                self.statistics.record_gold_earned(gold_found)
                self.show_hero_info()
            elif event_num <= 13:
                self.statistics.record_event_triggered("find_equipment")
                self.equipment_system.find_equipment()
            elif event_num <= 15:
                self.statistics.record_event_triggered("mysterious_merchant")
                self.event_system.mysterious_merchant(gold_multiplier)
            elif event_num <= 17:
                print("🐉 " + self.lang.get_text("encounter_boss"))
                self.statistics.record_event_triggered("boss_combat")
                self.combat_system.boss_combat(enemy_multiplier * 1.7)
            elif event_num <= 19:  # 神秘传送
                self.statistics.record_event_triggered("mysterious_teleport")
                self.event_system.mysterious_teleport()
            elif event_num <= 21:  # 贤者指引
                self.statistics.record_event_triggered("sage_guidance")
                self.event_system.sage_guidance()
            elif event_num <= 23:  # 遭遇强盗
                self.statistics.record_event_triggered("robber_encounter")
                self.event_system.robber_encounter()
            elif event_num <= 25:  # 路边营地
                self.statistics.record_event_triggered("roadside_camp")
                self.event_system.roadside_camp()
            else:
                print("✨ " + self.lang.get_text("safe_move"))
                # 使用统一的多语言格式化函数处理平安移动事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "safe_move"))
                self.statistics.record_event_triggered("safe_move")

        # 山脉地图事件
        elif self.map_type == "mountain":
            if event_num <= 3:
                damage = random.randint(18, 35)
                actual_damage = max(1, int(damage * enemy_multiplier * 1.4) - self.hero_defense)
                self.hero_hp -= actual_damage
                print(f"🪨 {self.lang.get_text('mountain_hazard')}{actual_damage}{self.lang.get_text('point_damage')}")
                # 使用统一的多语言格式化函数处理山体危险事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "mountain_hazard", actual_damage))
                self.statistics.record_event_triggered("mountain_hazard")
                self.show_hero_info()
            elif event_num <= 6:
                gold_found = int(random.randint(40, 80) * gold_multiplier)
                self.hero_gold += gold_found
                print(f"💎 {self.lang.get_text('find_gem')}{gold_found}{self.lang.get_text('gold_coins')}")
                # 使用统一的多语言格式化函数处理宝石事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_gem", gold_found))
                self.statistics.record_event_triggered("find_gem")
                self.statistics.record_gold_earned(gold_found)
                self.show_hero_info()
            elif event_num <= 9:
                print("🐲 " + self.lang.get_text("encounter_monster"))
                self.statistics.record_event_triggered("combat")
                self.combat_system.combat(enemy_multiplier * 1.3)
            elif event_num <= 11:
                print("🐲 " + self.lang.get_text("encounter_boss"))
                self.statistics.record_event_triggered("boss_combat")
                self.combat_system.boss_combat(enemy_multiplier * 1.8)
            elif event_num <= 13:
                self.statistics.record_event_triggered("find_equipment")
                self.equipment_system.find_equipment()
            elif event_num <= 15:
                self.statistics.record_event_triggered("mysterious_merchant")
                self.event_system.mysterious_merchant(gold_multiplier)
            elif event_num <= 17:  # 神秘传送
                self.statistics.record_event_triggered("mysterious_teleport")
                self.event_system.mysterious_teleport()
            elif event_num <= 19:  # 贤者指引
                self.statistics.record_event_triggered("sage_guidance")
                self.event_system.sage_guidance()
            elif event_num <= 21:  # 遭遇强盗
                self.statistics.record_event_triggered("robber_encounter")
                self.event_system.robber_encounter()
            elif event_num <= 23:  # 路边营地
                self.statistics.record_event_triggered("roadside_camp")
                self.event_system.roadside_camp()
            else:
                print("✨ " + self.lang.get_text("safe_move"))
                # 使用统一的多语言格式化函数处理平安移动事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "safe_move"))
                self.statistics.record_event_triggered("safe_move")

        # 沼泽地图事件
        elif self.map_type == "swamp":
            if event_num <= 3:  # 中毒云
                damage = random.randint(10, 20)
                actual_damage = max(1, int(damage * enemy_multiplier * 1.2))
                self.hero_hp -= actual_damage
                print(f"☠️ {self.lang.get_text('poison_cloud')}{actual_damage}{self.lang.get_text('point_damage')}")
                # 添加中毒状态效果，持续3回合
                self.add_status_effect("poison", 3)
                self.events_encountered.append(self.lang.format_text("event_text", "poison_cloud", actual_damage))
                self.statistics.record_event_triggered("poison_cloud")
                self.show_hero_info()
            elif event_num <= 6:  # 流沙
                damage = int(self.hero_hp * 0.15)  # 当前血量的15%
                actual_damage = max(5, damage)  # 最少损失5点
                self.hero_hp -= actual_damage
                print(f"🏖️ {self.lang.get_text('quicksand')}{actual_damage}{self.lang.get_text('point_damage')}")
                self.events_encountered.append(self.lang.format_text("event_text", "quicksand", actual_damage))
                self.statistics.record_event_triggered("quicksand")
                self.show_hero_info()
            elif event_num <= 9:
                print("🐊 " + self.lang.get_text("encounter_monster"))
                self.statistics.record_event_triggered("combat")
                self.combat_system.combat(enemy_multiplier * 1.1)
            elif event_num <= 11:
                heal = random.randint(30, 50)
                self.hero_hp = min(self.hero_hp + heal, self.hero_max_hp)
                print(f"🌿 {self.lang.get_text('rare_herbs')}{heal}{self.lang.get_text('point_hp')}")
                self.events_encountered.append(self.lang.format_text("event_text", "rare_herbs", heal))
                self.statistics.record_event_triggered("rare_herbs")
                self.show_hero_info()
            elif event_num <= 13:
                gold_found = int(random.randint(15, 35) * gold_multiplier)
                self.hero_gold += gold_found
                print(f"💎 {self.lang.get_text('find_chest')} {gold_found} {self.lang.get_text('coins')}")
                self.events_encountered.append(self.lang.format_text("event_text", "find_chest", gold_found))
                self.statistics.record_event_triggered("find_chest")
                self.statistics.record_gold_earned(gold_found)
                self.show_hero_info()
            elif event_num <= 15:
                self.statistics.record_event_triggered("swamp_merchant")
                self.event_system.swamp_merchant_event(gold_multiplier)
            elif event_num <= 17:
                print("🐲 " + self.lang.get_text("encounter_boss"))
                self.statistics.record_event_triggered("boss_combat")
                self.combat_system.boss_combat(enemy_multiplier * 1.6)
            elif event_num <= 19:  # 贤者指引
                self.statistics.record_event_triggered("sage_guidance")
                self.event_system.sage_guidance()
            elif event_num <= 21:  # 神秘祭坛
                self.statistics.record_event_triggered("mysterious_altar")
                self.event_system.mysterious_altar()
            elif event_num <= 23:  # 路边营地
                self.statistics.record_event_triggered("roadside_camp")
                self.event_system.roadside_camp()
            else:
                print("✨ " + self.lang.get_text("safe_move"))
                self.events_encountered.append(self.lang.format_text("event_text", "safe_move"))
                self.statistics.record_event_triggered("safe_move")

        # 雪地地图事件
        elif self.map_type == "snowfield":
            if event_num <= 3:  # 冻伤
                print(f"❄️ {self.lang.get_text('frostbite')}")
                # 添加冻伤状态效果，持续3回合
                self.add_status_effect("frostbite", 3)
                self.events_encountered.append(self.lang.format_text("event_text", "frostbite"))
                self.statistics.record_event_triggered("frostbite")
                self.show_hero_info()
            elif event_num <= 6:  # 雪崩
                damage = random.randint(20, 40)
                actual_damage = max(1, int(damage * enemy_multiplier * 1.3))
                self.hero_hp -= actual_damage
                print(f"🏔️ {self.lang.get_text('avalanche')}{actual_damage}{self.lang.get_text('point_damage')}")
                
                # 有概率发现稀有装备
                if random.random() < 0.3:  # 30%概率
                    print(f"🎁 {self.lang.get_text('avalanche_loot')}")
                    self.equipment_system.find_equipment(rarity_bonus=1)  # 提升稀有度
                
                self.events_encountered.append(self.lang.format_text("event_text", "avalanche", actual_damage))
                self.statistics.record_event_triggered("avalanche")
                self.show_hero_info()
            elif event_num <= 9:
                print("🐺 " + self.lang.get_text("encounter_monster"))
                self.statistics.record_event_triggered("combat")
                self.combat_system.combat(enemy_multiplier * 1.15)
            elif event_num <= 11:
                heal = random.randint(40, 60)
                self.hero_hp = min(self.hero_hp + heal, self.hero_max_hp)
                print(f"🧊 {self.lang.get_text('ice_cave')}{heal}{self.lang.get_text('point_hp')}")
                self.events_encountered.append(self.lang.format_text("event_text", "ice_cave", heal))
                self.statistics.record_event_triggered("ice_cave")
                self.show_hero_info()
            elif event_num <= 13:
                gold_found = int(random.randint(20, 40) * gold_multiplier)
                self.hero_gold += gold_found
                print(f"💎 {self.lang.get_text('find_chest')} {gold_found} {self.lang.get_text('coins')}")
                self.events_encountered.append(self.lang.format_text("event_text", "find_chest", gold_found))
                self.statistics.record_event_triggered("find_chest")
                self.statistics.record_gold_earned(gold_found)
                self.show_hero_info()
            elif event_num <= 15:
                print(f"❄️ {self.lang.get_text('frost_effect')}")
                # 添加冰霜状态效果，持续3回合
                self.add_status_effect("frost", 3)
                self.events_encountered.append(self.lang.format_text("event_text", "frost_effect"))
                self.statistics.record_event_triggered("frost_effect")
                self.show_hero_info()
            elif event_num <= 17:
                print("🐲 " + self.lang.get_text("encounter_boss"))
                self.statistics.record_event_triggered("boss_combat")
                self.combat_system.boss_combat(enemy_multiplier * 1.65)
            elif event_num <= 19:  # 神秘传送
                self.statistics.record_event_triggered("mysterious_teleport")
                self.event_system.mysterious_teleport()
            elif event_num <= 21:  # 贤者指引
                self.statistics.record_event_triggered("sage_guidance")
                self.event_system.sage_guidance()
            elif event_num <= 23:  # 神秘祭坛
                self.statistics.record_event_triggered("mysterious_altar")
                self.event_system.mysterious_altar()
            else:
                print("✨ " + self.lang.get_text("safe_move"))
                self.events_encountered.append(self.lang.format_text("event_text", "safe_move"))
                self.statistics.record_event_triggered("safe_move")

    def update_attributes(self):
        """更新英雄属性（基础属性 + 装备加成 + 特殊效果）"""
        self.hero_attack = self.base_attack
        self.hero_defense = self.base_defense
        self.hero_max_hp = self.base_max_hp
        
        # 重置特殊效果属性
        self.special_effects = {
            "crit_rate": 0.0,      # 暴击率
            "lifesteal_rate": 0.0, # 吸血率
            "dodge_rate": 0.0,     # 闪避率
            "counter_attack_rate": 0.0, # 反击率
            "ice_damage": 0,       # 冰霜伤害
            "fire_damage": 0,      # 火焰伤害
            "healing_rate": 0.0,   # 治疗效果
            "mana_boost": 0,       # 法力提升
            "backstab_damage": 0.0, # 背刺伤害
            "luck_bonus": 0.0,     # 幸运加成
            "wisdom_bonus": 0.0,   # 智慧加成
            "immortality_chance": 0.0, # 不死概率
            "health_regeneration": 0, # 生命恢复
            "mana_regeneration": 0,   # 法力恢复
            "holy_resistance": 0.0,   # 神圣抗性
            "fire_resistance": 0.0,   # 火焰抗性
            "stealth_chance": 0.0,    # 潜行概率
            "evasion_rate": 0.0,      # 闪避率
            "spell_power": 0.0,       # 法术强度
            "crit_damage": 0.0        # 暴击伤害
        }

        # 添加装备加成和特殊效果
        equipped_items = []
        for item in self.equipment.values():
            if item:
                equipped_items.append(item)
                self.hero_attack += item.get("attack", 0)
                self.hero_defense += item.get("defense", 0)
                self.hero_max_hp += item.get("hp", 0)
                
                # 处理特殊效果
                special_effects = item.get("special_effects", [])
                special_effects_values = item.get("special_effects_values", {})
                
                for effect in special_effects:
                    if effect in special_effects_values:
                        self.special_effects[effect] += special_effects_values[effect]
                    elif effect in self.special_effects:
                        # 默认效果值
                        default_values = {
                            "crit_rate": 0.05,
                            "lifesteal_rate": 0.1,
                            "dodge_rate": 0.05,
                            "counter_attack_rate": 0.1,
                            "ice_damage": 5,
                            "fire_damage": 5,
                            "healing_rate": 0.02,
                            "mana_boost": 10,
                            "backstab_damage": 0.2,
                            "luck_bonus": 0.05,
                            "wisdom_bonus": 0.05,
                            "immortality_chance": 0.02,
                            "health_regeneration": 2,
                            "mana_regeneration": 2,
                            "holy_resistance": 0.1,
                            "fire_resistance": 0.1,
                            "stealth_chance": 0.1,
                            "evasion_rate": 0.05,
                            "spell_power": 0.1,
                            "crit_damage": 0.2
                        }
                        if effect in default_values:
                            self.special_effects[effect] += default_values[effect]

        # 应用套装效果
        self.apply_set_bonuses(equipped_items)

        # 确保HP不超过最大值
        if self.hero_hp > self.hero_max_hp:
            self.hero_hp = self.hero_max_hp
    
    def apply_set_bonuses(self, equipped_items):
        """应用套装效果"""
        from hero.game_config import EQUIPMENT_SETS
        
        for set_name, set_info in EQUIPMENT_SETS.items():
            required_pieces = set_info["pieces"]
            equipped_pieces = []
            
            # 检查是否装备了该套装的所有部件
            for item in equipped_items:
                if item["type"] in required_pieces and item.get("set_bonus") == set_name:
                    equipped_pieces.append(item["type"])
            
            # 检查是否满足套装要求（必须装备该套装的所有部件）
            if len(equipped_pieces) == len(required_pieces):
                # 应用2件套效果
                if "2_piece" in set_info["effects"]:
                    effect = set_info["effects"]["2_piece"]
                    
                    # 应用属性加成
                    if "attack_bonus" in effect:
                        self.hero_attack += effect["attack_bonus"]
                    if "defense_bonus" in effect:
                        self.hero_defense += effect["defense_bonus"]
                    if "hp_bonus" in effect:
                        self.hero_max_hp += effect.get("hp_bonus", 0)
                    if "mana_bonus" in effect:
                        self.special_effects["mana_boost"] += effect.get("mana_bonus", 0)
                    if "spell_power" in effect:
                        self.special_effects["spell_power"] += effect.get("spell_power", 0)
                    if "crit_rate" in effect:
                        self.special_effects["crit_rate"] += effect.get("crit_rate", 0)
                    if "dodge_rate" in effect:
                        self.special_effects["dodge_rate"] += effect.get("dodge_rate", 0)
                    
                    # 显示套装激活信息
                    set_name_key = set_info["name_key"]
                    bonus_name_key = effect["name_key"]
                    print(f"✨ {self.lang.get_text('set_bonus_activated')} {self.lang.get_text(set_name_key)}: {self.lang.get_text(bonus_name_key)}")
                    
                    # 标记套装效果已激活
                    for item in equipped_items:
                        if item["type"] in required_pieces and item.get("set_bonus") == set_name:
                            item["set_bonus_active"] = True
    
    def apply_status_effects(self):
        """应用状态效果对属性的影响"""
        # 冻伤效果：攻击力降低10%
        if self.status_effects["frostbite"] > 0:
            self.hero_attack = int(self.hero_attack * 0.9)
        
        # 冰霜效果：防御力降低10%
        if self.status_effects["frost"] > 0:
            self.hero_defense = int(self.hero_defense * 0.9)
    
    def update_status_effects(self):
        """更新状态效果（每回合结束时调用）"""
        # 中毒效果：每回合损失5点血量
        if self.status_effects["poison"] > 0:
            poison_damage = 5
            self.hero_hp -= poison_damage
            print(f"☠️ {self.lang.get_text('poison_damage')} {poison_damage}{self.lang.get_text('point_damage')}")
            self.status_effects["poison"] -= 1
            if self.status_effects["poison"] <= 0:
                print(f"✅ {self.lang.get_text('poison_cured')}")
        
        # 减少状态效果回合数
        if self.status_effects["frostbite"] > 0:
            self.status_effects["frostbite"] -= 1
            if self.status_effects["frostbite"] <= 0:
                print(f"✅ {self.lang.get_text('poison_cured')}")
        
        if self.status_effects["frost"] > 0:
            self.status_effects["frost"] -= 1
            if self.status_effects["frost"] <= 0:
                print(f"✅ {self.lang.get_text('poison_cured')}")
    
    def add_status_effect(self, effect_type, duration):
        """添加状态效果
        
        Args:
            effect_type (str): 状态效果类型 ("poison", "frostbite", "frost")
            duration (int): 持续回合数
        """
        if effect_type in self.status_effects:
            self.status_effects[effect_type] = duration
            print(f"⚠️ {self.lang.get_text(f'status_{effect_type}')}! {self.lang.get_text('status_duration')}: {duration}")
    
    def get_active_status_effects(self):
        """获取当前活跃的状态效果
        
        Returns:
            list: 活跃状态效果列表
        """
        active_effects = []
        for effect, duration in self.status_effects.items():
            if duration > 0:
                active_effects.append((effect, duration))
        return active_effects
    
    def handle_quest_completions(self, completed_quests):
        """处理完成的任务，给予奖励并显示消息"""
        for quest in completed_quests:
            reward_gold, reward_exp = self.quest_system.get_quest_rewards(quest)
            self.hero_gold += reward_gold
            self.hero_exp += reward_exp
            
            print(f"🎉 {self.lang.get_text('quest_completed')}")
            print(f"💰 {self.lang.get_text('quest_reward_received').format(gold=reward_gold, exp=reward_exp)}")
            
            # 检查是否升级
            self.combat_system.check_level_up()

    def get_save_data(self):
        """
        获取当前游戏的存档数据

        Returns:
            SaveData: 包含所有游戏状态的存档数据实例
        """
        return SaveData(self)

    def load_from_save_data(self, save_data):
        """
        从存档数据加载游戏状态

        Args:
            save_data: SaveData实例
        """
        # 英雄基础属性
        self.hero_name = save_data.hero_name
        self.hero_class = save_data.hero_class
        self.hero_level = save_data.hero_level
        self.hero_exp = save_data.hero_exp

        # 英雄当前状态
        self.hero_hp = save_data.hero_hp
        self.hero_max_hp = save_data.hero_max_hp
        self.hero_attack = save_data.hero_attack
        self.hero_defense = save_data.hero_defense

        # 基础属性
        self.base_attack = save_data.base_attack
        self.base_defense = save_data.base_defense
        self.base_max_hp = save_data.base_max_hp

        # 游戏进度
        self.hero_position = save_data.hero_position
        self.game_over = save_data.game_over
        self.victory = save_data.victory

        # 资源
        self.hero_gold = save_data.hero_gold
        self.hero_potions = save_data.hero_potions

        # 技能系统
        self.skill_points = save_data.skill_points
        
        # 装备和背包
        self.equipment = save_data.equipment
        self.inventory = save_data.inventory

        # 技能
        self.hero_skills = save_data.hero_skills
        
        # 恢复技能树
        if save_data.skill_tree_data:
            self.skill_tree = SkillTree.from_dict(save_data.skill_tree_data, self.lang)
        else:
            self.skill_tree = SkillTree(self.hero_class, self.lang)

        # 游戏设置
        self.difficulty = save_data.difficulty
        self.map_type = save_data.map_type
        self.language = save_data.language
        self.map_length = save_data.map_length
        
        # 重新初始化游戏配置（重要！）
        self.difficulty_settings = DIFFICULTY_SETTINGS
        self.map_types = MAP_TYPES

        # 更新语言设置
        self.lang.set_language(self.language)

        # 统计数据
        self.monsters_defeated = save_data.monsters_defeated
        self.events_encountered = save_data.events_encountered
        self.visited_positions = save_data.visited_positions

        # 重新初始化子系统（确保它们引用正确的游戏实例）
        self.combat_system = CombatSystem(self)
        self.equipment_system = EquipmentSystem(self)
        self.event_system = EventSystem(self)
        self.newbie_village = NewbieVillage(self)

        # 加载技能状态
        self.shield_active = getattr(save_data, 'shield_active', False)
        self.berserk_turns = getattr(save_data, 'berserk_turns', 0)
        self.focus_active = getattr(save_data, 'focus_active', False)
        
        # 加载职业系统相关属性
        self.class_mana = getattr(save_data, 'class_mana', 0)
        self.class_max_mana = getattr(save_data, 'class_max_mana', 0)
        
        # 加载统计数据
        if hasattr(save_data, 'statistics_data') and save_data.statistics_data:
            self.statistics = GameStatistics.from_dict(save_data.statistics_data)
        else:
            self.statistics = GameStatistics()
        
        # 加载状态效果
        if hasattr(save_data, 'status_effects') and save_data.status_effects:
            self.status_effects = save_data.status_effects
        else:
            self.status_effects = {
                "poison": 0,
                "frostbite": 0,
                "frost": 0
            }
        
        # 加载任务系统
        if hasattr(save_data, 'quest_data') and save_data.quest_data:
            self.quest_system.from_dict(save_data.quest_data)
        else:
            self.quest_system = QuestSystem()

    def show_quests(self):
        """显示当前任务列表"""
        self.clear_screen()
        print(self.lang.get_text("block_separator"))
        print(f"          {self.lang.get_text('quests_menu')}")
        print(self.lang.get_text("block_separator"))
        print()
        
        # 显示当前任务
        quests_list = self.quest_system.format_quests_list(self.lang)
        print(quests_list)
        
        # 显示已完成任务数量
        completed_count = len(self.quest_system.completed_quests)
        print(f"\n{self.lang.get_text('completed_quests')}: {completed_count}")
        
        input(f"\n{self.lang.get_text('continue_prompt')}")

    def restart_game(self):
        """重新开始游戏"""
        print()
        choice = input(self.lang.get_text("restart_prompt") + " (y/n): ").strip().lower()
        confirm = choice in self.lang.get_text("yes_options")

        if confirm:
            # 重新初始化游戏
            self.__init__()
            self.start_game()
        else:
            print("\n" + self.lang.get_text("goodbye"))
            sys.exit(0)


def main():
    """主函数"""
    game = HeroGame()
    game.start_game()


if __name__ == "__main__":
    main()
