# -*- coding: utf-8 -*-
"""
新手村模块 - 处理新手村相关功能
"""

import random
import time


class NewbieVillage:
    """新手村类"""

    def __init__(self, game):
        self.game = game

    def newbie_village(self):
        """新手村主界面"""
        while True:
            self.game.clear_screen()
            print(self.game.lang.get_text("block_separator"))
            print(f"          {self.game.lang.get_text('newbie_village')}")
            print(self.game.lang.get_text("block_separator"))
            print()

            print(f"{self.game.lang.get_text('village_desc')}")
            print()

            print(f"1. {self.game.lang.get_text('training_ground')}")
            print(f"2. {self.game.lang.get_text('village_shop')}")
            print(f"3. {self.game.lang.get_text('village_clinic')}")
            print(f"4. {self.game.lang.get_text('elder_advice_short')}")
            print(f"5. {self.game.lang.get_text('start_adventure')}")

            choice = input(f"{self.game.lang.get_text('enter_choice')} (5): ").strip()

            if choice == "" or choice == "5":
                self.game.hero_hp = self.game.hero_max_hp
                print(f"\n{self.game.lang.get_text('hp_recovered')}")
                time.sleep(1)
                break
            elif choice == "1":
                self.training_ground()
            elif choice == "2":
                self.village_shop()
            elif choice == "3":
                self.village_clinic()
            elif choice == "4":
                self.elder_advice()
            else:
                print(self.game.lang.get_text("invalid_choice"))

    def training_ground(self):
        """训练场"""
        self.game.clear_screen()
        print(self.game.lang.get_text("block_separator"))
        print(f"          {self.game.lang.get_text('training_ground')}")
        print(self.game.lang.get_text("block_separator"))
        print()

        print(f"{self.game.lang.get_text('training_desc')}")
        print()

        print(f"1. {self.game.lang.get_text('practice_combat')}")
        print(f"2. {self.game.lang.get_text('return_to_village')}")

        while True:
            choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()

            if choice == "1":
                self.practice_combat()
                break
            elif choice == "2":
                break
            else:
                print(self.game.lang.get_text("invalid_choice"))

    def practice_combat(self):
        """练习战斗"""
        opponent_name = self.game.lang.get_text("training_dummy")
        opponent_hp = 50
        opponent_attack = 5

        print(f"\n{self.game.lang.get_text('practice_start')} {opponent_name}!")
        print(f"{opponent_name} - {self.game.lang.get_text('hp')}: {opponent_hp}, {self.game.lang.get_text('attack')}: {opponent_attack}")
        time.sleep(1)

        while opponent_hp > 0:
            action = self.get_combat_action()

            if action == "1" or action == "":
                damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack))
                opponent_hp -= damage
                print(f"🗡️ {self.game.lang.get_text('you_attack')} {opponent_name}{self.game.lang.get_text('caused_damage')} {damage}{self.game.lang.get_text('point_damage')}")

            elif action == "2" and self.game.hero_potions > 0:
                heal_amount = random.randint(20, 40)
                self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                self.game.hero_potions -= 1
                print(f"🧪 {self.game.lang.get_text('poison')} {heal_amount}{self.game.lang.get_text('point_hp')}")

            # 处理技能选择
            elif action.isdigit() and int(action) > 2:
                # 获取已学习的技能
                if self.game.skill_tree:
                    learned_skills = []
                    for skill_id, level in self.game.skill_tree.learned_skills.items():
                        if level > 0:
                            learned_skills.append(skill_id)
                    
                    # 计算技能选项的索引
                    skill_index = int(action) - 3  # 减去普通攻击和药剂选项
                    
                    if 0 <= skill_index < len(learned_skills):
                        skill_id = learned_skills[skill_index]
                        
                        # 处理技能效果
                        if skill_id == "fireball":
                            damage = random.randint(self.game.hero_attack, int(self.game.hero_attack * 1.5))
                            opponent_hp -= damage
                            print(f"🔥 {self.game.lang.get_text('fireball_skill')} {opponent_name}{self.game.lang.get_text('caused_damage')} {damage}{self.game.lang.get_text('point_damage')}")
                        
                        elif skill_id == "healing":
                            if self.game.hero_hp >= self.game.hero_max_hp:
                                print("✨ " + self.game.lang.get_text("full_hp_no_heal"))
                            else:
                                heal_amount = random.randint(25, 40)
                                self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                                print(f"✨ {self.game.lang.get_text('healing_skill')}{heal_amount}{self.game.lang.get_text('point_hp')}")
                        
                        elif skill_id == "power_strike":
                            damage = random.randint(self.game.hero_attack, int(self.game.hero_attack * 1.4))
                            opponent_hp -= damage
                            print(f"⚔️ {self.game.lang.get_text('power_strike_skill')} {opponent_name}{self.game.lang.get_text('caused_damage')} {damage}{self.game.lang.get_text('point_damage')}")
                        
                        elif skill_id == "shield_bash":
                            damage = random.randint(int(self.game.hero_attack * 0.8), self.game.hero_attack)
                            opponent_hp -= damage
                            print(f"🛡️ {self.game.lang.get_text('shield_bash_skill')} {opponent_name}{self.game.lang.get_text('caused_damage')} {damage}{self.game.lang.get_text('point_damage')}")
                        
                        elif skill_id == "battle_cry":
                            print(f"📣 {self.game.lang.get_text('battle_cry_skill')}!")
                            damage = random.randint(int(self.game.hero_attack * 0.9), int(self.game.hero_attack * 1.1))
                            opponent_hp -= damage
                            print(f"🗡️ {self.game.lang.get_text('you_attack')} {opponent_name}{self.game.lang.get_text('caused_damage')} {damage}{self.game.lang.get_text('point_damage')}")
                        
                        elif skill_id == "backstab":
                            damage = random.randint(int(self.game.hero_attack * 1.2), int(self.game.hero_attack * 1.5))
                            opponent_hp -= damage
                            print(f"🗡️ {self.game.lang.get_text('backstab_skill')} {opponent_name}{self.game.lang.get_text('caused_damage')} {damage}{self.game.lang.get_text('point_damage')}")
                        
                        elif skill_id == "shadow_strike":
                            damage = random.randint(self.game.hero_attack, int(self.game.hero_attack * 1.3))
                            opponent_hp -= damage
                            print(f"🌑 {self.game.lang.get_text('shadow_strike_skill')} {opponent_name}{self.game.lang.get_text('caused_damage')} {damage}{self.game.lang.get_text('point_damage')}")
                        
                        elif skill_id == "frost_armor":
                            print(f"❄️ {self.game.lang.get_text('frost_armor_skill')}!")
                            damage = random.randint(int(self.game.hero_attack * 0.7), int(self.game.hero_attack * 0.9))
                            opponent_hp -= damage
                            print(f"🗡️ {self.game.lang.get_text('you_attack')} {opponent_name}{self.game.lang.get_text('caused_damage')} {damage}{self.game.lang.get_text('point_damage')}")
                        
                        # 其他技能可以在这里添加
                        else:
                            # 默认技能处理
                            damage = random.randint(self.game.hero_attack, int(self.game.hero_attack * 1.2))
                            opponent_hp -= damage
                            # 检查技能ID是否已经包含"_skill"后缀
                            if skill_id.endswith("_skill"):
                                skill_name_key = skill_id
                            else:
                                skill_name_key = f"{skill_id}_skill"
                            skill_name = self.game.lang.get_text(skill_name_key)
                            print(f"⚔️ {skill_name} {opponent_name}{self.game.lang.get_text('caused_damage')} {damage}{self.game.lang.get_text('point_damage')}")
                    else:
                        # 无效技能选择
                        damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack))
                        opponent_hp -= damage
                        print(f"🗡️ {self.game.lang.get_text('you_attack')} {opponent_name}{self.game.lang.get_text('caused_damage')} {damage}{self.game.lang.get_text('point_damage')}")
                else:
                    # 没有技能树，使用普通攻击
                    damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack))
                    opponent_hp -= damage
                    print(f"🗡️ {self.game.lang.get_text('you_attack')} {opponent_name}{self.game.lang.get_text('caused_damage')} {damage}{self.game.lang.get_text('point_damage')}")

            else:
                print(self.game.lang.get_text("invalid_action"))
                damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack))
                opponent_hp -= damage
                print(f"🗡️ {self.game.lang.get_text('you_attack')} {opponent_name}{self.game.lang.get_text('caused_damage')} {damage}{self.game.lang.get_text('point_damage')}")

            if opponent_hp <= 0:
                print(f"\n🎉 {self.game.lang.get_text('practice_victory')} {opponent_name}!")
                print(f"{self.game.lang.get_text('practice_reward')}")
                exp_gain = 20000
                gold_gain = 10000
                self.game.hero_exp += exp_gain
                self.game.hero_gold += gold_gain
                print(f"{self.game.lang.get_text('got_exp')} {exp_gain} {self.game.lang.get_text('exp_points')} {self.game.lang.get_text('gold_coins')} {gold_gain}!")

                # 检查升级
                from .combat import CombatSystem
                combat_system = CombatSystem(self.game)
                combat_system.check_level_up()

                input(f"\n{self.game.lang.get_text('continue_prompt')}")
                break

            self.game.show_hero_info()
            time.sleep(1)

    def get_combat_action(self):
        """获取战斗动作（简化版）"""
        print(f"\n{self.game.lang.get_text('choose_action')}")
        print(f"1. {self.game.lang.get_text('normal_attack')}")
        
        option_index = 2
        
        # 药剂选项
        if self.game.hero_potions > 0:
            print(f"{option_index}. {self.game.lang.get_text('use_potion_short')}")
        else:
            print(f"{option_index}. {self.game.lang.get_text('no_potion')}")
        option_index += 1
        
        # 显示已学习的技能
        if self.game.skill_tree:
            # 获取已学习的技能
            learned_skills = []
            for skill_id, level in self.game.skill_tree.learned_skills.items():
                if level > 0:
                    learned_skills.append(skill_id)
            
            # 显示技能（按技能类别排序）
            def get_skill_priority(skill_id):
                from .game_config import SKILL_TREES
                skill_data = SKILL_TREES.get(self.game.hero_class, {}).get(skill_id, {})
                category = skill_data.get("category", "core")
                
                if category == "core":
                    return 0
                elif category == "combat":
                    return 1
                elif category == "passive":
                    return 2
                else:  # ultimate
                    return 3
            
            learned_skills.sort(key=get_skill_priority)
            
            # 显示技能
            for skill_id in learned_skills:
                # 获取技能名称
                # 检查技能ID是否已经包含"_skill"后缀
                if skill_id.endswith("_skill"):
                    skill_name_key = skill_id
                else:
                    skill_name_key = f"{skill_id}_skill"
                skill_name = self.game.lang.get_text(skill_name_key)
                
                # 获取技能等级
                skill_level = self.game.skill_tree.learned_skills.get(skill_id, 0)
                
                # 显示技能名称和等级
                if skill_level > 0:
                    print(f"{option_index}. {skill_name} (Lv.{skill_level})")
                else:
                    print(f"{option_index}. {skill_name}")
                option_index += 1

        return input(f"{self.game.lang.get_text('enter_choice')} (1): ").strip()

    def village_shop(self):
        """村庄商店"""
        self.game.clear_screen()
        print(self.game.lang.get_text("block_separator"))
        print(f"          {self.game.lang.get_text('village_shop')}")
        print(self.game.lang.get_text("block_separator"))
        print()

        print(f"{self.game.lang.get_text('shopkeeper_greeting')}")
        print()

        print(f"{self.game.lang.get_text('your_gold')}: {self.game.hero_gold}")
        print()

        print(f"1. {self.game.lang.get_text('buy_potion')} - 10 {self.game.lang.get_text('gold')}")
        print(f"2. {self.game.lang.get_text('exit_shop')}")

        while True:
            choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()

            if choice == "1":
                if self.game.hero_gold >= 10:
                    num = input(f"{self.game.lang.get_text('how_many')}: ").strip()
                    try:
                        num = int(num)
                        if num > 0 and num * 10 <= self.game.hero_gold:
                            self.game.hero_gold -= num * 10
                            self.game.hero_potions += num
                            print(f"{self.game.lang.get_text('buy_success')} {num} {self.game.lang.get_text('potions')}!")
                        else:
                            print(self.game.lang.get_text("not_enough_gold"))
                    except ValueError:
                        print(self.game.lang.get_text("invalid_choice"))
                else:
                    print(self.game.lang.get_text("not_enough_gold"))
                input(f"{self.game.lang.get_text('continue_prompt')}")
                break
            elif choice == "2":
                break
            else:
                print(self.game.lang.get_text("invalid_choice"))

    def village_clinic(self):
        """村庄诊所"""
        self.game.clear_screen()
        print(self.game.lang.get_text("block_separator"))
        print(f"          {self.game.lang.get_text('village_clinic')}")
        print(self.game.lang.get_text("block_separator"))
        print()

        if self.game.hero_hp >= self.game.hero_max_hp:
            print(f"{self.game.lang.get_text('hp_full')}")
        else:
            cost = 15
            heal_amount = self.game.hero_max_hp - self.game.hero_hp
            print(f"{self.game.lang.get_text('clinic_offer')} {heal_amount} {self.game.lang.get_text('hp')}")
            print(f"{self.game.lang.get_text('clinic_cost')} {cost} {self.game.lang.get_text('gold')}")

            if self.game.hero_gold >= cost:
                choice = input(f"{self.game.lang.get_text('confirm_treatment')}: ").strip()
                # 使用统一的多语言确认选项
                yes_options = self.game.lang.get_text("yes_options")
                confirm = choice in yes_options

                if confirm:
                    self.game.hero_gold -= cost
                    self.game.hero_hp = self.game.hero_max_hp
                    print(f"\n{self.game.lang.get_text('treatment_success')}")
                else:
                    print(f"{self.game.lang.get_text('cancel_treatment')}")
            else:
                print(self.game.lang.get_text("not_enough_gold"))

        input(f"\n{self.game.lang.get_text('continue_prompt')}")

    def elder_advice(self):
        """长老建议"""
        self.game.clear_screen()
        print(self.game.lang.get_text("block_separator"))
        print(f"          {self.game.lang.get_text('elder_advice_title')}")
        print(self.game.lang.get_text("block_separator"))
        print()

        print(f"{self.game.lang.get_text('elder_desc')}")
        print()

        # 使用统一的多语言建议列表
        advices = [
            self.game.lang.get_text("elder_advice_1"),
            self.game.lang.get_text("elder_advice_2"),
            self.game.lang.get_text("elder_advice_3"),
            self.game.lang.get_text("elder_advice_4"),
            self.game.lang.get_text("elder_advice_5"),
            self.game.lang.get_text("elder_advice_6")
        ]

        # 随机显示3条建议
        selected_advices = random.sample(advices, min(3, len(advices)))
        for i, advice in enumerate(selected_advices, 1):
            print(f"{i}. {advice}")

        input(f"\n{self.game.lang.get_text('continue_prompt')}")
