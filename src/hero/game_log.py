"""
游戏日志系统
记录游戏中的各种事件和活动
"""

import time
from datetime import datetime


class GameLog:
    """游戏日志类"""
    
    def __init__(self, language="zh"):
        """初始化游戏日志系统"""
        self.language = language
        self.log_entries = []
        self.max_entries = 200  # 最多保存200条日志
    
    def log_event(self, event_type, description, details=None):
        """
        记录游戏事件
        
        Args:
            event_type (str): 事件类型（战斗、事件、物品等）
            description (str): 事件描述
            details (dict): 事件详细信息
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        entry = {
            "timestamp": timestamp,
            "type": event_type,
            "description": description,
            "details": details or {}
        }
        
        self.log_entries.append(entry)
        
        # 保持日志长度不超过最大值
        if len(self.log_entries) > self.max_entries:
            self.log_entries = self.log_entries[-self.max_entries:]
    
    def log_combat(self, result, enemy_name, damage_taken=0, damage_dealt=0):
        """记录战斗事件"""
        details = {
            "result": result,
            "enemy": enemy_name,
            "damage_taken": damage_taken,
            "damage_dealt": damage_dealt
        }
        
        if self.language == "zh":
            description = f"与 {enemy_name} 战斗，结果：{result}"
        else:
            description = f"Combat with {enemy_name}, result: {result}"
        
        self.log_event("combat", description, details)
    
    def log_event_triggered(self, event_type, event_name, outcome=None):
        """记录随机事件"""
        details = {
            "event_type": event_type,
            "event_name": event_name,
            "outcome": outcome
        }
        
        if self.language == "zh":
            description = f"触发事件：{event_name}"
            if outcome:
                description += f"，结果：{outcome}"
        else:
            description = f"Event triggered: {event_name}"
            if outcome:
                description += f", outcome: {outcome}"
        
        self.log_event("event", description, details)
    
    def log_item_obtained(self, item_type, item_name, quantity=1):
        """记录获得物品"""
        details = {
            "item_type": item_type,
            "item_name": item_name,
            "quantity": quantity
        }
        
        if self.language == "zh":
            description = f"获得 {item_name} x{quantity}"
        else:
            description = f"Obtained {item_name} x{quantity}"
        
        self.log_event("item", description, details)
    
    def log_level_up(self, new_level, stat_changes=None):
        """记录升级事件"""
        details = {
            "new_level": new_level,
            "stat_changes": stat_changes or {}
        }
        
        if self.language == "zh":
            description = f"升级到 {new_level} 级"
        else:
            description = f"Leveled up to level {new_level}"
        
        self.log_event("level", description, details)
    
    def log_position_change(self, new_position, map_type):
        """记录位置变化"""
        details = {
            "position": new_position,
            "map_type": map_type
        }
        
        if self.language == "zh":
            description = f"移动到位置 {new_position} ({map_type}地图)"
        else:
            description = f"Moved to position {new_position} ({map_type} map)"
        
        self.log_event("movement", description, details)
    
    def log_achievement(self, achievement_name):
        """记录成就解锁"""
        details = {
            "achievement": achievement_name
        }
        
        if self.language == "zh":
            description = f"解锁成就：{achievement_name}"
        else:
            description = f"Achievement unlocked: {achievement_name}"
        
        self.log_event("achievement", description, details)
    
    def get_recent_logs(self, count=10, event_type=None):
        """
        获取最近的日志条目
        
        Args:
            count (int): 返回的日志数量
            event_type (str): 过滤的事件类型
            
        Returns:
            list: 日志条目列表
        """
        if event_type:
            filtered_logs = [log for log in self.log_entries if log["type"] == event_type]
            return filtered_logs[-count:]
        else:
            return self.log_entries[-count:]
    
    def format_log_entry(self, entry):
        """格式化单个日志条目"""
        timestamp = entry["timestamp"]
        description = entry["description"]
        
        return f"[{timestamp}] {description}"
    
    def format_log_summary(self, count=20, event_type=None):
        """
        格式化日志摘要
        
        Args:
            count (int): 显示的日志数量
            event_type (str): 过滤的事件类型
            
        Returns:
            str: 格式化的日志摘要
        """
        logs = self.get_recent_logs(count, event_type)
        
        if not logs:
            if self.language == "zh":
                return "暂无游戏日志"
            else:
                return "No game logs available"
        
        formatted_logs = []
        for entry in logs:
            formatted_logs.append(self.format_log_entry(entry))
        
        return "\n".join(formatted_logs)
    
    def clear_log(self):
        """清空日志"""
        self.log_entries = []
    
    def to_dict(self):
        """将日志转换为字典，用于序列化"""
        return {
            "language": self.language,
            "log_entries": self.log_entries,
            "max_entries": self.max_entries
        }
    
    def from_dict(self, data):
        """从字典加载日志"""
        self.language = data.get("language", "zh")
        self.log_entries = data.get("log_entries", [])
        self.max_entries = data.get("max_entries", 200)
    
    def get_statistics(self):
        """获取日志统计信息"""
        stats = {
            "total_entries": len(self.log_entries),
            "event_types": {},
            "recent_activity": {}
        }
        
        # 统计事件类型分布
        for entry in self.log_entries:
            event_type = entry["type"]
            stats["event_types"][event_type] = stats["event_types"].get(event_type, 0) + 1
        
        # 最近一小时的活动统计
        current_time = datetime.now()
        one_hour_ago = current_time.timestamp() - 3600
        
        for entry in self.log_entries:
            # 这里简化处理，实际应该解析时间戳
            stats["recent_activity"] = {"last_hour": len(self.log_entries) // 2}  # 简化统计
            break
        
        return stats
    
    def get_logs(self):
        """获取所有日志条目"""
        return self.log_entries
    
    def get_logs_by_type(self, event_type):
        """按类型获取日志条目"""
        return [log for log in self.log_entries if log["type"] == event_type]
    
    def show_all_logs(self):
        """显示所有日志"""
        logs = self.get_logs()
        if not logs:
            if self.language == "zh":
                print("暂无游戏日志记录")
            else:
                print("No game logs available")
            return
        
        for i, entry in enumerate(logs, 1):
            print(f"{i}. {self.format_log_entry(entry)}")
    
    def show_recent_logs(self, count=10):
        """显示最近的日志"""
        logs = self.get_recent_logs(count)
        if not logs:
            if self.language == "zh":
                print("暂无游戏日志记录")
            else:
                print("No game logs available")
            return
        
        for i, entry in enumerate(logs, 1):
            print(f"{i}. {self.format_log_entry(entry)}")
    
    def show_logs_by_type(self, event_type):
        """按类型显示日志"""
        logs = self.get_logs_by_type(event_type)
        if not logs:
            if self.language == "zh":
                print(f"暂无{event_type}类型的日志记录")
            else:
                print(f"No {event_type} logs available")
            return
        
        for i, entry in enumerate(logs, 1):
            print(f"{i}. {self.format_log_entry(entry)}")
    
    def add_log(self, event_type, description, details=None):
        """添加日志（兼容性方法）"""
        self.log_event(event_type, description, details)