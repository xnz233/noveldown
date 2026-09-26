from pydantic import BaseModel

from .chapter import Chapter


class Book(BaseModel):
    source_url: str  # 唯一主页链接,可用于去重
    title: str
    author: str | None = None
    chapters: list[Chapter] = []
    completed_chapters: int = 0
    total_chapters: int = 0
    cover_url: str | None = None
    description: str | None = None
    status: str | None = None  # 比如 "连载中" "已完结"

    def to_txt(self, file_path: str = "", encoding: str = "UTF-8"):
        with open(file_path + self.title + ".txt", "w", encoding=encoding) as f:
            f.writelines(str(chapter) for chapter in self.chapters)
