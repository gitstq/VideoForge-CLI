<div align="center">

# 🎬 VideoForge-CLI

**轻量级终端AI视频智能生成引擎**

*Lightweight Terminal AI Video Intelligent Generation Engine*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)]()
[![Zero Dependencies](https://img.shields.io/badge/Zero-Dependencies-brightgreen.svg)]()

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 简体中文

### 🎉 项目介绍

VideoForge-CLI 是一款**零依赖**的轻量级终端AI视频智能生成引擎，专为内容创作者、开发者和视频制作爱好者打造。只需输入主题，即可利用AI大模型自动生成专业级视频脚本、字幕和项目文件。

**灵感来源**：受 [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) 启发，我们打造了一个更加轻量级、零依赖的替代方案，让视频创作变得前所未有的简单！

**自研差异化亮点**：
- 🚀 **纯Python标准库实现**，零第三方依赖
- 🤖 **多LLM后端支持**（OpenAI / Claude / Gemini）
- 📝 **智能脚本生成引擎**，自动分段、自动时间戳
- 🎬 **自动SRT字幕生成**，支持多语言
- 🖥️ **交互式TUI界面** + 命令行双模式
- ⚡ **轻量级架构**，启动快、资源占用低

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🎯 **零依赖核心** | 纯Python标准库实现，无需安装任何第三方包 |
| 🤖 **多LLM支持** | 支持OpenAI GPT、Claude、Gemini等多种AI模型 |
| 📝 **智能脚本** | AI自动生成视频脚本，包含时间戳、旁白、视觉描述 |
| 🎬 **自动字幕** | 自动生成SRT格式字幕文件，支持中英文 |
| 🎨 **多种风格** | modern、cinematic、minimal、dynamic 四种视频风格 |
| 🖥️ **双模式操作** | 交互式TUI界面 + 命令行模式，满足不同场景 |
| ⚙️ **灵活配置** | 支持自定义API Base URL，兼容各类代理服务 |
| 📁 **项目管理** | 自动保存项目文件，支持项目列表查看 |

### 🚀 快速开始

#### 环境要求

- Python 3.8+
- FFmpeg（可选，用于视频渲染）

#### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/ahg0/VideoForge-CLI.git
cd VideoForge-CLI

# 直接运行（零依赖，无需安装）
python3 videoforge.py

# 或安装到系统
pip3 install -e .
```

#### 首次配置

```bash
# 配置LLM提供者
videoforge config --provider openai --api-key sk-your-api-key

# 或使用 Claude
videoforge config --provider claude --api-key your-api-key

# 或使用 Gemini
videoforge config --provider gemini --api-key your-api-key

# 配置自定义API地址（可选）
videoforge config --provider openai --api-key sk-xxx --base-url https://api.example.com/v1
```

#### 创建你的第一个视频

```bash
# 交互式模式
videoforge

# 命令行模式
videoforge create "AI的未来" --duration 60 --style modern

# 英文视频
videoforge create "Future of AI" --duration 90 --style cinematic --language en
```

### 📖 详细使用指南

#### 命令行参数

```bash
# 基础用法
videoforge create <主题> [选项]

# 选项说明
-d, --duration    视频时长（秒），默认60
-s, --style       视频风格：modern/cinematic/minimal/dynamic
-l, --language    语言：zh/en
-o, --output      输出目录，默认./output
```

#### 交互式TUI操作

```
🎮 主菜单
1. 🎬 创建新视频
2. 📋 查看项目列表
3. ⚙️  配置LLM提供者
4. ❌ 退出
```

#### 项目输出结构

```
output/
├── video_1234567890.json      # 项目配置文件
├── video_1234567890.srt       # 字幕文件
└── ...
```

### 💡 设计思路与迭代规划

#### 设计理念

1. **极简主义**：零依赖设计，降低使用门槛
2. **模块化架构**：LLM提供者、脚本引擎、渲染引擎完全解耦
3. **可扩展性**：易于添加新的LLM后端和视频风格

#### 技术选型原因

- **纯Python标准库**：最大化兼容性，无需处理依赖冲突
- **Dataclass**：类型安全、代码简洁
- **urllib**：标准库HTTP客户端，无需requests

#### 后续迭代计划

- [ ] 集成FFmpeg视频渲染功能
- [ ] 添加更多视频风格模板
- [ ] 支持批量视频生成
- [ ] 添加背景音乐生成
- [ ] 支持语音合成(TTS)
- [ ] Web界面版本

### 📦 打包与部署指南

#### 本地开发

```bash
make install-dev    # 安装开发依赖
make test           # 运行测试
make lint           # 代码检查
make format         # 代码格式化
```

#### 构建分发包

```bash
make build          # 构建wheel和tar.gz
make upload         # 上传到PyPI（需配置twine）
```

#### 直接运行

```bash
chmod +x videoforge.py
./videoforge.py
```

### 🤝 贡献指南

欢迎提交Issue和PR！请遵循以下规范：

1. **Issue**：描述问题时请提供复现步骤和环境信息
2. **PR**：请确保代码通过lint检查，并添加必要的测试
3. **Commit**：遵循Angular提交规范（feat/fix/docs/refactor等）

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 繁體中文

### 🎉 項目介紹

VideoForge-CLI 是一款**零依賴**的輕量級終端AI視頻智能生成引擎，專為內容創作者、開發者和視頻製作愛好者打造。只需輸入主題，即可利用AI大模型自動生成專業級視頻腳本、字幕和項目文件。

**自研差異化亮點**：
- 🚀 **純Python標準庫實現**，零第三方依賴
- 🤖 **多LLM後端支援**（OpenAI / Claude / Gemini）
- 📝 **智能腳本生成引擎**，自動分段、自動時間戳
- 🎬 **自動SRT字幕生成**，支援多語言
- 🖥️ **互動式TUI介面** + 命令行雙模式
- ⚡ **輕量級架構**，啟動快、資源佔用低

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🎯 **零依賴核心** | 純Python標準庫實現，無需安裝任何第三方套件 |
| 🤖 **多LLM支援** | 支援OpenAI GPT、Claude、Gemini等多種AI模型 |
| 📝 **智能腳本** | AI自動生成視頻腳本，包含時間戳、旁白、視覺描述 |
| 🎬 **自動字幕** | 自動生成SRT格式字幕文件，支援中英文 |
| 🎨 **多種風格** | modern、cinematic、minimal、dynamic 四種視頻風格 |
| 🖥️ **雙模式操作** | 互動式TUI介面 + 命令行模式，滿足不同場景 |
| ⚙️ **靈活配置** | 支援自定義API Base URL，相容各類代理服務 |
| 📁 **項目管理** | 自動保存項目文件，支援項目列表查看 |

### 🚀 快速開始

#### 環境要求

- Python 3.8+
- FFmpeg（可選，用於視頻渲染）

#### 安裝步驟

```bash
# 克隆倉庫
git clone https://github.com/ahg0/VideoForge-CLI.git
cd VideoForge-CLI

# 直接運行（零依賴，無需安裝）
python3 videoforge.py

# 或安裝到系統
pip3 install -e .
```

#### 首次配置

```bash
# 配置LLM提供者
videoforge config --provider openai --api-key sk-your-api-key

# 或使用 Claude
videoforge config --provider claude --api-key your-api-key

# 或使用 Gemini
videoforge config --provider gemini --api-key your-api-key
```

#### 創建你的第一個視頻

```bash
# 互動式模式
videoforge

# 命令行模式
videoforge create "AI的未來" --duration 60 --style modern

# 英文視頻
videoforge create "Future of AI" --duration 90 --style cinematic --language en
```

### 📖 詳細使用指南

#### 命令行參數

```bash
# 基礎用法
videoforge create <主題> [選項]

# 選項說明
-d, --duration    視頻時長（秒），默認60
-s, --style       視頻風格：modern/cinematic/minimal/dynamic
-l, --language    語言：zh/en
-o, --output      輸出目錄，默認./output
```

### 📦 打包與部署指南

```bash
make install        # 安裝項目
make install-dev    # 安裝開發依賴
make test           # 運行測試
make build          # 構建分發包
```

### 📄 開源協議

本項目採用 [MIT License](LICENSE) 開源協議。

---

## English

### 🎉 Project Introduction

VideoForge-CLI is a **zero-dependency** lightweight terminal AI video intelligent generation engine, designed for content creators, developers, and video production enthusiasts. Simply enter a topic, and leverage AI large models to automatically generate professional-grade video scripts, subtitles, and project files.

**Self-developed Differentiation Highlights**:
- 🚀 **Pure Python standard library implementation**, zero third-party dependencies
- 🤖 **Multi-LLM backend support** (OpenAI / Claude / Gemini)
- 📝 **Intelligent script generation engine** with auto-segmentation and timestamps
- 🎬 **Automatic SRT subtitle generation**, multilingual support
- 🖥️ **Interactive TUI interface** + Command line dual mode
- ⚡ **Lightweight architecture**, fast startup, low resource usage

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🎯 **Zero Dependency Core** | Pure Python standard library, no third-party packages needed |
| 🤖 **Multi-LLM Support** | Support OpenAI GPT, Claude, Gemini and more AI models |
| 📝 **Smart Scripting** | AI auto-generates video scripts with timestamps, narration, visual descriptions |
| 🎬 **Auto Subtitles** | Auto-generate SRT format subtitle files, Chinese/English support |
| 🎨 **Multiple Styles** | modern, cinematic, minimal, dynamic four video styles |
| 🖥️ **Dual Mode Operation** | Interactive TUI + Command line mode for different scenarios |
| ⚙️ **Flexible Configuration** | Support custom API Base URL, compatible with various proxy services |
| 📁 **Project Management** | Auto-save project files, support project list viewing |

### 🚀 Quick Start

#### Requirements

- Python 3.8+
- FFmpeg (optional, for video rendering)

#### Installation

```bash
# Clone repository
git clone https://github.com/ahg0/VideoForge-CLI.git
cd VideoForge-CLI

# Run directly (zero dependencies, no installation needed)
python3 videoforge.py

# Or install to system
pip3 install -e .
```

#### Initial Configuration

```bash
# Configure LLM provider
videoforge config --provider openai --api-key sk-your-api-key

# Or use Claude
videoforge config --provider claude --api-key your-api-key

# Or use Gemini
videoforge config --provider gemini --api-key your-api-key

# Configure custom API endpoint (optional)
videoforge config --provider openai --api-key sk-xxx --base-url https://api.example.com/v1
```

#### Create Your First Video

```bash
# Interactive mode
videoforge

# Command line mode
videoforge create "Future of AI" --duration 60 --style modern

# Chinese video
videoforge create "人工智能的未来" --duration 90 --style cinematic --language zh
```

### 📖 Detailed Usage Guide

#### Command Line Arguments

```bash
# Basic usage
videoforge create <topic> [options]

# Options
-d, --duration    Video duration (seconds), default 60
-s, --style       Video style: modern/cinematic/minimal/dynamic
-l, --language    Language: zh/en
-o, --output      Output directory, default ./output
```

#### Interactive TUI

```
🎮 Main Menu
1. 🎬 Create New Video
2. 📋 View Project List
3. ⚙️  Configure LLM Provider
4. ❌ Exit
```

#### Project Output Structure

```
output/
├── video_1234567890.json      # Project config file
├── video_1234567890.srt       # Subtitle file
└── ...
```

### 💡 Design Philosophy & Roadmap

#### Design Principles

1. **Minimalism**: Zero-dependency design, lowering the barrier to entry
2. **Modular Architecture**: LLM providers, script engine, rendering engine fully decoupled
3. **Extensibility**: Easy to add new LLM backends and video styles

#### Technical Choices

- **Pure Python Standard Library**: Maximum compatibility, no dependency conflicts
- **Dataclass**: Type safety, clean code
- **urllib**: Standard library HTTP client, no requests needed

#### Future Roadmap

- [ ] Integrate FFmpeg video rendering
- [ ] Add more video style templates
- [ ] Support batch video generation
- [ ] Add background music generation
- [ ] Support text-to-speech (TTS)
- [ ] Web interface version

### 📦 Packaging & Deployment Guide

#### Local Development

```bash
make install-dev    # Install development dependencies
make test           # Run tests
make lint           # Code linting
make format         # Code formatting
```

#### Build Distribution Package

```bash
make build          # Build wheel and tar.gz
make upload         # Upload to PyPI (requires twine config)
```

#### Run Directly

```bash
chmod +x videoforge.py
./videoforge.py
```

### 🤝 Contribution Guidelines

Issues and PRs are welcome! Please follow these guidelines:

1. **Issue**: Provide reproduction steps and environment info when describing problems
2. **PR**: Ensure code passes lint checks and add necessary tests
3. **Commit**: Follow Angular commit conventions (feat/fix/docs/refactor, etc.)

### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ by VideoForge Team**

⭐ Star us on GitHub — it motivates us a lot!

</div>
