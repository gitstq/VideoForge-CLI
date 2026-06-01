# VideoForge-CLI Makefile

.PHONY: help install install-dev test lint format clean build upload

PYTHON := python3
PIP := pip3

help:
	@echo "🎬 VideoForge-CLI 构建工具"
	@echo ""
	@echo "可用命令:"
	@echo "  make install      - 安装项目"
	@echo "  make install-dev  - 安装开发依赖"
	@echo "  make test         - 运行测试"
	@echo "  make lint         - 代码检查"
	@echo "  make format       - 代码格式化"
	@echo "  make clean        - 清理构建文件"
	@echo "  make build        - 构建分发包"
	@echo "  make run          - 运行程序"

install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e ".[dev]"
	$(PIP) install pytest black flake8 mypy

test:
	pytest tests/ -v

lint:
	flake8 videoforge.py --max-line-length=120
	mypy videoforge.py --ignore-missing-imports

format:
	black videoforge.py --line-length=120

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	$(PYTHON) setup.py sdist bdist_wheel

upload: build
	twine upload dist/*

run:
	$(PYTHON) videoforge.py

dev:
	$(PYTHON) videoforge.py --no-color
