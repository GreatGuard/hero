# -*- coding: utf-8 -*-
"""
战斗系统模块 - 处理战斗相关功能
"""

import random
import time


class CombatSystem:
    """战斗系统类"""

    def __init__(self, game):
        self.game = game

    def get_combat_action(self):
        """获取玩家战斗动作"""
        print(f"\n{self.game.lang.get_text('choose_action')}")
        print(f"1. {self.game.lang.get_text('normal_attack')}")
        if self.game.hero_potions > 0:
            print(f"2. {self.game.lang.get_text('use_potion_short')}")
        else:
            print(f"2. {self.game.lang.get_text('no_potion')}")

        # 只在学会火球术时显示选项
        fireball_skill = self.game.lang.get_text('fireball_skill')
        if fireball_skill in self.game.hero_skills:
            print(f"3. {self.game.lang.get_text('cast_fireball')}")
        else:
            print(f"3. ({self.game.lang.get_text('locked')}) {self.game.lang.get_text('cast_fireball')}")

        # 只在学会治疗术时显示选项
        healing_skill = self.game.lang.get_text('healing_skill')
        if healing_skill in self.game.hero_skills:
            print(f"4. {self.game.lang.get_text('healing_spell_short')}")
        else:
            print(f"4. ({self.game.lang.get_text('locked')}) {self.game.lang.get_text('healing_spell_short')}")

        return input(f"{self.game.lang.get_text('enter_choice')} (1): ").strip()

    def combat(self, enemy_multiplier=1.0):
        """普通战斗系统"""
        # 基础怪物名称列表
        monster_names = [
            self.game.lang.get_text("monster_goblin"),
            self.game.lang.get_text("monster_skeleton"),
            self.game.lang.get_text("monster_wolf"),
            self.game.lang.get_text("monster_bandit"),
            self.game.lang.get_text("monster_slime")
        ]

        # 根据英雄等级选择怪物名称和强度
        if self.game.hero_level <= 2:
            monster_names = [
                self.game.lang.get_text("monster_goblin"),
                self.game.lang.get_text("monster_slime"),
                self.game.lang.get_text("monster_pixie")
            ]
            hp_range = (20, 35)
            atk_range = (5, 12)
            def_range = (0, 3)
        elif self.game.hero_level <= 5:
            monster_names = [
                self.game.lang.get_text("monster_skeleton"),
                self.game.lang.get_text("monster_wolf"),
                self.game.lang.get_text("monster_orc_warrior")
            ]
            hp_range = (30, 50)
            atk_range = (10, 20)
            def_range = (2, 6)
        else:
            monster_names = [
                self.game.lang.get_text("monster_bandit_leader"),
                self.game.lang.get_text("monster_dark_mage"),
                self.game.lang.get_text("monster_elite_assassin"),
                self.game.lang.get_text("monster_troll")
            ]
            hp_range = (40, 70)
            atk_range = (15, 30)
            def_range = (5, 10)

        monster_name = random.choice(monster_names)

        # 根据英雄等级和难度计算怪物属性
        level_bonus = (self.game.hero_level - 1) * 2
        monster_hp = int((random.randint(hp_range[0], hp_range[1]) + level_bonus * 2) * enemy_multiplier)
        monster_attack = int((random.randint(atk_range[0], atk_range[1]) + level_bonus) * enemy_multiplier)
        monster_defense = int((random.randint(def_range[0], def_range[1]) + level_bonus // 2) * enemy_multiplier)

        # 应用难度经验/金币倍数
        settings = self.game.difficulty_settings[self.game.difficulty]
        exp_multiplier = settings["exp_multiplier"]
        gold_multiplier = settings["gold_multiplier"]

        exp_gain = int((random.randint(10, 25) + self.game.hero_level * 3) * exp_multiplier)
        gold_gain = int((random.randint(5, 20) + self.game.hero_level * 2) * gold_multiplier)

        print(f"\n👹 {self.game.lang.get_text('encounter_monster')} {monster_name}!")
        print(f"{monster_name} - {self.game.lang.get_text('hp')}{self.game.lang.get_text('item_separator')}{monster_hp}, {self.game.lang.get_text('attack')}{self.game.lang.get_text('item_separator')}{monster_attack}, {self.game.lang.get_text('defense')}{self.game.lang.get_text('item_separator')}{monster_defense}")
        print(self.game.lang.get_text("battle_start"))
        time.sleep(1)

        combat_round = 1
        while monster_hp > 0 and self.game.hero_hp > 0:
            print(f"\n--- {self.game.lang.get_text('round')} {combat_round} ---")

            # 显示战斗选项
            action = self.get_combat_action()

            if action == "1" or action == "":  # 普通攻击
                hero_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - monster_defense)
                monster_hp -= hero_damage
                print(f"🗡️ {self.game.lang.get_text('you_attack')} {monster_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
            elif action == "2" and self.game.hero_potions > 0:  # 使用药剂
                heal_amount = random.randint(20, 40)
                self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                self.game.hero_potions -= 1
                print(f"🧪 {self.game.lang.get_text('poison')} {heal_amount}{self.game.lang.get_text('point_hp')}")
            elif action == "3":  # 使用火球术技能
                fireball_skill = self.game.lang.get_text('fireball_skill')
                if fireball_skill in self.game.hero_skills:
                    hero_damage = random.randint(self.game.hero_attack, int(self.game.hero_attack * 1.5))
                    monster_hp -= hero_damage
                    print(f"🔥 {self.game.lang.get_text('fireball')} {monster_name}{self.game.lang.get_text('fireball_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
                else:
                    # 如果没有火球术技能，改为普通攻击
                    hero_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - monster_defense)
                    monster_hp -= hero_damage
                    print(f"🗡️ {self.game.lang.get_text('you_attack')} {monster_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
            elif action == "4":  # 使用治疗术技能
                healing_skill = self.game.lang.get_text('healing_skill')
                if healing_skill in self.game.hero_skills:
                    if self.game.hero_hp >= self.game.hero_max_hp:
                        print("✨ " + self.game.lang.get_text("full_hp_no_heal"))
                    else:
                        heal_amount = random.randint(1000, 2000)
                        self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                        print(f"✨ {self.game.lang.get_text('healing_spell')}{heal_amount}{self.game.lang.get_text('point_hp')}")
                else:
                    # 如果没有治疗术技能，改为普通攻击
                    hero_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - monster_defense)
                    monster_hp -= hero_damage
                    print(f"🗡️ {self.game.lang.get_text('you_attack')} {monster_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
            else:
                print(self.game.lang.get_text("invalid_action"))
                hero_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - monster_defense)
                monster_hp -= hero_damage
                print(f"🗡️ {self.game.lang.get_text('you_attack')} {monster_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")

            if monster_hp <= 0:
                self.game.monsters_defeated += 1
                self.game.hero_exp += exp_gain
                self.game.hero_gold += gold_gain
                print(f"\n🎉 {self.game.lang.get_text('battle_victory')} {monster_name}!")
                print(f"{self.game.lang.get_text('got_exp')} {exp_gain} {self.game.lang.get_text('exp_points')} {self.game.lang.get_text('gold_coins')} {gold_gain}!")

                # 检查升级
                self.check_level_up()

                input(f"\n{self.game.lang.get_text('continue_prompt')}")
                break

            # 怪物反击
            monster_damage = max(1, random.randint(monster_attack // 2, monster_attack) - self.game.hero_defense)
            self.game.hero_hp -= monster_damage
            print(f"🩸 {monster_name}{self.game.lang.get_text('monster_attack')} {monster_damage}{self.game.lang.get_text('damage')}")

            print(f"{self.game.lang.get_text('your_hp')} {self.game.hero_hp}, {self.game.lang.get_text('monster_hp')} {monster_name}{self.game.lang.get_text('item_separator')}{monster_hp}")
            combat_round += 1
            time.sleep(1)

        self.game.show_hero_info()

    def boss_combat(self, enemy_multiplier=1.0):
        """Boss战斗系统"""
        # 根据英雄等级选择Boss名称和强度
        if self.game.hero_level <= 3:
            boss_names = [
                self.game.lang.get_text("boss_lesser_demon_leader"),
                self.game.lang.get_text("boss_cave_troll"),
                self.game.lang.get_text("boss_shadow_spider")
            ]
            hp_range = (60, 80)
            atk_range = (15, 30)
            def_range = (3, 7)
            exp_range = (40, 70)
            gold_range = (25, 50)
        elif self.game.hero_level <= 6:
            boss_names = [
                self.game.lang.get_text("boss_dark_lord"),
                self.game.lang.get_text("boss_frost_queen"),
                self.game.lang.get_text("boss_fire_lizard")
            ]
            hp_range = (80, 120)
            atk_range = (25, 45)
            def_range = (6, 12)
            exp_range = (70, 120)
            gold_range = (50, 90)
        else:
            boss_names = [
                self.game.lang.get_text("boss_ancient_dragon"),
                self.game.lang.get_text("boss_abyss_demon"),
                self.game.lang.get_text("boss_death_knight"),
                self.game.lang.get_text("boss_chaos_wizard")
            ]
            hp_range = (100, 150)
            atk_range = (35, 65)
            def_range = (10, 18)
            exp_range = (120, 200)
            gold_range = (80, 150)

        boss_name = random.choice(boss_names)
        boss_level = max(1, self.game.hero_level + random.randint(-1, 1))

        # 应用难度倍数
        level_bonus = self.game.hero_level * 3
        boss_hp = int((random.randint(hp_range[0], hp_range[1]) + level_bonus * 3) * enemy_multiplier)
        boss_attack = int((random.randint(atk_range[0], atk_range[1]) + level_bonus * 2) * enemy_multiplier)
        boss_defense = int((random.randint(def_range[0], def_range[1]) + level_bonus) * enemy_multiplier)

        # 应用难度经验/金币倍数
        settings = self.game.difficulty_settings[self.game.difficulty]
        exp_multiplier = settings["exp_multiplier"]
        gold_multiplier = settings["gold_multiplier"]

        exp_gain = int((random.randint(exp_range[0], exp_range[1]) + self.game.hero_level * 8) * exp_multiplier)
        gold_gain = int((random.randint(gold_range[0], gold_range[1]) + self.game.hero_level * 5) * gold_multiplier)

        print(f"\n⚠️ {self.game.lang.get_text('danger_encounter')} Lv.{boss_level} {boss_name}!")
        print(f"{boss_name} - {self.game.lang.get_text('hp')}{self.game.lang.get_text('item_separator')}{boss_hp}, {self.game.lang.get_text('attack')}{self.game.lang.get_text('item_separator')}{boss_attack}, {self.game.lang.get_text('defense')}{self.game.lang.get_text('item_separator')}{boss_defense}")
        print(self.game.lang.get_text("boss_battle_start"))
        time.sleep(2)

        combat_round = 1
        while boss_hp > 0 and self.game.hero_hp > 0:
            print(f"\n--- {self.game.lang.get_text('round')} {combat_round} ---")

            action = self.get_combat_action()

            if action == "1" or action == "":  # 普通攻击
                base_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - boss_defense)

                critical_skill = self.game.lang.get_text('critical_skill')
                if critical_skill in self.game.hero_skills and random.random() < 0.15:
                    hero_damage = base_damage * 2
                    print(f"💥 {self.game.lang.get_text('critical_hit')} {boss_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
                else:
                    hero_damage = base_damage
                    print(f"🗡️ {self.game.lang.get_text('you_attack')} {boss_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")

                boss_hp -= hero_damage

                lifesteal_skill = self.game.lang.get_text('lifesteal_skill')
                if lifesteal_skill in self.game.hero_skills:
                    heal = int(hero_damage * 0.3)
                    self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                    print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")

            elif action == "2" and self.game.hero_potions > 0:
                heal_amount = random.randint(20, 40)
                self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                self.game.hero_potions -= 1
                print(f"🧪 {self.game.lang.get_text('poison')} {heal_amount}{self.game.lang.get_text('point_hp')}")
            elif action == "3":
                fireball_skill = self.game.lang.get_text('fireball_skill')
                if fireball_skill not in self.game.hero_skills:
                    print(self.game.lang.get_text("invalid_action"))
                    hero_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - boss_defense)
                    boss_hp -= hero_damage
                    print(f"🗡️ {self.game.lang.get_text('you_attack')} {boss_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")

                    lifesteal_skill = self.game.lang.get_text('lifesteal_skill')
                    if lifesteal_skill in self.game.hero_skills:
                        heal = int(hero_damage * 0.3)
                        self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                        print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")
                    continue
                base_damage = random.randint(self.game.hero_attack, int(self.game.hero_attack * 1.8))

                critical_skill = self.game.lang.get_text('critical_skill')
                if critical_skill in self.game.hero_skills and random.random() < 0.15:
                    hero_damage = int(base_damage * 1.5)
                    print(f"🔥💥 {self.game.lang.get_text('fireball_critical')} {boss_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
                else:
                    hero_damage = base_damage
                    print(f"🔥 {self.game.lang.get_text('fireball')} {boss_name}{self.game.lang.get_text('fireball_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")

                boss_hp -= hero_damage

                lifesteal_skill = self.game.lang.get_text('lifesteal_skill')
                if lifesteal_skill in self.game.hero_skills:
                    heal = int(hero_damage * 0.3)
                    self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                    print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")
            elif action == "4":
                healing_skill = self.game.lang.get_text('healing_skill')
                if healing_skill not in self.game.hero_skills:
                    print(self.game.lang.get_text("invalid_action"))
                    hero_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - boss_defense)
                    boss_hp -= hero_damage
                    print(f"🗡️ {self.game.lang.get_text('you_attack')} {boss_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")

                    lifesteal_skill = self.game.lang.get_text('lifesteal_skill')
                    if lifesteal_skill in self.game.hero_skills:
                        heal = int(hero_damage * 0.3)
                        self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                        print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")
                    continue
                if self.game.hero_hp >= self.game.hero_max_hp:
                    print("✨ " + self.game.lang.get_text("full_hp_no_heal"))
                else:
                    heal_amount = random.randint(1000, 2000)
                    self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                    print(f"✨ {self.game.lang.get_text('healing_spell')}{heal_amount}{self.game.lang.get_text('point_hp')}")
            else:
                print(self.game.lang.get_text("invalid_action"))
                hero_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - boss_defense)
                boss_hp -= hero_damage
                print(f"🗡️ {self.game.lang.get_text('you_attack')} {boss_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")

                lifesteal_skill = self.game.lang.get_text('lifesteal_skill')
                if lifesteal_skill in self.game.hero_skills:
                    heal = int(hero_damage * 0.3)
                    self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                    print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")

            if boss_hp <= 0:
                self.game.monsters_defeated += 2
                self.game.hero_exp += exp_gain
                self.game.hero_gold += gold_gain
                print(f"\n🎉 {self.game.lang.get_text('boss_victory')}{boss_name}!")
                print(f"{self.game.lang.get_text('got_exp')} {exp_gain} {self.game.lang.get_text('exp_points')} {self.game.lang.get_text('gold_coins')} {gold_gain}!")
                print("🏆 " + (self.game.lang.get_text('hero_badge') if self.game.lang.get_text('hero_badge') else "Got Hero Badge!"))

                self.check_level_up()

                lifesteal_skill = self.game.lang.get_text('lifesteal_skill_name')
                if lifesteal_skill not in self.game.hero_skills:
                    self.game.hero_hp = self.game.hero_max_hp
                    print(self.game.lang.get_text("victory_full_restore"))
                else:
                    print(self.game.lang.get_text("lifesteal_advantage"))

                self.game.events_encountered.append(f"{self.game.lang.get_text('defeat_boss_event')} {boss_name}, {self.game.lang.get_text('got_exp')} {exp_gain}")
                input(f"\n{self.game.lang.get_text('continue_prompt')}")
                break

            # Boss反击（更强）
            if combat_round % 3 == 0:
                dodge_skill = self.game.lang.get_text('dodge_skill')
                if dodge_skill in self.game.hero_skills and random.random() < 0.2:
                    print(f"💨 {self.game.lang.get_text('dodge_attack')} {boss_name} {self.game.lang.get_text('dodge_success')}")
                else:
                    boss_skill_damage = max(5, random.randint(boss_attack, int(boss_attack * 1.5)) - self.game.hero_defense)
                    self.game.hero_hp -= boss_skill_damage
                    print(f"💀 {self.game.lang.get_text('boss_powerful_attack')} {boss_skill_damage}{self.game.lang.get_text('point_damage')}!")
            else:
                dodge_skill = self.game.lang.get_text('dodge_skill')
                if dodge_skill in self.game.hero_skills and random.random() < 0.2:
                    print(f"💨 {self.game.lang.get_text('dodge_attack')}{boss_name}{self.game.lang.get_text('dodge_success')}")
                else:
                    boss_damage = max(1, random.randint(boss_attack // 2, boss_attack) - self.game.hero_defense)
                    self.game.hero_hp -= boss_damage
                    print(f"🩸 {boss_name}{self.game.lang.get_text('monster_attack')} {boss_damage}{self.game.lang.get_text('damage')}")

            print(f"{self.game.lang.get_text('your_hp')}{self.game.hero_hp}, {self.game.lang.get_text('boss_hp')}{boss_name}{self.game.lang.get_text('item_separator')}{boss_hp}")
            combat_round += 1
            time.sleep(1)

        self.game.show_hero_info()

    def ghost_combat(self, enemy_multiplier=1.0):
        """鬼魂战斗（无经验奖励，有特殊掉落）"""
        ghost_names = [
            self.game.lang.get_text("ghost_wandering"),
            self.game.lang.get_text("ghost_vengeful"),
            self.game.lang.get_text("ghost_soul_guardian")
        ]

        ghost_name = random.choice(ghost_names)

        ghost_hp = int(random.randint(15, 25) + self.game.hero_level * 3 * enemy_multiplier)
        ghost_attack = int(random.randint(8, 15) + self.game.hero_level * 1.5 * enemy_multiplier)
        ghost_defense = 0

        print(f"\n👻 {self.game.lang.get_text('encounter_ghost')} {ghost_name}!")
        print(f"{ghost_name} - {self.game.lang.get_text('hp')}{self.game.lang.get_text('item_separator')}{ghost_hp}, {self.game.lang.get_text('attack')}{self.game.lang.get_text('item_separator')}{ghost_attack}, {self.game.lang.get_text('defense')}{self.game.lang.get_text('item_separator')}0")
        print(self.game.lang.get_text("ghost_no_exp_warning"))
        print(self.game.lang.get_text("battle_start"))
        time.sleep(1)

        combat_round = 1
        while ghost_hp > 0 and self.game.hero_hp > 0:
            print(f"\n--- {self.game.lang.get_text('round')} {combat_round} ---")

            action = self.get_combat_action()

            if action == "1" or action == "":
                hero_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - ghost_defense)
                ghost_hp -= hero_damage
                print(f"🗡️ {self.game.lang.get_text('you_attack')} {ghost_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
            elif action == "2" and self.game.hero_potions > 0:
                heal_amount = random.randint(20, 40)
                self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                self.game.hero_potions -= 1
                print(f"🧪 {self.game.lang.get_text('poison')}{heal_amount}{self.game.lang.get_text('point_hp')}")
            elif action == "3":
                fireball_skill = self.game.lang.get_text('fireball_skill')
                if fireball_skill in self.game.hero_skills:
                    hero_damage = random.randint(self.game.hero_attack, int(self.game.hero_attack * 1.5))
                    ghost_hp -= hero_damage
                    print(f"🔥 {self.game.lang.get_text('fireball')} {ghost_name}{self.game.lang.get_text('fireball_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
                else:
                    hero_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - ghost_defense)
                    ghost_hp -= hero_damage
                    print(f"🗡️ {self.game.lang.get_text('you_attack')} {ghost_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
            elif action == "4":
                healing_skill = self.game.lang.get_text('healing_skill')
                if healing_skill in self.game.hero_skills:
                    if self.game.hero_hp >= self.game.hero_max_hp:
                        print("✨ " + self.game.lang.get_text("full_hp_no_heal"))
                    else:
                        heal_amount = random.randint(25, 40)
                        self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                        print(f"✨ {self.game.lang.get_text('healing_spell')}{heal_amount}{self.game.lang.get_text('point_hp')}")
                else:
                    hero_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - ghost_defense)
                    ghost_hp -= hero_damage
                    print(f"🗡️ {self.game.lang.get_text('you_attack')} {ghost_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
            else:
                print(self.game.lang.get_text("invalid_action"))
                hero_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - ghost_defense)
                ghost_hp -= hero_damage
                print(f"🗡️ {self.game.lang.get_text('you_attack')} {ghost_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")

            if ghost_hp <= 0:
                self.game.monsters_defeated += 1
                # 鬼魂不提供经验值，但有概率掉落装备或宝石
                drop_roll = random.randint(1, 10)
                if drop_roll <= 3:
                    print(f"\n👻 {self.game.lang.get_text('ghost_dissipate_nothing')}")
                elif drop_roll <= 6:
                    gold_found = random.randint(5, 15)
                    self.game.hero_gold += gold_found
                    print(f"\n👻 {self.game.lang.get_text('find_chest')} {gold_found} {self.game.lang.get_text('coins')}")
                    # 使用统一的多语言格式化函数处理鬼魂金币事件文本
                    ghost_gold_event = self.game.lang.format_text("event_text", "got_gold_from_ghost", gold_found)
                    self.game.events_encountered.append(ghost_gold_event)
                else:
                    # 获得一个随机装备（可能是特殊的）
                    from equipment import EquipmentSystem
                    equip_system = EquipmentSystem(self.game)
                    print(f"\n👻 {self.game.lang.get_text('ghost_leave_equipment')}")
                    equip_system.find_equipment()

                input(f"\n{self.game.lang.get_text('continue_prompt')}")
                break

            ghost_damage = max(1, random.randint(ghost_attack // 2, ghost_attack) - self.game.hero_defense)
            self.game.hero_hp -= ghost_damage
            print(f"🩸 {ghost_name}{self.game.lang.get_text('monster_attack')} {ghost_damage}{self.game.lang.get_text('damage')}")

            print(f"{self.game.lang.get_text('your_hp')} {self.game.hero_hp}, {self.game.lang.get_text('ghost_hp')}{ghost_name}{self.game.lang.get_text('item_separator')}{ghost_hp}")
            combat_round += 1
            time.sleep(1)

        self.game.show_hero_info()

    def check_level_up(self):
        """检查升级"""
        level_up_thresholds = {
            1: 100,
            2: 300,
            3: 600,
            4: 1000,
            5: 1500,
            6: 2500,
            7: 4000,
            8: 6000,
            9: 9000,
            10: 12000
        }

        for level, exp_needed in level_up_thresholds.items():
            if self.game.hero_exp >= exp_needed and self.game.hero_level < level:
                self.game.hero_level = level
                print(f"\n🎊 {self.game.lang.get_text('level_up')} {level}!")
                self.game.base_attack += 5
                self.game.base_defense += 3
                self.game.base_max_hp += 20
                self.game.hero_max_hp = self.game.base_max_hp
                self.game.hero_hp = self.game.hero_max_hp
                self.game.update_attributes()

                print(f"{self.game.lang.get_text('attack')} {self.game.hero_attack}, {self.game.lang.get_text('defense')} {self.game.hero_defense}, {self.game.lang.get_text('max_hp')} {self.game.hero_max_hp}")

                # 升级时有概率学习新技能
                if random.random() < 0.3:
                    from events import EventSystem
                    event_system = EventSystem(self.game)
                    event_system.learn_skill(level_up=True)

                input(f"\n{self.game.lang.get_text('continue_prompt')}")
