import asyncio

import typer
from rich import print
from rich.console import Console

from noveldown.core.scheduler import Scheduler

app = typer.Typer(no_args_is_help=True)
console = Console()

@app.command()
def download(url: str, max_concurrent: int = 5, retry_times: int = 3):
    scheduler = Scheduler(max_concurrent,retry_times)
    with console.status("下载中"):
        book = asyncio.run(scheduler.download(url))
    print(book.chapters[0])
    book.to_txt()


if __name__ == "__main__":
    app()
