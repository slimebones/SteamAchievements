import asyncio

from orwynn.boot import Boot

from src.domain import *
from src.idea import *
from src.project import *
from src.task import *
from src.timing import *


async def main():
    await Boot.run_cli()

if __name__ == "__main__":
    asyncio.run(main())
