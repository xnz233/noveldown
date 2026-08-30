from abc import ABC, abstractmethod
from typing import NotRequired, TypedDict

from noveldown.models import Chapter


class ChapterDict(TypedDict):
    author: str
    title: str
    status: str
    description: str
    cover_url: NotRequired[str]


class BaseRule(ABC):
    """网站解析规则的抽象基类"""

    # 声明支持的域名列表
    domain_patterns: tuple[str]

    @classmethod
    def supports_url(cls, url: str) -> bool:
        """检查该规则是否支持给定的 URL"""
        for pattern in cls.domain_patterns:
            if pattern in url:  # 简单包含匹配
                return True
        return False

    @abstractmethod
    def parse_metadata(self, html: str) -> ChapterDict:
        """解析小说首页，返回元数据"""

    @abstractmethod
    def parse_chapter_list(self, html: str) -> list[Chapter]:
        """解析章节列表页，返回 Chapter 对象列表"""

    @abstractmethod
    def parse_content(self, html: str) -> str:
        """解析内容页，返回章节正文"""
