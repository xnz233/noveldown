from pydantic import BaseModel


class SearchResult(BaseModel):
    title: str
    author: str | None = None
    source_url: str
    cover_url: str | None = None

    def __str__(self):
        return f"{self.title} - {self.author}"
