#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行带有错误处理的英雄游戏
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from hero.main import main
    
    # 运行游戏主函数
    main()
    
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有必要的模块都在正确位置。")
    
except Exception as e:
    print(f"运行错误: {e}")
    print("请检查游戏文件是否完整。")