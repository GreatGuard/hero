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
        all_skills = {
            "zh": ["火球术", "治疗术", "暴击", "吸血", "闪避"],
            "en": ["Fireball", "Healing", "Critical", "Lifesteal", "Dodge"]
        }

        # 获取还未学习的技能
        if self.game.language == "zh":
            available_skills = [s for s in all_skills["zh"] if s not in self.game.hero_skills]
        else:
            available_skills = [s for s in all_skills["en"] if s not in self.game.hero_skills]

        if not available_skills:
            if self.game.language == "zh":
                print("\n你已经学会了所有技能！")
            else:
                print("\nYou have already learned all skills!")
            return

        # 如果不是升级时学习，给玩家选择
        if not level_up:
            print()
            if self.game.language == "zh":
                print("你遇到了一位神秘的老师！他可以教你一个技能。")
            else:
                print("You met a mysterious teacher! He can teach you a skill.")
            print()
            for i, skill in enumerate(available_skills):
                print(f"{i+1}. {skill}")

            while True:
                choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()
                try:
                    skill_index = int(choice) - 1
                    if 0 <= skill_index < len(available_skills):
                        skill = available_skills[skill_index]
                        self.game.hero_skills.append(skill)
                        if self.game.language == "zh":
                            print(f"\n{self.game.lang.get_text('learn_skill_success')}【{skill}】!")
                        else:
                            print(f"\n{self.game.lang.get_text('learn_skill_success')} [{skill}]!")
                        self.game.events_encountered.append(f"学会了技能: {skill}")
                        break
                    else:
                        print(self.game.lang.get_text("invalid_choice"))
                except ValueError:
                    print(self.game.lang.get_text("invalid_choice"))
        else:
            # 升级时随机学习一个技能
            skill = random.choice(available_skills)
            self.game.hero_skills.append(skill)
            if self.game.language == "zh":
                print(f"\n{self.game.lang.get_text('learn_skill_success')}【{skill}】!")
            else:
                print(f"\n{self.game.lang.get_text('learn_skill_success')} [{skill}]!")

    def merchant_event(self, gold_multiplier=1.0):
        """商人事件"""
        from equipment import EquipmentSystem
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

    def mysterious_merchant(self, gold_multiplier=1.0):
        """神秘商人事件（地牢/山脉特殊）"""
        from equipment import EquipmentSystem
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
        from equipment import EquipmentSystem
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
        self.game.events_encountered.append(f"使用了药剂，恢复了{heal_amount}点血量")
        self.game.show_hero_info()
