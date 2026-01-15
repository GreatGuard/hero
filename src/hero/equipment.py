# -*- coding: utf-8 -*-
"""
装备系统模块 - 处理装备相关功能
"""

import random
import copy

# 特殊效果类型 - 使用统一的多语言键名
SPECIAL_EFFECTS = {
    "crit_rate": {
        "name_key": "critical_skill",
        "description_key": "crit_desc"
    },
    "lifesteal": {
        "name_key": "lifesteal_skill",
        "description_key": "lifesteal_desc"
    },
    "dodge": {
        "name_key": "dodge_skill",
        "description_key": "dodge_desc"
    },
    "counter_attack": {
        "name_key": "counter_attack_skill",
        "description_key": "counter_attack_desc"
    },
    "ice_damage": {
        "name_key": "ice_damage_skill",
        "description_key": "ice_damage_desc"
    },
    "fire_damage": {
        "name_key": "fire_damage_skill",
        "description_key": "fire_damage_desc"
    },
    "light_damage": {
        "name_key": "light_damage_skill",
        "description_key": "light_damage_desc"
    },
    "healing": {
        "name_key": "healing_skill",
        "description_key": "heal_desc"
    },
    "mana_boost": {
        "name_key": "mana_boost_skill",
        "description_key": "mana_boost_desc"
    },
    "backstab": {
        "name_key": "backstab_skill",
        "description_key": "backstab_desc"
    },
    "poison": {
        "name_key": "poison_skill",
        "description_key": "poison_desc"
    },
    "shadow_power": {
        "name_key": "shadow_power_skill",
        "description_key": "shadow_power_desc"
    },
    "fire_resistance": {
        "name_key": "fire_resistance_skill",
        "description_key": "fire_resistance_desc"
    },
    "holy_resistance": {
        "name_key": "holy_resistance_skill",
        "description_key": "holy_resistance_desc"
    },
    "stealth": {
        "name_key": "stealth_skill",
        "description_key": "stealth_desc"
    },
    "evasion": {
        "name_key": "evasion_skill",
        "description_key": "evasion_desc"
    },
    "wisdom": {
        "name_key": "wisdom_skill",
        "description_key": "wisdom_desc"
    },
    "mana_regeneration": {
        "name_key": "mana_regeneration_skill",
        "description_key": "mana_regeneration_desc"
    },
    "luck": {
        "name_key": "luck_skill",
        "description_key": "luck_desc"
    },
    "crit_damage": {
        "name_key": "crit_damage_skill",
        "description_key": "crit_damage_desc"
    },
    "immortality": {
        "name_key": "immortality_skill",
        "description_key": "immortality_desc"
    },
    "health_regeneration": {
        "name_key": "health_regeneration_skill",
        "description_key": "health_regeneration_desc"
    }
}


class EquipmentSystem:
    """装备系统类"""

    def __init__(self, game):
        self.game = game
        # 性能优化：添加装备缓存
        self._equipment_cache = {}
        self.equipment_database = self.create_equipment_database()

    def create_equipment_database(self):
        """创建装备数据库"""
        database = {
            "weapon": {
                "zh": {
                    "common": ["木剑", "铁剑", "铜剑"],
                    "uncommon": ["钢剑", "银剑", "精铁剑"],
                    "rare": ["魔法剑", "火焰剑", "冰霜剑"],
                    "epic": ["屠龙刀", "圣剑", "暗影之刃"],
                    "legendary": ["传说之剑", "弑神剑", "天神之剑"]
                },
                "en": {
                    "common": ["Wooden Sword", "Iron Sword", "Copper Sword"],
                    "uncommon": ["Steel Sword", "Silver Sword", "Refined Iron Sword"],
                    "rare": ["Magic Sword", "Flame Sword", "Frost Sword"],
                    "epic": ["Dragon Slayer", "Holy Sword", "Shadow Blade"],
                    "legendary": ["Legendary Sword", "God Slayer", "Divine Sword"]
                }
            },
            "armor": {
                "zh": {
                    "common": ["布甲", "皮甲", "铁甲"],
                    "uncommon": ["钢甲", "银甲", "精铁甲"],
                    "rare": ["魔法甲", "火焰甲", "冰霜甲"],
                    "epic": ["屠龙甲", "圣甲", "暗影甲"],
                    "legendary": ["传说之甲", "弑神甲", "天神之甲"]
                },
                "en": {
                    "common": ["Cloth Armor", "Leather Armor", "Iron Armor"],
                    "uncommon": ["Steel Armor", "Silver Armor", "Refined Iron Armor"],
                    "rare": ["Magic Armor", "Flame Armor", "Frost Armor"],
                    "epic": ["Dragon Armor", "Holy Armor", "Shadow Armor"],
                    "legendary": ["Legendary Armor", "God Slayer Armor", "Divine Armor"]
                }
            },
            "accessory": {
                "zh": {
                    "common": ["普通戒指", "铜戒指", "银戒指"],
                    "uncommon": ["护身符", "力量戒指", "敏捷戒指"],
                    "rare": ["魔法戒指", "火焰护符", "冰霜护符"],
                    "epic": ["屠龙护符", "圣护符", "暗影护符"],
                    "legendary": ["传说护符", "弑神护符", "天神护符"]
                },
                "en": {
                    "common": ["Plain Ring", "Copper Ring", "Silver Ring"],
                    "uncommon": ["Amulet", "Strength Ring", "Agility Ring"],
                    "rare": ["Magic Ring", "Flame Amulet", "Frost Amulet"],
                    "epic": ["Dragon Amulet", "Holy Amulet", "Shadow Amulet"],
                    "legendary": ["Legendary Amulet", "God Slayer Amulet", "Divine Amulet"]
                }
            }
        }
        return database

    def get_rarity_color(self, rarity):
        """获取稀有度对应的颜色代码"""
        colors = {
            "common": "\033[37m",      # 白色
            "uncommon": "\033[32m",    # 绿色
            "rare": "\033[34m",        # 蓝色
            "epic": "\033[35m",        # 紫色
            "legendary": "\033[33m"    # 金色
        }
        return colors.get(rarity, "\033[37m")

    def get_rarity_name(self, rarity):
        """获取稀有度名称"""
        # 直接使用多语言系统获取稀有度名称
        return self.game.lang.get_text(f"rarity_{rarity}")

    def create_random_equipment(self, item_type=None, rarity_bonus=0, is_legendary=False):
        """创建随机装备
        
        Args:
            item_type (str): 装备类型，None表示随机
            rarity_bonus (float): 稀有度提升值
            is_legendary (bool): 是否为传奇装备
        """
        # 性能优化：生成缓存键
        cache_key = f"{item_type}_{rarity_bonus}_{is_legendary}"
        
        # 检查缓存（仅对基础装备进行缓存，不含随机属性）
        if cache_key in self._equipment_cache and not is_legendary:
            base_equipment = self._equipment_cache[cache_key].copy()
            # 重新生成随机属性
            return self._generate_random_attributes(base_equipment)
        
        if item_type is None:
            item_type = random.choice(["weapon", "armor", "accessory"])

        # 如果是传奇装备，直接返回传奇装备
        if is_legendary:
            return self.create_legendary_equipment(item_type)

        # 根据稀有度概率生成
        rarity_roll = random.random()
        
        # 应用稀有度提升（提升后稀有概率更高）
        adjusted_roll = min(0.99, rarity_roll + rarity_bonus * 0.1)  # 每点稀有度提升10%概率
        
        if adjusted_roll < 0.5:
            rarity = "common"
        elif adjusted_roll < 0.75:
            rarity = "uncommon"
        elif adjusted_roll < 0.9:
            rarity = "rare"
        elif adjusted_roll < 0.97:
            rarity = "epic"
        else:
            rarity = "legendary"

        # 创建基础装备对象（延迟计算详细属性）
        base_equipment = {
            "type": item_type,
            "rarity": rarity,
            "enhancement_level": 0,
            "is_legendary": False,
            "_cached_name": None  # 延迟计算名称
        }
        
        # 缓存基础装备对象
        self._equipment_cache[cache_key] = base_equipment.copy()
        
        # 生成随机属性并返回
        return self._generate_random_attributes(base_equipment)
    
    def _generate_random_attributes(self, equipment):
        """延迟计算装备的随机属性"""
        item_type = equipment["type"]
        rarity = equipment["rarity"]
        
        # 性能优化：延迟计算名称
        if equipment["_cached_name"] is None:
            equipment["name"] = self.game.lang.format_text("equipment_name", self.equipment_database, item_type, rarity)
            equipment["_cached_name"] = equipment["name"]
        else:
            equipment["name"] = equipment["_cached_name"]

        # 根据稀有度和类型生成属性
        rarity_multiplier = {"common": 1, "uncommon": 1.5, "rare": 2, "epic": 3, "legendary": 5}

        if item_type == "weapon":
            attack_bonus = int(random.randint(3, 8) * rarity_multiplier[rarity])
            defense_bonus = 0
            hp_bonus = 0
        elif item_type == "armor":
            attack_bonus = 0
            defense_bonus = int(random.randint(2, 6) * rarity_multiplier[rarity])
            hp_bonus = int(random.randint(5, 15) * rarity_multiplier[rarity])
        else:  # accessory
            attack_bonus = int(random.randint(1, 4) * rarity_multiplier[rarity])
            defense_bonus = int(random.randint(1, 4) * rarity_multiplier[rarity])
            hp_bonus = int(random.randint(3, 10) * rarity_multiplier[rarity])

        # 添加特殊效果
        special_effects = self.generate_special_effects(rarity)
        
        # 为装备分配套装（稀有度越高，越有可能属于套装）
        set_bonus = None
        if rarity in ["rare", "epic", "legendary"]:
            # 根据装备类型决定可能的套装
            if item_type == "weapon":
                # 武器可以属于任何套装
                possible_sets = ["warrior_set", "mage_set", "assassin_set"]
            elif item_type == "armor":
                # 护甲只能属于战士套装
                possible_sets = ["warrior_set"]
            else:  # accessory
                # 饰品可以属于法师或刺客套装
                possible_sets = ["mage_set", "assassin_set"]
            
            # 根据稀有度决定套装概率
            set_probability = {"rare": 0.3, "epic": 0.6, "legendary": 0.9}
            if random.random() < set_probability.get(rarity, 0):
                set_bonus = random.choice(possible_sets)

        # 更新装备属性
        equipment.update({
            "attack": attack_bonus,
            "defense": defense_bonus,
            "hp": hp_bonus,
            "special_effects": special_effects,
            "set_bonus": set_bonus,  # 套装效果
            "base_attack": attack_bonus,  # 基础攻击力，用于强化计算
            "base_defense": defense_bonus,  # 基础防御力，用于强化计算
            "base_hp": hp_bonus,  # 基础生命值，用于强化计算
        })
        
        return equipment

    def create_legendary_equipment(self, item_type):
        """创建传奇装备"""
        import game_config
        
        if item_type not in game_config.LEGENDARY_EQUIPMENT:
            item_type = random.choice(list(game_config.LEGENDARY_EQUIPMENT.keys()))
        
        legendary_item = random.choice(game_config.LEGENDARY_EQUIPMENT[item_type])
        
        # 使用统一的多语言系统获取名称
        name_key = legendary_item.get("name_key", "unknown_legendary_item")
        name = self.game.lang.get_text(name_key)
        
        return {
            "name": name,
            "type": item_type,
            "rarity": "legendary",
            "attack": legendary_item["attack"],
            "defense": legendary_item["defense"],
            "hp": legendary_item["hp"],
            "special_effects": legendary_item.get("special_effects", []),
            "special_effects_values": {k: v for k, v in legendary_item.items() if k not in ["name_key", "attack", "defense", "hp", "special_effects"]},
            "set_bonus": None,
            "enhancement_level": 0,  # 强化等级，初始为0
            "base_attack": legendary_item["attack"],  # 基础攻击力，用于强化计算
            "base_defense": legendary_item["defense"],  # 基础防御力，用于强化计算
            "base_hp": legendary_item["hp"],  # 基础生命值，用于强化计算
            "is_legendary": True
        }

    def generate_special_effects(self, rarity):
        """根据稀有度生成特殊效果"""
        effects = []
        
        # 稀有度越高，特殊效果越多
        effect_chances = {
            "common": 0.1,    # 10% 概率有特殊效果
            "uncommon": 0.3,  # 30%
            "rare": 0.6,     # 60%
            "epic": 0.8,     # 80%
            "legendary": 1.0 # 100%
        }
        
        chance = effect_chances.get(rarity, 0)
        
        if random.random() < chance:
            # 根据稀有度决定效果数量
            max_effects = {"common": 1, "uncommon": 1, "rare": 2, "epic": 2, "legendary": 3}
            num_effects = random.randint(1, max_effects.get(rarity, 1))
            
            available_effects = list(SPECIAL_EFFECTS.keys())
            effects = random.sample(available_effects, min(num_effects, len(available_effects)))
        
        return effects

    def show_inventory(self):
        """显示背包内容"""
        print(f"\n{self.game.lang.get_text('inventory')}:")
        if not self.game.inventory:
            print(f"  {self.game.lang.get_text('empty_inventory')}")
        else:
            for i, item in enumerate(self.game.inventory):
                color = self.get_rarity_color(item["rarity"])
                rarity_name = self.get_rarity_name(item["rarity"])
                reset_color = "\033[0m"

                stats = []
                if item["attack"] > 0:
                    stats.append(f"⚔️+{item['attack']}")
                if item["defense"] > 0:
                    stats.append(f"🛡️+{item['defense']}")
                if item["hp"] > 0:
                    stats.append(f"❤️+{item['hp']}")
                    
                # 显示强化等级
                enhancement_level = item.get("enhancement_level", 0)
                enhancement_text = ""
                if enhancement_level > 0:
                    enhancement_text = f" +{enhancement_level}"

                print(f"  {i+1}. {color}{item['name']}{enhancement_text} {reset_color}[{rarity_name}] {', '.join(stats)}")

    def equip_item(self, item_index):
        """装备物品"""
        if item_index < 0 or item_index >= len(self.game.inventory):
            print(self.game.lang.get_text("invalid_choice"))
            return

        item = self.game.inventory[item_index]
        item_type = item["type"]

        # 如果该位置已有装备，先卸下
        if self.game.equipment[item_type] is not None:
            self.game.inventory.append(self.game.equipment[item_type])
            equipped_item_name = self.game.equipment[item_type]["name"]
            self.game.equipment[item_type] = None
            print(f"{self.game.lang.get_text('unequip_success')} {equipped_item_name}")

        # 装备新物品
        self.game.equipment[item_type] = item
        self.game.inventory.pop(item_index)

        # 性能优化：清除属性缓存
        self.game.invalidate_attributes_cache()
        self.game.update_attributes()
        print(f"{self.game.lang.get_text('equip_success')} {item['name']}!")

    def unequip_item(self, item_type):
        """卸下装备"""
        if self.game.equipment[item_type] is None:
            print(self.game.lang.get_text("no_equipment_in_slot"))
            return

        item = self.game.equipment[item_type]
        self.game.inventory.append(item)
        self.game.equipment[item_type] = None

        # 性能优化：清除属性缓存
        self.game.invalidate_attributes_cache()
        self.game.update_attributes()
        print(f"{self.game.lang.get_text('unequip_success')} {item['name']}")

    def equipment_management(self):
        """装备管理界面"""
        while True:
            self.game.clear_screen()
            print(self.game.lang.get_text("block_separator"))
            print(f"          {self.game.lang.get_text('equipment_management')}")
            print(self.game.lang.get_text("block_separator"))
            print()

            # 显示当前装备
            print(f"{self.game.lang.get_text('current_equipment')}:")
            for slot in ["weapon", "armor", "accessory"]:
                item = self.game.equipment[slot]
                color = self.get_rarity_color(item["rarity"]) if item else ""
                reset_color = "\033[0m" if item else ""
                rarity_name = self.get_rarity_name(item["rarity"]) if item else ""

                if item:
                    stats = []
                    if item["attack"] > 0:
                        stats.append(f"⚔️+{item['attack']}")
                    if item["defense"] > 0:
                        stats.append(f"🛡️+{item['defense']}")
                    if item["hp"] > 0:
                        stats.append(f"❤️+{item['hp']}")
                    
                    # 显示强化等级
                    enhancement_level = item.get("enhancement_level", 0)
                    enhancement_text = ""
                    if enhancement_level > 0:
                        enhancement_text = f" +{enhancement_level}"
                        
                    # 显示传说属性
                    legendary_text = ""
                    if item.get("legendary_attribute"):
                        if item["legendary_attribute"] == "flame_damage":
                            legendary_text = " 🔥"
                        elif item["legendary_attribute"] == "damage_reduction":
                            legendary_text = " 🛡️"
                        elif item["legendary_attribute"] == "hp_regen":
                            legendary_text = " 💚"
                            
                    print(f"  {color}{item['name']}{enhancement_text}{reset_color}[{rarity_name}] {', '.join(stats)}{legendary_text}")
                else:
                    print(f"  {self.game.lang.get_text(slot)}: {self.game.lang.get_text('none')}")

            print()
            self.show_inventory()

            print()
            print(f"1. {self.game.lang.get_text('equip_item')}")
            print(f"2. {self.game.lang.get_text('unequip_item')}")
            print(f"3. {self.game.lang.get_text('return_to_game')}")

            choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()

            if choice == "1":
                self.show_inventory()
                if self.game.inventory:
                    try:
                        from hero.safe_input import safe_input
                        from hero.error_handler import handle_error
                        user_input = safe_input(f"{self.game.lang.get_text('enter_item_number')}: ")
                        if user_input is not None:
                            item_index = int(user_input) - 1
                            self.equip_item(item_index)
                    except Exception as e:
                        from hero.error_handler import handle_error
                        error_msg = handle_error(e, "装备物品", "装备物品时发生错误。")
                        print(error_msg)
                    input(f"{self.game.lang.get_text('continue_prompt')}")
            elif choice == "2":
                print()
                print(f"1. {self.game.lang.get_text('weapon')}")
                print(f"2. {self.game.lang.get_text('armor')}")
                print(f"3. {self.game.lang.get_text('accessory')}")
                slot_choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()
                slot_map = {"1": "weapon", "2": "armor", "3": "accessory"}
                if slot_choice in slot_map:
                    self.unequip_item(slot_map[slot_choice])
                    input(f"{self.game.lang.get_text('continue_prompt')}")
            elif choice == "3":
                break
            else:
                print(self.game.lang.get_text("invalid_choice"))

    def enchant_equipment(self, equipment_slot, enchantment_type):
        """为装备附魔
        
        Args:
            equipment_slot (str): 装备槽位（weapon/armor/accessory）
            enchantment_type (str): 附魔类型
            
        Returns:
            bool: 附魔是否成功
        """
        import game_config
        
        if self.game.equipment[equipment_slot] is None:
            print(self.game.lang.get_text("no_equipment_in_slot"))
            return False
            
        equipment = self.game.equipment[equipment_slot]
        
        # 检查附魔限制
        if enchantment_type not in game_config.ENCHANTMENT_RESTRICTIONS.get(equipment["type"], []):
            print(self.game.lang.get_text("enchantment_not_allowed", type=equipment["type"]))
            return False
            
        # 检查是否已经附魔
        if equipment.get("enchantment"):
            print(self.game.lang.get_text("already_enchanted"))
            return False
            
        # 获取附魔配置
        enchantment_config = game_config.ENCHANTMENT_TYPES.get(enchantment_type)
        if not enchantment_config:
            print(self.game.lang.get_text("invalid_enchantment"))
            return False
            
        # 检查金币是否足够
        enchantment_cost = enchantment_config["cost"]
        if self.game.hero_gold < enchantment_cost:
            print(self.game.lang.get_text("not_enough_gold_enchant", cost=enchantment_cost))
            return False
            
        # 计算成功率
        base_success_rate = enchantment_config["success_rate"]
        rarity_bonus = game_config.ENCHANTMENT_RARITY_BONUS.get(equipment["rarity"], 0)
        total_success_rate = min(0.95, base_success_rate + rarity_bonus)
        
        # 确认附魔
        enchantment_name = self.game.lang.get_text(enchantment_config["name_key"])
        print(f"\n{self.game.lang.get_text('enchantment_info')}:")
        print(f"  {equipment['name']}")
        print(f"  {self.game.lang.get_text('enchantment_type')}: {enchantment_name}")
        print(f"  {self.game.lang.get_text('enchantment_cost')}: {enchantment_cost} {self.game.lang.get_text('gold')}")
        print(f"  {self.game.lang.get_text('success_rate')}: {int(total_success_rate * 100)}%")
        
        confirm = input(f"\n{self.game.lang.get_text('confirm_enchantment')} (y/n): ").strip().lower()
        if confirm not in self.game.lang.get_text("yes_options"):
            print(self.game.lang.get_text("enchantment_cancelled"))
            return False
            
        # 扣除金币
        self.game.hero_gold -= enchantment_cost
        self.game.statistics.record_gold_spent(enchantment_cost)
        
        # 进行附魔尝试
        import random
        success = random.random() < total_success_rate
        
        if success:
            # 附魔成功
            equipment["enchantment"] = enchantment_type
            
            # 应用附魔效果
            for effect_key, effect_value in enchantment_config["effects"].items():
                equipment[effect_key] = effect_value
                
            # 添加特殊效果
            if "special_effects" in enchantment_config["effects"]:
                for effect in enchantment_config["effects"]["special_effects"]:
                    if effect not in equipment["special_effects"]:
                        equipment["special_effects"].append(effect)
                        
            print(f"\n✨ {self.game.lang.get_text('enchantment_success')} ✨")
            print(f"  {equipment['name']} {self.game.lang.get_text('now_enchanted_with')} {enchantment_name}")
            
            # 记录附魔成功
            self.game.statistics.record_enchantment_success()
            
        else:
            # 附魔失败
            print(f"\n❌ {self.game.lang.get_text('enchantment_failed')}")
            print(f"  {self.game.lang.get_text('enchantment_failed_desc')}")
            
            # 记录附魔失败
            self.game.statistics.record_enchantment_failed()
            
        return success
        
    def enchant_equipment_menu(self):
        """附魔装备菜单"""
        import game_config
        
        while True:
            self.game.clear_screen()
            print(self.game.lang.get_text("block_separator"))
            print(f"          {self.game.lang.get_text('enchant_equipment')}")
            print(self.game.lang.get_text("block_separator"))
            print()
            
            print(f"{self.game.lang.get_text('your_gold')}: {self.game.hero_gold}")
            print()
            print(f"{self.game.lang.get_text('current_equipment')}:")
            
            # 显示当前装备及其可附魔选项
            equipment_list = []
            for i, slot in enumerate(["weapon", "armor", "accessory"]):
                item = self.game.equipment[slot]
                if item:
                    color = self.get_rarity_color(item["rarity"])
                    reset_color = "\033[0m"
                    rarity_name = self.get_rarity_name(item["rarity"])
                    
                    stats = []
                    if item["attack"] > 0:
                        stats.append(f"⚔️+{item['attack']}")
                    if item["defense"] > 0:
                        stats.append(f"🛡️+{item['defense']}")
                    if item["hp"] > 0:
                        stats.append(f"❤️+{item['hp']}")
                    
                    # 显示附魔状态
                    enchantment_text = ""
                    if item.get("enchantment"):
                        enchantment_name = self.game.lang.get_text(game_config.ENCHANTMENT_TYPES[item["enchantment"]]["name_key"])
                        enchantment_text = f" 🔮{enchantment_name}"
                    
                    print(f"  {i+1}. {color}{item['name']} {reset_color}[{rarity_name}] {', '.join(stats)}{enchantment_text}")
                    equipment_list.append(slot)
                else:
                    print(f"  {i+1}. {self.game.lang.get_text(slot)}: {self.game.lang.get_text('none')}")
                    equipment_list.append(None)
            
            print()
            print(f"1. {self.game.lang.get_text('weapon')}")
            print(f"2. {self.game.lang.get_text('armor')}")
            print(f"3. {self.game.lang.get_text('accessory')}")
            print(f"4. {self.game.lang.get_text('return_to_shop')}")
            
            choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()
            
            if choice in ["1", "2", "3"]:
                slot_index = int(choice) - 1
                if equipment_list[slot_index]:
                    slot = equipment_list[slot_index]
                    self.show_enchantment_options(slot)
                else:
                    print(self.game.lang.get_text("no_equipment_in_slot"))
                    input(f"{self.game.lang.get_text('continue_prompt')}")
            elif choice == "4":
                break
            else:
                print(self.game.lang.get_text("invalid_choice"))
                input(f"{self.game.lang.get_text('continue_prompt')}")
    
    def show_enchantment_options(self, equipment_slot):
        """显示可用的附魔选项
        
        Args:
            equipment_slot (str): 装备槽位
        """
        import game_config
        
        equipment = self.game.equipment[equipment_slot]
        if not equipment:
            return
            
        while True:
            self.game.clear_screen()
            print(self.game.lang.get_text("block_separator"))
            print(f"          {self.game.lang.get_text('enchantment_options')}")
            print(self.game.lang.get_text("block_separator"))
            print()
            
            # 显示装备信息
            color = self.get_rarity_color(equipment["rarity"])
            reset_color = "\033[0m"
            rarity_name = self.get_rarity_name(equipment["rarity"])
            
            stats = []
            if equipment["attack"] > 0:
                stats.append(f"⚔️+{equipment['attack']}")
            if equipment["defense"] > 0:
                stats.append(f"🛡️+{equipment['defense']}")
            if equipment["hp"] > 0:
                stats.append(f"❤️+{equipment['hp']}")
            
            print(f"{color}{equipment['name']} {reset_color}[{rarity_name}] {', '.join(stats)}")
            
            # 显示可用的附魔选项
            print(f"\n{self.game.lang.get_text('available_enchantments')}:")
            
            available_enchantments = []
            for i, enchant_type in enumerate(game_config.ENCHANTMENT_RESTRICTIONS.get(equipment["type"], [])):
                enchant_config = game_config.ENCHANTMENT_TYPES[enchant_type]
                enchant_name = self.game.lang.get_text(enchant_config["name_key"])
                enchant_desc = self.game.lang.get_text(enchant_config["description_key"])
                success_rate = enchant_config["success_rate"] + game_config.ENCHANTMENT_RARITY_BONUS.get(equipment["rarity"], 0)
                
                print(f"  {i+1}. {enchant_name} - {enchant_config['cost']} {self.game.lang.get_text('gold')} ({int(success_rate * 100)}%)")
                print(f"     {enchant_desc}")
                available_enchantments.append(enchant_type)
            
            print(f"\n  {len(available_enchantments) + 1}. {self.game.lang.get_text('back')}")
            
            choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()
            
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(available_enchantments):
                    enchant_type = available_enchantments[choice_num - 1]
                    self.enchant_equipment(equipment_slot, enchant_type)
                    input(f"{self.game.lang.get_text('continue_prompt')}")
                    break
                elif choice_num == len(available_enchantments) + 1:
                    break
                else:
                    print(self.game.lang.get_text("invalid_choice"))
                    input(f"{self.game.lang.get_text('continue_prompt')}")
            else:
                print(self.game.lang.get_text("invalid_choice"))
                input(f"{self.game.lang.get_text('continue_prompt')}")

    def get_enchantment_display(self, equipment):
        """获取附魔装备的显示文本
        
        Args:
            equipment (dict): 装备字典
            
        Returns:
            str: 装备显示文本
        """
        if equipment is None:
            return self.game.lang.get_text("none")
            
        name = equipment["name"]
        
        # 如果有附魔，显示在名称后
        if equipment.get("enchantment"):
            import game_config
            enchant_config = game_config.ENCHANTMENT_TYPES.get(equipment["enchantment"])
            if enchant_config:
                enchant_name = self.game.lang.get_text(enchant_config["name_key"])
                name = f"{name} 🔮{enchant_name}"
                
        return name

    def update_equipment_shop_menu(self):
        """更新装备商店菜单，添加附魔选项"""
        # 在商店菜单中添加附魔选项
        print(f"1. {self.game.lang.get_text('buy_equipment')}")
        print(f"2. {self.game.lang.get_text('enhance_equipment')}")
        print(f"3. {self.game.lang.get_text('enchant_equipment')}")
        print(f"4. {self.game.lang.get_text('exit_shop')}")

    def show_shop_items(self, items):
        """显示商店物品"""
        for i, item in enumerate(items):
            color = self.get_rarity_color(item["rarity"])
            rarity_name = self.get_rarity_name(item["rarity"])
            reset_color = "\033[0m"

            stats = []
            if item["attack"] > 0:
                stats.append(f"⚔️+{item['attack']}")
            if item["defense"] > 0:
                stats.append(f"🛡️+{item['defense']}")
            if item["hp"] > 0:
                stats.append(f"❤️+{item['hp']}")
                
            # 显示强化等级
            enhancement_level = item.get("enhancement_level", 0)
            enhancement_text = ""
            if enhancement_level > 0:
                enhancement_text = f" +{enhancement_level}"

            print(f"  {i+1}. {color}{item['name']}{enhancement_text} {reset_color}[{rarity_name}] {', '.join(stats)} - {item['price']} {self.game.lang.get_text('gold')}")

    def equipment_shop(self, gold_multiplier=1.0, rarity_bonus=0):
        """装备商店
        
        Args:
            gold_multiplier (float): 金币倍率
            rarity_bonus (float): 稀有度提升
        """
        # 生成商店商品（3-5件）
        shop_items = []
        num_items = random.randint(3, 5)
        for _ in range(num_items):
            item = self.create_random_equipment(rarity_bonus=rarity_bonus)
            # 根据稀有度和属性定价
            rarity_multiplier = {"common": 1, "uncommon": 2, "rare": 5, "epic": 10, "legendary": 20}
            base_price = (item["attack"] * 5 + item["defense"] * 5 + item["hp"] * 2) * rarity_multiplier[item["rarity"]]
            item["price"] = int(base_price / gold_multiplier)
            shop_items.append(item)

        # 记录访问商店
        self.game.statistics.record_shop_visit()

        while True:
            self.game.clear_screen()
            print(self.game.lang.get_text("block_separator"))
            print(f"          {self.game.lang.get_text('equipment_shop')}")
            print(self.game.lang.get_text("block_separator"))
            print()

            print(f"{self.game.lang.get_text('your_gold')}: {self.game.hero_gold}")
            print()
            print(f"{self.game.lang.get_text('shop_items')}:")
            self.show_shop_items(shop_items)

            print()
            print(f"1. {self.game.lang.get_text('buy_equipment')}")
            print(f"2. {self.game.lang.get_text('enhance_equipment')}")
            print(f"3. {self.game.lang.get_text('enchant_equipment')}")
            print(f"4. {self.game.lang.get_text('exit_shop')}")

            choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()

            if choice == "1":
                try:
                    from hero.safe_input import safe_input
                    from hero.error_handler import handle_error
                    user_input = safe_input(f"{self.game.lang.get_text('enter_item_number')}: ")
                    if user_input is not None:
                        item_index = int(user_input) - 1
                        if 0 <= item_index < len(shop_items):
                            item = shop_items[item_index]
                            if self.game.hero_gold >= item["price"]:
                                self.game.hero_gold -= item["price"]
                                self.game.inventory.append(item)
                                print(f"{self.game.lang.get_text('buy_success')} {item['name']}!")
                                # 记录购买装备和花费
                                self.game.statistics.record_item_purchased()
                                self.game.statistics.record_gold_spent(item["price"])
                            else:
                                print(self.game.lang.get_text("not_enough_gold"))
                        else:
                            print(self.game.lang.get_text("invalid_choice"))
                except Exception as e:
                    from hero.error_handler import handle_error
                    error_msg = handle_error(e, "购买装备", "购买装备时发生错误。")
                    print(error_msg)
                input(f"{self.game.lang.get_text('continue_prompt')}")
            elif choice == "2":
                self.enhance_equipment_menu()
            elif choice == "3":
                self.enchant_equipment_menu()
            elif choice == "4":
                break
            else:
                print(self.game.lang.get_text("invalid_choice"))

    def find_equipment(self, rarity_bonus=0):
        """发现装备事件
        
        Args:
            rarity_bonus (int): 稀有度提升值
        """
        # 根据难度和地图类型调整发现概率
        settings = self.game.difficulty_settings[self.game.difficulty]
        # 高难度更容易发现稀有装备
        difficulty_bonus = (settings["enemy_multiplier"] - 0.5) * 2
        
        # 总稀有度提升 = 难度提升 + 传入的参数提升
        total_rarity_bonus = difficulty_bonus + rarity_bonus

        item = self.create_random_equipment(rarity_bonus=total_rarity_bonus)
        color = self.get_rarity_color(item["rarity"])
        rarity_name = self.get_rarity_name(item["rarity"])
        reset_color = "\033[0m"

        stats = []
        if item["attack"] > 0:
            stats.append(f"⚔️  +{item['attack']}")
        if item["defense"] > 0:
            stats.append(f"🛡️  +{item['defense']}")
        if item["hp"] > 0:
            stats.append(f"❤️  +{item['hp']}")

        print(f"\n✨ {self.game.lang.get_text('found_equipment')}{color}{item['name']} {reset_color}[{rarity_name}]")
        print(f"   {self.game.lang.get_text('equipment_stats')}{', '.join(stats)}")

        self.game.inventory.append(item)
        self.game.events_encountered.append(f"{self.game.lang.get_text('found_equipment_event')}{item['name']}")

        # 记录获得装备
        self.game.statistics.record_equipment_found(item["rarity"])

    def enhance_equipment(self, equipment_slot):
        """强化装备
        
        Args:
            equipment_slot (str): 装备槽位（weapon/armor/accessory）
            
        Returns:
            bool: 强化是否成功
        """
        if self.game.equipment[equipment_slot] is None:
            print(self.game.lang.get_text("no_equipment_in_slot"))
            return False
            
        equipment = self.game.equipment[equipment_slot]
        current_level = equipment.get("enhancement_level", 0)
        
        # 最大强化等级为+15
        if current_level >= 15:
            print(self.game.lang.get_text("max_enhancement_level"))
            return False
            
        # 计算强化费用：基础费用 + (当前等级 * 递增费用)
        base_cost = 100
        increment_cost = 50
        enhancement_cost = base_cost + (current_level * increment_cost)
        
        # 检查金币是否足够
        if self.game.hero_gold < enhancement_cost:
            print(self.game.lang.get_text("not_enough_gold_enhance", cost=enhancement_cost))
            return False
            
        # 确认强化
        print(f"\n{self.game.lang.get_text('enhancement_info')}:")
        print(f"  {equipment['name']} (+{current_level})")
        print(f"  {self.game.lang.get_text('enhancement_cost')}: {enhancement_cost} {self.game.lang.get_text('gold')}")
        print(f"  {self.game.lang.get_text('next_level')}: +{current_level + 1}")
        
        confirm = input(f"\n{self.game.lang.get_text('confirm_enhancement')} (y/n): ").strip().lower()
        if confirm not in self.game.lang.get_text("yes_options"):
            print(self.game.lang.get_text("enhancement_cancelled"))
            return False
            
        # 扣除金币
        self.game.hero_gold -= enhancement_cost
        self.game.statistics.record_gold_spent(enhancement_cost)
        
        # 增加强化等级
        equipment["enhancement_level"] = current_level + 1
        
        # 应用属性提升（每级+10%基础属性）
        enhancement_bonus = 0.1 * equipment["enhancement_level"]
        equipment["attack"] = int(equipment["base_attack"] * (1 + enhancement_bonus))
        equipment["defense"] = int(equipment["base_defense"] * (1 + enhancement_bonus))
        equipment["hp"] = int(equipment["base_hp"] * (1 + enhancement_bonus))
        
        # 检查是否达到+10，获得传说属性
        if equipment["enhancement_level"] == 10:
            self.add_legendary_attribute(equipment)
            print(f"\n✨ {self.game.lang.get_text('legendary_attribute_unlocked')} ✨")
            
        # 更新英雄属性
        self.game.update_attributes()
        
        # 显示强化结果
        print(f"\n{self.game.lang.get_text('enhancement_success')}")
        print(f"  {equipment['name']} (+{equipment['enhancement_level']})")
        
        return True
        
    def add_legendary_attribute(self, equipment):
        """为+10装备添加传说属性
        
        Args:
            equipment (dict): 装备字典
        """
        item_type = equipment["type"]
        
        if item_type == "weapon":
            # 武器：附加火焰伤害（攻击力+5%）
            equipment["legendary_attribute"] = "flame_damage"
            equipment["flame_damage_percent"] = 0.05
            print(f"  {self.game.lang.get_text('flame_attribute_unlocked')}")
        elif item_type == "armor":
            # 防具：伤害减免（受到伤害-5%）
            equipment["legendary_attribute"] = "damage_reduction"
            equipment["damage_reduction_percent"] = 0.05
            print(f"  {self.game.lang.get_text('damage_reduction_attribute_unlocked')}")
        else:  # accessory
            # 饰品：生命恢复（每回合恢复1%最大生命值）
            equipment["legendary_attribute"] = "hp_regen"
            equipment["hp_regen_percent"] = 0.01
            print(f"  {self.game.lang.get_text('hp_regen_attribute_unlocked')}")
            
    def get_enhanced_equipment_display(self, equipment):
        """获取强化装备的显示文本
        
        Args:
            equipment (dict): 装备字典
            
        Returns:
            str: 装备显示文本
        """
        if equipment is None:
            return self.game.lang.get_text("none")
            
        name = equipment["name"]
        enhancement_level = equipment.get("enhancement_level", 0)
        
        # 如果有强化等级，显示在名称后
        if enhancement_level > 0:
            name = f"{name} (+{enhancement_level})"
            
        # 获取传说属性描述
        legendary_desc = ""
        if equipment.get("legendary_attribute"):
            if equipment["legendary_attribute"] == "flame_damage":
                legendary_desc = f" 🔥{self.game.lang.get_text('flame_damage_desc')}"
            elif equipment["legendary_attribute"] == "damage_reduction":
                legendary_desc = f" 🛡️{self.game.lang.get_text('damage_reduction_desc')}"
            elif equipment["legendary_attribute"] == "hp_regen":
                legendary_desc = f" 💚{self.game.lang.get_text('hp_regen_desc')}"
                
        return f"{name}{legendary_desc}"
        
    def get_enhancement_cost(self, equipment):
        """获取装备强化费用
        
        Args:
            equipment (dict): 装备字典
            
        Returns:
            int: 强化费用
        """
        current_level = equipment.get("enhancement_level", 0)
        
        # 如果已经达到最大等级，返回0
        if current_level >= 15:
            return 0
            
        # 计算强化费用：基础费用 + (当前等级 * 递增费用)
        base_cost = 100
        increment_cost = 50
        return base_cost + (current_level * increment_cost)
        
    def enhance_equipment_menu(self):
        """强化装备菜单"""
        while True:
            self.game.clear_screen()
            print(self.game.lang.get_text("block_separator"))
            print(f"          {self.game.lang.get_text('enhance_equipment')}")
            print(self.game.lang.get_text("block_separator"))
            print()
            
            print(f"{self.game.lang.get_text('your_gold')}: {self.game.hero_gold}")
            print()
            print(f"{self.game.lang.get_text('current_equipment')}:")
            
            # 显示当前装备及其强化费用
            equipment_list = []
            for i, slot in enumerate(["weapon", "armor", "accessory"]):
                item = self.game.equipment[slot]
                if item:
                    color = self.get_rarity_color(item["rarity"])
                    reset_color = "\033[0m"
                    rarity_name = self.get_rarity_name(item["rarity"])
                    
                    stats = []
                    if item["attack"] > 0:
                        stats.append(f"⚔️+{item['attack']}")
                    if item["defense"] > 0:
                        stats.append(f"🛡️+{item['defense']}")
                    if item["hp"] > 0:
                        stats.append(f"❤️+{item['hp']}")
                    
                    # 显示强化等级
                    enhancement_level = item.get("enhancement_level", 0)
                    enhancement_text = ""
                    if enhancement_level > 0:
                        enhancement_text = f" +{enhancement_level}"
                    
                    # 显示传说属性
                    legendary_text = ""
                    if item.get("legendary_attribute"):
                        if item["legendary_attribute"] == "flame_damage":
                            legendary_text = " 🔥"
                        elif item["legendary_attribute"] == "damage_reduction":
                            legendary_text = " 🛡️"
                        elif item["legendary_attribute"] == "hp_regen":
                            legendary_text = " 💚"
                    
                    # 获取强化费用
                    enhancement_cost = self.get_enhancement_cost(item)
                    cost_text = f" - {enhancement_cost} {self.game.lang.get_text('gold')}" if enhancement_cost > 0 else f" - {self.game.lang.get_text('max_enhancement')}"
                    
                    print(f"  {i+1}. {color}{item['name']}{enhancement_text} {reset_color}[{rarity_name}] {', '.join(stats)}{legendary_text}{cost_text}")
                    equipment_list.append(slot)
                else:
                    print(f"  {i+1}. {self.game.lang.get_text(slot)}: {self.game.lang.get_text('none')}")
                    equipment_list.append(None)
            
            print()
            print(f"1. {self.game.lang.get_text('weapon')}")
            print(f"2. {self.game.lang.get_text('armor')}")
            print(f"3. {self.game.lang.get_text('accessory')}")
            print(f"4. {self.game.lang.get_text('return_to_shop')}")
            
            choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()
            
            if choice in ["1", "2", "3"]:
                slot_index = int(choice) - 1
                if equipment_list[slot_index]:
                    slot = equipment_list[slot_index]
                    self.enhance_equipment(slot)
                    input(f"{self.game.lang.get_text('continue_prompt')}")
                else:
                    print(self.game.lang.get_text("no_equipment_in_slot"))
                    input(f"{self.game.lang.get_text('continue_prompt')}")
            elif choice == "4":
                break
            else:
                print(self.game.lang.get_text("invalid_choice"))
                input(f"{self.game.lang.get_text('continue_prompt')}")
