from pathlib import Path

from aiohttp import web


async def handle_share(req: web.Request):
    return web.FileResponse(Path("assets/share", req.match_info["filename"]))

