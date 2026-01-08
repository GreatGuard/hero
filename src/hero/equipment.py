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
    }
}


class EquipmentSystem:
    """装备系统类"""

    def __init__(self, game):
        self.game = game
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

        # 使用统一的多语言格式化函数获取装备名称
        name = self.game.lang.format_text("equipment_name", self.equipment_database, item_type, rarity)

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

        return {
            "name": name,
            "type": item_type,
            "rarity": rarity,
            "attack": attack_bonus,
            "defense": defense_bonus,
            "hp": hp_bonus,
            "special_effects": special_effects,
            "set_bonus": set_bonus,  # 套装效果
            "is_legendary": False
        }

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

                print(f"  {i+1}. {color}{item['name']} {reset_color}[{rarity_name}] {', '.join(stats)}")

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
                    print(f"  {color}{item['name']} {reset_color}[{rarity_name}] {', '.join(stats)}")
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
                        item_index = int(input(f"{self.game.lang.get_text('enter_item_number')}: ")) - 1
                        self.equip_item(item_index)
                    except ValueError:
                        print(self.game.lang.get_text("invalid_choice"))
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

            print(f"  {i+1}. {color}{item['name']} {reset_color}[{rarity_name}] {', '.join(stats)} - {item['price']} {self.game.lang.get_text('gold')}")

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
            print(f"2. {self.game.lang.get_text('exit_shop')}")

            choice = input(f"{self.game.lang.get_text('enter_choice')}: ").strip()

            if choice == "1":
                try:
                    item_index = int(input(f"{self.game.lang.get_text('enter_item_number')}: ")) - 1
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
                except ValueError:
                    print(self.game.lang.get_text("invalid_choice"))
                input(f"{self.game.lang.get_text('continue_prompt')}")
            elif choice == "2":
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
