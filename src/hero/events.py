# -*- coding: utf-8 -*-
"""
事件系统模块 - 处理随机事件、商人等
"""

import random
import time


class EventSystem:
    """事件系统类"""

    def __init__(self, game):
        self.game = game

    def learn_skill(self, level_up=False):
        """学习技能"""
        from hero.game_config import CLASS_DEFINITIONS
        
        # 获取当前职业信息
        class_info = CLASS_DEFINITIONS.get(self.game.hero_class, {})
        class_skills = class_info.get("class_skills", [])
        skill_affinity = class_info.get("skill_affinity", [])
        
        # 获取所有职业的专属技能
        all_class_skills = []
        for class_name, class_data in CLASS_DEFINITIONS.items():
            all_class_skills.extend(class_data.get("class_skills", []))
        
        # 使用统一的多语言技能名称 - 只包含通用技能
        all_skills = [
            self.game.lang.get_text("fireball_skill"),
            self.game.lang.get_text("healing_skill"),
            self.game.lang.get_text("critical_skill"),
            self.game.lang.get_text("lifesteal_skill"),
            self.game.lang.get_text("dodge_skill"),
            # 新增技能
            self.game.lang.get_text("combo_skill"),
            self.game.lang.get_text("shield_skill"),
            self.game.lang.get_text("berserk_skill"),
            self.game.lang.get_text("focus_skill")
        ]
        
        # 添加当前职业的专属技能
        for skill_key in class_skills:
            skill_name = self.game.lang.get_text(f"{skill_key}_skill")
            if skill_name not in all_skills:
                all_skills.append(skill_name)

        # 获取还未学习的技能，并根据职业亲和度排序
        available_skills = [s for s in all_skills if s not in self.game.hero_skills]
        
        # 过滤掉其他职业的专属技能
        def is_skill_allowed(skill_name):
            # 检查技能是否属于某个职业的专属技能
            for class_name, class_data in CLASS_DEFINITIONS.items():
                if class_name == self.game.hero_class:
                    continue  # 跳过当前职业
                
                for skill_key in class_data.get("class_skills", []):
                    if skill_name == self.game.lang.get_text(f"{skill_key}_skill"):
                        return False  # 这是其他职业的专属技能，不允许学习
            
            return True  # 允许学习
        
        available_skills = [s for s in available_skills if is_skill_allowed(s)]
        
        # 根据职业亲和度排序技能列表（亲和度高的在前）
        def get_skill_priority(skill_name):
            # 检查是否是当前职业的专属技能
            for skill_key in class_skills:
                if skill_name == self.game.lang.get_text(f"{skill_key}_skill"):
                    return 0  # 职业专属技能最高优先级
            
            # 检查是否是职业亲和技能
            for skill_key in skill_affinity:
                if skill_name == self.game.lang.get_text(f"{skill_key}_skill"):
                    return 1  # 职业亲和技能中等优先级
            
            return 2  # 普通技能最低优先级
        
        available_skills.sort(key=get_skill_priority)

        if not available_skills:
            print(f"\n{self.game.lang.get_text('all_skills_learned')}")
            return

        # 如果不是升级时学习，给玩家选择
        if not level_up:
            print()
            print(f"{self.game.lang.get_text('mysterious_teacher')}")
            for i, skill in enumerate(available_skills):
                print(f"{i+1}. {skill}")

            while True:
                choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()
                try:
                    skill_index = int(choice) - 1
                    if 0 <= skill_index < len(available_skills):
                        skill = available_skills[skill_index]
                        self.game.hero_skills.append(skill)
                        # 使用统一的多语言格式化函数处理技能括号
                        bracket_start, bracket_end = self.game.lang.format_text("skill_brackets")
                        print(f"\n{self.game.lang.get_text('learn_skill_success')}{bracket_start}{skill}{bracket_end}!")
                        self.game.events_encountered.append(f"{self.game.lang.get_text('learned_skill_event')}{skill}")
                        # 记录学习技能
                        self.game.statistics.record_skill_learned(skill)
                        break
                    else:
                        print(self.game.lang.get_text("invalid_choice"))
                except ValueError:
                    print(self.game.lang.get_text("invalid_choice"))
        else:
            # 升级时随机学习一个技能
            skill = random.choice(available_skills)
            self.game.hero_skills.append(skill)
            # 使用统一的多语言格式化函数处理技能括号
            bracket_start, bracket_end = self.game.lang.format_text("skill_brackets")
            print(f"\n{self.game.lang.get_text('learn_skill_success')}{bracket_start}{skill}{bracket_end}!")
            # 记录学习技能
            self.game.statistics.record_skill_learned(skill)

    def merchant_event(self, gold_multiplier=1.0):
        """商人事件"""
        from hero.equipment import EquipmentSystem
        equip_system = EquipmentSystem(self.game)

        self.game.clear_screen()
        print(self.game.lang.get_text("block_separator"))
        print(f"          {self.game.lang.get_text('merchant_encounter')}")
        print(self.game.lang.get_text("block_separator"))
        print()

        print(f"{self.game.lang.get_text('merchant')}")
        print()
        print(self.game.lang.get_text("merchant_speak"))
        print()
        print(f"{self.game.lang.get_text('your_gold')}: {self.game.hero_gold}")
        print()

        # 记录访问商店
        self.game.statistics.record_shop_visit()

        # 商店商品
        potions_price = int(10 / gold_multiplier)
        skill_teach_price = int(50 / gold_multiplier)

        print(f"1. {self.game.lang.get_text('buy_potion')} - {potions_price} {self.game.lang.get_text('gold')}")
        print(f"2. {self.game.lang.get_text('learn_skill')} - {skill_teach_price} {self.game.lang.get_text('gold')}")
        print(f"3. {self.game.lang.get_text('buy_equipment_short')} - {self.game.lang.get_text('equipment_shop')}")
        print(f"4. {self.game.lang.get_text('leave_merchant')}")

        while True:
            choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()

            if choice == "1":
                if self.game.hero_gold >= potions_price:
                    num = input(f"{self.game.lang.get_text('how_many')}: ").strip()
                    try:
                        num = int(num)
                        if num > 0 and num * potions_price <= self.game.hero_gold:
                            self.game.hero_gold -= num * potions_price
                            self.game.hero_potions += num
                            print(f"{self.game.lang.get_text('buy_success')} {num} {self.game.lang.get_text('potions')}!")
                            # 记录购买和花费
                            self.game.statistics.record_item_purchased(num)
                            self.game.statistics.record_gold_spent(num * potions_price)
                            self.game.statistics.record_potion_found()  # 购买的药剂也计入获得
                        else:
                            print(self.game.lang.get_text("not_enough_gold"))
                    except ValueError:
                        print(self.game.lang.get_text("invalid_choice"))
                else:
                    print(self.game.lang.get_text("not_enough_gold"))
                input(f"{self.game.lang.get_text('continue_prompt')}")
                break
            elif choice == "2":
                if self.game.hero_gold >= skill_teach_price:
                    self.game.hero_gold -= skill_teach_price
                    # 记录花费金币
                    self.game.statistics.record_gold_spent(skill_teach_price)
                    self.learn_skill()
                else:
                    print(self.game.lang.get_text("not_enough_gold"))
                input(f"{self.game.lang.get_text('continue_prompt')}")
                break
            elif choice == "3":
                equip_system.equipment_shop(gold_multiplier)
                break
            elif choice == "4":
                break
            else:
                print(self.game.lang.get_text("invalid_choice"))
    
    def mysterious_teleport(self):
        """神秘传送事件"""
        from hero.game_config import EVENT_TYPES
        event_config = EVENT_TYPES["mysterious_teleport"]
        
        # 随机决定前进或后退
        direction = random.choice(["forward", "backward"])
        steps = random.randint(abs(event_config["min_effect"]), abs(event_config["max_effect"]))
        
        if direction == "backward":
            # 后退
            new_position = max(1, self.game.hero_position - steps)
            print(f"🌀 {self.game.lang.get_text('event_mysterious_teleport_desc')}")
            print(f"💫 {self.game.lang.get_text('teleported_to_position', position=new_position)}")
        else:
            # 前进
            new_position = min(self.game.map_length, self.game.hero_position + steps)
            print(f"🌀 {self.game.lang.get_text('event_mysterious_teleport_desc')}")
            print(f"💫 {self.game.lang.get_text('teleported_to_position', position=new_position)}")
        
        # 记录事件
        self.game.events_encountered.append(f"{self.game.lang.get_text('event_mysterious_teleport')} - {self.game.lang.get_text('moved_to_position', position=new_position)}")
        self.game.statistics.record_event_triggered("mysterious_teleport")
        
        # 更新位置
        self.game.hero_position = new_position
    
    def sage_guidance(self):
        """贤者指引事件"""
        from hero.game_config import EVENT_TYPES
        event_config = EVENT_TYPES["sage_guidance"]
        
        # 随机获得经验值
        exp_gained = random.randint(event_config["min_exp"], event_config["max_exp"])
        self.game.hero_exp += exp_gained
        
        print(f"🧙 {self.game.lang.get_text('event_sage_guidance_desc')}")
        print(f"✨ {self.game.lang.get_text('gained_exp', exp=exp_gained)}")
        
        # 记录事件
        self.game.events_encountered.append(f"{self.game.lang.get_text('event_sage_guidance')} - {self.game.lang.get_text('gained_exp', exp=exp_gained)}")
        self.game.statistics.record_event_triggered("sage_guidance")
        self.game.statistics.record_exp_earned(exp_gained)
        
        # 检查升级
        if self.game.hero_exp >= self.game.hero_level * 50:
            from .combat import CombatSystem
            combat_system = CombatSystem(self.game)
            combat_system.check_level_up()
    
    def robber_encounter(self):
        """遭遇强盗事件"""
        from hero.game_config import EVENT_TYPES
        event_config = EVENT_TYPES["robber_encounter"]
        
        print(f"🗡️ {self.game.lang.get_text('event_robber_encounter_desc')}")
        print()
        print(f"1. {self.game.lang.get_text('combat_option')}")
        print(f"2. {self.game.lang.get_text('pay_gold_option')}")
        
        choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()
        
        if choice == "1":  # 选择战斗
            print(f"\n{self.game.lang.get_text('decide_to_combat')}")
            # 记录事件
            self.game.events_encountered.append(f"{self.game.lang.get_text('event_robber_encounter')} - {self.game.lang.get_text('chose_combat')}")
            self.game.statistics.record_event_triggered("robber_combat")
            # 与强盗战斗
            self.game.combat_system.combat(self.game.difficulty_settings[self.game.difficulty]["enemy_multiplier"])
        elif choice == "2":  # 选择交金币
            gold_loss = random.randint(event_config["min_gold_loss"], event_config["max_gold_loss"])
            gold_loss = min(gold_loss, self.game.hero_gold)  # 不能失去比拥有的更多的金币
            
            print(f"\n{self.game.lang.get_text('gave_gold_to_robber', gold=gold_loss)}")
            self.game.hero_gold -= gold_loss
            
            # 记录事件
            self.game.events_encountered.append(f"{self.game.lang.get_text('event_robber_encounter')} - {self.game.lang.get_text('lost_gold', gold=gold_loss)}")
            self.game.statistics.record_event_triggered("robber_pay")
            self.game.statistics.record_gold_spent(gold_loss)
        else:
            print(self.game.lang.get_text("invalid_choice"))
            self.robber_encounter()  # 重新选择
    
    def mysterious_altar(self):
        """神秘祭坛事件"""
        from hero.game_config import EVENT_TYPES
        event_config = EVENT_TYPES["mysterious_altar"]
        
        print(f"🪦 {self.game.lang.get_text('event_mysterious_altar_desc')}")
        print()
        print(f"1. {self.game.lang.get_text('sacrifice_hp_for_attack')}")
        print(f"2. {self.game.lang.get_text('sacrifice_hp_for_defense')}")
        print(f"3. {self.game.lang.get_text('leave_altar')}")
        
        choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()
        
        if choice == "1":  # 换取攻击力
            hp_cost = int(self.game.hero_max_hp * event_config["hp_cost_percent"])
            hp_cost = min(hp_cost, self.game.hero_hp - 1)  # 保留至少1点血
            
            print(f"\n{self.game.lang.get_text('sacrificed_hp_for_attack_desc', hp=hp_cost)}")
            self.game.hero_hp -= hp_cost
            self.game.base_attack += event_config["attack_boost"]
            self.game.update_attributes()  # 重新计算属性
            
            # 记录事件
            self.game.events_encountered.append(f"{self.game.lang.get_text('event_mysterious_altar')} - {self.game.lang.get_text('sacrificed_hp_for_attack_event')}")
            self.game.statistics.record_event_triggered("altar_attack")
            self.game.show_hero_info()
        elif choice == "2":  # 换取防御力
            hp_cost = int(self.game.hero_max_hp * event_config["hp_cost_percent"])
            hp_cost = min(hp_cost, self.game.hero_hp - 1)  # 保留至少1点血
            
            print(f"\n{self.game.lang.get_text('sacrificed_hp_for_defense_desc', hp=hp_cost)}")
            self.game.hero_hp -= hp_cost
            self.game.base_defense += event_config["defense_boost"]
            self.game.update_attributes()  # 重新计算属性
            
            # 记录事件
            self.game.events_encountered.append(f"{self.game.lang.get_text('event_mysterious_altar')} - {self.game.lang.get_text('sacrificed_hp_for_defense_event')}")
            self.game.statistics.record_event_triggered("altar_defense")
            self.game.show_hero_info()
        elif choice == "3":  # 离开
            print(f"\n{self.game.lang.get_text('decide_to_leave_altar')}")
            self.game.events_encountered.append(f"{self.game.lang.get_text('event_mysterious_altar')} - {self.game.lang.get_text('chose_to_leave_altar')}")
            self.game.statistics.record_event_triggered("altar_leave")
        else:
            print(self.game.lang.get_text("invalid_choice"))
            self.mysterious_altar()  # 重新选择
    
    def roadside_camp(self):
        """路边营地事件"""
        from hero.game_config import EVENT_TYPES
        event_config = EVENT_TYPES["roadside_camp"]
        
        # 随机恢复生命值
        heal_amount = random.randint(event_config["min_heal"], event_config["max_heal"])
        self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
        
        print(f"🏕️ {self.game.lang.get_text('event_roadside_camp_desc')}")
        print(f"💚 {self.game.lang.get_text('rested_at_camp', heal=heal_amount)}")
        
        # 记录事件
        self.game.events_encountered.append(f"{self.game.lang.get_text('event_roadside_camp')} - {self.game.lang.get_text('restored_hp', heal=heal_amount)}")
        self.game.statistics.record_event_triggered("roadside_camp")
        self.game.show_hero_info()

    def mysterious_merchant(self, gold_multiplier=1.0):
        """神秘商人事件（地牢/山脉特殊）"""
        from hero.equipment import EquipmentSystem
        equip_system = EquipmentSystem(self.game)

        self.game.clear_screen()
        print(self.game.lang.get_text("block_separator"))
        print(f"          {self.game.lang.get_text('mysterious_merchant_encounter')}")
        print(self.game.lang.get_text("block_separator"))
        print()

        print(f"{self.game.lang.get_text('mysterious_merchant_desc')}")
        print()
        print(f"{self.game.lang.get_text('your_gold')}: {self.game.hero_gold}")
        print()

        # 记录访问商店
        self.game.statistics.record_shop_visit()

        print(f"1. {self.game.lang.get_text('buy_equipment_short')}")
        print(f"2. {self.game.lang.get_text('leave_merchant')}")

        while True:
            choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()

            if choice == "1":
                equip_system.equipment_shop(gold_multiplier * 1.5)  # 神秘商人价格更高
                break
            elif choice == "2":
                break
            else:
                print(self.game.lang.get_text("invalid_choice"))

    def treasure_chest_with_equipment(self):
        """带有装备的宝箱"""
        from hero.equipment import EquipmentSystem
        equip_system = EquipmentSystem(self.game)

        self.game.clear_screen()
        print(self.game.lang.get_text("block_separator"))
        print(f"          {self.game.lang.get_text('treasure_chest')}")
        print(self.game.lang.get_text("block_separator"))
        print()

        print(f"{self.game.lang.get_text('treasure_chest_desc')}")
        print()

        # 随机获得装备
        equip_system.find_equipment()
        input(f"\n{self.game.lang.get_text('continue_prompt')}")

    def show_adventure_history(self):
        """显示冒险历史"""
        self.game.clear_screen()
        print(self.game.lang.get_text("block_separator"))
        print(f"          {self.game.lang.get_text('adventure_history')}")
        print(self.game.lang.get_text("block_separator"))
        print()

        if not self.game.events_encountered:
            print(f"{self.game.lang.get_text('no_events_yet')}")
        else:
            for i, event in enumerate(self.game.events_encountered[-10:], 1):
                print(f"{i}. {event}")

        input(f"\n{self.game.lang.get_text('continue_prompt')}")

    def use_potion(self):
        """使用药剂"""
        heal_amount = random.randint(20, 40)
        self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
        self.game.hero_potions -= 1
        print(f"🧪 {self.game.lang.get_text('poison')} {heal_amount}{self.game.lang.get_text('point_hp')}")
        self.game.events_encountered.append(f"{self.game.lang.get_text('used_potion_event', heal=heal_amount)}")
        # 记录使用药剂
        self.game.statistics.record_potion_used()
        self.game.show_hero_info()

    def swamp_merchant_event(self, gold_multiplier=1.0):
        """沼泽商人事件"""
        from hero.equipment import EquipmentSystem
        equip_system = EquipmentSystem(self.game)

        self.game.clear_screen()
        print(self.game.lang.get_text("block_separator"))
        print(f"          {self.game.lang.get_text('swamp_merchant_encounter')}")
        print(self.game.lang.get_text("block_separator"))
        print()

        print(f"{self.game.lang.get_text('swamp_merchant_desc')}")
        print()
        print(f"{self.game.lang.get_text('your_gold')}: {self.game.hero_gold}")
        print()

        # 记录访问商店
        self.game.statistics.record_shop_visit()

        # 商店商品 - 沼泽商人有特殊折扣
        potions_price = int(8 / gold_multiplier)  # 比普通商人便宜
        skill_teach_price = int(40 / gold_multiplier)

        print(f"1. {self.game.lang.get_text('buy_potion')} - {potions_price} {self.game.lang.get_text('gold')}")
        print(f"2. {self.game.lang.get_text('learn_skill')} - {skill_teach_price} {self.game.lang.get_text('gold')}")
        print(f"3. {self.game.lang.get_text('buy_equipment_short')} - {self.game.lang.get_text('equipment_shop')}")
        print(f"4. {self.game.lang.get_text('leave_merchant')}")

        while True:
            choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()

            if choice == "1":
                if self.game.hero_gold >= potions_price:
                    num = input(f"{self.game.lang.get_text('how_many')}: ").strip()
                    try:
                        num = int(num)
                        if num > 0 and num * potions_price <= self.game.hero_gold:
                            self.game.hero_gold -= num * potions_price
                            self.game.hero_potions += num
                            print(f"{self.game.lang.get_text('buy_success')} {num} {self.game.lang.get_text('potions')}!")
                            # 记录购买和花费
                            self.game.statistics.record_item_purchased(num)
                            self.game.statistics.record_gold_spent(num * potions_price)
                            self.game.statistics.record_potion_found()  # 购买的药剂也计入获得
                        else:
                            print(self.game.lang.get_text("not_enough_gold"))
                    except ValueError:
                        print(self.game.lang.get_text("invalid_choice"))
                else:
                    print(self.game.lang.get_text("not_enough_gold"))
                input(f"{self.game.lang.get_text('continue_prompt')}")
                break
            elif choice == "2":
                if self.game.hero_gold >= skill_teach_price:
                    self.game.hero_gold -= skill_teach_price
                    # 记录花费金币
                    self.game.statistics.record_gold_spent(skill_teach_price)
                    self.learn_skill()
                else:
                    print(self.game.lang.get_text("not_enough_gold"))
                input(f"{self.game.lang.get_text('continue_prompt')}")
                break
            elif choice == "3":
                equip_system.equipment_shop(gold_multiplier * 1.2)  # 装备有折扣但不如神秘商人
                break
            elif choice == "4":
                break
            else:
                print(self.game.lang.get_text("invalid_choice"))
