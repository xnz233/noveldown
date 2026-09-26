import asyncio
from typing import Annotated

import typer
from rich import inspect

from noveldown.core.scheduler import Scheduler

app = typer.Typer(no_args_is_help=True,help="异步小说下载器")



@app.command()
def download(url: str, max_concurrent: Annotated[int,typer.Option(help="最大下载并发数")] = 12):
    scheduler = Scheduler(max_concurrent)

    book = asyncio.run(scheduler.download(url))
    inspect(book.chapters[0])
    book.to_txt()


if __name__ == "__main__":
    app()
