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
from language import LanguageSupport
from game_config import DIFFICULTY_SETTINGS, MAP_TYPES
from combat import CombatSystem
from equipment import EquipmentSystem
from events import EventSystem
from newbie_village import NewbieVillage
from save_data import SaveData, SaveManager
from statistics import GameStatistics


class HeroGame:
    """英雄无敌游戏主类"""

    def __init__(self):
        """初始化游戏"""
        self.language = "zh"  # 默认中文
        self.lang = LanguageSupport(self.language)

        # 先选择语言
        self.select_language()

        # 选择地图类型和难度
        self.select_map_and_difficulty()

        # 初始化英雄属性
        self.hero_name = ""
        self.hero_hp = 100  # 初始血量
        self.hero_max_hp = 100  # 最大血量
        self.hero_attack = 20  # 初始攻击力
        self.hero_defense = 5  # 初始防御力
        self.hero_position = 0  # 当前位置
        self.hero_exp = 0  # 经验值
        self.hero_level = 1  # 等级
        self.hero_skills = []  # 英雄技能
        self.game_over = False
        self.victory = False
        self.monsters_defeated = 0  # 击败的怪物数量
        self.events_encountered = []  # 遇到的事件历史

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

        # 初始化子系统
        self.combat_system = CombatSystem(self)
        self.equipment_system = EquipmentSystem(self)
        self.event_system = EventSystem(self)
        self.newbie_village = NewbieVillage(self)

        # 初始化统计系统
        self.statistics = GameStatistics()

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

    def show_hero_info(self):
        """显示英雄信息"""
        print(f"\n【{self.hero_name}】 Lv.{self.hero_level}")
        print(f"❤️  {self.lang.get_text('hp')}{self.lang.get_text('item_separator')}{self.hero_hp}/{self.hero_max_hp}")
        print(f"⚔️  {self.lang.get_text('attack')}{self.lang.get_text('item_separator')}{self.hero_attack}")
        print(f"🛡️  {self.lang.get_text('defense')}{self.lang.get_text('item_separator')}{self.hero_defense}")
        print(f"💰  {self.lang.get_text('gold')}{self.lang.get_text('item_separator')}{self.hero_gold}")
        print(f"⭐  {self.lang.get_text('exp')}{self.lang.get_text('item_separator')}{self.hero_exp}")
        print(f"🧪  {self.lang.get_text('potions')}{self.lang.get_text('item_separator')}{self.hero_potions}")
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

        # 显示技能
        if self.hero_skills:
            print(f"🔥  {self.lang.get_text('skills')}{self.lang.get_text('item_separator')}{', '.join(self.hero_skills)}")
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
            print(f"4. {self.lang.get_text('exit_game')}")
            print()

            choice = input(f"{self.lang.get_text('enter_choice')} (1): ").strip()

            if choice == "" or choice == "1":
                # 新游戏
                self.get_hero_name()
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
        print(f"7. {self.lang.get_text('save_and_exit')}")

        while True:
            choice = input(f"{self.lang.get_text('enter_choice')} (1): ").strip()

            if choice == "" or choice == "1":
                if self.hero_position < self.map_length - 1:
                    self.hero_position += 1
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
            elif choice == "5":
                self.event_system.merchant_event()
            elif choice == "6":
                self.equipment_system.equipment_management()
            elif choice == "7":
                self.save_game_menu()
            else:
                print(self.lang.get_text("invalid_choice"))

    def random_event(self):
        """随机事件处理（根据地图类型和难度调整）"""
        # 根据难度获取设置
        settings = self.difficulty_settings[self.difficulty]
        enemy_multiplier = settings["enemy_multiplier"]
        gold_multiplier = settings["gold_multiplier"]

        # 根据地图类型调整事件
        map_info = self.map_types[self.map_type]

        event_num = random.randint(1, 30)
        print(f"\n{self.lang.get_text('step_forward')}")
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
                self.show_hero_info()
            elif event_num <= 6:  # 吃到包子
                heal = random.randint(15, 30)
                self.hero_hp = min(self.hero_hp + heal, self.hero_max_hp)
                print(f"🥢 {self.lang.get_text('find_bun')} {heal} {self.lang.get_text('point_hp')}")
                # 使用统一的多语言格式化函数处理包子事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_bun", heal))
                self.show_hero_info()
            elif event_num <= 9:  # 遇到怪物
                print("👹 " + self.lang.get_text("encounter_monster"))
                self.combat_system.combat(enemy_multiplier)
            elif event_num <= 11:  # 发现宝箱
                gold_found = int(random.randint(10, 30) * gold_multiplier)
                self.hero_gold += gold_found
                print(f"💎 {self.lang.get_text('find_chest')} {gold_found} {self.lang.get_text('coins')}")
                # 使用统一的多语言格式化函数处理宝箱事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_chest", gold_found))
                self.show_hero_info()
            elif event_num <= 13:  # 遇到商人
                self.event_system.merchant_event(gold_multiplier)
            elif event_num <= 15:  # 获得技能
                self.event_system.learn_skill()
            elif event_num <= 17:  # 发现药剂
                self.hero_potions += 1
                print("🧪 " + self.lang.get_text("find_potion"))
                # 使用统一的多语言格式化函数处理药剂事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_potion"))
                self.show_hero_info()
            elif event_num <= 19:  # 发现装备
                self.equipment_system.find_equipment()
            elif event_num <= 21:  # 遇到强敌
                print("🐉 " + self.lang.get_text("encounter_boss"))
                self.combat_system.boss_combat(enemy_multiplier)
            else:
                print("✨ " + self.lang.get_text("safe_move"))
                # 使用统一的多语言格式化函数处理平安移动事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "safe_move"))

        # 森林地图事件
        elif self.map_type == "forest":
            if event_num <= 3:
                damage = random.randint(8, 20)
                actual_damage = max(1, int(damage * enemy_multiplier) - self.hero_defense // 2)
                self.hero_hp -= actual_damage
                print(f"🌿 {self.lang.get_text('thorns_damage')}{actual_damage}{self.lang.get_text('point_damage')}")
                # 使用统一的多语言格式化函数处理荆棘伤害事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "thorns_damage", actual_damage))
                self.show_hero_info()
            elif event_num <= 6:
                heal = random.randint(20, 35)
                self.hero_hp = min(self.hero_hp + heal, self.hero_max_hp)
                print(f"🌱 {self.lang.get_text('find_herbs')}{heal}{self.lang.get_text('point_hp')}")
                # 使用统一的多语言格式化函数处理草药事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_herbs", heal))
                self.show_hero_info()
            elif event_num <= 9:
                print("🐺 " + self.lang.get_text("encounter_monster"))
                self.combat_system.combat(enemy_multiplier)
            elif event_num <= 11:
                gold_found = int(random.randint(15, 35) * gold_multiplier)
                self.hero_gold += gold_found
                print(f"💎 {self.lang.get_text('find_chest')} {gold_found} {self.lang.get_text('coins')}")
                # 使用统一的多语言格式化函数处理宝箱事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_chest", gold_found))
                self.show_hero_info()
            elif event_num <= 13:
                self.event_system.merchant_event(gold_multiplier)
            elif event_num <= 15:
                self.equipment_system.find_equipment()
            elif event_num <= 17:
                print("🐉 " + self.lang.get_text("encounter_boss"))
                self.combat_system.boss_combat(enemy_multiplier)
            elif event_num <= 19:
                self.hero_potions += 1
                print("🧪 " + self.lang.get_text("find_potion"))
                # 使用统一的多语言格式化函数处理药剂事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_potion"))
                self.show_hero_info()
            else:
                print("✨ " + self.lang.get_text("safe_move"))
                # 使用统一的多语言格式化函数处理平安移动事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "safe_move"))

        # 沙漠地图事件
        elif self.map_type == "desert":
            if event_num <= 3:
                damage = random.randint(12, 28)
                actual_damage = max(1, int(damage * enemy_multiplier * 1.2))
                self.hero_hp -= actual_damage
                print(f"☀️ {self.lang.get_text('dehydration')}{actual_damage}{self.lang.get_text('point_damage')}")
                # 使用统一的多语言格式化函数处理脱水事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "dehydration", actual_damage))
                self.show_hero_info()
            elif event_num <= 6:
                heal = random.randint(25, 40)
                self.hero_hp = min(self.hero_hp + heal, self.hero_max_hp)
                print(f"💧 {self.lang.get_text('find_oasis')}{heal}{self.lang.get_text('point_hp')}")
                # 使用统一的多语言格式化函数处理绿洲事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_oasis", heal))
                self.show_hero_info()
            elif event_num <= 9:
                print("🦂 " + self.lang.get_text("encounter_monster"))
                self.combat_system.combat(enemy_multiplier * 1.1)
            elif event_num <= 11:
                gold_found = int(random.randint(20, 40) * gold_multiplier)
                self.hero_gold += gold_found
                print(f"💎 {self.lang.get_text('find_chest')} {gold_found} {self.lang.get_text('coins')}")
                # 使用统一的多语言格式化函数处理宝箱事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_chest", gold_found))
                self.show_hero_info()
            elif event_num <= 13:
                self.event_system.merchant_event(gold_multiplier)
            elif event_num <= 15:
                self.equipment_system.find_equipment()
            elif event_num <= 17:
                print("🐉 " + self.lang.get_text("encounter_boss"))
                self.combat_system.boss_combat(enemy_multiplier * 1.1)
            elif event_num <= 19:
                self.hero_potions += 1
                print("🧪 " + self.lang.get_text("find_potion"))
                # 使用统一的多语言格式化函数处理药剂事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_potion"))
                self.show_hero_info()
            else:
                print("✨ " + self.lang.get_text("safe_move"))
                # 使用统一的多语言格式化函数处理平安移动事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "safe_move"))

        # 地牢地图事件
        elif self.map_type == "dungeon":
            if event_num <= 3:
                damage = random.randint(15, 30)
                actual_damage = max(1, int(damage * enemy_multiplier * 1.3) - self.hero_defense // 2)
                self.hero_hp -= actual_damage
                print(f"🕳️ {self.lang.get_text('dungeon_trap')}{actual_damage}{self.lang.get_text('point_damage')}")
                # 使用统一的多语言格式化函数处理地牢陷阱事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "dungeon_trap", actual_damage))
                self.show_hero_info()
            elif event_num <= 5:
                print("👻 " + self.lang.get_text("encounter_ghost"))
                self.combat_system.ghost_combat(enemy_multiplier)
            elif event_num <= 8:
                print("💀 " + self.lang.get_text("encounter_monster"))
                self.combat_system.combat(enemy_multiplier * 1.2)
            elif event_num <= 11:
                gold_found = int(random.randint(25, 50) * gold_multiplier)
                self.hero_gold += gold_found
                print(f"💎 {self.lang.get_text('find_chest')} {gold_found} {self.lang.get_text('coins')}")
                # 使用统一的多语言格式化函数处理宝箱事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_chest", gold_found))
                self.show_hero_info()
            elif event_num <= 13:
                self.equipment_system.find_equipment()
            elif event_num <= 15:
                self.event_system.mysterious_merchant(gold_multiplier)
            elif event_num <= 17:
                print("🐉 " + self.lang.get_text("encounter_boss"))
                self.combat_system.boss_combat(enemy_multiplier * 1.2)
            else:
                print("✨ " + self.lang.get_text("safe_move"))
                # 使用统一的多语言格式化函数处理平安移动事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "safe_move"))

        # 山脉地图事件
        elif self.map_type == "mountain":
            if event_num <= 3:
                damage = random.randint(18, 35)
                actual_damage = max(1, int(damage * enemy_multiplier * 1.4) - self.hero_defense)
                self.hero_hp -= actual_damage
                print(f"🪨 {self.lang.get_text('mountain_hazard')}{actual_damage}{self.lang.get_text('point_damage')}")
                # 使用统一的多语言格式化函数处理山体危险事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "mountain_hazard", actual_damage))
                self.show_hero_info()
            elif event_num <= 6:
                gold_found = int(random.randint(40, 80) * gold_multiplier)
                self.hero_gold += gold_found
                print(f"💎 {self.lang.get_text('find_gem')}{gold_found}{self.lang.get_text('gold_coins')}")
                # 使用统一的多语言格式化函数处理宝石事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "find_gem", gold_found))
                self.show_hero_info()
            elif event_num <= 9:
                print("🐲 " + self.lang.get_text("encounter_monster"))
                self.combat_system.combat(enemy_multiplier * 1.3)
            elif event_num <= 11:
                print("🐲 " + self.lang.get_text("encounter_boss"))
                self.combat_system.boss_combat(enemy_multiplier * 1.3)
            elif event_num <= 13:
                self.equipment_system.find_equipment()
            elif event_num <= 15:
                self.event_system.mysterious_merchant(gold_multiplier)
            else:
                print("✨ " + self.lang.get_text("safe_move"))
                # 使用统一的多语言格式化函数处理平安移动事件文本
                self.events_encountered.append(self.lang.format_text("event_text", "safe_move"))

    def update_attributes(self):
        """更新英雄属性（基础属性 + 装备加成）"""
        self.hero_attack = self.base_attack
        self.hero_defense = self.base_defense
        self.hero_max_hp = self.base_max_hp

        # 添加装备加成
        for item in self.equipment.values():
            if item:
                self.hero_attack += item.get("attack", 0)
                self.hero_defense += item.get("defense", 0)
                self.hero_max_hp += item.get("hp", 0)

        # 确保HP不超过最大值
        if self.hero_hp > self.hero_max_hp:
            self.hero_hp = self.hero_max_hp

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

        # 装备和背包
        self.equipment = save_data.equipment
        self.inventory = save_data.inventory

        # 技能
        self.hero_skills = save_data.hero_skills

        # 游戏设置
        self.difficulty = save_data.difficulty
        self.map_type = save_data.map_type
        self.language = save_data.language
        self.map_length = save_data.map_length

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

        # 加载统计数据
        if hasattr(save_data, 'statistics_data') and save_data.statistics_data:
            self.statistics = GameStatistics.from_dict(save_data.statistics_data)
        else:
            self.statistics = GameStatistics()

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
