# 英雄无敌 (Heroes Invincible) - 架构说明

## 文档信息

- **项目名称**: 英雄无敌 (Heroes Invincible)
- **版本**: 3.0+ (阶段一完成)
- **更新日期**: 2026-01-07
- **维护者**: Kevin

---

## 系统架构概览

### 核心架构模式

```
HeroGame (主控制器)
├── LanguageSupport (国际化系统)
├── CombatSystem (战斗系统)
├── EquipmentSystem (装备系统)
├── EventSystem (事件系统)
├── NewbieVillage (新手村系统)
├── GameStatistics (统计系统) ⭐ NEW
└── SaveManager (存档管理) ⭐ NEW
```

**架构原则**:
- **组合优于继承**: 通过依赖注入组装子系统
- **单一职责**: 每个模块只负责一个核心功能
- **松耦合**: 模块间通过接口通信，减少直接依赖
- **可测试性**: 使用 Mock 对象隔离依赖进行单元测试

---

## 模块详细说明

### 1. 主控制器 (main.py)

**类**: `HeroGame`

**职责**:
- 游戏流程控制（初始化、主循环、游戏结束）
- 子系统协调和初始化
- 玩家输入处理
- UI 显示和交互

**新增功能 (阶段一)**:
- `show_main_menu()` - 主菜单界面
- `load_game_menu()` - 加载存档菜单
- `save_game_menu()` - 保存游戏菜单
- `show_statistics_menu()` - 显示统计信息
- `get_save_data()` - 获取存档数据
- `load_from_save_data()` - 从存档数据恢复游戏

**关键属性**:
```python
# 游戏状态
hero_name, hero_level, hero_exp, hero_hp, hero_max_hp
hero_attack, hero_defense, base_attack, base_defense, base_max_hp
hero_position, hero_gold, hero_potions, hero_skills
equipment, inventory, monsters_defeated, events_encountered

# 游戏设置
difficulty, map_type, language, map_length

# 子系统实例
combat_system, equipment_system, event_system
newbie_village, statistics ⭐ NEW
```

### 2. 存档数据模块 (save_data.py) ⭐ NEW

**类**:
- `SaveData` - 存档数据容器
- `SaveManager` - 存档管理器

#### SaveData 类

**职责**: 封装所有需要持久化的游戏状态

**核心方法**:
```python
__init__(game)  # 从游戏实例提取数据
to_dict()  # 转换为字典（用于JSON序列化）
from_dict(data)  # 从字典创建实例（用于反序列化）
```

**数据字段**:
```python
# 时间戳
save_time, version

# 英雄属性
hero_name, hero_level, hero_exp
hero_hp, hero_max_hp, hero_attack, hero_defense
base_attack, base_defense, base_max_hp

# 游戏进度
hero_position, game_over, victory
hero_gold, hero_potions

# 装备和背包
equipment (dict), inventory (list)

# 游戏设置
difficulty, map_type, language, map_length

# 统计数据
monsters_defeated, events_encountered
visited_positions, statistics_data ⭐ NEW
```

#### SaveManager 类

**职责**: 处理存档的保存、加载和管理

**核心方法**:
```python
save_game(save_data, slot_number)  # 保存游戏
load_game(slot_number)  # 加载游戏
list_save_slots()  # 列出所有存档槽位
delete_save(slot_number)  # 删除存档
get_save_path(slot_number)  # 获取存档文件路径
_validate_save_data(data)  # 验证数据完整性
```

**特点**:
- 支持最多5个存档槽位
- 自动创建存档目录
- JSON 格式存储
- 异常处理和数据验证

### 3. 统计系统模块 (statistics.py) ⭐ NEW

**类**: `GameStatistics`

**职责**: 追踪和记录游戏过程中的各种数据

**统计维度**:

```python
# 时间统计
session_start_time, total_play_time

# 移动统计
total_steps

# 战斗统计
total_battles, battles_won, battles_lost
max_win_streak, current_win_streak

# 怪物统计
monsters_defeated, monsters_by_type (dict)
bosses_defeated, bosses_by_type (dict)

# 资源统计
total_gold_earned, total_gold_spent
total_exp_earned

# 事件统计
total_events_triggered, events_by_type (dict)

# 装备统计
equipment_found, equipment_by_rarity (dict)

# 药剂统计
potions_found, potions_used

# 技能统计
skills_learned, skill_uses (dict)

# 商店统计
shop_visits, items_purchased
```

**集成方式**:

统计系统已完全集成到游戏的所有子系统中：

```python
# 在 HeroGame 中初始化
self.statistics = GameStatistics()

# 在各个事件中调用统计记录
self.statistics.record_step()  # 移动时
self.statistics.record_battle_start()  # 战斗开始
self.statistics.record_battle_victory(monster_name, is_boss)  # 战斗胜利
self.statistics.record_gold_earned(amount)  # 获得金币
self.statistics.record_event_triggered(event_type)  # 触发事件
# ... 等等
```

**集成位置**:
- **CombatSystem**: 战斗开始/结束、技能使用、药剂使用
- **EventSystem**: 学习技能、商店访问、药剂使用
- **EquipmentSystem**: 商店访问、购买装备、获得装备
- **HeroGame**: 移动步数、所有类型事件触发

**核心方法**:
```python
# 记录方法
record_step()  # 记录移动
record_battle_start()  # 记录战斗开始
record_battle_victory(monster_name, is_boss)  # 记录战斗胜利
record_battle_defeat()  # 记录战斗失败
record_gold_earned(amount)  # 记录获得金币
record_gold_spent(amount)  # 记录花费金币
record_exp_earned(amount)  # 记录获得经验
record_event_triggered(event_type)  # 记录事件触发
record_equipment_found(rarity)  # 记录获得装备
record_potion_found()  # 记录获得药剂
record_potion_used()  # 记录使用药剂
record_skill_learned(skill_name)  # 记录学习技能
record_skill_used(skill_name)  # 记录使用技能
record_shop_visit()  # 记录访问商店
record_item_purchased(count)  # 记录购买物品

# 计算方法
get_win_rate()  # 计算胜率
get_average_gold_per_battle()  # 计算平均金币
get_play_time_formatted()  # 获取格式化时长
format_summary(lang)  # 格式化统计摘要
update_play_time()  # 更新游戏时长

# 序列化方法
to_dict()  # 转换为字典
from_dict(data)  # 从字典创建
```

### 4. 语言支持模块 (language.py)

**类**: `LanguageSupport`

**职责**: 提供中英双语支持

**新增文本 (阶段一)**:
- 存档系统相关文本（约30个）
- 统计系统相关文本（约20个）

**核心方法**:
```python
get_text(key)  # 获取指定键的文本
format_text(format_type, *args)  # 格式化文本
```

### 5. 其他模块

#### CombatSystem (combat.py)
战斗系统，处理回合制战斗逻辑

#### EquipmentSystem (equipment.py)
装备系统，生成和管理装备

#### EventSystem (events.py)
事件系统，触发随机事件

#### NewbieVillage (newbie_village.py)
新手村系统，教程和准备区域

### 6. 扩展的游戏配置模块 (game_config.py) ⭐ UPDATED

**职责**: 管理所有游戏数据配置和模板

**新增功能 (阶段二)**:
- **新增地图类型**: 沼泽（swamp）和雪原（snowfield）
- **新增怪物模板**: 6个新怪物（鳄鱼、毒蛇、沼泽巨兽、冰狼、雪怪、冰霜巨人）
- **新增Boss模板**: 沼泽九头蛇和冰霜之王
- **扩展特殊事件系统**: 每个地图的独特事件

**关键数据结构更新**:
```python
# 地图类型扩展 (从5个增加到7个)
MAP_TYPES = {
    "plains": {...},
    "forest": {...},
    "desert": {...},
    "volcano": {...},
    "mountains": {...},
    "swamp": {  # ⭐ NEW
        "name": "swamp",
        "monsters": ["crocodile", "venom_snake", "swamp_beast"],
        "special_events": ["poison_cloud", "quicksand", "rare_herbs", "swamp_merchant"],
        "boss": "swamp_hydra"
    },
    "snowfield": {  # ⭐ NEW
        "name": "snowfield",
        "monsters": ["ice_wolf", "snow_beast", "frost_giant"],
        "special_events": ["frostbite", "avalanche", "ice_cave", "frost_effect"],
        "boss": "frost_king"
    }
}

# 怪物模板扩展
MONSTER_TEMPLATES = {
    # 原有怪物...
    "crocodile": {  # ⭐ NEW
        "name": "crocodile", "hp": 35, "attack": 18, "defense": 12
    },
    "venom_snake": {  # ⭐ NEW
        "name": "venom_snake", "hp": 25, "attack": 20, "defense": 8, "special": "poison"
    },
    # ... 其他新怪物
}

# Boss模板扩展
BOSS_TEMPLATES = {
    # 原有Boss...
    "swamp": {  # ⭐ NEW
        "name": "swamp_hydra", "hp": 150, "attack": 25, "defense": 15,
        "skills": ["poison_bite", "regeneration"]
    },
    "snowfield": {  # ⭐ NEW
        "name": "frost_king", "hp": 180, "attack": 28, "defense": 18,
        "skills": ["blizzard", "ice_prison"]
    }
}
```

### 7. 扩展的战斗系统模块 (combat.py) ⭐ UPDATED

**职责**: 战斗逻辑、状态效果、伤害计算

**新增功能 (阶段二)**:
- **状态效果系统**: 中毒、冻伤、冰霜效果
- **状态效果持续时间管理**
- **状态效果伤害计算**
- **新Boss技能实现**

**关键功能更新**:
```python
# 状态效果系统
class CombatSystem:
    def __init__(self, game):
        self.game = game
        
    def apply_status_effect(self, target, effect_type, duration):
        """应用状态效果"""
        # 实现中毒、冻伤、冰霜效果
        
    def update_status_effects(self):
        """更新状态效果持续时间"""
        
    def calculate_status_damage(self, effect_type):
        """计算状态效果伤害"""
        
    # 新Boss技能实现
    def boss_poison_bite(self, boss_name, boss_attack):
        """Boss毒液咬技能"""
        
    def boss_blizzard(self, boss_name, boss_attack):
        """Boss暴风雪技能"""
```

### 8. 新功能测试模块 (tests/test_new_features.py) ⭐ NEW

**职责**: 验证阶段二新增功能的完整性和正确性

**测试范围**:
- 新地图验证测试
- 新怪物系统测试
- 状态效果系统测试
- Boss系统测试
- 存档/读档功能测试

**关键测试类**:
```python
class TestNewFeatures(unittest.TestCase):
    """测试新增功能的类"""
    
    def test_swamp_map_exists(self):
        """测试沼泽地图是否存在"""
        
    def test_snowfield_map_exists(self):
        """测试雪原地图是否存在"""
        
    def test_new_monsters_exist(self):
        """测试新怪物是否存在"""
        
    def test_boss_templates_exist(self):
        """测试Boss模板是否存在"""
        
    def test_status_effects_initialization(self):
        """测试状态效果初始化"""
        
    def test_status_effects_methods(self):
        """测试状态效果方法"""
        
    def test_status_effects_update(self):
        """测试状态效果更新"""
        
    def test_save_load_status_effects(self):
        """测试状态效果的保存和加载"""
```

---

## 数据流

### 游戏启动流程

```
1. main() → HeroGame.__init__()
   ├── 初始化语言系统
   ├── select_language() - 选择语言
   ├── select_map_and_difficulty() - 选择地图和难度
   └── 初始化英雄属性和子系统

2. show_welcome() - 显示欢迎界面

3. show_main_menu() - 显示主菜单
   ├── 选项1: 新游戏
   │   ├── get_hero_name()
   │   ├── select_map_and_difficulty()
   │   ├── newbie_village.newbie_village()
   │   └── game_loop()
   ├── 选项2: 加载存档
   │   └── load_game_menu()
   ├── 选项3: 查看统计 ⭐ NEW
   │   └── show_statistics_menu()
   └── 选项4: 退出游戏
```

### 存档流程

```
保存游戏:
HeroGame → save_game_menu()
    → SaveManager.save_game()
        → SaveData.to_dict()
            → JSON序列化 → 文件

加载游戏:
HeroGame → load_game_menu()
    → SaveManager.load_game()
        → JSON反序列化
        → SaveData.from_dict()
            → HeroGame.load_from_save_data()
```

### 统计数据收集流程

```
游戏事件 → GameStatistics.record_*()
    → 更新内部统计计数器
    → 保存时通过 to_dict() 序列化
    → 加载时通过 from_dict() 反序列化
```

---

## 文件结构

```
src/hero/
├── main.py              # 主控制器
├── language.py          # 语言支持
├── game_config.py       # 游戏配置 (已扩展) ⭐ UPDATED
├── combat.py            # 战斗系统 (已扩展) ⭐ UPDATED
├── equipment.py         # 装备系统
├── events.py            # 事件系统
├── newbie_village.py    # 新手村
├── save_data.py         # 存档系统 ⭐ NEW
└── statistics.py        # 统计系统 ⭐ NEW

tests/
├── test_save_data.py    # 存档测试 ⭐ NEW
├── test_statistics.py   # 统计测试 ⭐ NEW
├── test_new_features.py # 新功能测试套件 ⭐ NEW
├── test_combat.py
├── test_equipment.py
├── test_events.py
└── test_newbie_village.py

saves/                   # 存档目录 ⭐ NEW
├── save_slot_1.json
├── save_slot_2.json
├── ...
└── save_slot_5.json

memory-bank/            # 文档目录 ⭐ NEW
├── design-doc.md       # 设计文档
├── implementation-plan.md  # 实施计划
├── progress.md         # 项目进展 ⭐ NEW
└── architecture.md     # 架构说明 (本文件)
```

---

## 设计模式应用

### 1. 组合模式 (Composition)
```
HeroGame 包含多个子系统实例，而不是继承它们
```

### 2. 工厂模式 (Factory)
```
EquipmentSystem.create_random_equipment() - 创建装备
SaveData.from_dict() - 从字典创建SaveData
GameStatistics.from_dict() - 从字典创建统计
```

### 3. 单例模式 (Singleton)
```
每个HeroGame实例只有一个SaveManager实例
```

### 4. 策略模式 (Strategy)
```
不同难度和地图类型的配置策略
```

### 5. 观察者模式 (Observer)
```
语言切换触发所有UI文本更新
```

---

## 扩展指南

### 添加新的统计追踪

1. 在 `GameStatistics` 类中添加记录方法
2. 在相应的事件处理中调用记录方法
3. 更新 `format_summary()` 方法显示新统计
4. 在 `to_dict()` 和 `from_dict()` 中添加序列化支持
5. 在 `language.py` 添加相关文本

### 添加新的存档字段

1. 在 `SaveData.__init__()` 中添加字段提取
2. 在 `to_dict()` 中添加序列化
3. 在 `from_dict()` 中添加反序列化
4. 在 `HeroGame.load_from_save_data()` 中添加恢复逻辑

### 添加新的UI选项

1. 在 `language.py` 添加文本
2. 在相应的菜单方法中添加选项
3. 添加处理逻辑
4. 更新测试

---

## 性能考虑

- **存档大小**: 单个存档约 5-10KB
- **内存占用**: 统计系统约增加 2KB
- **序列化速度**: JSON 序列化 < 10ms
- **存档目录**: 自动创建，支持多槽位

---

## 安全考虑

- **输入验证**: 所有用户输入都有验证
- **异常处理**: 存档操作有完整的异常处理
- **数据验证**: 加载存档时验证数据完整性
- **文件权限**: 存档目录权限检查

---

## 测试策略

### 单元测试
- `test_save_data.py` - 存档系统测试（10个测试）
- `test_statistics.py` - 统计系统测试（16个测试）
- 其他模块测试

### 集成测试
- 存档和加载完整流程
- 统计数据在游戏过程中的收集
- 多语言界面测试

### 测试覆盖率
- 存档系统: 100%
- 统计系统: 100%
- 总体: >90%

---

## 未来改进

### 短期 (阶段二 - ✅ 已完成)
- ✅ 更多地图类型（沼泽、雪原）
- ✅ Boss 战机制
- ✅ 更多怪物和装备
- ✅ 状态效果系统

### 中期 (阶段三)
- 成就系统
- 职业系统
- 技能树

### 长期
- GUI 界面
- 网络多人
- 数据库持久化

---

*最后更新: 2026-01-07*
*维护者: Kevin*
