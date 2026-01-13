# -*- coding: utf-8 -*-
"""
战斗系统模块 - 处理战斗相关功能
"""

import random
import time
from .game_config import MONSTER_TEMPLATES, BOSS_TEMPLATES, CLASS_DEFINITIONS


class CombatSystem:
    """战斗系统类"""

    def __init__(self, game):
        self.game = game
    
    def get_skill_name(self, skill_id):
        """获取技能名称，处理多语言问题"""
        # 检查技能ID是否已经包含"_skill"后缀
        if skill_id.endswith("_skill"):
            skill_name_key = skill_id
        else:
            skill_name_key = f'{skill_id}_skill'
        return self.game.lang.get_text(skill_name_key)

    def apply_class_passives(self):
        """应用职业被动效果"""
        class_info = CLASS_DEFINITIONS.get(self.game.hero_class, {})
        passive_effects = class_info.get("passive_effects", {})
        
        # 战士被动：减伤和生命恢复
        if self.game.hero_class == "warrior":
            if passive_effects.get("damage_reduction", 0) > 0:
                self.game.special_effects["damage_reduction"] = passive_effects["damage_reduction"]
            
            # 每回合恢复生命值
            if passive_effects.get("hp_regen_per_turn", 0) > 0:
                hp_regen = int(self.game.hero_max_hp * passive_effects["hp_regen_per_turn"])
                if hp_regen > 0:
                    self.game.hero_hp = min(self.game.hero_hp + hp_regen, self.game.hero_max_hp)
                    print(f"🛡️ {self.game.lang.get_text('warrior_hp_regen')} +{hp_regen} HP!")
        
        # 法师被动：法力恢复
        elif self.game.hero_class == "mage":
            if hasattr(self.game, 'hero_mana') and passive_effects.get("mana_regen", 0) > 0:
                mana_regen = passive_effects["mana_regen"]
                self.game.hero_mana = min(self.game.hero_mana + mana_regen, self.game.class_max_mana)
                print(f"✨ {self.game.lang.get_text('mage_mana_regen')} +{mana_regen} MP!")
        
        # 刺客被动：暴击和闪避
        elif self.game.hero_class == "assassin":
            if passive_effects.get("crit_rate", 0) > 0:
                self.game.special_effects["crit_rate"] += passive_effects["crit_rate"]
            if passive_effects.get("dodge_chance", 0) > 0:
                self.game.special_effects["dodge_rate"] += passive_effects["dodge_chance"]

    def handle_skill_by_id(self, skill_id, monster_name, monster_hp, combat_round, monster_defense=0):
        """统一处理技能效果，根据skill_id处理所有技能"""
        from .game_config import CLASS_DEFINITIONS, SKILL_TREES
        
        # 获取技能名称用于显示
        skill_name = self.get_skill_name(skill_id)
        
        # 处理药剂
        if skill_id == "use_potion":
            if self.game.hero_potions > 0:
                heal_amount = random.randint(20, 40)
                self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                self.game.hero_potions -= 1
                print(f"🧪 {self.game.lang.get_text('poison')} {heal_amount}{self.game.lang.get_text('point_hp')}")
                # 记录使用药剂
                self.game.statistics.record_potion_used()
            else:
                print(self.game.lang.get_text("no_potion"))
            return monster_hp
        
        # 处理职业技能
        class_info = CLASS_DEFINITIONS.get(self.game.hero_class, {})
        class_skills = class_info.get("class_skills", [])
        
        if skill_id in class_skills:
            return self.handle_class_skill(skill_id, monster_name, monster_hp, combat_round)
        
        # 获取技能效果
        if self.game.skill_tree and skill_id in self.game.skill_tree.skill_nodes:
            skill_node = self.game.skill_tree.skill_nodes[skill_id]
            skill_level = self.game.skill_tree.learned_skills.get(skill_id, 0)
            skill_data = SKILL_TREES.get(self.game.hero_class, {}).get(skill_id, {})
            skill_category = skill_data.get("category", "core")
            
            # 处理不同类别的技能
            if skill_category == "combat":
                return self._handle_combat_skill(skill_id, skill_node, skill_level, monster_name, monster_hp, combat_round, monster_defense)
            elif skill_category == "passive":
                return self._handle_passive_skill(skill_id, skill_node, skill_level, monster_name, monster_hp, combat_round, monster_defense)
            elif skill_category == "ultimate":
                return self._handle_ultimate_skill(skill_id, skill_node, skill_level, monster_name, monster_hp, combat_round, monster_defense)
            else:  # core技能
                return self._handle_core_skill(skill_id, skill_node, skill_level, monster_name, monster_hp, combat_round, monster_defense)
        
        # 对于未知技能，不造成伤害
        print(self.game.lang.get_text("invalid_action"))
        return monster_hp

    def _handle_core_skill(self, skill_id, skill_node, skill_level, monster_name, monster_hp, combat_round, monster_defense=0):
        """处理核心技能"""
        from .game_config import SKILL_TREES
        
        skill_data = SKILL_TREES.get(self.game.hero_class, {}).get(skill_id, {})
        skill_name = self.get_skill_name(skill_id)
        
        # 计算基础伤害
        base_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - monster_defense)
        
        # 应用技能效果
        effects_per_level = skill_data.get("effects_per_level", [])
        if effects_per_level:
            # 核心技能通常是增加基础属性
            effect_value = effects_per_level[0] * skill_level
            if skill_id == "power_strike":  # 战士力量打击
                base_damage += int(effect_value)
            elif skill_id == "fireball":    # 法师火球术
                base_damage = int(base_damage * 1.2) + int(effect_value)
            elif skill_id == "backstab":    # 刺客背刺
                backstab_bonus = int(base_damage * (0.2 + effect_value))
                base_damage += backstab_bonus
        
        # 应用暴击效果
        if random.random() < self.game.special_effects["crit_rate"]:
            hero_damage = int(base_damage * (1.5 + self.game.special_effects["crit_damage"]))
            print(f"💥 {self.game.lang.get_text('critical_hit')} {skill_name} {monster_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
        else:
            hero_damage = base_damage
            print(f"⚔️ {skill_name} {monster_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}!")
        
        monster_hp -= hero_damage
        
        # 记录技能使用
        self.game.statistics.record_skill_used(skill_name)
        return monster_hp

    def _handle_combat_skill(self, skill_id, skill_node, skill_level, monster_name, monster_hp, combat_round, monster_defense=0):
        """处理战斗技能"""
        from .game_config import SKILL_TREES
        
        skill_data = SKILL_TREES.get(self.game.hero_class, {}).get(skill_id, {})
        skill_name = self.get_skill_name(skill_id)
        effects_per_level = skill_data.get("effects_per_level", [])
        
        if skill_id == "shield_bash":  # 战士盾击
            base_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - monster_defense)
            
            # 应用技能效果
            if effects_per_level:
                damage_multiplier = effects_per_level[0]
                attack_reduction = effects_per_level[1] * skill_level
                hero_damage = int(base_damage * damage_multiplier)
                
                # 降低敌人攻击力
                self.game.enemy_attack_debuff = attack_reduction
                print(f"🔻 {monster_name} {self.game.lang.get_text('attack_reduced_percent')} {int(attack_reduction * 100)}%!")
            
            print(f"🛡️ {skill_name} {hero_damage}{self.game.lang.get_text('point_damage')}!")
            monster_hp -= hero_damage
            
        elif skill_id == "frost_armor":  # 法师冰霜护甲
            if effects_per_level:
                duration = effects_per_level[0]
                defense_multiplier = effects_per_level[1] * skill_level
                self.game.frost_armor_active = duration
                print(f"❄️ {skill_name} {self.game.lang.get_text('defense_reduced')} {int(defense_multiplier * 100)}%!")
            
        elif skill_id == "shadow_strike":  # 刺客影袭
            total_damage = 0
            base_hits = 2
            
            if effects_per_level:
                damage_multiplier = effects_per_level[0]
                extra_hits = int(effects_per_level[1] * skill_level)
                hits = base_hits + extra_hits
            
            for i in range(hits):
                base_damage = max(1, int(random.randint(self.game.hero_attack // 3, self.game.hero_attack // 2)) - monster_defense)
                hero_damage = int(base_damage * damage_multiplier)
                
                # 高暴击率
                if random.random() < (self.game.special_effects["crit_rate"] + 0.2):
                    hero_damage = int(hero_damage * 2)
                    print(f"💥 {skill_name} {hero_damage}{self.game.lang.get_text('point_damage')}!")
                else:
                    print(f"🔪 {skill_name} {hero_damage}{self.game.lang.get_text('point_damage')}!")
                
                monster_hp -= hero_damage
                total_damage += hero_damage
                
                if monster_hp <= 0:
                    break
            
            print(f"⚔️ {self.game.lang.get_text('shadow_strike_hits')} {total_damage}{self.game.lang.get_text('point_damage')}!")
        
        # 记录技能使用
        self.game.statistics.record_skill_used(skill_name)
        return monster_hp

    def _handle_passive_skill(self, skill_id, skill_node, skill_level, monster_name, monster_hp, combat_round, monster_defense=0):
        """处理被动技能"""
        from .game_config import SKILL_TREES
        
        skill_data = SKILL_TREES.get(self.game.hero_class, {}).get(skill_id, {})
        skill_name = self.get_skill_name(skill_id)
        effects_per_level = skill_data.get("effects_per_level", [])
        
        if skill_id == "iron_will":  # 战士钢铁意志
            if effects_per_level:
                defense_bonus = effects_per_level[0] * skill_level
                hp_bonus = effects_per_level[1] * skill_level
                
                # 永久增加防御和生命值上限
                self.game.base_defense += defense_bonus
                self.game.base_max_hp += hp_bonus
                self.game.update_attributes()
                print(f"🛡️ {skill_name} {self.game.lang.get_text('defense_reduced')} {defense_bonus}, {self.game.lang.get_text('max_hp')} +{hp_bonus}!")
        
        elif skill_id == "counter_attack":  # 战士反击
            if effects_per_level:
                counter_rate = effects_per_level[0] * skill_level
                self.game.special_effects["counter_attack_rate"] += counter_rate
                print(f"🔄 {skill_name} {self.game.lang.get_text('counter_attack_rate')} +{int(counter_rate * 100)}%!")
        
        elif skill_id == "meditation":  # 法师冥想
            if effects_per_level:
                mana_regen = effects_per_level[0] * skill_level
                self.game.special_effects["mana_regen"] += mana_regen
                print(f"✨ {skill_name} {self.game.lang.get_text('mana_regen')} +{mana_regen}!")
        
        elif skill_id == "arcane_power":  # 法师奥术能量
            if effects_per_level:
                spell_power = effects_per_level[0] * skill_level
                max_mana = effects_per_level[1] * skill_level
                self.game.special_effects["spell_power"] += spell_power
                self.game.class_max_mana += max_mana
                print(f"✨ {skill_name} {self.game.lang.get_text('spell_power')} +{int(spell_power * 100)}%, {self.game.lang.get_text('max_mana')} +{max_mana}!")
        
        # 被动技能不造成伤害，只应用效果
        print(f"✨ {skill_name} {self.game.lang.get_text('passive_skill_activated')}!")
        
        # 记录技能使用
        self.game.statistics.record_skill_used(skill_name)
        return monster_hp

    def _handle_ultimate_skill(self, skill_id, skill_node, skill_level, monster_name, monster_hp, combat_round, monster_defense=0):
        """处理终极技能"""
        from .game_config import SKILL_TREES
        
        skill_data = SKILL_TREES.get(self.game.hero_class, {}).get(skill_id, {})
        skill_name = self.get_skill_name(skill_id)
        effects_per_level = skill_data.get("effects_per_level", [])
        
        if skill_id == "berserker_rage":  # 战士狂暴之怒
            if effects_per_level:
                duration = effects_per_level[0]
                attack_multiplier = effects_per_level[1] * skill_level
                defense_reduction = effects_per_level[2]
                
                self.game.berserk_turns = duration
                self.game.special_effects["berserk_attack"] = attack_multiplier
                self.game.special_effects["berserk_defense"] = defense_reduction
                
                print(f"🔥 {skill_name} {self.game.lang.get_text('berserk_activated')}!")
                print(f"⚔️ {self.game.lang.get_text('attack_reduced_percent')} {int(attack_multiplier * 100)}%!")
                print(f"🛡️ {self.game.lang.get_text('defense_reduced')} {int(defense_reduction * 100)}%!")
        
        elif skill_id == "meteor":  # 法师陨石术
            base_damage = max(1, random.randint(self.game.hero_attack, int(self.game.hero_attack * 2)) - monster_defense)
            
            if effects_per_level:
                damage_multiplier = effects_per_level[0] * skill_level
                hero_damage = int(base_damage * damage_multiplier)
                
                # 陨石术造成巨大伤害
                print(f"🌋 {skill_name} {hero_damage}{self.game.lang.get_text('point_damage')}!")
                monster_hp -= hero_damage
        
        # 记录技能使用
        self.game.statistics.record_skill_used(skill_name)
        return monster_hp

    def handle_class_skill(self, skill_key, monster_name, monster_hp, combat_round):
        """处理职业技能"""
        from .game_config import CLASS_DEFINITIONS
        
        class_info = CLASS_DEFINITIONS.get(self.game.hero_class, {})
        
        if skill_key == "shield_bash" and self.game.hero_class == "warrior":
            # 盾击：造成伤害并降低敌人攻击力
            base_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack))
            
            # 战士专属：盾击造成额外伤害
            if self.game.hero_class == "warrior":
                base_damage = int(base_damage * 1.3)  # 盾击伤害提升30%
            
            # 应用暴击效果
            if random.random() < self.game.special_effects["crit_rate"]:
                hero_damage = int(base_damage * (1.5 + self.game.special_effects["crit_damage"]))
                print(f"💥 {self.game.lang.get_text('critical_hit')} {monster_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
            else:
                hero_damage = base_damage
                print(f"🛡️ {self.game.lang.get_text('shield_bash_effect')} {hero_damage}{self.game.lang.get_text('point_damage')}!")
            
            monster_hp -= hero_damage
            
            # 降低敌人攻击力（下回合生效）
            self.game.enemy_attack_debuff = 0.2  # 降低20%攻击力
            print(f"🔻 {monster_name} {self.game.lang.get_text('attack_reduced_percent')} 20%!")
            
            # 记录技能使用
            self.game.statistics.record_skill_used(self.game.lang.get_text("shield_bash_skill"))
            return monster_hp
        
        elif skill_key == "battle_cry" and self.game.hero_class == "warrior":
            # 战吼：提升自身攻击和防御
            self.game.battle_cry_active = 3  # 持续3回合
            print(f"📢 {self.game.lang.get_text('battle_cry_effect')}!")
            print(f"⚔️ {self.game.lang.get_text('attack_reduced_percent')} 20%!")
            print(f"🛡️ {self.game.lang.get_text('defense_reduced')} 15%!")
            
            # 记录技能使用
            self.game.statistics.record_skill_used(self.game.lang.get_text("battle_cry_skill"))
            return monster_hp
        
        elif skill_key == "frost_armor" and self.game.hero_class == "mage":
            # 冰霜护甲：提升防御并反弹伤害
            self.game.frost_armor_active = 3  # 持续3回合
            print(f"❄️ {self.game.lang.get_text('frost_armor_effect')}!")
            print(f"🛡️ {self.game.lang.get_text('defense_reduced')} 25%!")
            print(f"⚡ {self.game.lang.get_text('damage_reflected')} 20%!")
            
            # 记录技能使用
            self.game.statistics.record_skill_used(self.game.lang.get_text("frost_armor_skill"))
            return monster_hp
        
        elif skill_key == "shadow_strike" and self.game.hero_class == "assassin":
            # 影袭：快速连续攻击
            total_damage = 0
            hits = random.randint(2, 4)  # 2-4次攻击
            
            for i in range(hits):
                base_damage = max(1, int(random.randint(self.game.hero_attack // 3, self.game.hero_attack // 2)))
                
                # 刺客专属：影袭高暴击率
                if random.random() < (self.game.special_effects["crit_rate"] + 0.2):  # 额外20%暴击率
                    hero_damage = int(base_damage * 2)
                    print(f"💥 {self.game.lang.get_text('assassin_crit_triggered')} {hero_damage}{self.game.lang.get_text('point_damage')}!")
                else:
                    hero_damage = base_damage
                    print(f"🔪 影袭命中 {hero_damage}{self.game.lang.get_text('point_damage')}!")
                
                # 应用背刺效果（首回合，仅第一次攻击）
                if combat_round == 1 and i == 0 and self.game.special_effects["backstab_damage"] > 0:
                    backstab_bonus = int(hero_damage * self.game.special_effects["backstab_damage"])
                    hero_damage += backstab_bonus
                    print(f"🔪 {self.game.lang.get_text('backstab')} +{backstab_bonus}!")
                
                # 应用元素伤害
                if self.game.special_effects["ice_damage"] > 0:
                    hero_damage += self.game.special_effects["ice_damage"]
                    print(f"❄️ {self.game.lang.get_text('ice_damage')} +{self.game.special_effects['ice_damage']}!")
                
                if self.game.special_effects["fire_damage"] > 0:
                    hero_damage += self.game.special_effects["fire_damage"]
                    print(f"🔥 {self.game.lang.get_text('fire_damage')} +{self.game.special_effects['fire_damage']}!")
                
                monster_hp -= hero_damage
                total_damage += hero_damage
                
                if monster_hp <= 0:
                    break
            
            print(f"⚔️ {self.game.lang.get_text('shadow_strike_hits')} {total_damage}{self.game.lang.get_text('point_damage')}!")
            
            # 记录技能使用
            self.game.statistics.record_skill_used(self.game.lang.get_text("shadow_strike_skill"))
            return monster_hp
        
        # 如果没有匹配的技能，返回普通攻击
        return self.handle_normal_attack(monster_name, monster_hp, combat_round)

    def handle_normal_attack(self, monster_name, monster_hp, combat_round):
        """处理普通攻击"""
        base_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack))
        
        # 应用首回合加成（刺客专属）
        class_info = CLASS_DEFINITIONS.get(self.game.hero_class, {})
        passive_effects = class_info.get("passive_effects", {})
        
        if combat_round == 1 and passive_effects.get("first_turn_damage", 0) > 0:
            bonus_damage = int(base_damage * passive_effects["first_turn_damage"])
            base_damage += bonus_damage
            print(f"⚡ {self.game.lang.get_text('first_turn_bonus')} +{bonus_damage}!")
        
        # 应用专注状态
        if self.game.focus_active:
            hero_damage = int(base_damage * 2)
            print(f"🗡️ {self.game.lang.get_text('you_attack')} {monster_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}!")
            print(f"⚡ {self.game.lang.get_text('focus_critical')}!")
            self.game.focus_active = False
        # 应用暴击效果
        elif random.random() < self.game.special_effects["crit_rate"]:
            hero_damage = int(base_damage * (1.5 + self.game.special_effects["crit_damage"]))
            print(f"💥 {self.game.lang.get_text('critical_hit')} {monster_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
        else:
            hero_damage = base_damage
            print(f"🗡️ {self.game.lang.get_text('you_attack')} {monster_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}")
        
        # 应用背刺效果（首回合）
        if combat_round == 1 and self.game.special_effects["backstab_damage"] > 0:
            backstab_bonus = int(hero_damage * self.game.special_effects["backstab_damage"])
            hero_damage += backstab_bonus
            print(f"🔪 {self.game.lang.get_text('backstab')} +{backstab_bonus}!")
        
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
        
        return monster_hp

    def get_combat_action(self):
        """获取玩家战斗动作"""
        from .game_config import CLASS_DEFINITIONS
        
        print(f"\n{self.game.lang.get_text('choose_action')}")
        print(f"1. {self.game.lang.get_text('normal_attack')}")
        
        option_index = 2
        
        # 药剂选项
        if self.game.hero_potions > 0:
            print(f"{option_index}. {self.game.lang.get_text('use_potion_short')}")
        else:
            print(f"{option_index}. {self.game.lang.get_text('no_potion')}")
        option_index += 1
        
        # 根据职业显示专属技能选项
        class_info = CLASS_DEFINITIONS.get(self.game.hero_class, {})
        class_skills = class_info.get("class_skills", [])
        
        # 显示已学习的技能（从技能树中获取）
        if self.game.skill_tree:
            # 按技能类别排序显示
            learned_skills = []
            for skill_id, level in self.game.skill_tree.learned_skills.items():
                if level > 0:
                    learned_skills.append(skill_id)
            
            # 按技能类别排序
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
                skill_name = self.get_skill_name(skill_id)
                
                # 获取技能等级
                skill_level = self.game.skill_tree.learned_skills.get(skill_id, 0)
                
                # 显示技能名称和等级
                if skill_level > 0:
                    print(f"{option_index}. {skill_name} (Lv.{skill_level})")
                else:
                    print(f"{option_index}. {skill_name}")
                option_index += 1

        return input(f"{self.game.lang.get_text('enter_choice')} (1): ").strip()
    
    def handle_skill_action(self, action, monster_name, monster_hp, combat_round, monster_defense=0):
        """统一处理技能行动"""
        from .game_config import CLASS_DEFINITIONS
        
        class_info = CLASS_DEFINITIONS.get(self.game.hero_class, {})
        class_skills = class_info.get("class_skills", [])
        
        # 构建技能映射表
        skill_mapping = {
            "2": "use_potion"
        }
        
        # 动态添加已学习的技能到映射表
        option_index = 3  # 从第3个选项开始是技能
        if self.game.skill_tree:
            # 按技能类别排序显示
            learned_skills = []
            for skill_id, level in self.game.skill_tree.learned_skills.items():
                if level > 0:
                    learned_skills.append(skill_id)
            
            # 按技能类别排序
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
            
            # 添加技能到映射表
            for skill_id in learned_skills:
                skill_mapping[str(option_index)] = skill_id
                option_index += 1
        
        # 处理技能
        if action in skill_mapping:
            skill_key = skill_mapping[action]
            
            # 处理药剂
            if skill_key == "use_potion":
                if self.game.hero_potions > 0:
                    heal_amount = random.randint(20, 40)
                    self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                    self.game.hero_potions -= 1
                    print(f"🧪 {self.game.lang.get_text('poison')} {heal_amount}{self.game.lang.get_text('point_hp')}")
                    # 记录使用药剂
                    self.game.statistics.record_potion_used()
                else:
                    print(self.game.lang.get_text("no_potion"))
                    return self.handle_normal_attack(monster_name, monster_hp, combat_round)
                return monster_hp
            
            # 处理技能（统一处理所有技能，包括职业技能和通用技能）
            else:
                return self.handle_skill_by_id(skill_key, monster_name, monster_hp, combat_round)
        else:
            # 无效选择，使用普通攻击
            print(self.game.lang.get_text("invalid_action"))
            return self.handle_normal_attack(monster_name, monster_hp, combat_round)

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
        
        # 初始化战斗变量
        self.game.enemy_attack_debuff = 0
        self.game.battle_cry_active = 0
        self.game.frost_armor_active = 0
        
        while monster_hp > 0 and self.game.hero_hp > 0:
            print(f"\n--- {self.game.lang.get_text('round')} {combat_round} ---")
            
            # 应用职业被动效果
            self.apply_class_passives()

            # 显示战斗选项
            action = self.get_combat_action()

            # 处理玩家行动 - 使用统一的方法
            if action == "1" or action == "":  # 普通攻击
                monster_hp = self.handle_normal_attack(monster_name, monster_hp, combat_round)
            else:
                monster_hp = self.handle_skill_action(action, monster_name, monster_hp, combat_round, monster_defense)
            
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
                
                # 计算怪物伤害
                monster_damage = max(1, random.randint(monster_attack // 2, monster_attack) - self.game.hero_defense)
                
                # 应用狂暴状态（如果处于狂暴状态，防御降低50%）
                if self.game.berserk_turns > 0:
                    monster_damage = int(monster_damage * 1.5)  # 防御降低50%，所以伤害增加
                    print(f"🔥 {self.game.lang.get_text('berserk_defense_active')}!")
                
                # 应用护盾效果（如果护盾激活，受到伤害减少50%）
                if self.game.shield_active:
                    monster_damage = int(monster_damage * 0.5)
                    print(f"🛡️ {self.game.lang.get_text('shield_reduced_damage')} {monster_damage}{self.game.lang.get_text('damage')}")
                    self.game.shield_active = False  # 护盾使用后取消
                else:
                    print(f"🩸 {monster_name}{self.game.lang.get_text('monster_attack')} {monster_damage}{self.game.lang.get_text('damage')}")
                
                # 应用抗性效果
                if monster_template.get("special") == "poison" and self.game.special_effects["holy_resistance"] > 0:
                    monster_damage = int(monster_damage * (1 - self.game.special_effects["holy_resistance"]))
                
                if monster_template.get("special") == "fire" and self.game.special_effects["fire_resistance"] > 0:
                    monster_damage = int(monster_damage * (1 - self.game.special_effects["fire_resistance"]))
                
                self.game.hero_hp -= monster_damage
            
            # 特殊能力效果
            if has_poison and random.random() < 0.3:  # 30%概率施加中毒
                self.game.add_status_effect("poison", 3)
                print(f"☠️ {monster_name} {self.game.lang.get_text('monster_attack')}{self.game.lang.get_text('poisoned')}")
            
            if has_frost and random.random() < 0.3:  # 30%概率施加冰霜
                self.game.add_status_effect("frost", 3)
                print(f"❄️ {monster_name} {self.game.lang.get_text('monster_attack')}{self.game.lang.get_text('frost_effect_desc')}")

            print(f"{self.game.lang.get_text('your_hp')} {self.game.hero_hp}, {self.game.lang.get_text('monster_hp')} {monster_name}{self.game.lang.get_text('item_separator')}{monster_hp}")
            
            # 更新狂暴状态
            if self.game.berserk_turns > 0:
                self.game.berserk_turns -= 1
                if self.game.berserk_turns > 0:
                    print(f"🔥 {self.game.lang.get_text('berserk_remaining')} {self.game.berserk_turns} {self.game.lang.get_text('berserk_turns')}")
                else:
                    print(f"💤 {self.game.lang.get_text('berserk_ended')}")
            
            combat_round += 1
            time.sleep(1)

        # 记录战斗失败
        if self.game.hero_hp <= 0:
            self.game.statistics.record_battle_defeat()

        self.game.show_hero_info()









    def handle_boss_normal_attack(self, boss_name, boss_hp, combat_round, boss_defense):
        """处理Boss战的普通攻击"""
        # 计算基础伤害
        base_damage = max(1, random.randint(self.game.hero_attack // 2, self.game.hero_attack) - boss_defense)
        
        # 应用狂暴状态（如果处于狂暴状态，攻击提升50%）
        if self.game.berserk_turns > 0:
            base_damage = int(base_damage * 1.5)
            print(f"🔥 {self.game.lang.get_text('berserk_attack_active')}!")
        
        # 应用专注状态（如果处于专注状态，攻击必中且暴击）
        if self.game.focus_active:
            hero_damage = int(base_damage * 2)
            print(f"🗡️ {self.game.lang.get_text('you_attack')} {boss_name}{self.game.lang.get_text('caused_damage')} {hero_damage}{self.game.lang.get_text('point_damage')}!")
            print(f"⚡ {self.game.lang.get_text('focus_critical')}!")
            self.game.focus_active = False  # 使用后取消专注状态
        # 应用暴击效果（优先使用装备的暴击率）
        elif random.random() < self.game.special_effects["crit_rate"]:
            hero_damage = int(base_damage * (1.5 + self.game.special_effects["crit_damage"]))
            print(f"💥 {self.game.lang.get_text('critical_hit')} {boss_name}{self.game.lang.get_text('caused_damage')}{hero_damage}{self.game.lang.get_text('point_damage')}!")
        else:
            # 如果没有装备暴击，检查技能暴击（通过技能树系统）
            has_critical_skill = False
            if self.game.skill_tree:
                has_critical_skill = self.game.skill_tree.learned_skills.get("critical", 0) > 0
            if has_critical_skill and random.random() < 0.15:
                hero_damage = int(base_damage * 2)  # 修复bug：添加int()转换
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
            # 如果没有装备吸血，检查技能吸血（通过技能树系统）
            has_lifesteal_skill = False
            if self.game.skill_tree:
                has_lifesteal_skill = self.game.skill_tree.learned_skills.get("lifesteal", 0) > 0
            if has_lifesteal_skill:
                heal = int(hero_damage * 0.3)
                self.game.hero_hp = min(self.game.hero_hp + heal, self.game.hero_max_hp)
                print(f"🩸 {self.game.lang.get_text('lifesteal_effect')}{heal}{self.game.lang.get_text('point_hp')}!")
        
        return boss_hp

    def handle_boss_skill_attack(self, skill_key, boss_name, boss_hp, combat_round, boss_defense):
        """处理Boss战的技能攻击"""
        # 处理药剂
        if skill_key == "use_potion":
            if self.game.hero_potions > 0:
                heal_amount = random.randint(20, 40)
                self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                self.game.hero_potions -= 1
                print(f"🧪 {self.game.lang.get_text('poison')} {heal_amount}{self.game.lang.get_text('point_hp')}")
                # 记录使用药剂
                self.game.statistics.record_potion_used()
            else:
                print(self.game.lang.get_text("no_potion"))
                return self.handle_boss_normal_attack(boss_name, boss_hp, combat_round, boss_defense)
            return boss_hp
        
        # 处理职业技能和技能树技能
        from .game_config import CLASS_DEFINITIONS
        class_info = CLASS_DEFINITIONS.get(self.game.hero_class, {})
        class_skills = class_info.get("class_skills", [])
        
        # 职业技能和技能树技能统一处理
        if skill_key in class_skills or (self.game.skill_tree and skill_key in self.game.skill_tree.learned_skills and self.game.skill_tree.learned_skills[skill_key] > 0):
            return self.handle_skill_by_id(skill_key, boss_name, boss_hp, combat_round, boss_defense)
        
        # 对于未知技能，使用普通攻击
        print(self.game.lang.get_text("invalid_action"))
        return self.handle_boss_normal_attack(boss_name, boss_hp, combat_round, boss_defense)

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

            # 处理玩家行动 - 使用抽离的方法
            if action == "1" or action == "":  # 普通攻击
                boss_hp = self.handle_boss_normal_attack(boss_name, boss_hp, combat_round, boss_defense)
            else:
                # 构建技能映射表
                skill_mapping = {
                    "2": "use_potion",
                    "3": "fireball",
                    "4": "healing", 
                    "5": "combo",
                    "6": "shield",
                    "7": "focus"
                }
                
                # 动态添加职业技能到映射表
                from .game_config import CLASS_DEFINITIONS
                class_info = CLASS_DEFINITIONS.get(self.game.hero_class, {})
                class_skills = class_info.get("class_skills", [])
                
                option_index = 3  # 从第3个选项开始是技能
                
                # 添加职业技能
                for skill_key in class_skills:
                    # 检查是否学会了该技能（通过技能树系统）
                    has_skill = False
                    if self.game.skill_tree:
                        has_skill = self.game.skill_tree.learned_skills.get(skill_key, 0) > 0
                    
                    if has_skill:
                        skill_mapping[str(option_index)] = skill_key
                        option_index += 1
                
                # 添加技能树中的技能
                if self.game.skill_tree:
                    # 按技能类别排序显示
                    learned_skills = []
                    for skill_id, level in self.game.skill_tree.learned_skills.items():
                        if level > 0 and skill_id not in class_skills:
                            learned_skills.append(skill_id)
                    
                    # 按技能类别排序
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
                    
                    # 添加技能到映射表
                    for skill_id in learned_skills:
                        skill_mapping[str(option_index)] = skill_id
                        option_index += 1
                
                # 处理技能
                if action in skill_mapping:
                    skill_key = skill_mapping[action]
                    boss_hp = self.handle_boss_skill_attack(skill_key, boss_name, boss_hp, combat_round, boss_defense)
                else:
                    # 无效选择，使用普通攻击
                    print(self.game.lang.get_text("invalid_action"))
                    boss_hp = self.handle_boss_normal_attack(boss_name, boss_hp, combat_round, boss_defense)

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

                # 检查是否学会了吸血技能（通过技能树系统）
                has_lifesteal_skill = False
                if self.game.skill_tree:
                    has_lifesteal_skill = self.game.skill_tree.learned_skills.get("lifesteal", 0) > 0
                
                if not has_lifesteal_skill:
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
                    # 如果没有装备闪避，检查技能闪避（通过技能树系统）
                    has_dodge_skill = False
                    if self.game.skill_tree:
                        has_dodge_skill = self.game.skill_tree.learned_skills.get("dodge", 0) > 0
                    if has_dodge_skill and random.random() < 0.2:
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
            
            # 更新狂暴状态
            if self.game.berserk_turns > 0:
                self.game.berserk_turns -= 1
                if self.game.berserk_turns > 0:
                    print(f"🔥 {self.game.lang.get_text('berserk_remaining')} {self.game.berserk_turns} {self.game.lang.get_text('berserk_turns')}")
                else:
                    print(f"💤 {self.game.lang.get_text('berserk_ended')}")
            
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
                if "fireball" in self.game.hero_skills:
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
                if "healing" in self.game.hero_skills:
                    if self.game.hero_hp >= self.game.hero_max_hp:
                        print("✨ " + self.game.lang.get_text("full_hp_no_heal"))
                    else:
                        heal_amount = random.randint(25, 40)
                        self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
                        print(f"✨ {self.game.lang.get_text('healing_spell')}{heal_amount}{self.game.lang.get_text('point_hp')}")
                        # 记录使用技能（使用 skill_id）
                        self.game.statistics.record_skill_used("healing")
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
                # 应用职业成长倍率
                attack_growth = int(5 * self.game.get_class_growth_multiplier('attack'))
                defense_growth = int(3 * self.game.get_class_growth_multiplier('defense'))
                hp_growth = int(20 * self.game.get_class_growth_multiplier('max_hp'))
                
                self.game.base_attack += attack_growth
                self.game.base_defense += defense_growth
                self.game.base_max_hp += hp_growth
                self.game.hero_max_hp = self.game.base_max_hp
                self.game.hero_hp = self.game.hero_max_hp
                self.game.update_attributes()

                print(f"{self.game.lang.get_text('attack')} {self.game.hero_attack}, {self.game.lang.get_text('defense')} {self.game.hero_defense}, {self.game.lang.get_text('max_hp')} {self.game.hero_max_hp}")

                # 升级时获得技能点
                skill_points_gained = 1 + (level // 3)  # 每3级多获得1点技能点
                self.game.skill_points += skill_points_gained
                print(f"{self.game.lang.get_text('skill_points_earned').format(points=skill_points_gained)}")
                
                input(f"\n{self.game.lang.get_text('continue_prompt')}")








