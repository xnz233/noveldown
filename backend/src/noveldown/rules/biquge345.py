from typing import cast

from bs4 import BeautifulSoup, Tag

from noveldown.models import Chapter
from noveldown.rules.base import BaseRule, ChapterDict


class Biquge345(BaseRule):
    domain_patterns = ("biquge345.com",)

    def parse_metadata(self, html: str) -> ChapterDict:
        soup = BeautifulSoup(html, "lxml")

        title_elm = soup.select_one("h1")
        xinxi_div = cast(Tag, soup.select_one("div.xinxi"))
        if title_elm:
            title = title_elm.get_text()
        else:
            title = "Unknown"

        data = xinxi_div.select("span")
        author = data[0].get_text("：")[1]
        # type = data[1].get_text("：")[1]
        status = data[2].get_text("：")[1]
        # click = data[3].get_text("：")[1]
        # fav = data[4].get_text("：")[1]
        # update_time = data[5].get_text("：")[1]
        description = data[6].get_text("：")[1]

        # print(xinxi_div)

        return {
            "title": title,
            "author": author,
            "status": status,
            "description": description,
        }

    def parse_chapter_list(self, html: str) -> list[Chapter]:
        soup = BeautifulSoup(html, "lxml")
        chapters = []

        chapter_container = soup.select_one("ul.info")

        if not chapter_container:
            return chapters

        for item in chapter_container.select("li"):
            a_tag = item.find("a")
            if a_tag and a_tag.get("href"):
                title = a_tag.get_text(strip=True)
                url = "https://biquge345.com" + cast(str, a_tag["href"])  # 处理相对路径

                chapter = Chapter(
                    title=title,
                    index=len(chapters) + 1,
                    url=url,
                    content="",  # 内容稍后填充
                )
                chapters.append(chapter)
        return chapters

    def parse_content(self, html: str) -> str:
        soup = BeautifulSoup(html, "lxml")

        content_div = soup.select_one("#txt")

        if not content_div:
            return ""

        paragraphs = content_div.find_all("p")
        if paragraphs:
            # 如果正文由 <p> 标签组成
            content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            # 否则直接获取所有文本，并用换行分割
            content = content_div.get_text(separator="\n", strip=True)

        return content
