#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VideoForge-CLI 安装脚本
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name="videoforge-cli",
    version="1.0.0",
    author="VideoForge Team",
    author_email="hello@videoforge.dev",
    description="🎬 VideoForge-CLI - 轻量级终端AI视频智能生成引擎",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahg0/VideoForge-CLI",
    py_modules=["videoforge"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Content Creators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "videoforge=videoforge:main",
            "vf=videoforge:main",
        ],
    },
    keywords="ai video generation cli tool llm openai claude gemini",
    project_urls={
        "Bug Reports": "https://github.com/ahg0/VideoForge-CLI/issues",
        "Source": "https://github.com/ahg0/VideoForge-CLI",
        "Documentation": "https://github.com/ahg0/VideoForge-CLI#readme",
    },
)
