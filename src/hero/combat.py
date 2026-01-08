# -*- coding: utf-8 -*-
"""
战斗系统模块 - 处理战斗相关功能
"""

import random
import time
from .game_config import MONSTER_TEMPLATES, BOSS_TEMPLATES


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
        # 根据地图类型选择可能的怪物
        map_monsters = self.game.map_types[self.game.map_type]["monsters"]
        available_monsters = []
        
        # 为每个地图类型的怪物添加模板数据
        for monster_key in map_monsters:
            if monster_key in MONSTER_TEMPLATES:
                available_monsters.append(monster_key)
        
        # 根据英雄等级添加一些通用怪物
        if self.game.hero_level <= 2:
            general_monsters = ["goblin", "slime"]
        elif self.game.hero_level <= 5:
            general_monsters = ["skeleton", "wolf", "beast"]
        else:
            general_monsters = ["troll", "giant"]
        
        # 添加通用怪物到可用列表（如果不在地图怪物中）
        for monster_key in general_monsters:
            if monster_key in MONSTER_TEMPLATES and monster_key not in available_monsters:
                available_monsters.append(monster_key)
        
        # 随机选择一个怪物
        monster_key = random.choice(available_monsters)
        monster_template = MONSTER_TEMPLATES[monster_key]
        
        # 获取怪物名称
        monster_name = self.game.lang.get_text(monster_template["name_key"])
        
        # 根据英雄等级和难度计算怪物属性
        level_bonus = (self.game.hero_level - 1) * 2
        hp_range = monster_template["base_hp"]
        atk_range = monster_template["base_attack"]
        def_range = monster_template["base_defense"]
        gold_range = monster_template["gold_reward"]
        exp_range = monster_template["exp_reward"]
        
        # 计算怪物属性
        monster_hp = int((random.randint(hp_range[0], hp_range[1]) + level_bonus * 2) * enemy_multiplier)
        monster_attack = int((random.randint(atk_range[0], atk_range[1]) + level_bonus) * enemy_multiplier)
        monster_defense = int((random.randint(def_range[0], def_range[1]) + level_bonus // 2) * enemy_multiplier)
        
        # 计算奖励
        settings = self.game.difficulty_settings[self.game.difficulty]
        exp_multiplier = settings["exp_multiplier"]
        gold_multiplier = settings["gold_multiplier"]
        
        exp_gain = int((random.randint(exp_range[0], exp_range[1]) + self.game.hero_level * 3) * exp_multiplier)
        gold_gain = int((random.randint(gold_range[0], gold_range[1]) + self.game.hero_level * 2) * gold_multiplier)
        
        # 检查怪物是否有特殊能力
        monster_special = monster_template.get("special", None)
        is_elite = random.random() < 0.1  # 10%概率出现精英怪物
        
        if is_elite:
            monster_hp = int(monster_hp * 1.5)
            monster_attack = int(monster_attack * 1.5)
            monster_defense = int(monster_defense * 1.5)
            exp_gain = int(exp_gain * 1.5)
            gold_gain = int(gold_gain * 1.5)
            # 精英怪物名称前缀
            monster_name = f"🟣 {monster_name}"  # 紫色标记
        
        # 特殊怪物效果
        has_poison = monster_special == "poison"
        has_frost = monster_special == "frost"

        print(f"\n👹 {self.game.lang.get_text('encounter_monster')} {monster_name}!")
        print(f"{monster_name} - {self.game.lang.get_text('hp')}{self.game.lang.get_text('item_separator')}{monster_hp}, {self.game.lang.get_text('attack')}{self.game.lang.get_text('item_separator')}{monster_attack}, {self.game.lang.get_text('defense')}{self.game.lang.get_text('item_separator')}{monster_defense}")
        print(self.game.lang.get_text("battle_start"))
        time.sleep(1)

        # 记录战斗开始
        self.game.statistics.record_battle_start()

        combat_round = 1
        while monster_hp > 0 and self.game.hero_hp > 0:
            print(f"\n--- {self.game.lang.get_text('round')} {combat_round} ---")

            # 显示战斗选项
            action = self.get_combat_action()

            if action == "1" or action == "":  # 普通攻击
                base_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - monster_defense)
                
                # 应用暴击效果
                if random.random() < self.game.special_effects["crit_rate"]:
                    hero_damage = int(base_damage * (1.5 + self.game.special_effects["crit_damage"]))
                    print(f"💥 {self.game.lang.get_text('critical_hit')} {monster_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
                else:
                    hero_damage = base_damage
                    
                    # 应用背刺效果（首回合）
                    if combat_round == 1 and self.game.special_effects["backstab_damage"] > 0:
                        backstab_bonus = int(hero_damage * self.game.special_effects["backstab_damage"])
                        hero_damage += backstab_bonus
                        print(f"🔪 {self.game.lang.get_text('backstab')} +{backstab_bonus}!")
                        print(f"🗡️ {self.game.lang.get_text('you_attack')} {monster_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
                    else:
                        print(f"🗡️ {self.game.lang.get_text('you_attack')} {monster_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
                
                # 应用元素伤害
                if self.game.special_effects["ice_damage"] > 0:
                    hero_damage += self.game.special_effects["ice_damage"]
                    print(f"❄️ {self.game.lang.get_text('ice_damage')} +{self.game.special_effects['ice_damage']}!")
                
                if self.game.special_effects["fire_damage"] > 0:
                    hero_damage += self.game.special_effects["fire_damage"]
                    print(f"🔥 {self.game.lang.get_text('fire_damage')} +{self.game.special_effects['fire_damage']}!")
                
                monster_hp -= hero_damage
                
                # 应用吸血效果
                if self.game.special_effects["lifesteal_rate"] > 0:
                    heal = int(hero_damage * self.game.special_effects["lifesteal_rate"])
                    self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                    print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")
            elif action == "2" and self.game.hero_potions > 0:  # 使用药剂
                heal_amount = random.randint(20, 40)
                self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                self.game.hero_potions -= 1
                print(f"🧪 {self.game.lang.get_text('poison')} {heal_amount}{self.game.lang.get_text('point_hp')}")
                # 记录使用药剂
                self.game.statistics.record_potion_used()
            elif action == "3":  # 使用火球术技能
                fireball_skill = self.game.lang.get_text('fireball_skill')
                if fireball_skill in self.game.hero_skills:
                    base_damage = random.randint(self.game.hero_attack, int(self.game.hero_attack * 1.8))
                    base_damage = int(base_damage * (1.0 + self.game.special_effects["spell_power"]))
                    
                    # 应用暴击效果
                    if random.random() < self.game.special_effects["crit_rate"]:
                        hero_damage = int(base_damage * (1.5 + self.game.special_effects["crit_damage"]))
                        print(f"🔥💥 {self.game.lang.get_text('fireball_critical')} {monster_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
                    else:
                        hero_damage = base_damage
                        print(f"🔥 {self.game.lang.get_text('fireball')} {monster_name}{self.game.lang.get_text('fireball_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
                    
                    monster_hp -= hero_damage
                    # 记录使用技能
                    self.game.statistics.record_skill_used(fireball_skill)
                    
                    # 应用吸血效果
                    if self.game.special_effects["lifesteal_rate"] > 0:
                        heal = int(hero_damage * self.game.special_effects["lifesteal_rate"])
                        self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                        print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")
                else:
                    # 如果没有火球术技能，改为普通攻击
                    base_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - monster_defense)
                    
                    # 应用暴击效果
                    if random.random() < self.game.special_effects["crit_rate"]:
                        hero_damage = int(base_damage * (1.5 + self.game.special_effects["crit_damage"]))
                        print(f"💥 {self.game.lang.get_text('critical_hit')} {monster_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
                    else:
                        hero_damage = base_damage
                        print(f"🗡️ {self.game.lang.get_text('you_attack')} {monster_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
                    
                    monster_hp -= hero_damage
                    
                    # 应用吸血效果
                    if self.game.special_effects["lifesteal_rate"] > 0:
                        heal = int(hero_damage * self.game.special_effects["lifesteal_rate"])
                        self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                        print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")
            elif action == "4":  # 使用治疗术技能
                healing_skill = self.game.lang.get_text('healing_skill')
                if healing_skill in self.game.hero_skills:
                    if self.game.hero_hp >= self.game.hero_max_hp:
                        print("✨ " + self.game.lang.get_text("full_hp_no_heal"))
                    else:
                        heal_amount = random.randint(100, 200)
                        heal_amount = int(heal_amount * (1.0 + self.game.special_effects["healing_rate"]))
                        self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                        print(f"✨ {self.game.lang.get_text('healing_spell')}{heal_amount}{self.game.lang.get_text('point_hp')}")
                        # 记录使用技能
                        self.game.statistics.record_skill_used(healing_skill)
                else:
                    # 如果没有治疗术技能，改为普通攻击
                    base_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - monster_defense)
                    
                    # 应用暴击效果
                    if random.random() < self.game.special_effects["crit_rate"]:
                        hero_damage = int(base_damage * (1.5 + self.game.special_effects["crit_damage"]))
                        print(f"💥 {self.game.lang.get_text('critical_hit')} {monster_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
                    else:
                        hero_damage = base_damage
                        print(f"🗡️ {self.game.lang.get_text('you_attack')} {monster_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
                    
                    monster_hp -= hero_damage
                    
                    # 应用吸血效果
                    if self.game.special_effects["lifesteal_rate"] > 0:
                        heal = int(hero_damage * self.game.special_effects["lifesteal_rate"])
                        self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                        print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")
            else:
                print(self.game.lang.get_text("invalid_action"))
                base_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - monster_defense)
                
                # 应用暴击效果
                if random.random() < self.game.special_effects["crit_rate"]:
                    hero_damage = int(base_damage * (1.5 + self.game.special_effects["crit_damage"]))
                    print(f"💥 {self.game.lang.get_text('critical_hit')} {monster_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
                else:
                    hero_damage = base_damage
                    print(f"🗡️ {self.game.lang.get_text('you_attack')} {monster_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
                
                monster_hp -= hero_damage
                
                # 应用吸血效果
                if self.game.special_effects["lifesteal_rate"] > 0:
                    heal = int(hero_damage * self.game.special_effects["lifesteal_rate"])
                    self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                    print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")

            if monster_hp <= 0:
                self.game.monsters_defeated += 1
                self.game.hero_exp += exp_gain
                self.game.hero_gold += gold_gain
                print(f"\n🎉 {self.game.lang.get_text('battle_victory')} {monster_name}!")
                print(f"{self.game.lang.get_text('got_exp')} {exp_gain} {self.game.lang.get_text('exp_points')} {self.game.lang.get_text('gold_coins')} {gold_gain}!")

                # 记录战斗胜利
                self.game.statistics.record_battle_victory(monster_name, is_boss=False)
                self.game.statistics.record_gold_earned(gold_gain)
                self.game.statistics.record_exp_earned(exp_gain)

                # 检查升级
                self.check_level_up()

                input(f"\n{self.game.lang.get_text('continue_prompt')}")
                break

            # 怪物反击
            # 应用闪避效果
            if random.random() < self.game.special_effects["dodge_rate"]:
                print(f"💨 {self.game.lang.get_text('dodge_attack')} {monster_name} {self.game.lang.get_text('dodge_success')}")
            else:
                # 应用反击效果
                if random.random() < self.game.special_effects["counter_attack_rate"]:
                    counter_damage = max(1, int(monster_attack * 0.5) - self.game.hero_defense)
                    monster_hp -= counter_damage
                    print(f"🔄 {self.game.lang.get_text('counter_attack')} {counter_damage}{self.game.lang.get_text('point_damage')}!")
                
                monster_damage = max(1, random.randint(monster_attack // 2, monster_attack) - self.game.hero_defense)
                
                # 应用抗性效果
                if monster_template.get("special") == "poison" and self.game.special_effects["holy_resistance"] > 0:
                    monster_damage = int(monster_damage * (1 - self.game.special_effects["holy_resistance"]))
                
                if monster_template.get("special") == "fire" and self.game.special_effects["fire_resistance"] > 0:
                    monster_damage = int(monster_damage * (1 - self.game.special_effects["fire_resistance"]))
                
                self.game.hero_hp -= monster_damage
                print(f"🩸 {monster_name}{self.game.lang.get_text('monster_attack')} {monster_damage}{self.game.lang.get_text('damage')}")
            
            # 特殊能力效果
            if has_poison and random.random() < 0.3:  # 30%概率施加中毒
                self.game.add_status_effect("poison", 3)
                print(f"☠️ {monster_name} {self.game.lang.get_text('monster_attack')}{self.game.lang.get_text('poisoned')}")
            
            if has_frost and random.random() < 0.3:  # 30%概率施加冰霜
                self.game.add_status_effect("frost", 3)
                print(f"❄️ {monster_name} {self.game.lang.get_text('monster_attack')}{self.game.lang.get_text('frost_effect_desc')}")

            print(f"{self.game.lang.get_text('your_hp')} {self.game.hero_hp}, {self.game.lang.get_text('monster_hp')} {monster_name}{self.game.lang.get_text('item_separator')}{monster_hp}")
            combat_round += 1
            time.sleep(1)

        # 记录战斗失败
        if self.game.hero_hp <= 0:
            self.game.statistics.record_battle_defeat()

        self.game.show_hero_info()

    def boss_combat(self, enemy_multiplier=1.0):
        """Boss战斗系统"""
        # 根据地图类型选择对应的Boss
        map_type = self.game.map_type
        if map_type in BOSS_TEMPLATES:
            boss_template = BOSS_TEMPLATES[map_type]
        else:
            # 如果没有为该地图定义Boss，使用默认Boss
            boss_template = BOSS_TEMPLATES["plains"]
        
        # 获取Boss名称
        boss_name = self.game.lang.get_text(boss_template["name_key"])
        boss_level = max(1, self.game.hero_level + random.randint(-1, 1))
        
        # 获取Boss属性范围
        hp_range = boss_template["base_hp"]
        atk_range = boss_template["base_attack"]
        def_range = boss_template["base_defense"]
        gold_range = boss_template["gold_reward"]
        exp_range = boss_template["exp_reward"]
        
        # 获取Boss技能列表
        boss_skills = boss_template["skills"]
        
        # 应用难度倍数
        level_bonus = self.game.hero_level * 3
        max_boss_hp = int((random.randint(hp_range[0], hp_range[1]) + level_bonus * 3) * enemy_multiplier)
        boss_hp = max_boss_hp
        boss_attack = int((random.randint(atk_range[0], atk_range[1]) + level_bonus * 2) * enemy_multiplier)
        boss_defense = int((random.randint(def_range[0], def_range[1]) + level_bonus) * enemy_multiplier)
        
        # 应用难度经验/金币倍数
        settings = self.game.difficulty_settings[self.game.difficulty]
        exp_multiplier = settings["exp_multiplier"]
        gold_multiplier = settings["gold_multiplier"]
        
        exp_gain = int((random.randint(exp_range[0], exp_range[1]) + self.game.hero_level * 8) * exp_multiplier)
        gold_gain = int((random.randint(gold_range[0], gold_range[1]) + self.game.hero_level * 5) * gold_multiplier)
        
        # Boss战标志
        boss_enraged = False  # 是否进入狂暴状态
        next_skill_round = 3  # 下次使用技能的回合

        print(f"\n⚠️ {self.game.lang.get_text('danger_encounter')} Lv.{boss_level} {boss_name}!")
        print(f"{boss_name} - {self.game.lang.get_text('hp')}{self.game.lang.get_text('item_separator')}{boss_hp}, {self.game.lang.get_text('attack')}{self.game.lang.get_text('item_separator')}{boss_attack}, {self.game.lang.get_text('defense')}{self.game.lang.get_text('item_separator')}{boss_defense}")
        print(self.game.lang.get_text("boss_battle_start"))
        time.sleep(2)

        # 记录战斗开始
        self.game.statistics.record_battle_start()

        combat_round = 1
        while boss_hp > 0 and self.game.hero_hp > 0:
            print(f"\n--- {self.game.lang.get_text('round')} {combat_round} ---")

            # 检查Boss是否进入狂暴状态（血量低于50%）
            if not boss_enraged and boss_hp <= max_boss_hp * 0.5:
                boss_enraged = True
                boss_attack = int(boss_attack * 1.3)  # 攻击力提升30%
                print(f"🔥 {self.game.lang.get_text('boss_enraged')}")

            action = self.get_combat_action()

            if action == "1" or action == "":  # 普通攻击
                base_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - boss_defense)
                
                # 应用暴击效果（优先使用装备的暴击率）
                if random.random() < self.game.special_effects["crit_rate"]:
                    hero_damage = int(base_damage * (1.5 + self.game.special_effects["crit_damage"]))
                    print(f"💥 {self.game.lang.get_text('critical_hit')} {boss_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
                else:
                    # 如果没有装备暴击，检查技能暴击
                    critical_skill = self.game.lang.get_text('critical_skill')
                    if critical_skill in self.game.hero_skills and random.random() < 0.15:
                        hero_damage = base_damage * 2
                        print(f"💥 {self.game.lang.get_text('critical_hit')} {boss_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
                    else:
                        hero_damage = base_damage
                        
                        # 应用背刺效果（首回合）
                        if combat_round == 1 and self.game.special_effects["backstab_damage"] > 0:
                            backstab_bonus = int(hero_damage * self.game.special_effects["backstab_damage"])
                            hero_damage += backstab_bonus
                            print(f"🔪 {self.game.lang.get_text('backstab')} +{backstab_bonus}!")
                            print(f"🗡️ {self.game.lang.get_text('you_attack')} {boss_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
                        else:
                            print(f"🗡️ {self.game.lang.get_text('you_attack')} {boss_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
                
                # 应用元素伤害
                if self.game.special_effects["ice_damage"] > 0:
                    hero_damage += self.game.special_effects["ice_damage"]
                    print(f"❄️ {self.game.lang.get_text('ice_damage')} +{self.game.special_effects['ice_damage']}!")
                
                if self.game.special_effects["fire_damage"] > 0:
                    hero_damage += self.game.special_effects["fire_damage"]
                    print(f"🔥 {self.game.lang.get_text('fire_damage')} +{self.game.special_effects['fire_damage']}!")
                
                boss_hp -= hero_damage

                # 应用吸血效果（优先使用装备的吸血）
                if self.game.special_effects["lifesteal_rate"] > 0:
                    heal = int(hero_damage * self.game.special_effects["lifesteal_rate"])
                    self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                    print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")
                else:
                    # 如果没有装备吸血，检查技能吸血
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
                # 记录使用药剂
                self.game.statistics.record_potion_used()
            elif action == "3":
                fireball_skill = self.game.lang.get_text('fireball_skill')
                if fireball_skill not in self.game.hero_skills:
                    print(self.game.lang.get_text("invalid_action"))
                    base_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - boss_defense)
                    
                    # 应用暴击效果
                    if random.random() < self.game.special_effects["crit_rate"]:
                        hero_damage = int(base_damage * (1.5 + self.game.special_effects["crit_damage"]))
                        print(f"💥 {self.game.lang.get_text('critical_hit')} {boss_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
                    else:
                        hero_damage = base_damage
                        print(f"🗡️ {self.game.lang.get_text('you_attack')} {boss_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
                    
                    boss_hp -= hero_damage

                    # 应用吸血效果
                    if self.game.special_effects["lifesteal_rate"] > 0:
                        heal = int(hero_damage * self.game.special_effects["lifesteal_rate"])
                        self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                        print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")
                    continue
                
                base_damage = random.randint(self.game.hero_attack, int(self.game.hero_attack * 1.8))
                base_damage = int(base_damage * (1.0 + self.game.special_effects["spell_power"]))

                # 应用暴击效果（优先使用装备的暴击率）
                if random.random() < self.game.special_effects["crit_rate"]:
                    hero_damage = int(base_damage * (1.5 + self.game.special_effects["crit_damage"]))
                    print(f"🔥💥 {self.game.lang.get_text('fireball_critical')} {boss_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
                else:
                    # 如果没有装备暴击，检查技能暴击
                    critical_skill = self.game.lang.get_text('critical_skill')
                    if critical_skill in self.game.hero_skills and random.random() < 0.15:
                        hero_damage = int(base_damage * 1.5)
                        print(f"🔥💥 {self.game.lang.get_text('fireball_critical')} {boss_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
                    else:
                        hero_damage = base_damage
                        print(f"🔥 {self.game.lang.get_text('fireball')} {boss_name}{self.game.lang.get_text('fireball_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")

                boss_hp -= hero_damage
                # 记录使用火球术技能
                self.game.statistics.record_skill_used(fireball_skill)

                # 应用吸血效果（优先使用装备的吸血）
                if self.game.special_effects["lifesteal_rate"] > 0:
                    heal = int(hero_damage * self.game.special_effects["lifesteal_rate"])
                    self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                    print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")
            elif action == "4":
                healing_skill = self.game.lang.get_text('healing_skill')
                if healing_skill not in self.game.hero_skills:
                    print(self.game.lang.get_text("invalid_action"))
                    base_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - boss_defense)
                    
                    # 应用暴击效果
                    if random.random() < self.game.special_effects["crit_rate"]:
                        hero_damage = int(base_damage * (1.5 + self.game.special_effects["crit_damage"]))
                        print(f"💥 {self.game.lang.get_text('critical_hit')} {boss_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
                    else:
                        hero_damage = base_damage
                        print(f"🗡️ {self.game.lang.get_text('you_attack')} {boss_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
                    
                    boss_hp -= hero_damage

                    # 应用吸血效果
                    if self.game.special_effects["lifesteal_rate"] > 0:
                        heal = int(hero_damage * self.game.special_effects["lifesteal_rate"])
                        self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                        print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")
                    continue
                if self.game.hero_hp >= self.game.hero_max_hp:
                    print("✨ " + self.game.lang.get_text("full_hp_no_heal"))
                else:
                    heal_amount = random.randint(100, 200)
                    heal_amount = int(heal_amount * (1.0 + self.game.special_effects["healing_rate"]))
                    self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                    print(f"✨ {self.game.lang.get_text('healing_spell')}{heal_amount}{self.game.lang.get_text('point_hp')}")
                    # 记录使用治疗术技能
                    self.game.statistics.record_skill_used(healing_skill)
            else:
                print(self.game.lang.get_text("invalid_action"))
                base_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - boss_defense)
                
                # 应用暴击效果
                if random.random() < self.game.special_effects["crit_rate"]:
                    hero_damage = int(base_damage * (1.5 + self.game.special_effects["crit_damage"]))
                    print(f"💥 {self.game.lang.get_text('critical_hit')} {boss_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
                else:
                    hero_damage = base_damage
                    print(f"🗡️ {self.game.lang.get_text('you_attack')} {boss_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
                
                boss_hp -= hero_damage

                # 应用吸血效果
                if self.game.special_effects["lifesteal_rate"] > 0:
                    heal = int(hero_damage * self.game.special_effects["lifesteal_rate"])
                    self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                    print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")

            if boss_hp <= 0:
                self.game.monsters_defeated += 2
                self.game.hero_exp += exp_gain
                self.game.hero_gold += gold_gain
                print(f"\n🎉 {self.game.lang.get_text('boss_victory')}{boss_name}!")
                print(f"{self.game.lang.get_text('got_exp')} {exp_gain} {self.game.lang.get_text('exp_points')} {self.game.lang.get_text('gold_coins')} {gold_gain}!")
                print("🏆 " + (self.game.lang.get_text('hero_badge') if self.game.lang.get_text('hero_badge') else "Got Hero Badge!"))

                # 记录Boss战胜利
                self.game.statistics.record_battle_victory(boss_name, is_boss=True)
                self.game.statistics.record_gold_earned(gold_gain)
                self.game.statistics.record_exp_earned(exp_gain)

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

            # Boss反击和技能系统
            # 检查Boss是否使用技能
            if combat_round == next_skill_round and boss_skills:
                # 随机选择一个Boss技能
                skill = random.choice(boss_skills)
                skill_name_key = f"boss_skill_{skill}"
                skill_name = self.game.lang.get_text(skill_name_key)
                
                print(f"💀 {self.game.lang.get_text('boss_skill_used')} {skill_name}!")
                
                # 应用不同技能的效果
                if skill == "power_strike":
                    skill_damage = max(10, random.randint(int(boss_attack * 1.2), int(boss_attack * 1.8)) - self.game.hero_defense)
                    self.game.hero_hp -= skill_damage
                    print(f"{boss_name} {skill_name} {self.game.lang.get_text('caused_damage')} {skill_damage}{self.game.lang.get_text('point_damage')}!")
                
                elif skill == "heal":
                    heal_amount = int(max_boss_hp * 0.15)  # 恢复15%最大血量
                    boss_hp = min(boss_hp + heal_amount, max_boss_hp)
                    print(f"{boss_name} {skill_name} {heal_amount}{self.game.lang.get_text('point_hp')}!")
                
                elif skill == "root_trap":
                    # 陷阱效果，下回合英雄无法攻击
                    print(f"{boss_name} {skill_name}!")
                    print(self.game.lang.get_text("root_trap_effect"))
                    # 这里可以添加一个状态效果来表示被困
                    # 为简单起见，这里只打印提示
                
                elif skill == "nature_heal":
                    heal_amount = int(max_boss_hp * 0.2)  # 恢复20%最大血量
                    boss_hp = min(boss_hp + heal_amount, max_boss_hp)
                    print(f"{boss_name} {skill_name} {heal_amount}{self.game.lang.get_text('point_hp')}!")
                
                elif skill == "sandstorm":
                    skill_damage = max(5, random.randint(int(boss_attack * 0.8), int(boss_attack * 1.2)) - self.game.hero_defense)
                    self.game.hero_hp -= skill_damage
                    print(f"{boss_name} {skill_name} {self.game.lang.get_text('caused_damage')} {skill_damage}{self.game.lang.get_text('point_damage')}!")
                
                elif skill == "summon_minions":
                    print(f"{boss_name} {skill_name}!")
                    print(self.game.lang.get_text("summon_minions_effect"))
                    # 这里可以添加一个状态效果表示下次攻击增强
                    # 为简单起见，这里只打印提示
                
                elif skill == "dragon_breath":
                    skill_damage = max(15, random.randint(int(boss_attack * 1.3), int(boss_attack * 1.7)) - self.game.hero_defense)
                    self.game.hero_hp -= skill_damage
                    print(f"{boss_name} {skill_name} {self.game.lang.get_text('caused_damage')} {skill_damage}{self.game.lang.get_text('point_damage')}!")
                
                elif skill == "poison_bite":
                    skill_damage = max(8, random.randint(int(boss_attack * 0.9), int(boss_attack * 1.3)) - self.game.hero_defense)
                    self.game.hero_hp -= skill_damage
                    self.game.add_status_effect("poison", 3)
                    print(f"{boss_name} {skill_name} {self.game.lang.get_text('caused_damage')} {skill_damage}{self.game.lang.get_text('point_damage')}!")
                    print(f"{boss_name} {self.game.lang.get_text('monster_attack')}{self.game.lang.get_text('poisoned')}")
                
                elif skill == "regeneration":
                    heal_amount = int(max_boss_hp * 0.1)  # 恢复10%最大血量
                    boss_hp = min(boss_hp + heal_amount, max_boss_hp)
                    print(f"{boss_name} {skill_name} {heal_amount}{self.game.lang.get_text('point_hp')}!")
                
                elif skill == "blizzard":
                    skill_damage = max(10, random.randint(int(boss_attack * 1.0), int(boss_attack * 1.4)) - self.game.hero_defense)
                    self.game.hero_hp -= skill_damage
                    self.game.add_status_effect("frost", 3)
                    print(f"{boss_name} {skill_name} {self.game.lang.get_text('caused_damage')} {skill_damage}{self.game.lang.get_text('point_damage')}!")
                    print(f"{boss_name} {self.game.lang.get_text('monster_attack')}{self.game.lang.get_text('frost_effect_desc')}")
                
                elif skill == "ice_prison":
                    # 冰牢效果，下回合英雄无法攻击
                    print(f"{boss_name} {skill_name}!")
                    print(self.game.lang.get_text("ice_prison_effect"))
                    # 这里可以添加一个状态效果来表示被困
                    # 为简单起见，这里只打印提示
                
                # 设置下次使用技能的回合
                next_skill_round = combat_round + 3
            
            else:
                # 普通攻击
                # 应用闪避效果（优先使用装备的闪避率）
                if random.random() < self.game.special_effects["dodge_rate"]:
                    print(f"💨 {self.game.lang.get_text('dodge_attack')} {boss_name} {self.game.lang.get_text('dodge_success')}")
                else:
                    # 如果没有装备闪避，检查技能闪避
                    dodge_skill = self.game.lang.get_text('dodge_skill')
                    if dodge_skill in self.game.hero_skills and random.random() < 0.2:
                        print(f"💨 {self.game.lang.get_text('dodge_attack')} {boss_name} {self.game.lang.get_text('dodge_success')}")
                    else:
                        # 应用反击效果
                        if random.random() < self.game.special_effects["counter_attack_rate"]:
                            counter_damage = max(1, int(boss_attack * 0.5) - self.game.hero_defense)
                            boss_hp -= counter_damage
                            print(f"🔄 {self.game.lang.get_text('counter_attack')} {counter_damage}{self.game.lang.get_text('point_damage')}!")
                        
                        boss_damage = max(1, random.randint(boss_attack // 2, boss_attack) - self.game.hero_defense)
                        
                        # 应用抗性效果
                        if boss_template.get("special") == "poison" and self.game.special_effects["holy_resistance"] > 0:
                            boss_damage = int(boss_damage * (1 - self.game.special_effects["holy_resistance"]))
                        
                        if boss_template.get("special") == "fire" and self.game.special_effects["fire_resistance"] > 0:
                            boss_damage = int(boss_damage * (1 - self.game.special_effects["fire_resistance"]))
                        
                        self.game.hero_hp -= boss_damage
                        print(f"🩸 {boss_name}{self.game.lang.get_text('monster_attack')} {boss_damage}{self.game.lang.get_text('damage')}")

            print(f"{self.game.lang.get_text('your_hp')}{self.game.hero_hp}, {self.game.lang.get_text('boss_hp')}{boss_name}{self.game.lang.get_text('item_separator')}{boss_hp}")
            combat_round += 1
            time.sleep(1)

        # 记录战斗失败
        if self.game.hero_hp <= 0:
            self.game.statistics.record_battle_defeat()

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

        # 记录战斗开始
        self.game.statistics.record_battle_start()

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
                # 记录使用药剂
                self.game.statistics.record_potion_used()
            elif action == "3":
                fireball_skill = self.game.lang.get_text('fireball_skill')
                if fireball_skill in self.game.hero_skills:
                    hero_damage = random.randint(self.game.hero_attack, int(self.game.hero_attack * 1.5))
                    ghost_hp -= hero_damage
                    print(f"🔥 {self.game.lang.get_text('fireball')} {ghost_name}{self.game.lang.get_text('fireball_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
                    # 记录使用技能
                    self.game.statistics.record_skill_used(fireball_skill)
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
                        # 记录使用技能
                        self.game.statistics.record_skill_used(healing_skill)
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
                # 记录战斗胜利
                self.game.statistics.record_battle_victory(ghost_name, is_boss=False)

                # 鬼魂不提供经验值，但有概率掉落装备或宝石
                drop_roll = random.randint(1, 10)
                if drop_roll <= 3:
                    print(f"\n👻 {self.game.lang.get_text('ghost_dissipate_nothing')}")
                elif drop_roll <= 6:
                    gold_found = random.randint(5, 15)
                    self.game.hero_gold += gold_found
                    print(f"\n👻 {self.game.lang.get_text('find_chest')} {gold_found} {self.game.lang.get_text('coins')}")
                    # 记录获得金币
                    self.game.statistics.record_gold_earned(gold_found)
                    # 使用统一的多语言格式化函数处理鬼魂金币事件文本
                    ghost_gold_event = self.game.lang.format_text("event_text", "got_gold_from_ghost", gold_found)
                    self.game.events_encountered.append(ghost_gold_event)
                else:
                    # 获得一个随机装备（可能是特殊的）
                    from .equipment import EquipmentSystem
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

        # 记录战斗失败
        if self.game.hero_hp <= 0:
            self.game.statistics.record_battle_defeat()

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
                    from .events import EventSystem
                    event_system = EventSystem(self.game)
                    event_system.learn_skill(level_up=True)

                input(f"\n{self.game.lang.get_text('continue_prompt')}")
