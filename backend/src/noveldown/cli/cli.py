import logging
from typing import Annotated

import questionary
import typer
from async_typer import AsyncTyper

from noveldown.core.scheduler import Scheduler

app = AsyncTyper(no_args_is_help=True, help="异步小说下载器")
logging.getLogger("fetcher").setLevel(logging.DEBUG)


@app.callback()
def main(
    ctx: typer.Context,
    max_concurrent: Annotated[int, typer.Option(help="最大下载并发数")] = 12,
):
    """全局选项"""
    ctx.obj = Scheduler(max_concurrent=max_concurrent)


@app.command()
async def download(ctx: typer.Context, url: str):
    """直接指定小说主页url来下载小说"""
    scheduler: Scheduler = ctx.obj
    book = await scheduler.download(url)
    book.to_txt()


@app.command()
async def search(ctx: typer.Context, book_name: str):
    """通过小说名字来搜索"""
    scheduler = ctx.obj
    results = (await scheduler.search(book_name))[:10]
    if not results:
        print("未搜索到该小说!")
        raise typer.Abort()

    book_url = await questionary.select(
        "请选择你需要的小说:",
        choices=[{"name": str(book), "value": book.source_url} for book in results],
    ).ask_async()
    book = await scheduler.download(book_url)
    book.to_txt()


if __name__ == "__main__":
    app()
