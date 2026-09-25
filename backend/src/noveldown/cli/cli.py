import asyncio
import logging

import typer
from rich import print

from noveldown.core.scheduler import Scheduler

app = typer.Typer(no_args_is_help=True)
logging.basicConfig(level=logging.INFO)


@app.command()
def download(url: str, max_concurrent: int = 5):
    scheduler = Scheduler(max_concurrent)

    book = asyncio.run(scheduler.download(url))
    print(book.chapters[0])
    book.to_txt()


if __name__ == "__main__":
    app()
