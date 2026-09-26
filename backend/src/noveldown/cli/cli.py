import asyncio

import typer
from rich import inspect

from noveldown.core.scheduler import Scheduler

app = typer.Typer(no_args_is_help=True)



@app.command()
def download(url: str, max_concurrent: int = 12):
    scheduler = Scheduler(max_concurrent)

    book = asyncio.run(scheduler.download(url))
    inspect(book.chapters[0])
    book.to_txt()


if __name__ == "__main__":
    app()
