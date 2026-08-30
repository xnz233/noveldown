import pytest
from noveldown.core.scheduler import Scheduler


@pytest.mark.asyncio
async def test_download():
    scheduler = Scheduler()
    book = await scheduler.download("https://www.xbiquge345.com/book/073742/")

    assert book.title == "盗墓：你们偷我家小麒麟？"
    assert book.chapters[0].title == "第1章 盗墓世界"