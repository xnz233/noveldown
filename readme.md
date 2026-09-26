# noveldown - 小说下载器

一个前后端分离的小说下载 Web 应用，支持输入小说 URL 自动解析并导出为 TXT/EPUB 格式。

## 项目简介

noveldown 是一个模块化设计的小说下载工具，核心思想是“网站适配（规则）与下载引擎分离”。添加新网站只需新增规则类，无需改动核心代码。

> 当前处于开发初期，核心下载引擎已完成并可通过测试。

### 核心功能

- 输入小说目录页 URL
- 自动识别网站并匹配解析规则
- 拉取全部章节内容
- 导出为 TXT

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
2. 继承 `BaseRule` 并实现抽象方法
3. 声明类属性 `domain_patterns`，如 `["example.com"]`
4. 在 `rules/__init__.py` 的 `RULE_CLASSES` 列表中注册

示例：

```python
from noveldown.rules.base import BaseRule
from noveldown.models import Chapter

class QidianRule(BaseRule):
    domain_patterns = ["example.com"]
    def parse_metadata(self, html: str) -> ChapterDict:
        # 获取元数据
    def parse_chapter_list(self, html: str) -> list[Chapter]:
        # 解析章节列表

    def parse_content(self, html: str) -> str:
        # 解析章节正文
```
## TODO
- [x] 数据模型定义
- [x] 网络层封装
- [x] 规则基类
- [x] biquge345.com 规则
- [x] 调度器核心流程
- [x] 单元测试框架
- [x] 书籍元信息解析
- [x] 并发下载优化
- [ ] FastAPI 接口
- [ ] 任务持久化
- [ ] 前端界面
- [ ] EPUB 导出