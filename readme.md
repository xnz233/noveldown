# noveldown - 小说下载器

一个前后端分离的小说下载 Web 应用，支持输入小说 URL 自动解析并导出为 TXT/EPUB 格式。

## 项目简介

noveldown 是一个模块化设计的小说下载工具，核心思想是“网站适配（规则）与下载引擎分离”。添加新网站只需新增规则类，无需改动核心代码。

### 核心功能

- 输入小说目录页 URL
- 自动识别网站并匹配解析规则
- 拉取全部章节内容
- 导出为 TXT 或 EPUB 格式（开发中）

### 技术栈

后端
- Python 3.14+
- FastAPI + Uvicorn
- httpx（异步 HTTP 客户端）
- BeautifulSoup4 + lxml（HTML 解析）
- Pydantic v2（数据验证）
- SQLAlchemy + aiosqlite（任务持久化，规划中）

包管理
- uv（v0.12+）

前端
- 待定（Vue）

## 项目状态

当前处于开发初期，核心下载引擎已完成并可通过测试。

已完成
- 数据模型（Book, Chapter）
- 网络请求层（异步 fetcher）
- 规则基类（BaseRule）及网站域名匹配
- 具体规则：biquge345.com
- 调度器（Scheduler）：自动匹配规则、下载全书
- 单元测试：通过真实 URL 验证完整流程

规划中
- 书籍元信息解析（书名、作者、简介）
- 并发下载（提升速度）
- 失败重试机制
- FastAPI 接口
- 任务持久化与队列管理
- 前端界面
- EPUB 导出

## 目录结构

```
noveldown/
├── backend/                          # 后端（Python + uv）
│   ├── pyproject.toml               # 项目配置与依赖
│   └── src/
│       └── noveldown/               # 源代码根包
│           ├── models/              # 数据模型（Book, Chapter）
│           ├── rules/               # 解析规则
│           │   ├── base.py          # BaseRule 抽象基类
│           │   └── biquge345.py     # biquge345.com 规则
│           ├── download/            # 网络层（fetcher）
│           ├── core/                # 调度器（Scheduler）
│           ├── api/                 # FastAPI 路由（规划中）
│           ├── db/                  # 数据库模型（规划中）
│           └── utils/               # 工具函数
├── frontend/                        # 前端（待初始化）
├── tests/                           # 测试
│   ├── fixtures/                    # 本地 HTML 测试文件
│   └── test_rules.py               # 规则单元测试
└── README.md
```

## 安装与运行

### 环境要求

- Python 3.14+
- uv

### 安装步骤

克隆仓库

```bash
git clone https://github.com/xnz233/noveldown
cd noveldown
```

安装 uv（如未安装）

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安装依赖

```bash
cd backend
uv sync
```

### 运行测试

```bash
uv run pytest ../tests/
```

## 添加新网站规则

1. 在 `backend/src/noveldown/rules/` 下新建文件，如 `qidian.py`
2. 继承 `BaseRule` 并实现 `parse_chapter_list` 和 `parse_content` 方法
3. 声明类属性 `domain_patterns`，如 `["example.com"]`
4. 在 `rules/__init__.py` 的 `RULE_CLASSES` 列表中注册

示例：

```python
from noveldown.rules.base import BaseRule
from noveldown.models import Chapter

class QidianRule(BaseRule):
    domain_patterns = ["example.com"]

    def parse_chapter_list(self, html: str) -> list[Chapter]:
        # 解析章节列表
        pass

    def parse_content(self, html: str) -> str:
        # 解析章节正文
        pass
```

## 核心设计原则

- 分层模块化：规则、网络、调度、业务解耦
- 先写抽象接口，再写具体实现
- 网站适配（规则）与下载引擎分离
- 异步优先：所有网络 IO 使用异步

---

## 开发进度

### 已完成
- [x] 数据模型定义
- [x] 网络层封装
- [x] 规则基类
- [x] biquge345.com 规则
- [x] 调度器核心流程
- [x] 单元测试框架

### 进行中
- [ ] 书籍元信息解析
- [ ] 并发下载优化

### 计划中
- [ ] FastAPI 接口
- [ ] 任务持久化
- [ ] 前端界面
- [ ] EPUB 导出