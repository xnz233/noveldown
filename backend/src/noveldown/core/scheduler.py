import asyncio
import logging

from noveldown.download import fetch
from noveldown.models import Book
from noveldown.rules import RULE_CLASSES, BaseRule

logger = logging.getLogger(__name__)

class Scheduler:
    def __init__(self, max_concurrent:int = 5, retry_times = 3):
        self.max_concurrent = max_concurrent
        self.retry_times = retry_times
        self._rules = RULE_CLASSES
        self.sem = asyncio.Semaphore(max_concurrent)

    def _get_rule(self, url: str) -> BaseRule:
        for rule_cls in self._rules:
            if rule_cls.supports_url(url):
                return rule_cls()
        logger.error(f"未找到适合 {url} 的规则")
        raise ValueError(f"未找到适合 {url} 的规则")

    async def download(self, book_url: str, rule: BaseRule | None = None) -> Book:
        rule = rule or self._get_rule(book_url)
        novel_home = await fetch(book_url)
        metadata = rule.parse_metadata(novel_home)
        chapters = rule.parse_chapter_list(novel_home)
        if not chapters:
            logger.error("未解析到章节")
            raise RuntimeError("未解析到章节")
        
        async with self.sem:
            tasks = [fetch(chapter.url) for chapter in chapters]
            
            for content_html,chapter in zip(await asyncio.gather(*tasks,return_exceptions=True),chapters):
                if isinstance(content_html, Exception):
                    chapter.content = "本章下载失败"
                    logger.error(chapter.title,"下载失败")
                    continue
                else:
                    chapter.content = rule.parse_content(str(content_html))
        info = {
            'source_url':book_url,
            'chapters':chapters,
            'total_chapters':len(chapters),
            **metadata
        }
        return Book(**info)

        
