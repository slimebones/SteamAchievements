import asyncio

from orwynn.boot import Boot

from src.game import *
from src.achievement import *

async def main():
    await Boot.run_cli()

if __name__ == "__main__":
    asyncio.run(main())
