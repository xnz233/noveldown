import asyncio

import typer
from rich import print

from rich.traceback import install

from noveldown.core.scheduler import Scheduler

install()
app = typer.Typer(no_args_is_help=True)


@app.command()
def download(url: str, max_concurrent: int = 10):
    scheduler = Scheduler(max_concurrent)

    book = asyncio.run(scheduler.download(url))
    print(book.chapters[0])
    book.to_txt()


if __name__ == "__main__":
    app()
