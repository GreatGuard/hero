# -*- coding: utf-8 -*-
"""
游戏统计模块 - 追踪游戏数据统计
"""

import time
from datetime import datetime, timedelta


class GameStatistics:
    """游戏统计数据类 - 追踪各种游戏行为数据"""

    def __init__(self):
        """初始化统计数据"""
        # 时间统计
        self.session_start_time = time.time()
        self.total_play_time = 0  # 总游戏时长（秒）

        # 移动统计
        self.total_steps = 0  # 总移动步数

        # 战斗统计
        self.total_battles = 0  # 总战斗次数
        self.battles_won = 0  # 战斗胜利次数
        self.battles_lost = 0  # 战斗失败次数
        self.max_win_streak = 0  # 最大连胜
        self.current_win_streak = 0  # 当前连胜

        # 怪物统计
        self.monsters_defeated = 0  # 击败怪物总数
        self.monsters_by_type = {}  # 各类型怪物击败数量

        # Boss统计
        self.bosses_defeated = 0  # 击败Boss总数
        self.bosses_by_type = {}  # 各类型Boss击败数量

        # 资源统计
        self.total_gold_earned = 0  # 总获得金币
        self.total_gold_spent = 0  # 总花费金币
        self.total_exp_earned = 0  # 总获得经验

        # 事件统计
        self.total_events_triggered = 0  # 总触发事件数
        self.events_by_type = {}  # 各类型事件触发次数

        # 装备统计
        self.equipment_found = 0  # 获得装备数量
        self.equipment_by_rarity = {  # 各稀有度装备数量
            "common": 0,
            "uncommon": 0,
            "rare": 0,
            "epic": 0,
            "legendary": 0
        }
        
        # 附魔统计
        self.enchantments_attempted = 0  # 附魔尝试次数
        self.enchantments_successful = 0  # 附魔成功次数
        self.enchantments_failed = 0  # 附魔失败次数
        self.enchantments_by_type = {}  # 各类型附魔次数

        # 药剂使用统计
        self.potions_used = 0  # 使用的药剂总数
        self.potions_found = 0  # 获得的药剂总数

        # 技能统计
        self.skills_learned = 0  # 学习的技能数
        self.skill_uses = {}  # 各技能使用次数

        # 商店访问统计
        self.shop_visits = 0  # 访问商店次数
        self.items_purchased = 0  # 购买物品数量

    def record_step(self):
        """记录移动一步"""
        self.total_steps += 1

    def record_battle_start(self):
        """记录战斗开始"""
        self.total_battles += 1

    def record_battle_victory(self, monster_name=None, is_boss=False):
        """
        记录战斗胜利

        Args:
            monster_name: 怪物名称
            is_boss: 是否为Boss
        """
        self.battles_won += 1
        self.current_win_streak += 1

        # 更新最大连胜
        if self.current_win_streak > self.max_win_streak:
            self.max_win_streak = self.current_win_streak

        # 记录怪物击败
        if monster_name:
            if is_boss:
                self.bosses_defeated += 1
                self.bosses_by_type[monster_name] = self.bosses_by_type.get(monster_name, 0) + 1
            else:
                self.monsters_defeated += 1
                self.monsters_by_type[monster_name] = self.monsters_by_type.get(monster_name, 0) + 1

    def record_battle_defeat(self):
        """记录战斗失败"""
        self.battles_lost += 1
        self.current_win_streak = 0

    def record_gold_earned(self, amount):
        """记录获得金币"""
        self.total_gold_earned += amount

    def record_gold_spent(self, amount):
        """记录花费金币"""
        self.total_gold_spent += amount

    def record_exp_earned(self, amount):
        """记录获得经验"""
        self.total_exp_earned += amount

    def record_event_triggered(self, event_type):
        """
        记录事件触发

        Args:
            event_type: 事件类型（如"mine_trap", "find_bun", "encounter_monster"等）
        """
        self.total_events_triggered += 1
        self.events_by_type[event_type] = self.events_by_type.get(event_type, 0) + 1

    def record_equipment_found(self, rarity):
        """
        记录获得装备

        Args:
            rarity: 装备稀有度（"common", "uncommon", "rare", "epic", "legendary"）
        """
        self.equipment_found += 1
        if rarity in self.equipment_by_rarity:
            self.equipment_by_rarity[rarity] += 1

    def record_potion_found(self):
        """记录获得药剂"""
        self.potions_found += 1

    def record_potion_used(self):
        """记录使用药剂"""
        self.potions_used += 1

    def record_skill_learned(self, skill_name):
        """
        记录学习技能

        Args:
            skill_name: 技能名称
        """
        self.skills_learned += 1
        self.skill_uses[skill_name] = self.skill_uses.get(skill_name, 0)  # 初始化使用次数为0

    def record_skill_used(self, skill_name):
        """
        记录使用技能

        Args:
            skill_name: 技能名称
        """
        self.skill_uses[skill_name] = self.skill_uses.get(skill_name, 0) + 1

    def record_shop_visit(self):
        """记录访问商店"""
        self.shop_visits += 1

    def record_item_purchased(self, count=1):
        """
        记录购买物品

        Args:
            count: 购买数量
        """
        self.items_purchased += count

    def record_enchantment_success(self, enchantment_type=None):
        """
        记录附魔成功

        Args:
            enchantment_type: 附魔类型
        """
        self.enchantments_attempted += 1
        self.enchantments_successful += 1
        if enchantment_type:
            self.enchantments_by_type[enchantment_type] = self.enchantments_by_type.get(enchantment_type, 0) + 1

    def record_enchantment_failed(self):
        """记录附魔失败"""
        self.enchantments_attempted += 1
        self.enchantments_failed += 1

    def update_play_time(self):
        """更新总游戏时长"""
        current_session = time.time() - self.session_start_time
        self.total_play_time += current_session
        self.session_start_time = time.time()  # 重置会话开始时间

    def get_win_rate(self):
        """
        计算胜率

        Returns:
            float: 胜率百分比（0-100）
        """
        if self.total_battles == 0:
            return 0.0
        return (self.battles_won / self.total_battles) * 100

    def get_average_gold_per_battle(self):
        """
        计算平均每场战斗获得金币

        Returns:
            float: 平均金币数
        """
        if self.total_battles == 0:
            return 0.0
        return self.total_gold_earned / self.total_battles

    def get_play_time_formatted(self):
        """
        获取格式化的游戏时长

        Returns:
            str: 格式化的时长字符串（如"1小时30分钟"）
        """
        self.update_play_time()
        hours = int(self.total_play_time // 3600)
        minutes = int((self.total_play_time % 3600) // 60)
        seconds = int(self.total_play_time % 60)

        return f"{hours}h {minutes}m {seconds}s"

    def to_dict(self):
        """
        将统计数据转换为字典（用于存档）

        Returns:
            dict: 包含所有统计数据的字典
        """
        return {
            "total_play_time": self.total_play_time,
            "total_steps": self.total_steps,
            "total_battles": self.total_battles,
            "battles_won": self.battles_won,
            "battles_lost": self.battles_lost,
            "max_win_streak": self.max_win_streak,
            "monsters_defeated": self.monsters_defeated,
            "monsters_by_type": self.monsters_by_type,
            "bosses_defeated": self.bosses_defeated,
            "bosses_by_type": self.bosses_by_type,
            "total_gold_earned": self.total_gold_earned,
            "total_gold_spent": self.total_gold_spent,
            "total_exp_earned": self.total_exp_earned,
            "total_events_triggered": self.total_events_triggered,
            "events_by_type": self.events_by_type,
            "equipment_found": self.equipment_found,
            "equipment_by_rarity": self.equipment_by_rarity,
            "potions_used": self.potions_used,
            "potions_found": self.potions_found,
            "skills_learned": self.skills_learned,
            "skill_uses": self.skill_uses,
            "shop_visits": self.shop_visits,
            "items_purchased": self.items_purchased,
            "enchantments_attempted": self.enchantments_attempted,
            "enchantments_successful": self.enchantments_successful,
            "enchantments_failed": self.enchantments_failed,
            "enchantments_by_type": self.enchantments_by_type
        }

    @classmethod
    def from_dict(cls, data):
        """
        从字典创建统计数据实例（用于读档）

        Args:
            data: 包含统计数据的字典

        Returns:
            GameStatistics: 统计数据实例
        """
        stats = cls()
        stats.total_play_time = data.get("total_play_time", 0)
        stats.total_steps = data.get("total_steps", 0)
        stats.total_battles = data.get("total_battles", 0)
        stats.battles_won = data.get("battles_won", 0)
        stats.battles_lost = data.get("battles_lost", 0)
        stats.max_win_streak = data.get("max_win_streak", 0)
        stats.monsters_defeated = data.get("monsters_defeated", 0)
        stats.monsters_by_type = data.get("monsters_by_type", {})
        stats.bosses_defeated = data.get("bosses_defeated", 0)
        stats.bosses_by_type = data.get("bosses_by_type", {})
        stats.total_gold_earned = data.get("total_gold_earned", 0)
        stats.total_gold_spent = data.get("total_gold_spent", 0)
        stats.total_exp_earned = data.get("total_exp_earned", 0)
        stats.total_events_triggered = data.get("total_events_triggered", 0)
        stats.events_by_type = data.get("events_by_type", {})
        stats.equipment_found = data.get("equipment_found", 0)
        stats.equipment_by_rarity = data.get("equipment_by_rarity", {
            "common": 0,
            "uncommon": 0,
            "rare": 0,
            "epic": 0,
            "legendary": 0
        })
        stats.potions_used = data.get("potions_used", 0)
        stats.potions_found = data.get("potions_found", 0)
        stats.skills_learned = data.get("skills_learned", 0)
        stats.skill_uses = data.get("skill_uses", {})
        stats.shop_visits = data.get("shop_visits", 0)
        stats.items_purchased = data.get("items_purchased", 0)
        stats.enchantments_attempted = data.get("enchantments_attempted", 0)
        stats.enchantments_successful = data.get("enchantments_successful", 0)
        stats.enchantments_failed = data.get("enchantments_failed", 0)
        stats.enchantments_by_type = data.get("enchantments_by_type", {})

        return stats

    def format_summary(self, lang):
        """
        格式化统计摘要（支持中英双语）

        Args:
            lang: LanguageSupport实例

        Returns:
            str: 格式化的统计摘要字符串
        """
        lines = []
        separator = lang.get_text("block_separator")

        lines.append(separator)
        lines.append(f"          {lang.get_text('adventure_history')}")
        lines.append(separator)
        lines.append("")

        # 时间统计
        lines.append(f"⏱️  {lang.get_text('play_time')}: {self.get_play_time_formatted()}")
        lines.append(f"📍 {lang.get_text('total_steps')}: {self.total_steps}")
        lines.append("")

        # 战斗统计
        lines.append(f"⚔️  {lang.get_text('battle_statistics')}:")
        lines.append(f"   {lang.get_text('total_battles')}: {self.total_battles}")
        lines.append(f"   {lang.get_text('battles_won')}: {self.battles_won}")
        lines.append(f"   {lang.get_text('battles_lost')}: {self.battles_lost}")
        lines.append(f"   {lang.get_text('win_rate')}: {self.get_win_rate():.1f}%")
        lines.append(f"   {lang.get_text('max_win_streak')}: {self.max_win_streak}")
        lines.append("")

        # 怪物统计
        lines.append(f"💀 {lang.get_text('monster_statistics')}:")
        lines.append(f"   {lang.get_text('monsters_defeated')}: {self.monsters_defeated}")
        lines.append(f"   {lang.get_text('bosses_defeated')}: {self.bosses_defeated}")
        lines.append("")

        # 资源统计
        lines.append(f"💰 {lang.get_text('resource_statistics')}:")
        lines.append(f"   {lang.get_text('total_gold_earned')}: {self.total_gold_earned}")
        lines.append(f"   {lang.get_text('total_gold_spent')}: {self.total_gold_spent}")
        lines.append(f"   {lang.get_text('total_exp_earned')}: {self.total_exp_earned}")
        lines.append("")

        # 装备统计
        if self.equipment_found > 0:
            lines.append(f"🗡️  {lang.get_text('equipment_statistics')}:")
            lines.append(f"   {lang.get_text('equipment_found')}: {self.equipment_found}")
            for rarity, count in self.equipment_by_rarity.items():
                if count > 0:
                    rarity_name = lang.get_text(f"rarity_{rarity}")
                    lines.append(f"   {rarity_name}: {count}")
            lines.append("")

        # 药剂统计
        if self.potions_found > 0 or self.potions_used > 0:
            lines.append(f"🧪 {lang.get_text('potion_statistics')}:")
            lines.append(f"   {lang.get_text('potions_found')}: {self.potions_found}")
            lines.append(f"   {lang.get_text('potions_used')}: {self.potions_used}")
            lines.append("")

        # 技能统计
        if self.skills_learned > 0:
            lines.append(f"🔥 {lang.get_text('skill_statistics')}:")
            lines.append(f"   {lang.get_text('skills_learned')}: {self.skills_learned}")
            lines.append("")

        return "\n".join(lines)

