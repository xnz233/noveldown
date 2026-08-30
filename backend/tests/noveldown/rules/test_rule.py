from pathlib import Path

# 获取 fixtures 目录的路径
FIXTURES_DIR = Path(__file__).parent / "fixtures"

# 导入规则类
from noveldown.rules.biquge345 import Biquge345


def test_parse_chapter_list():
    """测试解析章节列表"""
    # 读取本地 HTML 文件
    html_path = FIXTURES_DIR / "biquge345_list.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # 创建规则实例（这里先占位，等实现了再替换）
    rule = Biquge345()
    chapters = rule.parse_chapter_list(html)
    metadata = rule.parse_metadata(html)
    assert metadata['title'] == "诸神愚戏"
    # 简单断言：至少有一个章节
    assert len(chapters) > 0
    # 或者检查第一个章节的标题是否符合预期
    assert chapters[0].title == "第1章 接生"
    
    # 暂时跳过，仅打印长度
    print(f"HTML 文件大小: {len(html)} 字符")
    assert len(html) > 1000  # 确保文件不是空的