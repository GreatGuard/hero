# 英雄无敌游戏测试文档

## 概述

本项目包含针对英雄无敌文字冒险游戏的全面单元测试和集成测试。测试覆盖了游戏的核心功能模块，包括游戏配置、语言支持、战斗系统、装备系统、事件系统、新手村和主游戏逻辑。

## 测试架构

### 目录结构

```
tests/
├── __init__.py                    # 测试模块初始化
├── README.md                      # 测试文档（本文件）
├── test_game_config.py            # 游戏配置模块测试
├── test_language.py               # 语言支持模块测试
├── test_combat.py                 # 战斗系统测试
├── test_equipment.py              # 装备系统测试
├── test_events.py                 # 事件系统测试
├── test_newbie_village.py         # 新手村测试
├── test_main.py                   # 主游戏类测试
├── integration/                   # 集成测试
│   ├── __init__.py
│   └── test_game_flow.py          # 游戏流程集成测试
├── fixtures/                      # 测试数据
│   ├── __init__.py
│   └── game_data.py               # 游戏测试数据
└── utils/                         # 测试工具
    ├── __init__.py
    ├── test_helpers.py             # 测试辅助函数
    └── mock_classes.py             # 模拟类定义
```

## 测试模块详解

### 1. 基础模块测试

#### test_game_config.py
测试游戏配置模块，包括：
- 难度设置结构完整性验证
- 难度递增数值合理性检查
- 地图类型设置完整性验证
- 配置值正数性检查

#### test_language.py
测试语言支持模块，包括：
- 语言初始化功能
- 文本获取功能
- 语言切换功能
- 格式化函数正确性

### 2. 核心功能模块测试

#### test_combat.py
测试战斗系统，包括：
- 战斗系统初始化
- 怪物和Boss生成机制
- 伤害计算逻辑
- 战斗胜利/失败条件
- 升级检查和技能使用

#### test_equipment.py
测试装备系统，包括：
- 装备系统初始化
- 装备生成机制
- 装备和卸下功能
- 属性计算逻辑
- 背包管理功能

#### test_events.py
测试事件系统，包括：
- 事件系统初始化
- 药剂使用功能
- 技能学习功能
- 商人事件
- 陷阱、宝箱等随机事件

#### test_newbie_village.py
测试新手村功能，包括：
- 新手村初始化
- 训练场功能
- 商店购物功能
- 技能大师教学
- 村庄菜单和地图

### 3. 主游戏类测试

#### test_main.py
测试主游戏类，包括：
- 游戏初始化
- 语言和设置选择
- 游戏核心功能
- 游戏状态检查
- 重新开始功能

### 4. 集成测试

#### test_game_flow.py
测试游戏流程集成，包括：
- 完整游戏流程测试
- 游戏胜利/失败流程
- 升级集成流程
- 装备集成流程
- 战斗集成流程
- 新手村集成流程
- 随机事件集成流程

## 运行测试

### 1. 运行所有测试

使用项目根目录的测试运行脚本：

```bash
python run_tests.py
```

或直接使用Python的unittest模块：

```bash
python -m unittest discover tests
```

### 2. 运行特定模块测试

```bash
python run_tests.py -m test_game_config
```

### 3. 运行特定类测试

```bash
python run_tests.py -m test_combat -c TestCombatSystem
```

### 4. 运行特定方法测试

```bash
python run_tests.py -m test_combat -c TestCombatSystem -f test_combat_victory
```

### 5. 生成测试报告

```bash
python run_tests.py --report --output test_report.txt
```

### 6. 详细输出模式

```bash
python run_tests.py --verbose
```

## 测试数据和工具

### 测试数据 (fixtures/game_data.py)

包含测试用的标准数据：
- 测试英雄数据
- 测试怪物数据
- 测试装备数据
- 测试事件序列
- 测试技能数据
- 测试商店数据

### 测试辅助函数 (utils/test_helpers.py)

提供测试辅助功能：
- 创建模拟游戏对象
- 捕获标准输出
- 比较字典
- 创建测试怪物和装备
- 模拟用户输入和随机值
- 断言辅助函数

### 模拟类 (utils/mock_classes.py)

提供完整的模拟类：
- MockHeroGame: 模拟游戏类
- MockLanguageSupport: 模拟语言支持类
- MockCombatSystem: 模拟战斗系统
- MockEquipmentSystem: 模拟装备系统
- MockEventSystem: 模拟事件系统

## 测试策略

### 1. 单元测试

- 独立测试每个模块的功能
- 使用模拟对象隔离依赖
- 覆盖核心业务逻辑和边界条件
- 验证输入输出和状态变化

### 2. 集成测试

- 测试模块间的交互
- 验证完整游戏流程
- 检查状态传递和一致性
- 模拟真实用户场景

### 3. 边界测试

- 测试极值情况
- 验证错误处理
- 检查资源限制
- 测试异常路径

## 代码覆盖率

为了获取代码覆盖率报告，可以使用coverage工具：

```bash
# 安装coverage
pip install coverage

# 运行测试并收集覆盖率数据
coverage run -m unittest discover tests

# 生成覆盖率报告
coverage report
coverage html  # 生成HTML报告
```

## 持续集成

可以将测试集成到CI/CD流程中，例如GitHub Actions：

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: python run_tests.py --report
    - name: Upload test report
      uses: actions/upload-artifact@v2
      with:
        name: test-report
        path: test_report.txt
```

## 测试最佳实践

1. **保持测试独立性**：每个测试应该独立运行，不依赖其他测试的状态。
2. **使用描述性名称**：测试方法名应该清楚描述测试的内容。
3. **测试边界条件**：确保测试覆盖了各种边界情况和异常情况。
4. **使用模拟对象**：对于外部依赖，使用模拟对象来隔离测试。
5. **保持测试代码简洁**：测试代码应该简单、清晰、易于理解。
6. **定期更新测试**：当代码变更时，及时更新相应的测试用例。

## 扩展测试

当添加新功能时，请遵循以下步骤：

1. 在相应的测试模块中添加新的测试用例
2. 确保新测试覆盖了新功能的各种情况
3. 更新测试数据和模拟类（如需要）
4. 运行所有测试确保没有破坏现有功能
5. 更新本文档（如需要）

## 常见问题

### Q: 测试运行失败，提示"ModuleNotFoundError"怎么办？
A: 确保在项目根目录运行测试脚本，或者将src目录添加到Python路径。

### Q: 如何调试失败的测试？
A: 可以使用`--verbose`选项获取详细输出，或者在测试代码中添加调试打印语句。

### Q: 测试运行缓慢怎么办？
A: 考虑使用模拟对象替代真实的耗时操作，或者只运行特定的测试模块。

### Q: 如何测试GUI或用户界面？
A: 对于GUI应用，可以使用专门的UI测试框架，如PyQtTest或Selenium。

## 贡献指南

如果您想为测试套件做贡献：

1. Fork项目
2. 创建功能分支
3. 添加新的测试或改进现有测试
4. 确保所有测试通过
5. 提交Pull Request

感谢您对项目测试的贡献！