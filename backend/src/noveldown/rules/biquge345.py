from typing import cast

from bs4 import BeautifulSoup, Tag

from noveldown.models import Chapter, SearchResult
from noveldown.rules.base import BaseRule, MetadataDict


class Biquge345(BaseRule):
    domain_patterns = ("biquge345.com",)
    url = "https://xbiquge345.com"
    search_url = "https://www.xbiquge345.com/s.php"
    search_method = "POST"

    def parse_metadata(self, html: str) -> MetadataDict:
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

    def build_search_req(self, name: str) -> dict:
        return {"type": "articlename", "s": name, "submit": ""}

    def parse_search_result(self, html: str) -> list[SearchResult | None]:
        soup = BeautifulSoup(html, "lxml")
        result_container = soup.select_one("ul.search")
        if not result_container:
            return []
        results = []
        for book in result_container.select("li"):
            if book.get("class"):
                continue
            metadatas = book.find_all("span")
            a = metadatas[1].find("a")
            if a:
                source_url = self.url + str(a.get("href"))
            else:
                source_url = ""
            title = metadatas[1].get_text()

            author = metadatas[3].get_text()
            results.append(
                SearchResult(title=title, author=author, source_url=source_url)
            )
        return results

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

        content = content_div.get_text(separator="\n", strip=True)
        content = "\n".join(content.split("\n")[3:])
        return content
