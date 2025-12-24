# -*- coding: utf-8 -*-
"""
模拟类定义
"""

from unittest.mock import Mock
from tests.utils.test_helpers import create_mock_game


class MockHeroGame:
    """模拟游戏类"""
    
    def __init__(self):
        # 使用辅助函数创建基本模拟
        self.mock_game = create_mock_game()
        
        # 设置所有属性
        for attr_name in dir(self.mock_game):
            if not attr_name.startswith('_'):
                setattr(self, attr_name, getattr(self.mock_game, attr_name))
    
    def update_attributes(self):
        """更新属性"""
        self.mock_game.update_attributes()
    
    def clear_screen(self):
        """清屏"""
        self.mock_game.clear_screen()
    
    def show_hero_info(self):
        """显示英雄信息"""
        self.mock_game.show_hero_info()
    
    def draw_map(self):
        """绘制地图"""
        self.mock_game.draw_map()
    
    def check_game_status(self):
        """检查游戏状态"""
        return self.mock_game.check_game_status()
    
    def restart_game(self):
        """重新开始游戏"""
        self.mock_game.restart_game()


class MockLanguageSupport:
    """模拟语言支持类"""
    
    def __init__(self, language="zh"):
        self.language = language
        self.texts = {
            "welcome_title": "Welcome to Hero Game" if language == "en" else "欢迎来到英雄无敌",
            "continue_prompt": "Press Enter to continue..." if language == "en" else "按回车键继续...",
            "hero_creation": "Create Your Hero" if language == "en" else "创建你的英雄",
            "enter_name": "Enter your hero name: " if language == "en" else "请输入你的英雄名字: ",
            "name_empty": "Name cannot be empty!" if language == "en" else "名字不能为空，请重新输入！",
            "game_start": "Game Start" if language == "en" else "游戏开始",
            "game_over": "Game Over" if language == "en" else "游戏结束",
            "victory": "Victory!" if language == "en" else "恭喜通关！",
            "block_separator": "=" * 50,
            "item_separator": ": ",
            "yes_options": ["y", "Y", "yes", "是"],
        }
    
    def get_text(self, key):
        """获取文本"""
        return self.texts.get(key, key)
    
    def format_text(self, format_type, *args):
        """格式化文本"""
        if format_type == "position_format":
            return f"Position {args[0]}/{args[1]}"
        elif format_type == "hero_marker":
            return "H"
        elif format_type == "event_text":
            if len(args) == 1:
                return f"Event: {args[0]}"
            elif len(args) == 2:
                return f"Event: {args[0]}, Value: {args[1]}"
        elif format_type == "skill_brackets":
            return f"[{args[0]}]"
        elif format_type == "equipment_name":
            if len(args) == 1:
                return args[0]
            elif len(args) == 2:
                return f"{args[0]} +{args[1]}"
        return f"Formatted: {format_type}, {args}"
    
    def set_language(self, language):
        """设置语言"""
        self.language = language
        self.__init__(language)


class MockCombatSystem:
    """模拟战斗系统类"""
    
    def __init__(self, game):
        self.game = game
        self.monsters = {
            "goblin": {"name": "Goblin", "hp": 30, "attack": 10, "defense": 2, "exp": 10, "gold": 10},
            "slime": {"name": "Slime", "hp": 20, "attack": 5, "defense": 5, "exp": 5, "gold": 5},
            "wolf": {"name": "Wolf", "hp": 40, "attack": 15, "defense": 3, "exp": 15, "gold": 15}
        }
        self.bosses = {
            "dragon": {"name": "Dragon", "hp": 100, "attack": 30, "defense": 15, "exp": 100, "gold": 200},
            "titan": {"name": "Titan", "hp": 150, "attack": 40, "defense": 20, "exp": 150, "gold": 300}
        }
    
    def generate_monster(self, multiplier=1.0):
        """生成怪物"""
        import random
        monster_name = random.choice(list(self.monsters.keys()))
        monster = self.monsters[monster_name].copy()
        
        # 应用难度倍数
        monster["hp"] = int(monster["hp"] * multiplier)
        monster["max_hp"] = monster["hp"]
        monster["attack"] = int(monster["attack"] * multiplier)
        monster["exp"] = int(monster["exp"] * multiplier)
        monster["gold"] = int(monster["gold"] * multiplier)
        
        return monster
    
    def generate_boss(self, multiplier=1.0):
        """生成Boss"""
        import random
        boss_name = random.choice(list(self.bosses.keys()))
        boss = self.bosses[boss_name].copy()
        
        # 应用难度倍数
        boss["hp"] = int(boss["hp"] * multiplier)
        boss["max_hp"] = boss["hp"]
        boss["attack"] = int(boss["attack"] * multiplier)
        boss["exp"] = int(boss["exp"] * multiplier)
        boss["gold"] = int(boss["gold"] * multiplier)
        
        return boss
    
    def calculate_damage(self, attack, defense):
        """计算伤害"""
        import random
        random_damage = random.randint(0, 10)
        return max(1, attack - defense + random_damage)
    
    def monster_attack(self, monster):
        """怪物攻击"""
        damage = self.calculate_damage(monster["attack"], self.game.hero_defense)
        self.game.hero_hp -= damage
        return damage
    
    def combat_loop(self, monster):
        """战斗循环"""
        while monster["hp"] > 0 and self.game.hero_hp > 0:
            # 英雄攻击
            damage = self.calculate_damage(self.game.hero_attack, monster["defense"])
            monster["hp"] -= damage
            
            if monster["hp"] <= 0:
                break
            
            # 怪物攻击
            self.monster_attack(monster)
        
        # 战斗结果
        if monster["hp"] <= 0:
            self.game.hero_exp += monster["exp"]
            self.game.hero_gold += monster["gold"]
            return True
        else:
            return False
    
    def combat(self, multiplier=1.0):
        """普通战斗"""
        monster = self.generate_monster(multiplier)
        return self.combat_loop(monster)
    
    def boss_combat(self, multiplier=1.0):
        """Boss战斗"""
        boss = self.generate_boss(multiplier)
        return self.combat_loop(boss)
    
    def ghost_combat(self, multiplier=1.0):
        """幽灵战斗"""
        # 幽灵攻击无视部分防御
        monster = self.generate_monster(multiplier * 0.8)
        monster["name"] = "Ghost"
        
        while monster["hp"] > 0 and self.game.hero_hp > 0:
            # 英雄攻击
            damage = self.calculate_damage(self.game.hero_attack, monster["defense"])
            monster["hp"] -= damage
            
            if monster["hp"] <= 0:
                break
            
            # 幽灵特殊攻击，无视部分防御
            special_damage = max(1, monster["attack"] - self.game.hero_defense // 2)
            self.game.hero_hp -= special_damage
        
        # 战斗结果
        if monster["hp"] <= 0:
            self.game.hero_exp += monster["exp"]
            self.game.hero_gold += monster["gold"]
            return True
        else:
            return False
    
    def gain_exp(self, exp_amount):
        """获得经验值"""
        self.game.hero_exp += exp_amount
        
        # 检查升级
        while self.game.hero_exp >= self.game.hero_level * 100:
            self.game.hero_exp -= self.game.hero_level * 100
            self.game.hero_level += 1
            
            # 提升基础属性
            self.game.base_attack += 2
            self.game.base_defense += 1
            self.game.base_max_hp += 10
            
            # 应用属性更新
            self.game.update_attributes()
    
    def calculate_skill_damage(self, skill_name, monster):
        """计算技能伤害"""
        skill_damage = {
            "fireball": 30,
            "iceball": 25,
            "lightning": 40
        }
        
        base_damage = skill_damage.get(skill_name, 20)
        return max(1, base_damage - monster["defense"] // 2)
    
    def can_use_skill(self, skill_name):
        """检查是否可以使用技能"""
        if skill_name not in self.game.hero_skills:
            return False
        
        skill_levels = {
            "fireball": 1,
            "iceball": 1,
            "lightning": 3
        }
        
        required_level = skill_levels.get(skill_name, 1)
        return self.game.hero_level >= required_level
    
    def use_skill(self, skill_name, monster):
        """使用技能"""
        if not self.can_use_skill(skill_name):
            return False
        
        damage = self.calculate_skill_damage(skill_name, monster)
        monster["hp"] -= damage
        
        return True


class MockEquipmentSystem:
    """模拟装备系统类"""
    
    def __init__(self, game):
        self.game = game
        self.weapons = {
            "Iron Sword": {"type": "weapon", "attack": 5, "defense": 0, "hp": 0, "value": 50},
            "Steel Sword": {"type": "weapon", "attack": 10, "defense": 0, "hp": 0, "value": 100},
            "Magic Sword": {"type": "weapon", "attack": 15, "defense": 0, "hp": 0, "value": 200}
        }
        self.armors = {
            "Leather Armor": {"type": "armor", "attack": 0, "defense": 5, "hp": 10, "value": 75},
            "Iron Armor": {"type": "armor", "attack": 0, "defense": 10, "hp": 20, "value": 150},
            "Magic Armor": {"type": "armor", "attack": 5, "defense": 15, "hp": 30, "value": 300}
        }
        self.accessories = {
            "Ring": {"type": "accessory", "attack": 5, "defense": 2, "hp": 10, "value": 100},
            "Amulet": {"type": "accessory", "attack": 3, "defense": 5, "hp": 15, "value": 150},
            "Crown": {"type": "accessory", "attack": 10, "defense": 3, "hp": 5, "value": 250}
        }
    
    def generate_equipment(self, equip_type):
        """生成装备"""
        import random
        
        if equip_type == "weapon":
            name = random.choice(list(self.weapons.keys()))
            equipment = self.weapons[name].copy()
        elif equip_type == "armor":
            name = random.choice(list(self.armors.keys()))
            equipment = self.armors[name].copy()
        elif equip_type == "accessory":
            name = random.choice(list(self.accessories.keys()))
            equipment = self.accessories[name].copy()
        else:
            # 随机类型
            equip_type = random.choice(["weapon", "armor", "accessory"])
            return self.generate_equipment(equip_type)
        
        equipment["name"] = name
        return equipment
    
    def equip_item(self, item):
        """装备物品"""
        equip_type = item["type"]
        
        # 如果已有装备，先卸下
        if self.game.equipment[equip_type]:
            self.unequip_item(equip_type)
        
        # 装备新物品
        self.game.equipment[equip_type] = item
        
        # 应用属性加成
        self.game.hero_attack += item.get("attack", 0)
        self.game.hero_defense += item.get("defense", 0)
        
        # 如果增加最大血量，按比例增加当前血量
        hp_bonus = item.get("hp", 0)
        if hp_bonus > 0:
            hp_ratio = self.game.hero_hp / self.game.hero_max_hp
            self.game.hero_max_hp += hp_bonus
            self.game.hero_hp = int(self.game.hero_max_hp * hp_ratio)
    
    def unequip_item(self, equip_type):
        """卸下装备"""
        item = self.game.equipment[equip_type]
        if not item:
            return False
        
        # 移除属性加成
        self.game.hero_attack -= item.get("attack", 0)
        self.game.hero_defense -= item.get("defense", 0)
        
        # 如果有血量加成，按比例减少当前血量
        hp_bonus = item.get("hp", 0)
        if hp_bonus > 0:
            hp_ratio = self.game.hero_hp / self.game.hero_max_hp
            self.game.hero_max_hp -= hp_bonus
            self.game.hero_hp = int(self.game.hero_max_hp * hp_ratio)
        
        # 卸下装备
        self.game.equipment[equip_type] = None
        return True
    
    def find_equipment(self):
        """发现装备"""
        import random
        if random.random() < 0.3:  # 30%概率发现装备
            equipment = self.generate_equipment("random")
            self.add_to_inventory(equipment)
            return True
        return False
    
    def add_to_inventory(self, item):
        """添加物品到背包"""
        self.game.inventory.append(item)
    
    def remove_from_inventory(self, item):
        """从背包移除物品"""
        if item in self.game.inventory:
            self.game.inventory.remove(item)
            return True
        return False
    
    def equipment_management(self):
        """装备管理"""
        # 这里只提供一个简单的接口，具体实现由测试类处理
        return True


class MockEventSystem:
    """模拟事件系统类"""
    
    def __init__(self, game):
        self.game = game
        self.events = {
            "trap": {"damage_range": (10, 20)},
            "treasure": {"gold_range": (10, 30)},
            "healing": {"heal_range": (15, 30)},
            "potion": {"count": 1},
            "skill": {"skills": ["fireball", "iceball", "lightning"]}
        }
    
    def use_potion(self):
        """使用药剂"""
        if self.game.hero_potions > 0 and self.game.hero_hp < self.game.hero_max_hp:
            import random
            heal_amount = random.randint(20, 40)
            self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
            self.game.hero_potions -= 1
            return True
        return False
    
    def learn_skill(self):
        """学习技能"""
        import random
        if random.random() < 0.2:  # 20%概率学习技能
            available_skills = [s for s in self.events["skill"]["skills"] 
                              if s not in self.game.hero_skills]
            if available_skills:
                skill = random.choice(available_skills)
                self.game.hero_skills.append(skill)
                return True
        return False
    
    def merchant_event(self, gold_multiplier=1.0):
        """商人事件"""
        # 这里只提供一个简单的接口，具体实现由测试类处理
        return True
    
    def mysterious_merchant(self, gold_multiplier=1.0):
        """神秘商人事件"""
        # 这里只提供一个简单的接口，具体实现由测试类处理
        return True
    
    def show_adventure_history(self):
        """显示冒险历史"""
        # 这里只提供一个简单的接口，具体实现由测试类处理
        return True
    
    def trap_event(self, enemy_multiplier=1.0):
        """陷阱事件"""
        import random
        damage_range = self.events["trap"]["damage_range"]
        base_damage = random.randint(damage_range[0], damage_range[1])
        actual_damage = int(base_damage * enemy_multiplier)
        actual_damage = max(1, actual_damage - self.game.hero_defense)
        self.game.hero_hp -= actual_damage
        return actual_damage
    
    def treasure_event(self, gold_multiplier=1.0):
        """宝箱事件"""
        import random
        gold_range = self.events["treasure"]["gold_range"]
        gold_found = random.randint(gold_range[0], gold_range[1])
        gold_found = int(gold_found * gold_multiplier)
        self.game.hero_gold += gold_found
        return gold_found
    
    def healing_event(self):
        """治疗事件"""
        import random
        heal_range = self.events["healing"]["heal_range"]
        heal_amount = random.randint(heal_range[0], heal_range[1])
        self.game.hero_hp = min(self.game.hero_hp + heal_amount, self.game.hero_max_hp)
        return heal_amount
    
    def potion_event(self):
        """药剂事件"""
        self.game.hero_potions += self.events["potion"]["count"]
        return self.events["potion"]["count"]
    
    def skill_event(self):
        """技能事件"""
        import random
        if random.random() < 0.3:  # 30%概率获得技能
            available_skills = [s for s in self.events["skill"]["skills"] 
                              if s not in self.game.hero_skills]
            if available_skills:
                skill = random.choice(available_skills)
                self.game.hero_skills.append(skill)
                return skill
        return None