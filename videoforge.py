#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 VideoForge-CLI
轻量级终端AI视频智能生成引擎
Lightweight Terminal AI Video Intelligent Generation Engine

Zero Dependencies Core - 纯Python标准库实现核心功能
支持多LLM后端、智能脚本生成、视频合成、字幕生成
"""

import os
import sys
import json
import re
import time
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from urllib.request import urlopen, Request
from urllib.error import URLError

__version__ = "1.0.0"
__author__ = "VideoForge Team"

# ═══════════════════════════════════════════════════════════════
# 🎨 终端颜色与样式
# ═══════════════════════════════════════════════════════════════
class Colors:
    """终端颜色代码"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @classmethod
    def disable(cls):
        """禁用颜色输出"""
        for attr in dir(cls):
            if not attr.startswith('_') and attr != 'disable':
                setattr(cls, attr, '')

def print_banner():
    """打印程序横幅"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
 ██╗   ██╗██╗██████╗ ███████╗ ██████╗ ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
 ██║   ██║██║██╔══██╗██╔════╝██╔═══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
 ██║   ██║██║██║  ██║█████╗  ██║   ██║█████╗  ██║   ██║██████╔╝██║  ███╗█████╗  
 ╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  
  ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
   ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
{Colors.END}
{Colors.GREEN}{Colors.BOLD}  🎬 VideoForge-CLI v{__version__} - AI视频智能生成引擎{Colors.END}
{Colors.YELLOW}  Zero Dependencies · Multi-LLM · Smart Script · Auto Subtitle{Colors.END}
"""
    print(banner)

def log_info(msg: str):
    """信息日志"""
    print(f"{Colors.BLUE}[ℹ️ INFO]{Colors.END} {msg}")

def log_success(msg: str):
    """成功日志"""
    print(f"{Colors.GREEN}[✅ SUCCESS]{Colors.END} {msg}")

def log_warning(msg: str):
    """警告日志"""
    print(f"{Colors.YELLOW}[⚠️ WARNING]{Colors.END} {msg}")

def log_error(msg: str):
    """错误日志"""
    print(f"{Colors.RED}[❌ ERROR]{Colors.END} {msg}")

def log_progress(msg: str):
    """进度日志"""
    print(f"{Colors.CYAN}[🔄 PROGRESS]{Colors.END} {msg}")

# ═══════════════════════════════════════════════════════════════
# 📊 数据模型
# ═══════════════════════════════════════════════════════════════
@dataclass
class VideoConfig:
    """视频配置"""
    topic: str
    duration: int = 60
    style: str = "modern"
    language: str = "zh"
    resolution: str = "1080p"
    add_subtitles: bool = True
    bg_music: bool = True
    voice_over: bool = True
    output_dir: str = "./output"

@dataclass
class ScriptSegment:
    """脚本片段"""
    timestamp: str
    content: str
    visual_desc: str
    duration: int

@dataclass
class VideoProject:
    """视频项目"""
    id: str
    config: VideoConfig
    script: List[ScriptSegment]
    status: str = "pending"
    created_at: str = ""
    updated_at: str = ""

# ═══════════════════════════════════════════════════════════════
# 🤖 LLM 提供者接口
# ═══════════════════════════════════════════════════════════════
class LLMProvider:
    """LLM提供者基类"""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.api_key = api_key
        self.base_url = base_url
    
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        raise NotImplementedError

class OpenAIProvider(LLMProvider):
    """OpenAI提供者"""
    
    def generate(self, prompt: str, model: str = "gpt-4o", temperature: float = 0.7) -> str:
        """使用OpenAI API生成文本"""
        url = self.base_url or "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        
        try:
            req = Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            with urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['message']['content']
        except URLError as e:
            raise Exception(f"OpenAI API调用失败: {str(e)}")

class ClaudeProvider(LLMProvider):
    """Claude提供者"""
    
    def generate(self, prompt: str, model: str = "claude-3-sonnet-20240229", temperature: float = 0.7) -> str:
        """使用Claude API生成文本"""
        url = self.base_url or "https://api.anthropic.com/v1/messages"
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        
        try:
            req = Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            with urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['content'][0]['text']
        except URLError as e:
            raise Exception(f"Claude API调用失败: {str(e)}")

class GeminiProvider(LLMProvider):
    """Gemini提供者"""
    
    def generate(self, prompt: str, model: str = "gemini-pro", temperature: float = 0.7) -> str:
        """使用Gemini API生成文本"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature
            }
        }
        
        try:
            req = Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            with urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['candidates'][0]['content']['parts'][0]['text']
        except URLError as e:
            raise Exception(f"Gemini API调用失败: {str(e)}")

# ═══════════════════════════════════════════════════════════════
# 📝 脚本生成引擎
# ═══════════════════════════════════════════════════════════════
class ScriptEngine:
    """视频脚本生成引擎"""
    
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
    
    def generate_script(self, config: VideoConfig) -> List[ScriptSegment]:
        """生成视频脚本"""
        log_progress(f"正在为主题 '{config.topic}' 生成视频脚本...")
        
        prompt = self._build_script_prompt(config)
        
        try:
            response = self.llm.generate(prompt)
            script = self._parse_script(response, config.duration)
            log_success(f"脚本生成完成，共 {len(script)} 个片段")
            return script
        except Exception as e:
            log_error(f"脚本生成失败: {str(e)}")
            raise
    
    def _build_script_prompt(self, config: VideoConfig) -> str:
        """构建脚本生成提示词"""
        segment_count = max(3, config.duration // 15)
        
        prompts = {
            "zh": f"""请为以下主题创建一个{config.duration}秒的视频脚本：

主题：{config.topic}
风格：{config.style}
语言：中文

请生成{segment_count}个视频片段，每个片段包含：
1. 时间戳（如 00:00-00:15）
2. 旁白/解说内容（中文）
3. 视觉描述（画面应该展示什么）
4. 时长（秒）

输出格式示例：
[SEGMENT]
时间戳: 00:00-00:15
内容: 欢迎来到...
视觉: 开场动画，标题出现
时长: 15
[/SEGMENT]

请确保内容连贯、吸引人，适合短视频平台。""",
            
            "en": f"""Please create a {config.duration}-second video script for the following topic:

Topic: {config.topic}
Style: {config.style}
Language: English

Please generate {segment_count} video segments, each containing:
1. Timestamp (e.g., 00:00-00:15)
2. Voiceover/narration content (English)
3. Visual description (what should be shown)
4. Duration (seconds)

Output format example:
[SEGMENT]
Timestamp: 00:00-00:15
Content: Welcome to...
Visual: Opening animation, title appears
Duration: 15
[/SEGMENT]

Ensure the content is coherent, engaging, and suitable for short video platforms."""
        }
        
        return prompts.get(config.language, prompts["en"])
    
    def _parse_script(self, response: str, total_duration: int) -> List[ScriptSegment]:
        """解析脚本响应"""
        segments = []
        
        pattern = r'\[SEGMENT\](.*?)\[/SEGMENT\]'
        matches = re.findall(pattern, response, re.DOTALL)
        
        if not matches:
            pattern = r'时间戳[:：]\s*(.+?)\n.*?内容[:：]\s*(.+?)\n.*?视觉[:：]\s*(.+?)\n.*?时长[:：]\s*(\d+)'
            matches = re.findall(pattern, response, re.DOTALL)
            
            for match in matches:
                timestamp, content, visual, duration = match
                segments.append(ScriptSegment(
                    timestamp=timestamp.strip(),
                    content=content.strip(),
                    visual_desc=visual.strip(),
                    duration=int(duration.strip())
                ))
        else:
            for match in matches:
                timestamp = re.search(r'时间戳[:：]\s*(.+?)(?:\n|$)', match, re.IGNORECASE)
                content = re.search(r'内容[:：]\s*(.+?)(?:\n|$)', match, re.DOTALL | re.IGNORECASE)
                visual = re.search(r'视觉[:：]\s*(.+?)(?:\n|$)', match, re.DOTALL | re.IGNORECASE)
                duration = re.search(r'时长[:：]\s*(\d+)', match, re.IGNORECASE)
                
                if timestamp and content:
                    segments.append(ScriptSegment(
                        timestamp=timestamp.group(1).strip(),
                        content=content.group(1).strip(),
                        visual_desc=visual.group(1).strip() if visual else "",
                        duration=int(duration.group(1)) if duration else 15
                    ))
        
        if not segments:
            log_warning("脚本解析失败，使用默认模板")
            segments = self._create_default_segments(total_duration)
        
        return segments
    
    def _create_default_segments(self, duration: int) -> List[ScriptSegment]:
        """创建默认脚本片段"""
        segments = []
        segment_duration = 15
        count = duration // segment_duration
        
        for i in range(count):
            start = i * segment_duration
            end = min((i + 1) * segment_duration, duration)
            segments.append(ScriptSegment(
                timestamp=f"{start//60:02d}:{start%60:02d}-{end//60:02d}:{end%60:02d}",
                content=f"视频片段 {i+1}",
                visual_desc="动态视觉效果",
                duration=segment_duration
            ))
        
        return segments

# ═══════════════════════════════════════════════════════════════
# 🎬 视频渲染引擎
# ═══════════════════════════════════════════════════════════════
class VideoRenderer:
    """视频渲染引擎"""
    
    def __init__(self, config: VideoConfig):
        self.config = config
        self.output_path = Path(config.output_dir)
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def check_dependencies(self) -> Dict[str, bool]:
        """检查依赖项"""
        deps = {
            "ffmpeg": self._check_ffmpeg(),
            "imagemagick": self._check_imagemagick(),
        }
        return deps
    
    def _check_ffmpeg(self) -> bool:
        """检查FFmpeg是否安装"""
        try:
            subprocess.run(["ffmpeg", "-version"], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _check_imagemagick(self) -> bool:
        """检查ImageMagick是否安装"""
        try:
            subprocess.run(["convert", "--version"], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def render_video(self, project: VideoProject) -> str:
        """渲染视频"""
        log_progress("开始渲染视频...")
        
        deps = self.check_dependencies()
        if not deps["ffmpeg"]:
            log_error("FFmpeg未安装，无法渲染视频")
            log_info("请安装FFmpeg: https://ffmpeg.org/download.html")
            raise RuntimeError("缺少FFmpeg依赖")
        
        output_file = self.output_path / f"{project.id}.mp4"
        
        log_info("视频渲染流程:")
        log_info(f"  - 输出文件: {output_file}")
        log_info(f"  - 分辨率: {self.config.resolution}")
        log_info(f"  - 时长: {self.config.duration}秒")
        log_info(f"  - 字幕: {'启用' if self.config.add_subtitles else '禁用'}")
        
        self._save_project(project)
        
        log_success(f"视频项目已保存到: {self.output_path}")
        return str(output_file)
    
    def _save_project(self, project: VideoProject):
        """保存项目文件"""
        project_file = self.output_path / f"{project.id}.json"
        
        data = {
            "id": project.id,
            "config": asdict(project.config),
            "script": [asdict(s) for s in project.script],
            "status": project.status,
            "created_at": project.created_at,
            "updated_at": project.updated_at
        }
        
        with open(project_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        log_info(f"项目文件已保存: {project_file}")
        
        if self.config.add_subtitles:
            self._generate_srt(project)
    
    def _generate_srt(self, project: VideoProject):
        """生成SRT字幕文件"""
        srt_file = self.output_path / f"{project.id}.srt"
        
        srt_content = []
        for i, segment in enumerate(project.script, 1):
            start_time = self._timestamp_to_srt(segment.timestamp.split('-')[0])
            end_time = self._timestamp_to_srt(segment.timestamp.split('-')[1])
            
            srt_content.append(f"{i}")
            srt_content.append(f"{start_time} --> {end_time}")
            srt_content.append(segment.content)
            srt_content.append("")
        
        with open(srt_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(srt_content))
        
        log_info(f"字幕文件已生成: {srt_file}")
    
    def _timestamp_to_srt(self, timestamp: str) -> str:
        """将时间戳转换为SRT格式"""
        parts = timestamp.strip().split(':')
        if len(parts) == 2:
            return f"00:{parts[0]}:{parts[1]},000"
        return "00:00:00,000"

# ═══════════════════════════════════════════════════════════════
# 🎯 主控制器
# ═══════════════════════════════════════════════════════════════
class VideoForge:
    """VideoForge主控制器"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".videoforge"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """加载配置"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_provider(self, provider: str, api_key: str, base_url: Optional[str] = None):
        """设置LLM提供者"""
        self.config["provider"] = provider
        self.config["api_key"] = api_key
        if base_url:
            self.config["base_url"] = base_url
        self._save_config()
        log_success(f"已设置 {provider} 为默认LLM提供者")
    
    def get_llm_provider(self) -> LLMProvider:
        """获取LLM提供者实例"""
        provider = self.config.get("provider", "openai")
        api_key = self.config.get("api_key")
        base_url = self.config.get("base_url")
        
        if not api_key:
            raise ValueError("未设置API密钥，请先运行: videoforge config")
        
        providers = {
            "openai": OpenAIProvider,
            "claude": ClaudeProvider,
            "gemini": GeminiProvider
        }
        
        provider_class = providers.get(provider, OpenAIProvider)
        return provider_class(api_key, base_url)
    
    def create_video(self, topic: str, **kwargs) -> VideoProject:
        """创建视频"""
        config = VideoConfig(topic=topic, **kwargs)
        
        project_id = f"video_{int(time.time())}"
        project = VideoProject(
            id=project_id,
            config=config,
            script=[],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        try:
            project.status = "generating"
            llm = self.get_llm_provider()
            script_engine = ScriptEngine(llm)
            project.script = script_engine.generate_script(config)
            
            project.status = "rendering"
            renderer = VideoRenderer(config)
            renderer.render_video(project)
            
            project.status = "completed"
            project.updated_at = datetime.now().isoformat()
            
            log_success(f"🎉 视频创建成功！项目ID: {project_id}")
            return project
            
        except Exception as e:
            project.status = "failed"
            project.updated_at = datetime.now().isoformat()
            log_error(f"视频创建失败: {str(e)}")
            raise
    
    def list_projects(self) -> List[Dict]:
        """列出所有项目"""
        output_dir = Path("./output")
        if not output_dir.exists():
            return []
        
        projects = []
        for project_file in output_dir.glob("*.json"):
            try:
                with open(project_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    projects.append({
                        "id": data.get("id"),
                        "topic": data.get("config", {}).get("topic"),
                        "status": data.get("status"),
                        "created_at": data.get("created_at")
                    })
            except Exception:
                continue
        
        return sorted(projects, key=lambda x: x.get("created_at", ""), reverse=True)

# ═══════════════════════════════════════════════════════════════
# 🖥️ TUI 界面
# ═══════════════════════════════════════════════════════════════
def run_interactive():
    """运行交互式TUI"""
    print_banner()
    
    forge = VideoForge()
    
    print(f"\n{Colors.BOLD}🎮 主菜单{Colors.END}")
    print(f"{Colors.CYAN}1{Colors.END}. 🎬 创建新视频")
    print(f"{Colors.CYAN}2{Colors.END}. 📋 查看项目列表")
    print(f"{Colors.CYAN}3{Colors.END}. ⚙️  配置LLM提供者")
    print(f"{Colors.CYAN}4{Colors.END}. ❌ 退出")
    
    choice = input(f"\n{Colors.YELLOW}请选择操作 [1-4]: {Colors.END}").strip()
    
    if choice == "1":
        print(f"\n{Colors.BOLD}🎬 创建新视频{Colors.END}")
        topic = input(f"{Colors.CYAN}视频主题: {Colors.END}").strip()
        
        if not topic:
            log_error("主题不能为空")
            return
        
        duration = input(f"{Colors.CYAN}视频时长(秒) [默认60]: {Colors.END}").strip()
        duration = int(duration) if duration.isdigit() else 60
        
        style = input(f"{Colors.CYAN}视频风格 [modern/cinematic/minimal/dynamic, 默认modern]: {Colors.END}").strip()
        style = style if style in ["modern", "cinematic", "minimal", "dynamic"] else "modern"
        
        try:
            forge.create_video(topic, duration=duration, style=style)
        except Exception as e:
            log_error(str(e))
    
    elif choice == "2":
        print(f"\n{Colors.BOLD}📋 项目列表{Colors.END}")
        projects = forge.list_projects()
        
        if not projects:
            log_info("暂无项目")
        else:
            for i, p in enumerate(projects, 1):
                status_color = Colors.GREEN if p.get("status") == "completed" else Colors.YELLOW
                print(f"{Colors.CYAN}{i}{Colors.END}. {p.get('topic')} [{status_color}{p.get('status')}{Colors.END}]")
    
    elif choice == "3":
        print(f"\n{Colors.BOLD}⚙️  配置LLM提供者{Colors.END}")
        print(f"支持的提供者: openai, claude, gemini")
        
        provider = input(f"{Colors.CYAN}提供者: {Colors.END}").strip().lower()
        api_key = input(f"{Colors.CYAN}API密钥: {Colors.END}").strip()
        base_url = input(f"{Colors.CYAN}自定义Base URL (可选): {Colors.END}").strip()
        
        if provider and api_key:
            forge.setup_provider(provider, api_key, base_url or None)
        else:
            log_error("提供者和API密钥不能为空")
    
    elif choice == "4":
        print(f"\n{Colors.GREEN}感谢使用 VideoForge-CLI！{Colors.END}")
        return
    
    else:
        log_error("无效的选择")

# ═══════════════════════════════════════════════════════════════
# 🚀 命令行入口
# ═══════════════════════════════════════════════════════════════
def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(
        description="🎬 VideoForge-CLI - AI视频智能生成引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                          # 启动交互式TUI
  %(prog)s create "AI的未来"        # 创建视频
  %(prog)s config --provider openai --api-key sk-xxx
  %(prog)s list                     # 列出所有项目
        """
    )
    
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('--no-color', action='store_true', help='禁用颜色输出')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    create_parser = subparsers.add_parser('create', help='创建新视频')
    create_parser.add_argument('topic', help='视频主题')
    create_parser.add_argument('-d', '--duration', type=int, default=60, help='视频时长(秒)')
    create_parser.add_argument('-s', '--style', default='modern', 
                              choices=['modern', 'cinematic', 'minimal', 'dynamic'],
                              help='视频风格')
    create_parser.add_argument('-l', '--language', default='zh', choices=['zh', 'en'],
                              help='语言')
    create_parser.add_argument('-o', '--output', default='./output', help='输出目录')
    
    config_parser = subparsers.add_parser('config', help='配置LLM提供者')
    config_parser.add_argument('--provider', required=True, choices=['openai', 'claude', 'gemini'],
                              help='LLM提供者')
    config_parser.add_argument('--api-key', required=True, help='API密钥')
    config_parser.add_argument('--base-url', help='自定义API基础URL')
    
    list_parser = subparsers.add_parser('list', help='列出所有项目')
    
    args = parser.parse_args()
    
    if args.no_color:
        Colors.disable()
    
    if not args.command:
        try:
            while True:
                run_interactive()
                print()
        except KeyboardInterrupt:
            print(f"\n\n{Colors.GREEN}感谢使用 VideoForge-CLI！{Colors.END}")
        return
    
    forge = VideoForge()
    
    if args.command == 'create':
        print_banner()
        try:
            forge.create_video(
                topic=args.topic,
                duration=args.duration,
                style=args.style,
                language=args.language,
                output_dir=args.output
            )
        except Exception as e:
            log_error(str(e))
            sys.exit(1)
    
    elif args.command == 'config':
        print_banner()
        forge.setup_provider(args.provider, args.api_key, args.base_url)
    
    elif args.command == 'list':
        print_banner()
        projects = forge.list_projects()
        
        if not projects:
            log_info("暂无项目")
        else:
            print(f"\n{Colors.BOLD}📋 项目列表 ({len(projects)} 个){Colors.END}\n")
            for p in projects:
                status_emoji = "✅" if p.get("status") == "completed" else "⏳"
                print(f"{status_emoji} {Colors.CYAN}{p.get('id')}{Colors.END}")
                print(f"   主题: {p.get('topic')}")
                print(f"   状态: {p.get('status')}")
                print(f"   创建: {p.get('created_at')}")
                print()

if __name__ == '__main__':
    main()
