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
        print(f"2. {self.game.lang.get_text('learn_skill_short')}")
        print(f"3. {self.game.lang.get_text('return_to_village')}")

        while True:
            choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()

            if choice == "1":
                self.practice_combat()
                break
            elif choice == "2":
                self.learn_skill_training()
                break
            elif choice == "3":
                break
            else:
                print(self.game.lang.get_text("invalid_choice"))

    def practice_combat(self):
        """练习战斗"""
        if self.game.language == "zh":
            opponent_name = "训练假人"
            opponent_hp = 50
            opponent_attack = 5
        else:
            opponent_name = "Training Dummy"
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

            elif action == "3":
                fireball_skill = "火球术" if self.game.language == "zh" else "Fireball"
                if fireball_skill in self.game.hero_skills:
                    damage = random.randint(self.game.hero_attack, int(self.game.hero_attack * 1.5))
                    opponent_hp -= damage
                    print(f"🔥 {self.game.lang.get_text('fireball')} {opponent_name}{self.game.lang.get_text('fireball_damage')} {damage}{self.game.lang.get_text('point_damage')}")
                else:
                    damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack))
                    opponent_hp -= damage
                    print(f"🗡️ {self.game.lang.get_text('you_attack')} {opponent_name}{self.game.lang.get_text('caused_damage')} {damage}{self.game.lang.get_text('point_damage')}")

            elif action == "4":
                healing_skill = "治疗术" if self.game.language == "zh" else "Healing"
                if healing_skill in self.game.hero_skills:
                    if self.game.hero_hp >= self.game.hero_max_hp:
                        print("✨ " + (self.game.lang.get_text("full_hp_no_heal") if self.game.language == "zh" else "Your HP is full, no need to heal!"))
                    else:
                        heal_amount = random.randint(25, 40)
                        self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                        print(f"✨ {self.game.lang.get_text('healing_spell')}{heal_amount}{self.game.lang.get_text('point_hp')}")
                else:
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
                exp_gain = 20
                gold_gain = 10
                self.game.hero_exp += exp_gain
                self.game.hero_gold += gold_gain
                print(f"{self.game.lang.get_text('got_exp')} {exp_gain} {self.game.lang.get_text('exp_points')} {self.game.lang.get_text('gold_coins')} {gold_gain}!")

                # 检查升级
                from combat import CombatSystem
                combat_system = CombatSystem(self.game)
                combat_system.check_level_up()

                input(f"\n{self.game.lang.get_text('continue_prompt')}")
                break

            self.game.show_hero_info()
            time.sleep(1)

    def get_combat_action(self):
        """获取战斗动作（简化版）"""
        fireball_skill = "火球术" if self.game.language == "zh" else "Fireball"
        healing_skill = "治疗术" if self.game.language == "zh" else "Healing"

        print(f"\n{self.game.lang.get_text('choose_action')}")
        print(f"1. {self.game.lang.get_text('normal_attack')}")
        if self.game.hero_potions > 0:
            print(f"2. {self.game.lang.get_text('use_potion_short')}")
        else:
            print(f"2. {self.game.lang.get_text('no_potion')}")

        # 只在学会火球术时显示选项
        if fireball_skill in self.game.hero_skills:
            print(f"3. {self.game.lang.get_text('cast_fireball')}")
        else:
            print(f"3. ({self.game.lang.get_text('locked')}) {self.game.lang.get_text('cast_fireball')}")

        # 只在学会治疗术时显示选项
        if healing_skill in self.game.hero_skills:
            print(f"4. {self.game.lang.get_text('healing_spell_short')}")
        else:
            print(f"4. ({self.game.lang.get_text('locked')}) {self.game.lang.get_text('healing_spell_short')}")

        return input(f"{self.game.lang.get_text('enter_choice')} (1): ").strip()

    def learn_skill_training(self):
        """训练场学习技能"""
        from events import EventSystem
        event_system = EventSystem(self.game)

        print()
        if self.game.language == "zh":
            print("训练师说：我可以教你一些有用的技能。")
        else:
            print("The trainer says: I can teach you some useful skills.")
        print()

        cost = 30
        print(f"{self.game.lang.get_text('learn_skill_cost')} {cost} {self.game.lang.get_text('gold')}")

        if self.game.hero_gold >= cost:
            choice = input(f"{self.game.lang.get_text('confirm_learn')}: ").strip()
            if self.game.language == "zh":
                confirm = choice in ["y", "Y", "yes", "是"]
            else:
                confirm = choice in ["y", "Y", "yes"]

            if confirm:
                self.game.hero_gold -= cost
                event_system.learn_skill()
            else:
                print(f"{self.game.lang.get_text('cancel_learn')}")
        else:
            print(self.game.lang.get_text("not_enough_gold"))

        input(f"\n{self.game.lang.get_text('continue_prompt')}")

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
                if self.game.language == "zh":
                    confirm = choice in ["y", "Y", "yes", "是"]
                else:
                    confirm = choice in ["y", "Y", "yes"]

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

        if self.game.language == "zh":
            advices = [
                "记住，药剂是救命的关键，不要吝啬使用！",
                "升级时要谨慎选择技能，不同的技能适合不同的战斗风格。",
                "高难度地图敌人更强，但奖励也更丰厚。",
                "不同的地图有不同的危险和机遇，选择适合自己的。",
                "装备可以大幅提升你的战斗力，尽可能收集更好的装备！",
                "Boss战每3回合会释放强力攻击，注意保持血量！"
            ]
        else:
            advices = [
                "Remember, potions are lifesavers, don't hesitate to use them!",
                "Choose skills carefully when leveling up, different skills suit different combat styles.",
                "Higher difficulty maps have stronger enemies, but also better rewards.",
                "Different maps have different dangers and opportunities, choose what suits you.",
                "Equipment can greatly boost your combat power, collect the best gear you can!",
                "Bosses use powerful attacks every 3 rounds, keep your health up!"
            ]

        # 随机显示3条建议
        selected_advices = random.sample(advices, min(3, len(advices)))
        for i, advice in enumerate(selected_advices, 1):
            print(f"{i}. {advice}")

        input(f"\n{self.game.lang.get_text('continue_prompt')}")
