# -*- coding: utf-8 -*-
"""
英雄无敌游戏 - 安装配置
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hero-game",
    version="3.0",
    author="Kevin",
    description="英雄无敌 - 中英双语文字冒险游戏",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hero",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "hero=hero.main:main",
        ],
    },
)
