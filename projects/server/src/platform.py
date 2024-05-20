import httpx
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from src.user import UserDoc

class PlatformProcessorArgs(BaseModel):
    user: "UserDoc"
    platform_user_sid: str
    api_token: str

class PlatformProcessor:
    async def process(self, args: PlatformProcessorArgs):
        raise NotImplementedError

class SteamUrls:
    GET_PLAYER_ACHIEVEMENTS = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={api_token}&steamid={steam_id}"
    GET_OWNED_GAMES = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_token}&steamid={steam_id}&format=json"

class SteamPlatformProcessor(PlatformProcessor):
    async def process(self, args: PlatformProcessorArgs):
        async with httpx.AsyncClient() as client:
            res = client.get(SteamUrls.GET_OWNED_GAMES.format(
                steam_id=args.platform_user_sid,
                api_token=args.api_token))
    # res = httpx.request("get", url)

    # if res.status_code >= 400:
    #     print(res.text)
    #     exit(1)

    # data = res.json()
    # pprint(data)
    # with open("out.json", "w") as f:
    #     json.dump(data, f)

PLATFORM_TO_PROCESSOR: dict[str, PlatformProcessor] = {
    "steam": SteamPlatformProcessor()
}
PLATFORMS = list(PLATFORM_TO_PROCESSOR.keys())
