"""
Ref: https://developer.valvesoftware.com/wiki/Steam_Web_API#GetUserStatsForGame_.28v0002.29
"""
import json
from pathlib import Path
import httpx
import dotenv
from pykit.env import EnvUtils
from pprint import pprint

from pykit.log import log

from src.platform import SteamUrls

ACHIEVEMENTS_OUT_PATH = Path(Path.cwd(), "tests/data/achievements.json")
GAMES_OUT_PATH = Path(Path.cwd(), "tests/data/games.json")

def _req_get_json_onetime(url: str) -> dict:
    res = httpx.request("get", url)
    if res.status_code >= 400:
        log.err(f"err during http req: {res.text}")
        exit(1)
    return res.json()

def main():
    ACHIEVEMENTS_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    GAMES_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    dotenv.load_dotenv()
    api_token = EnvUtils.get("API_TOKEN") 
    steam_id = EnvUtils.get("STEAM_ID")
    app_id="1365010"

    data = _req_get_json_onetime(SteamUrls.GET_PLAYER_ACHIEVEMENTS.format(
        api_token=api_token, steam_id=steam_id, app_id=app_id))
    with ACHIEVEMENTS_OUT_PATH.open("w") as f:
        json.dump(data, f, indent=2)

    data = _req_get_json_onetime(SteamUrls.GET_OWNED_GAMES.format(
        api_token=api_token, steam_id=steam_id))
    with GAMES_OUT_PATH.open("w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()
