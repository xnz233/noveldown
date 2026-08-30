from httpx import HTTPError

from noveldown.download import fetch
from noveldown.models import Book
from noveldown.rules import RULE_CLASSES, BaseRule


class Scheduler:
    def __init__(self, max_concurrent:int = 5, retry_times = 3):
        self.max_concurrent = max_concurrent
        self.retry_times = retry_times
        self._rules = RULE_CLASSES

    def _get_rule(self, url: str) -> BaseRule:
        for rule_cls in self._rules:
            if rule_cls.supports_url(url):
                return rule_cls()
        raise ValueError(f"未找到适合 {url} 的规则")

    async def download(self, book_url: str, rule: BaseRule | None = None) -> Book:
        rule = rule or self._get_rule(book_url)
        novel_home = await fetch(book_url)
        metadata = rule.parse_metadata(novel_home)
        chapters = rule.parse_chapter_list(novel_home)
        if not chapters:
            raise RuntimeError("未解析到章节")

        for chapter in chapters:
            try:
                content_html = await fetch(chapter.url)
                chapter.content = rule.parse_content(content_html)
            except HTTPError as e:
                # 网络错误，记录但不中断
                chapter.content = f"[网络错误] {e}"
            except (AttributeError, ValueError) as e:
                # 解析错误，可能是 HTML 结构不符
                chapter.content = f"[解析错误] {e}"
        info = {
            'source_url':book_url,
            'chapters':chapters,
            'total_chapters':len(chapters),
            **metadata
        }
        return Book(**info)

        
