from pydantic import BaseModel


class Chapter(BaseModel):
    title: str
    index: int                # 章节序号
    url: str                  # 章节完整URL
    content: str = ""
    word_count: int = 0